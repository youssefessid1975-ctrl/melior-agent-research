# Independent reproduction log — fill this in AFTER you run and analyze the code

> **This is an uncompleted template, not a claim that the applicant independently wrote or ran the experiment below.** The goal is to create an audit trail for work you personally perform, including mistakes and rejected hypotheses.

- Date and local environment:
- Git commit hash of code I tested:
- Commands I personally executed:
- Output and relevant log/screenshot path:
- Hypothesis before the experiment:
- Expected outcome before seeing the result:
- Actual result:
- What I concluded:
- What evidence would falsify my conclusion:
- What I changed in the code myself (link to commit):
- What code was generated or substantially modified with AI assistance:

## Three useful independent exercises

1. **Remove version-based invalidation deliberately.** Construct a task with `read → write → read`, confirm the optimized transcript becomes wrong, and add a regression test. Restore safe invalidation.
2. **Probe the cost metric.** Modify one experimental result to be a failure and calculate how the total cost-per-success metric responds. Explain why a low per-call cost can still be misleading.
3. **Change the workload, not the optimizer.** Generate tasks with different duplicate frequencies. Plot simulated reduction against repeat frequency and explain why the graph does not estimate natural behavior in a real AI agent.

These exercises only become personal evidence when you **actually perform** them and document your own reasoning. Do not publish this unchanged template as an accomplished research experiment.
