# Historical engineering results — reported checkpoints

**Provenance:** These metrics come from retained technical handoff and verification notes for the private Melior / Agent Optimizer development repository. The original source, raw logs, and private experiment databases are not distributed in this public starter repository. This page is a **reported checkpoint summary, not a fresh independent reproduction**.

## September 2026: earlier Phase 5B offline verification

- Verified offline on **22 September 2026**.
- **307 regression tests passed**, zero failed or skipped; **69 external integration tests** passed.
- Historical evidence snapshot: **1,357 files unchanged**.
- Pinned third-party versions: `mini-SWE-agent 2.4.6`, `SWE-ReX 1.4.0`, `SWE-bench 4.1.0`.
- Instrumented and uninstrumented pinned agent produced identical serialized request bytes, action sequence, tool observations, messages and submission in the controlled **non-executing fixture**.
- A fixture imported a deliberately non-solution patch and was **not independently evaluated for a real success**.
- **$0** actual API and cloud spending for that verification.
- Checkpoint: `668af8630314ca9471e4c63b517108140907fd07` (reported for Phase 5B).

## Later cloud-preparation checkpoint

- Reported clean commit: `c1e4630686af49d8acbe9ecdf386cbf7d0909797`.
- Package version reported: `0.5.1`.
- **338 tests passed**, zero failed or skipped, at the last documented cloud-preparation checkpoint.
- **1,466 historical evidence files preserved**; this is a *later* snapshot than the 1,357-file Phase 5B check.
- Live Modal startup, network compatibility, remote dependency installation, cleanup, billing and official cloud evaluation still **not verified**.
- **$0** newly incurred API/cloud spending during the cloud-preparation verification.

## The original 60-task internal benchmark

- **60/60 task successes**, with 120 model operations and 240 tool operations reported.
- Reference **simulated** cost: `$0.044112` across the 60 tasks.
- Simulated cost per successful task: `$0.0007352`.
- This was a **deterministic internal workload**, not SWE-bench, real user tasks or provider-billed savings.
- The first exact-duplicate-read policy found **zero opportunities** on this original benchmark, so no deduplication benefit was established on it.

## Separate engineered modular workload

- A distinct *constructed synthetic* task set intentionally contained eligible repeated reads.
- The first restricted optimizer eliminated **120** qualifying repeated-read operations.
- Reported simulated cost reduction: `$0.012`.
- Reported simulated cost-per-success improvement: **21.3858%**, with 100% task success in that setting.
- The workload is **not evidence of a similar percentage on natural agent traces**; tasks were engineered to create savings opportunities.

## Early paid internal-agent tests

- Two real-model smoke runs involved Melior's small **internal** agent, *not* mini-SWE-agent.
- One hit its step limit; the other returned an incorrect arithmetic result.
- Those failures were retained as failures. A later narrow arithmetic diagnostic did not convert them into successful tasks.

## Evidence and reproducibility limits

The prior private verification note contains hashes for source, test reports and package builds. Publishing a hash alone does not give a third party the artifact required to check it. If permitted, the next step is to publish a **redacted, versioned evidence bundle** and a reviewable subset of the actual original source, with the corresponding checksum manifest.

**Do not combine numbers from different checkpoints or call these reported synthetic cost differences actual dollar savings.**
