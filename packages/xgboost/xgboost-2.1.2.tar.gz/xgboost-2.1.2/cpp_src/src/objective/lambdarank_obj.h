/**
 * Copyright 2023, XGBoost contributors
 *
 * Vocabulary explanation:
 *
 * There are two different lists we need to handle in the objective, first is the list of
 * labels (relevance degree) provided by the user. Its order has no particular meaning
 * when bias estimation is NOT used. Another one is generated by our model, sorted index
 * based on prediction scores. `rank_high` refers to the position index of the model rank
 * list that is higher than `rank_low`, while `idx_high` refers to where does the
 * `rank_high` sample comes from. Simply put, `rank_high` indexes into the rank list
 * obtained from the model, while `idx_high` indexes into the user provided sample list.
 */
#ifndef XGBOOST_OBJECTIVE_LAMBDARANK_OBJ_H_
#define XGBOOST_OBJECTIVE_LAMBDARANK_OBJ_H_
#include <algorithm>                       // for min, max
#include <cassert>                         // for assert
#include <cmath>                           // for log, abs
#include <cstddef>                         // for size_t
#include <functional>                      // for greater
#include <memory>                          // for shared_ptr
#include <random>                          // for minstd_rand, uniform_int_distribution
#include <vector>                          // for vector

#include "../common/algorithm.h"           // for ArgSort
#include "../common/math.h"                // for Sigmoid
#include "../common/ranking_utils.h"       // for CalcDCGGain
#include "../common/transform_iterator.h"  // for MakeIndexTransformIter
#include "xgboost/base.h"                  // for GradientPair, XGBOOST_DEVICE, kRtEps
#include "xgboost/context.h"               // for Context
#include "xgboost/data.h"                  // for MetaInfo
#include "xgboost/host_device_vector.h"    // for HostDeviceVector
#include "xgboost/linalg.h"                // for VectorView, Vector
#include "xgboost/logging.h"               // for CHECK_EQ
#include "xgboost/span.h"                  // for Span

