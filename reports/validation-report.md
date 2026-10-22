## Validation status

This package is a candidate pending runtime and publication gates. The bundled MA-08 expert pack and its RAG were inspected; retrieval query was `最大流 最小割 平行边 残量 浮点容量`, yielding MA-08-MODELS, MA-08-FAILURES, MA-08-TASK-DESIGN, and related records. The corpus is explicitly `research-candidate`, so claims remain independently checked synthetic-contract claims rather than promoted expert evidence.

The blind red-team instruction-leakage review used only `instruction.md` and the agent-visible environment. It found no tests, solution directory, expected outputs, implementation symbols, or verifier mechanics in the public statement. Filenames are generic and do not identify a hidden defect. A second manual pass checked environment contents and found only the public entrypoint.

Static package checks and local pytest are planned. Environment build status is pending the frozen revision. The project Harbor CLI is available at `di/work/harbor-venv/Scripts/harbor.exe` version 0.24.0, and Docker daemon status is healthy through the approved desktop-linux context. Oracle/NOP/DeepSeek runs remain pending the frozen published revision. Domestic model status is pending the same frozen revision. GitHub CLI is unavailable, so repository publication remains pending; Git credentials and proxy are not inferred. Source network is not required for this standard-library package. No runtime score or model result is claimed until the exact frozen revision is run.

Mutation plan: remove parallel-edge separation, force nonnegative shortest-path relaxation, publish before validation, and sort source-side lexicographically. Each is mapped to the challenge tests above; execution remains pending the runtime environment.
