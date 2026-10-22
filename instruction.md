# Robust flow and path certificates

Implement `/app/solve.py` so it reads UTF-8 JSON from the first command-line path and atomically writes UTF-8 JSON to the second path.

The input object has exactly `nodes`, `edges`, `source`, and `sink`. Nodes are unique non-empty strings; terminals are distinct existing nodes. Each edge has exactly `u`, `v`, `capacity`, and `cost`; endpoints exist, capacities are finite numbers ≥ 0, costs are finite numbers, parallel edges and self-loops are allowed, and booleans are not numbers. A negative-cost cycle reachable from `source` invalidates the input.

The instance is a directed multigraph: preserve edge multiplicity as a collection of independent resources, reason about the residual-capacity boundary and its induced cut set, and retain finite numeric precision when comparing the two certificates. Validation and publication are separate state transitions: a late rejection must be atomic, leave no temporary or report artifact, and a repeated accepted run must be idempotent.

Return exactly `max_flow`, `min_cut_capacity`, `source_side`, `shortest_path_cost`, and `shortest_path`. Treat parallel edges as separate resources. The flow value and the cut induced by `source_side` must agree within 1e-9 relative and 1e-12 absolute error. `source_side` is the set reachable from `source` by positive residual capacity after the reported flow, listed in input node order. The path is a simple node sequence from source to sink and its cost is the sum of its original edge costs. If no path exists, both path fields are null. Equal-cost paths use the lexicographically smallest node sequence. Self-loops do not affect either certificate.

On malformed input, a reachable negative-cost cycle, certificate disagreement, or internal error, exit nonzero and leave the destination absent or byte-for-byte unchanged. Do not create report, ledger, summary, checkpoint, or temporary files for a rejected request. Publish output only after validation and all computations complete.