namespace xgboost::obj {
double constexpr Eps64() { return 1e-16; }

template <bool exp>
XGBOOST_DEVICE double DeltaNDCG(float y_high, float y_low, std::size_t rank_high,
                                std::size_t rank_low, double inv_IDCG,
                                common::Span<double const> discount) {
  // Use rank_high instead of idx_high as we are calculating discount based on ranks
  // provided by the model.
  double gain_high = exp ? ltr::CalcDCGGain(y_high) : y_high;
  double discount_high = discount[rank_high];

  double gain_low = exp ? ltr::CalcDCGGain(y_low) : y_low;
  double discount_low = discount[rank_low];

  double original = gain_high * discount_high + gain_low * discount_low;
  double changed = gain_low * discount_high + gain_high * discount_low;

  double delta_NDCG = (original - changed) * inv_IDCG;
  assert(delta_NDCG >= -1.0);
  assert(delta_NDCG <= 1.0);
  return delta_NDCG;
}

XGBOOST_DEVICE inline double DeltaMAP(float y_high, float y_low, std::size_t rank_high,
                                      std::size_t rank_low, common::Span<double const> n_rel,
                                      common::Span<double const> acc) {
  double r_h = static_cast<double>(rank_high) + 1.0;
  double r_l = static_cast<double>(rank_low) + 1.0;
  double delta{0.0};
  double n_total_relevances = n_rel.back();
  assert(n_total_relevances > 0.0);
  auto m = n_rel[rank_low];
  double n = n_rel[rank_high];

  if (y_high < y_low) {
    auto a = m / r_l - (n + 1.0) / r_h;
    auto b = acc[rank_low - 1] - acc[rank_high];
    delta = (a - b) / n_total_relevances;
  } else {
    auto a = n / r_h - m / r_l;
    auto b = acc[rank_low - 1] - acc[rank_high];
    delta = (a + b) / n_total_relevances;
  }
  return delta;
}

template <bool unbiased, typename Delta>
XGBOOST_DEVICE GradientPair
LambdaGrad(linalg::VectorView<float const> labels, common::Span<float const> predts,
           common::Span<size_t const> sorted_idx,
           std::size_t rank_high,                     // higher index on the model rank list
           std::size_t rank_low,                      // lower index on the model rank list
           Delta delta,                               // function to calculate delta score
           linalg::VectorView<double const> t_plus,   // input bias ratio
           linalg::VectorView<double const> t_minus,  // input bias ratio
           double* p_cost) {
  assert(sorted_idx.size() > 0 && "Empty sorted idx for a group.");
  std::size_t idx_high = sorted_idx[rank_high];
  std::size_t idx_low = sorted_idx[rank_low];

  if (labels(idx_high) == labels(idx_low)) {
    *p_cost = 0;
    return {0.0f, 0.0f};
  }

  auto best_score = predts[sorted_idx.front()];
  auto worst_score = predts[sorted_idx.back()];

  auto y_high = labels(idx_high);
  float s_high = predts[idx_high];
  auto y_low = labels(idx_low);
  float s_low = predts[idx_low];

  // Use double whenever possible as we are working on the exp space.
  double delta_score = std::abs(s_high - s_low);
  double const sigmoid = common::Sigmoid(s_high - s_low);
  // Change in metric score like \delta NDCG or \delta MAP
  double delta_metric = std::abs(delta(y_high, y_low, rank_high, rank_low));

  if (best_score != worst_score) {
    delta_metric /= (delta_score + 0.01);
  }

  if (unbiased) {
    *p_cost = std::log(1.0 / (1.0 - sigmoid)) * delta_metric;
  }

  auto lambda_ij = (sigmoid - 1.0) * delta_metric;
  auto hessian_ij = std::max(sigmoid * (1.0 - sigmoid), Eps64()) * delta_metric * 2.0;

  auto k = t_plus.Size();
  assert(t_minus.Size() == k && "Invalid size of position bias");

  // We need to skip samples that exceed the maximum number of tracked positions, and
  // samples that have low probability and might bring us floating point issues.
  if (unbiased && idx_high < k && idx_low < k && t_minus(idx_low) >= Eps64() &&
      t_plus(idx_high) >= Eps64()) {
    // The index should be ranks[idx_low], since we assume label is sorted, this reduces
    // to `idx_low`, which represents the position on the input list, as explained in the
    // file header.
    lambda_ij /= (t_plus(idx_high) * t_minus(idx_low));
    hessian_ij /= (t_plus(idx_high) * t_minus(idx_low));
  }
  auto pg = GradientPair{static_cast<float>(lambda_ij), static_cast<float>(hessian_ij)};
  return pg;
}

XGBOOST_DEVICE inline GradientPair Repulse(GradientPair pg) {
  auto ng = GradientPair{-pg.GetGrad(), pg.GetHess()};
  return ng;
}

namespace cuda_impl {
void LambdaRankGetGradientNDCG(Context const* ctx, std::int32_t iter,
                               HostDeviceVector<float> const& preds, MetaInfo const& info,
                               std::shared_ptr<ltr::NDCGCache> p_cache,
                               linalg::VectorView<double const> t_plus,   // input bias ratio
                               linalg::VectorView<double const> t_minus,  // input bias ratio
                               linalg::VectorView<double> li, linalg::VectorView<double> lj,
                               linalg::Matrix<GradientPair>* out_gpair);

/**
 * \brief Generate statistic for MAP used for calculating \Delta Z in lambda mart.
 */
void MAPStat(Context const* ctx, MetaInfo const& info, common::Span<std::size_t const> d_rank_idx,
             std::shared_ptr<ltr::MAPCache> p_cache);

void LambdaRankGetGradientMAP(Context const* ctx, std::int32_t iter,
                              HostDeviceVector<float> const& predt, MetaInfo const& info,
                              std::shared_ptr<ltr::MAPCache> p_cache,
                              linalg::VectorView<double const> t_plus,   // input bias ratio
                              linalg::VectorView<double const> t_minus,  // input bias ratio
                              linalg::VectorView<double> li, linalg::VectorView<double> lj,
                              linalg::Matrix<GradientPair>* out_gpair);

void LambdaRankGetGradientPairwise(Context const* ctx, std::int32_t iter,
                                   HostDeviceVector<float> const& predt, const MetaInfo& info,
                                   std::shared_ptr<ltr::RankingCache> p_cache,
                                   linalg::VectorView<double const> ti_plus,   // input bias ratio
                                   linalg::VectorView<double const> tj_minus,  // input bias ratio
                                   linalg::VectorView<double> li, linalg::VectorView<double> lj,
                                   linalg::Matrix<GradientPair>* out_gpair);

void LambdaRankUpdatePositionBias(Context const* ctx, linalg::VectorView<double const> li_full,
                                  linalg::VectorView<double const> lj_full,
                                  linalg::Vector<double>* p_ti_plus,
                                  linalg::Vector<double>* p_tj_minus, linalg::Vector<double>* p_li,
                                  linalg::Vector<double>* p_lj,
                                  std::shared_ptr<ltr::RankingCache> p_cache);
}  // namespace cuda_impl

namespace cpu_impl {
/**
 * \brief Generate statistic for MAP used for calculating \Delta Z in lambda mart.
 *
 * \param label    Ground truth relevance label.
 * \param rank_idx Sorted index of prediction.
 * \param p_cache  An initialized MAPCache.
 */
void MAPStat(Context const* ctx, linalg::VectorView<float const> label,
             common::Span<std::size_t const> rank_idx, std::shared_ptr<ltr::MAPCache> p_cache);
}  // namespace cpu_impl

/**
 * \param Construct pairs on CPU
 *
 * \tparam Op Functor for upgrading a pair of gradients.
 *
 * \param ctx     The global context.
 * \param iter    The boosting iteration.
 * \param cache   ltr cache.
 * \param g       The current query group
 * \param g_label label The labels for the current query group
 * \param g_rank  Sorted index of model scores for the current query group.
 * \param op      A callable that accepts two index for a pair of documents. The index is for
 *                the ranked list (labels sorted according to model scores).
 */
template <typename Op>
void MakePairs(Context const* ctx, std::int32_t iter,
               std::shared_ptr<ltr::RankingCache> const cache, bst_group_t g,
               linalg::VectorView<float const> g_label, common::Span<std::size_t const> g_rank,
               Op op) {
  auto group_ptr = cache->DataGroupPtr(ctx);
  ltr::position_t cnt = group_ptr[g + 1] - group_ptr[g];

  if (cache->Param().HasTruncation()) {
    for (std::size_t i = 0; i < std::min(cnt, cache->Param().NumPair()); ++i) {
      for (std::size_t j = i + 1; j < cnt; ++j) {
        op(i, j);
      }
    }
  } else {
    CHECK_EQ(g_rank.size(), g_label.Size());
    std::minstd_rand rnd(iter);
    rnd.discard(g);  // fixme(jiamingy): honor the global seed
    // sort label according to the rank list
    auto it = common::MakeIndexTransformIter(
        [&g_rank, &g_label](std::size_t idx) { return g_label(g_rank[idx]); });
    std::vector<std::size_t> y_sorted_idx =
        common::ArgSort<std::size_t>(ctx, it, it + cnt, std::greater<>{});
    // permutation iterator to get the original label
    auto rev_it = common::MakeIndexTransformIter(
        [&](std::size_t idx) { return g_label(g_rank[y_sorted_idx[idx]]); });

    for (std::size_t i = 0; i < cnt;) {
      std::size_t j = i + 1;
      // find the bucket boundary
      while (j < cnt && rev_it[i] == rev_it[j]) {
        ++j;
      }
      // Bucket [i,j), construct n_samples pairs for each sample inside the bucket with
      // another sample outside the bucket.
      //
      // n elements left to the bucket, and n elements right to the bucket
      std::size_t n_lefts = i, n_rights = static_cast<std::size_t>(cnt - j);
      if (n_lefts + n_rights == 0) {
        i = j;
        continue;
      }

      auto n_samples = cache->Param().NumPair();
      // for each pair specifed by the user
      while (n_samples--) {
        // for each sample in the bucket
        for (std::size_t pair_idx = i; pair_idx < j; ++pair_idx) {
          std::size_t ridx = std::uniform_int_distribution<std::size_t>(
              static_cast<std::size_t>(0), n_lefts + n_rights - 1)(rnd);
          if (ridx >= n_lefts) {
            ridx = ridx - i + j;  // shift to the right of the bucket
          }
          // index that points to the rank list.
          auto idx0 = y_sorted_idx[pair_idx];
          auto idx1 = y_sorted_idx[ridx];
          op(idx0, idx1);
        }
      }
      i = j;
    }
  }
}
}  // namespace xgboost::obj
#endif  // XGBOOST_OBJECTIVE_LAMBDARANK_OBJ_H_
