# Experiment design: making optimization claims falsifiable

## Hypothesis

> On tasks containing **identical repeated read-only operations under unchanged state**, skipping redundant execution reduces simulated tool cost without changing outcomes.

This is a narrow hypothesis. It does **not** predict general real-agent savings or reduced LLM token costs.

## Minimal experiment (in this repository)

The [public simulator](../experiments/public_demo.py) executes specified read/write/compute operations. It compares a baseline with a policy that reuses **read-only** results keyed by `(resource, resource version)`. Writes increment the version and invalidate earlier read results. `compute` and `write` operations are not cached.

An independent interpreter constructs the expected transcript and final resource state, so simply matching one flawed policy against another cannot count as correctness.

### Two controls

**Unique-read workload:** no eligible duplicated reads. Expected finding: zero reused reads, zero simulated reduction.

**Constructed repeat-read workload:** repeated reads deliberately inserted. Expected finding: reused read operations with unchanged transcript/state; positive simulated cost change. This tests the mechanism, not the prevalence of the mechanism.

### Observables

- Task success/failure under the independent interpreter
- Read executions and read-reuse count
- Total **simulated** operation cost (including failed attempts)
- Simulated cost per successful task; **undefined** if no successful task exists
- Transcript equality and final resource-state equality

No network or provider calls occur. The public demo has a separately chosen artificial cost model, so its numbers are **not** the historical private 21.3858% result.

## What an external-agent study must add

1. Freeze a representative task set **before** inspecting outcomes.
2. Record exact code and dependency revisions, model identities and price schedules.
3. Store complete baseline attempts, including failures, restarts, latency and cloud costs.
4. Validate both the original agent and observed agent generate equivalent requests/actions in a controlled setup.
5. Add one narrowly scoped intervention behind a feature flag.
6. Run matched tasks under comparable budgets and use an evaluator independent of the agent.
7. Compare success, total cost, time-to-success and failure cost. Include uncertainty intervals and sample sizes.
8. Repeat on held-out tasks; reject a policy if it violates the permitted reliability tolerance.

## Failure conditions

The optimization hypothesis fails if it changes output or state, if observed cost reductions disappear after counting failures and instrumentation overhead, if the targeted repetitions are absent from natural traces, or if the evidence cannot be reproduced.
