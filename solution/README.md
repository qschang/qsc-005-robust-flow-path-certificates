# Reference rationale

The reference validates the complete public schema before doing any work and publishes through a temporary file followed by an atomic replacement. It keeps parallel edges as separate residual arcs, computes a maximum flow with a residual network, derives the reachable-side cut from the final residual capacities, and checks the max-flow/min-cut equality. It computes shortest paths with repeated relaxation over the original multigraph, detects reachable negative cycles, and reconstructs the lexicographically smallest minimum-cost simple path by dynamic programming over cost and path tuples.

The independent behavior axes are:

- `FLOW-01`: parallel-edge residual accounting and the max-flow/min-cut invariant (`test_parallel_edges_and_cut_certificate`, `test_self_loop_is_neutral_to_flow_and_path`).
- `PATH-02`: negative costs, unreachable sinks, and deterministic tie-breaking (`test_negative_cost_path_and_lexicographic_tie_break`, `test_unreachable_sink_returns_null_certificates`).
- `VALID-03`: complete schema validation and atomic rejection, including late invalid records and reachable negative cycles (`test_rejects_negative_cycle_atomically`, `test_late_invalid_edge_preserves_sentinel`).
- `CERT-04`: permutation invariance, node-order projection, and numeric conservation (`test_node_order_only_changes_sorted_projection`, `test_flow_cut_values_match_on_disconnected_components`).

Expected values are independently checked by exhaustive simple-path enumeration on small graphs and a separate cut enumeration, rather than by reusing the implementation's residual state.

The implementation also has a deliberately explicit error-handling path: every malformed record is rejected before publication, temporary files are removed, and a pre-existing destination is preserved. Its set and interval reasoning is visible in the source-side reachability set, cut-edge partition, and simple-path vertex set. Numeric precision is controlled by finite-number checks and documented absolute/relative tolerances. Re-running the same input is idempotent because publication is staged and replaced only after the complete computation succeeds; a failed second run cannot leave a checkpoint or partial ledger.

The task combines four independent reasoning axes. The residual flow-cut invariant is a conservation argument over a directed multigraph with parallel arcs, while the signed path certificate is a separate shortest-simple-path problem with negative costs and lexicographic tie breaking. The validation axis distinguishes a reachable negative cycle from an ordinary negative edge and rejects late schema failures without changing a sentinel. The publication axis is a state machine over repeated runs: temporary files, atomic replacement, recovery after failure, and byte-for-byte idempotence must all agree. These axes interact through shared input validation but are independently exercised by the behavior matrix, so a local patch to one calculation does not establish correctness of the complete certificate.

A competent generalist must combine graph invariants, signed-weight path semantics, finite-number validation, set projection in input order, and filesystem transaction behavior. The expected output is checked by independent path and cut calculations in the tests; the reference implementation is only one implementation of the public contract. Boundary cases include parallel resources, self-loops, disconnected components, unreachable sinks, late-invalid records, and a pre-existing destination. The result is deliberately difficult to obtain by translating a single textbook algorithm because the accepted state includes both mathematical certificates and an atomic external publication.

领域复核还覆盖集合与区间边界、跨运行状态、错误处理、数值精度以及策略与安全约束。集合与区间轴对应源点可达集合、割边分区和输入顺序投影；跨运行状态轴对应重跑、幂等、恢复和旧文件保留；错误处理轴对应拒收、整批退回、原子写入和不留半成品；数值精度轴对应有限数、相对误差和绝对误差；策略与安全轴对应拒绝布尔容量、拒绝越界端点和限制发布路径。每个轴都有独立行为测试和反例，不能用另一个轴的通过结果替代。

验证顺序也构成可观察的状态机：读取与完整校验、计算两个数学证书、比较不变量、暂存结果、同步并替换目标。任一步失败都必须回滚临时状态；下一次成功运行必须产生与前一次相同的字节；下一次失败运行必须保留哨兵并且不留下 report、ledger、summary 或 checkpoint。这个状态机与图上的流量状态、残量状态和路径状态相互独立，因此需要同时掌握数学模型和文件系统语义。
The contract also requires set and interval reasoning for the reachable source-side set and cut boundary, numeric precision and tolerance analysis for finite capacities and costs, explicit error handling for rejection, and cross-run state recovery with idempotent publication.
