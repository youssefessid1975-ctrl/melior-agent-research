"""Deterministic unit tests for the separate public synthetic demonstration."""

import unittest
from dataclasses import replace

from experiments.public_demo import (
    Result,
    Step,
    Task,
    engineered_duplicate_tasks,
    execute,
    make_report,
    scenario,
    summarize,
    unique_read_tasks,
)


class PublicDemoTests(unittest.TestCase):
    def test_duplicate_read_is_reused_without_changing_outcome(self):
        task = Task("read twice", (Step("read", "alpha"), Step("read", "alpha")))
        baseline = execute(task, reuse_exact_reads=False)
        optimized = execute(task, reuse_exact_reads=True)
        self.assertTrue(optimized.passed_reference)
        self.assertEqual(optimized.reused_reads, 1)
        self.assertEqual(optimized.real_read_executions, 1)
        self.assertEqual(optimized.transcript, baseline.transcript)
        self.assertLess(optimized.simulated_cost_micro_usd, baseline.simulated_cost_micro_usd)

    def test_write_invalidates_previous_read_value(self):
        task = Task("mutated", (Step("read", "alpha"), Step("write", "alpha", "NEW"), Step("read", "alpha")))
        result = execute(task, reuse_exact_reads=True)
        self.assertTrue(result.passed_reference)
        self.assertEqual(result.reused_reads, 0)
        self.assertEqual(result.real_read_executions, 2)
        self.assertIn("READ alpha -> NEW", result.transcript)

    def test_writes_are_not_reused(self):
        task = Task("two writes", (Step("write", "alpha", "V"), Step("write", "alpha", "V")))
        result = execute(task, reuse_exact_reads=True)
        self.assertTrue(result.passed_reference)
        self.assertEqual(result.reused_reads, 0)
        self.assertEqual(result.simulated_cost_micro_usd, 8000)

    def test_compute_operations_are_not_reused(self):
        task = Task("repeat compute", (Step("compute", "x", "hello"), Step("compute", "x", "hello")))
        result = execute(task, reuse_exact_reads=True)
        self.assertTrue(result.passed_reference)
        self.assertEqual(result.simulated_cost_micro_usd, 2000)

    def test_missing_resource_is_stably_reused(self):
        task = Task("missing", (Step("read", "unknown"), Step("read", "unknown")))
        result = execute(task, reuse_exact_reads=True)
        self.assertTrue(result.passed_reference)
        self.assertEqual(result.reused_reads, 1)

    def test_no_op_control_reuses_no_reads(self):
        result = scenario("negative", unique_read_tasks(8))
        self.assertEqual(result["strict_read_reuse"]["reused_reads"], 0)
        self.assertEqual(result["simulated_cost_reduction_pct"], 0)
        self.assertTrue(result["same_transcript_and_state_all_tasks"])

    def test_engineered_repeats_reduce_only_simulated_cost(self):
        result = scenario("positive", engineered_duplicate_tasks(6))
        self.assertEqual(result["strict_read_reuse"]["reused_reads"], 12)
        self.assertGreater(result["simulated_cost_reduction_pct"], 0)
        self.assertTrue(result["same_transcript_and_state_all_tasks"])

    def test_metric_counts_failures_in_numerator_and_handles_zero_success(self):
        good = execute(Task("good", (Step("read", "alpha"),)), reuse_exact_reads=False)
        bad = replace(good, task="bad", passed_reference=False)
        both = summarize((good, bad))
        self.assertEqual(both["successful_tasks"], 1)
        self.assertEqual(both["simulated_total_cost_usd"], 0.004)
        self.assertEqual(both["simulated_cost_per_success_usd"], 0.004)
        zero = summarize((bad,))
        self.assertIsNone(zero["simulated_cost_per_success_usd"])

    def test_report_discloses_synthetic_origin(self):
        report = make_report()
        self.assertIn("NOT the original", report["provenance"])
        self.assertEqual(report["real_provider_spend_usd"], 0)
        self.assertEqual(report["real_cloud_spend_usd"], 0)


if __name__ == "__main__":
    unittest.main()
