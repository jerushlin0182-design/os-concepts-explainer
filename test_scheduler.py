"""
Unit tests and mathematical verification suite for Process Scheduling Engine.
Validates FCFS, SJF (Non-preemptive), and Round Robin against known hand calculations.
"""

import unittest
from scheduler_sim import Process, SchedulerSimulator


class TestSchedulerSimulator(unittest.TestCase):

    def setUp(self):
        # Canonical 4-process workload
        self.benchmark_procs = [
            Process(pid="P1", arrival_time=0, burst_time=5),
            Process(pid="P2", arrival_time=1, burst_time=3),
            Process(pid="P3", arrival_time=2, burst_time=8),
            Process(pid="P4", arrival_time=3, burst_time=6),
        ]

    def test_fcfs_metrics(self):
        result = SchedulerSimulator.simulate_fcfs(self.benchmark_procs)
        proc_map = {p.pid: p for p in result.processes}

        # Hand calculation verification
        self.assertEqual(proc_map["P1"].completion_time, 5)
        self.assertEqual(proc_map["P1"].turnaround_time, 5)
        self.assertEqual(proc_map["P1"].waiting_time, 0)

        self.assertEqual(proc_map["P2"].completion_time, 8)
        self.assertEqual(proc_map["P2"].turnaround_time, 7)
        self.assertEqual(proc_map["P2"].waiting_time, 4)

        self.assertEqual(proc_map["P3"].completion_time, 16)
        self.assertEqual(proc_map["P3"].turnaround_time, 14)
        self.assertEqual(proc_map["P3"].waiting_time, 6)

        self.assertEqual(proc_map["P4"].completion_time, 22)
        self.assertEqual(proc_map["P4"].turnaround_time, 19)
        self.assertEqual(proc_map["P4"].waiting_time, 13)

        self.assertAlmostEqual(result.avg_turnaround_time, 11.25, places=2)
        self.assertAlmostEqual(result.avg_waiting_time, 5.75, places=2)

    def test_sjf_non_preemptive_metrics(self):
        result = SchedulerSimulator.simulate_sjf_non_preemptive(self.benchmark_procs)
        proc_map = {p.pid: p for p in result.processes}

        self.assertEqual(proc_map["P1"].completion_time, 5)
        self.assertEqual(proc_map["P1"].turnaround_time, 5)
        self.assertEqual(proc_map["P1"].waiting_time, 0)

        self.assertEqual(proc_map["P2"].completion_time, 8)
        self.assertEqual(proc_map["P2"].turnaround_time, 7)
        self.assertEqual(proc_map["P2"].waiting_time, 4)

        self.assertEqual(proc_map["P4"].completion_time, 14)
        self.assertEqual(proc_map["P4"].turnaround_time, 11)
        self.assertEqual(proc_map["P4"].waiting_time, 5)

        self.assertEqual(proc_map["P3"].completion_time, 22)
        self.assertEqual(proc_map["P3"].turnaround_time, 20)
        self.assertEqual(proc_map["P3"].waiting_time, 12)

        self.assertAlmostEqual(result.avg_turnaround_time, 10.75, places=2)
        self.assertAlmostEqual(result.avg_waiting_time, 5.25, places=2)

    def test_round_robin_metrics(self):
        result = SchedulerSimulator.simulate_round_robin(self.benchmark_procs, time_quantum=2)
        proc_map = {p.pid: p for p in result.processes}

        self.assertEqual(proc_map["P1"].completion_time, 14)
        self.assertEqual(proc_map["P1"].turnaround_time, 14)
        self.assertEqual(proc_map["P1"].waiting_time, 9)

        self.assertEqual(proc_map["P2"].completion_time, 11)
        self.assertEqual(proc_map["P2"].turnaround_time, 10)
        self.assertEqual(proc_map["P2"].waiting_time, 7)

        self.assertEqual(proc_map["P4"].completion_time, 20)
        self.assertEqual(proc_map["P4"].turnaround_time, 17)
        self.assertEqual(proc_map["P4"].waiting_time, 11)

        self.assertEqual(proc_map["P3"].completion_time, 22)
        self.assertEqual(proc_map["P3"].turnaround_time, 20)
        self.assertEqual(proc_map["P3"].waiting_time, 12)

        self.assertAlmostEqual(result.avg_turnaround_time, 15.25, places=2)
        self.assertAlmostEqual(result.avg_waiting_time, 9.75, places=2)

    def test_cpu_idle_handling(self):
        procs_with_gap = [
            Process(pid="PA", arrival_time=0, burst_time=3),
            Process(pid="PB", arrival_time=7, burst_time=2)
        ]
        res = SchedulerSimulator.simulate_fcfs(procs_with_gap)
        self.assertEqual(res.gantt_chart[0].pid, "PA")
        self.assertEqual(res.gantt_chart[0].end_time, 3)
        self.assertEqual(res.gantt_chart[1].pid, "IDLE")
        self.assertEqual(res.gantt_chart[1].start_time, 3)
        self.assertEqual(res.gantt_chart[1].end_time, 7)
        self.assertEqual(res.gantt_chart[2].pid, "PB")
        self.assertEqual(res.gantt_chart[2].end_time, 9)


if __name__ == "__main__":
    unittest.main()
