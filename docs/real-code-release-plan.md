# Adding selected original Melior source to the public research repository

The public repo is designed to be understandable immediately. For a deeper technical review, publish **selected original source and reproducible evidence** from the existing private Melior codebase when appropriate.

## High-impact additions, ordered for a research reviewer

| Priority | Source / evidence | What it demonstrates |
|---|---|---|
| 1 | `model_bridge.py`, `budget.py`, and matching tests | Physical attempts, pre-dispatch reservations, unknown cost liability and failure handling |
| 2 | Restricted duplicate-read policy and matching comparison harness | Implemented safety contract, state invalidation and a falsifiable optimization test |
| 3 | Original task specifications, deterministic benchmark script and redacted report | Reproducible 60-task baseline, including the zero-opportunity result |
| 4 | Relevant `external/transport.py`, `runner.py`, `evidence.py`, integration tests | How the system observes an external agent without changing fixture behavior |
| 5 | Verification manifest, exact commands, dependency pins and sanitized output | A reader can connect the reported checkpoint with the implementation |

**A strong code review target:** choose one original module and walk through its invariant, one failure mode, the tests that enforce it, and its place in the full system architecture.

Before publishing, check rights to distribute third-party dependencies, remove provider keys, private traces and sensitive paths, and verify Git history doesn't include secrets. Publishing selected modules is about readability as much as openness—the whole private system does not need to go public at once.
