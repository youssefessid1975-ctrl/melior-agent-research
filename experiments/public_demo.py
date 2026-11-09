"""Runnable, stdlib-only synthetic study for the public Melior research dossier.

This code was created as an AI-assisted explanatory companion in November 2026.
It is NOT the code from the original private Melior implementation, and its
artificial monetary rates are NOT actual API charges or measured real-world gains.

Run:
    python -m experiments.public_demo
    python -m experiments.public_demo --json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Literal

Op = Literal["read", "write", "compute"]

# Invented accounting rates for a controlled simulation: 1 micro-USD = $0.000001.
SIMULATED_MICRO_USD = {"read": 2_000, "write": 4_000, "compute": 1_000}
INITIAL_RESOURCES = {"alpha": "A0", "beta": "B0", "gamma": "C0"}


@dataclass(frozen=True)
class Step:
    op: Op
    resource: str
    value: str = ""


@dataclass(frozen=True)
class Task:
    name: str
    steps: tuple[Step, ...]


@dataclass(frozen=True)
class Result:
    task: str
    passed_reference: bool
    simulated_cost_micro_usd: int
    real_read_executions: int
    reused_reads: int
    transcript: tuple[str, ...]
    final_resources: tuple[tuple[str, str], ...]


def reference_interpreter(task: Task) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...]]:
    """Simple separate reference semantics, always performs every operation."""
    state = dict(INITIAL_RESOURCES)
    observed: list[str] = []
    for step in task.steps:
        if step.op == "read":
            observed.append(f"READ {step.resource} -> {state.get(step.resource, '<missing>')}")
        elif step.op == "write":
            state[step.resource] = step.value
            observed.append(f"WRITE {step.resource} -> {step.value}")
        elif step.op == "compute":
            observed.append(f"COMPUTE {step.resource} -> {step.value.upper()}")
        else:
            raise ValueError(f"Unknown operation: {step.op}")
    return tuple(observed), tuple(sorted(state.items()))


def execute(task: Task, *, reuse_exact_reads: bool) -> Result:
    """Execute a synthetic task with optional exact read-only reuse.

    The cache key includes the resource version. Any write to a resource
    increments its version, so an old cached read cannot cross a mutation.
    No side-effectful step is cached.
    """
    state = dict(INITIAL_RESOURCES)
    version: dict[str, int] = {}
    read_cache: dict[tuple[str, int], str] = {}
    transcript: list[str] = []
    charged = 0
    executed_reads = 0
    reused_reads = 0

    for step in task.steps:
        if step.op == "read":
            cache_key = (step.resource, version.get(step.resource, 0))
            if reuse_exact_reads and cache_key in read_cache:
                observed = read_cache[cache_key]
                reused_reads += 1
            else:
                observed = state.get(step.resource, "<missing>")
                charged += SIMULATED_MICRO_USD["read"]
                executed_reads += 1
                if reuse_exact_reads:
                    read_cache[cache_key] = observed
            transcript.append(f"READ {step.resource} -> {observed}")
        elif step.op == "write":
            state[step.resource] = step.value
            version[step.resource] = version.get(step.resource, 0) + 1
            # Writes always happen; prior cached values become ineligible by version.
            charged += SIMULATED_MICRO_USD["write"]
            transcript.append(f"WRITE {step.resource} -> {step.value}")
        elif step.op == "compute":
            charged += SIMULATED_MICRO_USD["compute"]
            transcript.append(f"COMPUTE {step.resource} -> {step.value.upper()}")
        else:
            raise ValueError(f"Unknown operation: {step.op}")

    expected_transcript, expected_state = reference_interpreter(task)
    actual_transcript = tuple(transcript)
    actual_state = tuple(sorted(state.items()))
    return Result(
        task=task.name,
        passed_reference=(actual_transcript == expected_transcript and actual_state == expected_state),
        simulated_cost_micro_usd=charged,
        real_read_executions=executed_reads,
        reused_reads=reused_reads,
        transcript=actual_transcript,
        final_resources=actual_state,
    )


def unique_read_tasks(count: int = 60) -> tuple[Task, ...]:
    """Negative control: each key is read at most once per task."""
    return tuple(
        Task(
            name=f"unique-{i:03d}",
            steps=(
                Step("read", "alpha"),
                Step("read", "beta"),
                Step("write", "gamma", f"G{i}"),
                Step("compute", "sum", f"task{i}"),
            ),
        )
        for i in range(count)
    )


def engineered_duplicate_tasks(count: int = 24) -> tuple[Task, ...]:
    """Positive control: repeats are inserted deliberately.

    Reads before and after a write are *not* interchangeable. This is a
    mechanism test only; it is not a sample of natural agent behavior.
    """
    return tuple(
        Task(
            name=f"constructed-{i:03d}",
            steps=(
                Step("read", "alpha"),
                Step("read", "alpha"),  # can reuse the first read
                Step("write", "alpha", f"A{i+1}"),
                Step("read", "alpha"),  # must execute: version changed
                Step("read", "alpha"),  # can reuse the read AFTER the mutation
                Step("compute", "verify", f"ok{i}"),
            ),
        )
        for i in range(count)
    )


def summarize(results: tuple[Result, ...]) -> dict[str, int | float | None]:
    total_cost = sum(r.simulated_cost_micro_usd for r in results)
    successes = sum(r.passed_reference for r in results)
    return {
        "tasks": len(results),
        "successful_tasks": successes,
        "failed_tasks": len(results) - successes,
        "simulated_total_cost_usd": round(total_cost / 1_000_000, 8),
        "simulated_cost_per_success_usd": round(total_cost / 1_000_000 / successes, 8)
        if successes else None,
        "executed_reads": sum(r.real_read_executions for r in results),
        "reused_reads": sum(r.reused_reads for r in results),
    }


def scenario(name: str, tasks: tuple[Task, ...]) -> dict[str, object]:
    before = tuple(execute(t, reuse_exact_reads=False) for t in tasks)
    after = tuple(execute(t, reuse_exact_reads=True) for t in tasks)
    if any(b.transcript != a.transcript or b.final_resources != a.final_resources
           for b, a in zip(before, after)):
        raise AssertionError("Outcome/state changed under the tested optimization")

    b = summarize(before)
    a = summarize(after)
    before_cost = int(round(b["simulated_total_cost_usd"] * 1_000_000))
    after_cost = int(round(a["simulated_total_cost_usd"] * 1_000_000))
    return {
        "scenario": name,
        "baseline": b,
        "strict_read_reuse": a,
        "simulated_cost_reduction_usd": round((before_cost - after_cost) / 1_000_000, 8),
        "simulated_cost_reduction_pct": round(100 * (before_cost - after_cost) / before_cost, 4)
        if before_cost else None,
        "same_transcript_and_state_all_tasks": True,
    }


def make_report() -> dict[str, object]:
    return {
        "provenance": "NEW explanatory public simulator, November 2026; NOT the original private Melior benchmark",
        "source": "experiments/public_demo.py",
        "network_calls": 0,
        "real_provider_spend_usd": 0,
        "real_cloud_spend_usd": 0,
        "cost_model_micro_usd_per_operation": SIMULATED_MICRO_USD,
        "scenarios": [
            scenario("unique-reads-negative-control", unique_read_tasks()),
            scenario("engineered-duplicates-positive-control", engineered_duplicate_tasks()),
        ],
        "limitations": [
            "All tasks and prices are synthetic; not an agent, LLM, or cloud workload.",
            "Positive-control repetitions are deliberately constructed.",
            "Simulated cost reduction is not actual savings or a generalization estimate.",
            "No sampling uncertainty is estimated for this deterministic demonstration.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print deterministic JSON report")
    args = parser.parse_args()
    report = make_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    print("Melior | PUBLIC synthetic mechanism demonstration (not historical private results)")
    for result in report["scenarios"]:
        print(f"\n{result['scenario']}")
        print(f"  Tasks: {result['baseline']['tasks']} | successes: {result['strict_read_reuse']['successful_tasks']}")
        print(f"  Eligible reused reads: {result['strict_read_reuse']['reused_reads']}")
        print(f"  Simulated total cost: ${result['baseline']['simulated_total_cost_usd']:.6f} -> "
              f"${result['strict_read_reuse']['simulated_total_cost_usd']:.6f}")
        print(f"  Simulated reduction: {result['simulated_cost_reduction_pct']:.2f}%")
        print("  All transcripts and final state identical: yes")
    print("\nNo APIs, cloud resources or live agents were used. See docs/experiment-design.md.")


if __name__ == "__main__":
    main()
