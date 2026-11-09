# Melior — 90-second research reviewer guide

## The research thesis

**Can an AI agent change its execution plan to lower total cost while maintaining independent task success?**

That is the question behind Melior. Instead of optimizing a single LLM request, I focus on **whole-task execution**: model calls, tool actions, retries, state changes, spending and whether the task actually succeeds.

## Three reasons this project is technically interesting

**1. Measurement that does not perturb what it measures.** In a controlled offline fixture, the instrumented `mini-SWE-agent` matched the uninstrumented agent's serialized requests, action sequence and submission. That is a prerequisite for attributing later differences to an optimization policy rather than an observer effect.

**2. A reliability-constrained objective.** My metric includes failures and is checked by a separate outcome evaluator. Lower apparent spend is not an improvement if the agent fails more often.

**3. A negative result that changed the research direction.** A safe repeated-read rule showed a **21.39% simulated cost-per-success improvement on a constructed workload**, but **zero eligible duplicate reads in the original 60-task baseline**. This motivated moving toward external-agent trace analysis before selecting more sophisticated optimization methods.

## Evidence in the repository

| Time | Where | What to inspect |
|---|---|---|
| **1 minute** | [README](../README.md) | Research question, milestones and experimental boundaries |
| **3 minutes** | [Technical decisions](technical-decisions.md) | The choices behind metrics, safety constraints and negative results |
| **5 minutes** | [`experiments/public_demo.py`](../experiments/public_demo.py) | A small executable mechanism with independent correctness check |
| **5 minutes** | [`tests/test_public_demo.py`](../tests/test_public_demo.py) | Unit tests covering read reuse, invalidation and failure behavior |
| **10 minutes** | [Historical checkpoints](historical-results.md) | Reproducibility pins, 307-test and 338-test milestones |

## Questions I'd welcome in a research interview

- How would you estimate a policy's cost-per-success when outcomes are stochastic?
- How do you rule out a new instrumentation layer changing the agent's behavior?
- What does it mean to cache a tool call safely in a mutable environment?
- How would you design an experiment to distinguish genuine savings from benchmark-specific behavior?
- When would a contextual bandit or reinforcement learner be justified over a deterministic rule?

**What I want to investigate next:** robust agent evaluation, reliable decision-making under uncertainty, and evidence-driven optimization policies.

*Public scope: this repo includes a fresh companion simulator and records of the historical private work; the full original Python runtime and live external-agent experiments are not published here.*
