# Engineering contributions — Melior

**Role:** Founder and research/engineering lead.

Melior began with a technical question: **what does it mean to reduce the cost of an AI-agent task if the execution strategy can also change the outcome?** My work has centered on translating that question into a measurable system, testable constraints, and an incremental experimental program.

## Research direction and system decisions

- **Objective:** Chose cost *per successful task* as the key quantity, so failed or repeated attempts contribute to total cost rather than disappearing from the evaluation, instead of treating lower token counts as sufficient.
- **Measurement:** Developed a workflow for recording actual model and tool attempts, retries, usage, latency, outcomes and uncertainties, supported by immutable evidence and DuckDB.
- **Reliability constraints:** Prioritized pre-dispatch budget reservations, explicit authorization of live execution and separation of estimated/simulated costs from real spending.
- **First controlled intervention:** Investigated exact duplicate **read-only** reuse with state-sensitive validity, rather than presenting arbitrary tool-call caching as safe.
- **Evaluation:** Treated success as an independently checked outcome; developed deterministic controls and tests for negative cases, including the absence of reuse opportunities.
- **External integration:** Advanced from an internal synthetic benchmark toward a pinned `mini-SWE-agent` fixture and independent SWE-bench result-import path; recorded the difference between offline fixture equivalence and live evaluation.

## Technical scope documented at the last checkpoint

The private project records describe a Python codebase with execution spans, durable evidence, cost ledgers, budget controls, record/replay, a restricted optimizer, an external coding-agent boundary, CLI workflows, and a suite with **338 passing tests**. The source-tree and checkpoint structure are described in [architecture](architecture.md) and [historical results](historical-results.md).

## Decisions I can explain and defend

1. **Why optimize the task instead of the request?** A cheaper model call can increase task failures and total retried cost.
2. **Why record physical attempts?** A logical request can become multiple provider attempts; a timeout may still be billable.
3. **Why doesn't replay demonstrate savings?** Reusing recordings avoids new spend during analysis but does not show a better live execution policy.
4. **Why is state-aware reuse narrow?** Reads can become stale after writes; many tools have side effects that prohibit caching.
5. **Why preserve failed runs?** They constrain claims and reveal whether the chosen metric is hiding regressions.
6. **Why did the first baseline matter?** It showed zero eligible duplicate reads, changing what a useful next experiment should measure.

## Evidence and code navigation

- Historical test counts, reproducibility pins and task metrics: [historical-results.md](historical-results.md)
- Experimental decisions and hypotheses: [technical-decisions.md](technical-decisions.md)
- Current public, executable companion: [`experiments/public_demo.py`](../experiments/public_demo.py) and [`tests/test_public_demo.py`](../tests/test_public_demo.py)
- Original source modules to share selectively when cleared for publication: [real-code-release-plan.md](real-code-release-plan.md)

**Scope note:** The publicly runnable simulator was newly created to make the core idea easy to inspect. The original development occurred in a separate private codebase. Tools, including AI coding assistance, were used during development; that does not replace responsibility for understanding, testing and being able to explain the work. The exact original code and full logs are not reproduced here.
