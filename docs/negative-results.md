# Negative findings and failed assumptions

Research credibility requires documenting when a plausible approach does not work or when evidence is insufficient.

### 1. No natural duplicates in the original synthetic benchmark

The first 60-task deterministic benchmark had **zero eligible exact-read reuse opportunities**. Therefore the first narrow optimizer did **not** demonstrate savings on that workload. A later modular test was constructed to contain repeat reads and did show *simulated* savings. Those two findings must remain separate.

**Lesson:** Always measure the frequency of the target inefficiency on a real or independently chosen baseline before investing in an optimization mechanism.

### 2. Early real-model internal agent runs failed

Two small paid OpenAI smoke runs were performed with a private **internal** agent. One stopped at its step limit and the other returned an incorrect arithmetic answer. These are failed tasks, even if the instrumentation around them functioned.

**Lesson:** Infrastructure success is different from agent-task success. Diagnostic improvements cannot retroactively change past outcomes.

### 3. Offline external integration is not a complete real execution

The pinned mini-SWE-agent integration passed controlled behavior-preservation checks using fixtures. A candidate patch was submitted in fixture conditions, but this was not a valid independently graded success on SWE-bench.

**Lesson:** A clean offline test proves only the executed test conditions. It does not establish true cloud compatibility or end-to-end model/agent/evaluator operation.

### 4. Tests are not an independent audit

A 338-test checkpoint is useful engineering evidence, but source-code review, adversarial tests, live integration work and external replication remain separate requirements.
