/**
 * Copyright 2023-2024, XGBoost contributors
 */
#pragma once
#include "../../src/collective/coll.h"    // for Coll
#include "../../src/collective/comm.h"    // for Comm

namespace xgboost::collective {
class FederatedColl : public Coll {
 private:
  std::uint64_t sequence_number_{0};

 public:
  Coll *MakeCUDAVar() override;

  [[nodiscard]] Result Allreduce(Comm const &, common::Span<std::int8_t> data,
                                 ArrayInterfaceHandler::Type type, Op op) override;
  [[nodiscard]] Result Broadcast(Comm const &comm, common::Span<std::int8_t> data,
                                 std::int32_t root) override;
  [[nodiscard]] Result Allgather(Comm const &, common::Span<std::int8_t> data) override;
  [[nodiscard]] Result AllgatherV(Comm const &comm, common::Span<std::int8_t const> data,
                                  common::Span<std::int64_t const> sizes,
                                  common::Span<std::int64_t> recv_segments,
                                  common::Span<std::int8_t> recv, AllgatherVAlgo algo) override;
};
}  // namespace xgboost::collective
