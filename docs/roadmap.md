# Research roadmap, not an achievement list

| Stage | Research question | Evidence required | Status at last documented checkpoint |
|---|---|---|---|
| 0. Measurement | Can whole-task executions be observed faithfully? | Durable traces, known costs and unknown-cost handling | Private implementation, internal and offline tests |
| 1. Internal benchmark | Can results be replayed and compared? | Stable synthetic tasks, independent outcomes, failure accounting | Implemented privately |
| 2. Narrow transformation | Can eligible exact repeated reads be skipped safely? | Paired baseline and optimized traces with unmodified outcomes | Positive only on engineered modular synthetic tasks |
| 3. External agent baseline | Can a real independent agent run and be graded? | Actual model/tool work and independent PASS/FAIL/ERROR | Not demonstrated end-to-end |
| 4. Natural-use optimization | Are eligible inefficiencies frequent in real traces? | Frozen workload, natural opportunities, cost/success effect | Not established |
| 5. Context, routing and scheduling | Which execution policies transfer across agents? | Sufficient labeled data, representative holdout evaluations | Proposed research |
| 6. Learned selection or RL | Can policy selection improve without compromising safety? | Robust, calibrated cost-quality evidence | Long-term research direction |

Do not advertise stages 3–6 as existing features.
