# Technical decisions and research reasoning

This document tracks the decisions that make Melior an optimization research problem rather than a token-usage dashboard.

## Decision 1 — Measure cost per successful task

**Alternative rejected:** optimize the number of LLM calls or tokens in isolation.

**Reason:** An agent that skips calls can fail more frequently. Counting all execution attempts and dividing total cost by confirmed successful tasks gives a more meaningful result. When success count is zero, cost per success is undefined.

**Test implication:** retain failures, retries, uncertainty in charges, and independent task outcomes.

## Decision 2 — Observe both model and tool boundaries

**Alternative rejected:** derive the entire task cost from provider token counts alone.

**Reason:** Tool operations affect latency and success, while model SDKs can retry automatically. A trustworthy system needs a record of real physical attempts and what was visible at each interface.

**Test implication:** reconcile logical requests with physical attempts; never turn missing usage or uncertain charges into a measured zero.

## Decision 3 — Make measurement non-interfering

**Hypothesis:** instrumentation can preserve the behavior of an existing agent under a controlled replay fixture.

**Reported observation:** the pinned `mini-SWE-agent` generated identical serialized model requests, action sequences, tool observations and submission with or without Melior's observer in the tested offline fixture.

**Boundary:** the fixture was non-executing and incurred no real provider/cloud charge; this is not a production performance result.

## Decision 4 — Start with a conservative optimization rule

**Chosen experiment:** remove a repeated read of unchanged state under a restricted semantic contract.

**Why:** an arbitrary tool action may write data, produce side effects or depend on changing external state. Such calls cannot simply be cached.

**Controls:** compare with an unmodified baseline and an independent reference interpreter. After a write, cached read results must be invalidated.

## Decision 5 — Keep negative results

**Original benchmark:** 60 synthetic tasks passed, but the restricted read-elimination policy found **zero** eligible duplicate reads. There was no optimization gain for that mechanism on those tasks.

**Separate engineered workload:** an intentionally duplicate-heavy synthetic benchmark produced a **21.3858%** reduction in simulated cost per successful task; this shows a mechanism can work under its assumptions, not that those assumptions occur often in external agents.

**Research consequence:** gather real external-agent traces, find the actual recurring inefficiency, then define and test a new intervention.

## Decision 6 — Do not confuse a proposed method with a validated result

Potential future techniques include context selection, quality-aware model routing, dependency-aware scheduling, adaptive stopping and learned policies. Each is a hypothesis until tested with fixed tasks, independent outcomes and matched cost accounting.

## Proposed next experiment

1. Preselect a small set of real coding tasks and lock model/agent versions.
2. Run unoptimized `mini-SWE-agent` with authorized bounded execution.
3. Independently evaluate each patch and retain every failure.
4. Analyze execution traces for a repeated, measurable inefficiency.
5. Specify one intervention with a clear safety contract.
6. Run matched baseline/intervention trials and report success, cost, latency, uncertainty and generalization limits.

**Falsification rule:** Reject the intervention if it changes required behavior, has no benefit on real tasks, or violates reliability limits.
