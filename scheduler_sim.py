"""
CAPSTONE 13 — Operating Systems Concepts Explainer Pack
Module: Process Scheduling Simulation Engine
Author: Jerushlin W (Lead OS Engineer / Student Researcher)
Target Audience: 3rd-Semester CSE Students
Algorithms Implemented:
  1. First-Come, First-Served (FCFS)
  2. Shortest Job First (SJF - Non-Preemptive)
  3. Round Robin (RR) with configurable Time Quantum
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import copy


@dataclass
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    remaining_time: int = field(init=False)
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    start_time: int = -1
    response_time: int = -1

    def __post_init__(self):
        self.remaining_time = self.burst_time


@dataclass
class GanttSegment:
    pid: str  # PID or 'IDLE'
    start_time: int
    end_time: int


@dataclass
class SimulationResult:
    algorithm_name: str
    processes: List[Process]
    gantt_chart: List[GanttSegment]
    avg_turnaround_time: float
    avg_waiting_time: float
    avg_response_time: float
    total_time: int
    cpu_utilization: float


class SchedulerSimulator:
    """
    Modular Operating System CPU Scheduling Engine.
    Accurately tracks arrival order, CPU idle gaps, and context switches.
    """

    @staticmethod
    def simulate_fcfs(processes: List[Process]) -> SimulationResult:
        """
        First-Come, First-Served (FCFS) Scheduling.
        Non-preemptive algorithm servicing processes in order of arrival time.
        """
        # Create deep copies to prevent side-effects across simulations
        procs = sorted([copy.deepcopy(p) for p in processes], key=lambda x: (x.arrival_time, x.pid))
        
        current_time = 0
        gantt: List[GanttSegment] = []

        for p in procs:
            # Handle CPU idle gap if next process arrives after current_time
            if current_time < p.arrival_time:
                gantt.append(GanttSegment(pid="IDLE", start_time=current_time, end_time=p.arrival_time))
                current_time = p.arrival_time

            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.remaining_time = 0

            gantt.append(GanttSegment(pid=p.pid, start_time=p.start_time, end_time=p.completion_time))

        return SchedulerSimulator._generate_result("First-Come, First-Served (FCFS)", procs, gantt)

    @staticmethod
    def simulate_sjf_non_preemptive(processes: List[Process]) -> SimulationResult:
        """
        Shortest Job First (SJF) Scheduling (Non-Preemptive).
        Selects the process with the smallest burst time from all arrived processes.
        Tie-breaker: Earlier arrival time, then PID lexicographical order.
        """
        procs = [copy.deepcopy(p) for p in processes]
        n = len(procs)
        completed_count = 0
        current_time = 0
        gantt: List[GanttSegment] = []
        is_completed = [False] * n

        while completed_count < n:
            # Find all available processes at current_time that are not completed
            available_indices = [
                i for i in range(n)
                if not is_completed[i] and procs[i].arrival_time <= current_time
            ]

            if not available_indices:
                # CPU is idle; jump time to the next arriving process
                next_arrival = min(procs[i].arrival_time for i in range(n) if not is_completed[i])
                gantt.append(GanttSegment(pid="IDLE", start_time=current_time, end_time=next_arrival))
                current_time = next_arrival
                continue

            # Pick process with shortest burst time; tie break with arrival time
            idx = min(
                available_indices,
                key=lambda i: (procs[i].burst_time, procs[i].arrival_time, procs[i].pid)
            )
            p = procs[idx]

            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time
            current_time += p.burst_time
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.remaining_time = 0

            is_completed[idx] = True
            completed_count += 1
            gantt.append(GanttSegment(pid=p.pid, start_time=p.start_time, end_time=p.completion_time))

        return SchedulerSimulator._generate_result("Shortest Job First (SJF - Non-Preemptive)", procs, gantt)

    @staticmethod
    def simulate_round_robin(processes: List[Process], time_quantum: int = 2) -> SimulationResult:
        """
        Round Robin (RR) Scheduling.
        Preemptive algorithm where each process gets CPU time up to 'time_quantum'.
        Newly arrived processes are queued at their arrival time.
        When a process finishes its slice at time T, newly arrived processes at time T
        enter the ready queue BEFORE the pre-empted process re-enters.
        """
        if time_quantum <= 0:
            raise ValueError("Time Quantum must be a positive integer > 0.")

        # Sort input processes by arrival time initially
        raw_procs = sorted([copy.deepcopy(p) for p in processes], key=lambda x: (x.arrival_time, x.pid))
        proc_dict: Dict[str, Process] = {p.pid: p for p in raw_procs}
        
        current_time = 0
        ready_queue: List[str] = []
        arrived_pids = set()
        completed_pids = set()
        gantt_raw: List[GanttSegment] = []

        total_procs = len(raw_procs)

        # Enqueue initial arrivals at time 0 (or earliest arrival)
        for p in raw_procs:
            if p.arrival_time <= current_time:
                ready_queue.append(p.pid)
                arrived_pids.add(p.pid)

        while len(completed_pids) < total_procs:
            if not ready_queue:
                # Find earliest future arrival
                future_procs = [p for p in raw_procs if p.pid not in completed_pids and p.pid not in arrived_pids]
                if future_procs:
                    next_arrival = min(p.arrival_time for p in future_procs)
                    gantt_raw.append(GanttSegment(pid="IDLE", start_time=current_time, end_time=next_arrival))
                    current_time = next_arrival
                    for p in raw_procs:
                        if p.arrival_time <= current_time and p.pid not in arrived_pids:
                            ready_queue.append(p.pid)
                            arrived_pids.add(p.pid)
                continue

            curr_pid = ready_queue.pop(0)
            p = proc_dict[curr_pid]

            if p.start_time == -1:
                p.start_time = current_time
                p.response_time = p.start_time - p.arrival_time

            exec_time = min(p.remaining_time, time_quantum)
            seg_start = current_time
            current_time += exec_time
            p.remaining_time -= exec_time

            gantt_raw.append(GanttSegment(pid=p.pid, start_time=seg_start, end_time=current_time))

            # Important OS Queue Convention: Check for newly arrived processes during [seg_start+1, current_time]
            # They enter the ready queue BEFORE the current process is re-added
            for other_p in raw_procs:
                if (other_p.arrival_time <= current_time and 
                        other_p.pid not in arrived_pids and 
                        other_p.pid not in completed_pids):
                    ready_queue.append(other_p.pid)
                    arrived_pids.add(other_p.pid)

            if p.remaining_time == 0:
                p.completion_time = current_time
                p.turnaround_time = p.completion_time - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                completed_pids.add(p.pid)
            else:
                # Re-queue preempted process
                ready_queue.append(p.pid)

        # Merge contiguous gantt segments with identical PID
        merged_gantt: List[GanttSegment] = []
        for seg in gantt_raw:
            if merged_gantt and merged_gantt[-1].pid == seg.pid and merged_gantt[-1].end_time == seg.start_time:
                merged_gantt[-1].end_time = seg.end_time
            else:
                merged_gantt.append(seg)

        procs_list = [proc_dict[p.pid] for p in raw_procs]
        return SchedulerSimulator._generate_result(f"Round Robin (RR, Quantum={time_quantum})", procs_list, merged_gantt)

    @staticmethod
    def _generate_result(alg_name: str, procs: List[Process], gantt: List[GanttSegment]) -> SimulationResult:
        n = len(procs)
        avg_tat = sum(p.turnaround_time for p in procs) / n if n > 0 else 0.0
        avg_wt = sum(p.waiting_time for p in procs) / n if n > 0 else 0.0
        avg_rt = sum(p.response_time for p in procs) / n if n > 0 else 0.0
        
        total_time = gantt[-1].end_time if gantt else 0
        busy_time = sum(seg.end_time - seg.start_time for seg in gantt if seg.pid != "IDLE")
        cpu_util = (busy_time / total_time * 100.0) if total_time > 0 else 0.0

        # Sort procs alphabetically by PID for clean presentation
        procs.sort(key=lambda x: x.pid)

        return SimulationResult(
            algorithm_name=alg_name,
            processes=procs,
            gantt_chart=gantt,
            avg_turnaround_time=round(avg_tat, 2),
            avg_waiting_time=round(avg_wt, 2),
            avg_response_time=round(avg_rt, 2),
            total_time=total_time,
            cpu_utilization=round(cpu_util, 2)
        )


class Visualizer:
    """
    Renders formatted ASCII Gantt charts and markdown tables.
    """

    @staticmethod
    def render_ascii_gantt(gantt: List[GanttSegment], width_per_unit: int = 2) -> str:
        """
        Creates a crisp, dual-line ASCII Gantt chart with precise timestamps.
        Example:
        |  P1  |  P2  |  P3  |
        0      5      8      16
        """
        if not gantt:
            return "[Empty Gantt Chart]"

        # Bar representation
        top_bar = "+"
        label_bar = "|"
        time_bar = ""

        # We construct blocks
        timestamps = [gantt[0].start_time]
        block_labels = []

        for seg in gantt:
            duration = seg.end_time - seg.start_time
            # Cell width proportional to duration, minimum 6 characters for readability
            cell_width = max(len(seg.pid) + 2, duration * width_per_unit)
            
            # Format top border
            top_bar += "-" * cell_width + "+"
            
            # Format label centered
            centered_pid = seg.pid.center(cell_width)
            label_bar += centered_pid + "|"
            
            timestamps.append(seg.end_time)
            block_labels.append(cell_width)

        # Build timeline string matching the column positions
        time_bar = str(timestamps[0])
        for i, width in enumerate(block_labels):
            next_t = str(timestamps[i + 1])
            # Calculate spaces needed so next_t aligns directly below the right '|'
            spaces_needed = width - len(next_t) + 1
            if spaces_needed < 1:
                spaces_needed = 1
            time_bar += " " * (spaces_needed - 1) + next_t

        return f"{top_bar}\n{label_bar}\n{top_bar}\n{time_bar}"

    @staticmethod
    def render_process_table(result: SimulationResult) -> str:
        header = "| Process | Arrival Time (AT) | Burst Time (BT) | Completion Time (CT) | Turnaround Time (TAT) | Waiting Time (WT) | Response Time (RT) |"
        sep    = "|:-------:|:-----------------:|:---------------:|:--------------------:|:---------------------:|:-----------------:|:------------------:|"
        rows = [header, sep]
        for p in result.processes:
            rows.append(f"| {p.pid:^7} | {p.arrival_time:^17} | {p.burst_time:^15} | {p.completion_time:^20} | {p.turnaround_time:^21} | {p.waiting_time:^17} | {p.response_time:^18} |")
        return "\n".join(rows)

    @staticmethod
    def render_comparison_summary(results: List[SimulationResult]) -> str:
        header = "| Algorithm | Avg Turnaround Time (TAT) | Avg Waiting Time (WT) | Avg Response Time (RT) | Total Time | CPU Utilization |"
        sep    = "|:--------------------------------------|:-------------------------:|:---------------------:|:----------------------:|:----------:|:---------------:|"
        rows = [header, sep]
        for r in results:
            rows.append(f"| {r.algorithm_name:<38} | {r.avg_turnaround_time:^25.2f} | {r.avg_waiting_time:^21.2f} | {r.avg_response_time:^22.2f} | {r.total_time:^10} | {r.cpu_utilization:^14.1f}% |")
        return "\n".join(rows)


def run_capstone_benchmark() -> Tuple[List[SimulationResult], str]:
    """
    Standard benchmark test set for CSE 3rd semester capstone verification.
    4 processes with varying arrival and burst times:
      P1: AT = 0, BT = 5
      P2: AT = 1, BT = 3
      P3: AT = 2, BT = 8
      P4: AT = 3, BT = 6
    """
    sample_processes = [
        Process(pid="P1", arrival_time=0, burst_time=5),
        Process(pid="P2", arrival_time=1, burst_time=3),
        Process(pid="P3", arrival_time=2, burst_time=8),
        Process(pid="P4", arrival_time=3, burst_time=6),
    ]

    fcfs_res = SchedulerSimulator.simulate_fcfs(sample_processes)
    sjf_res = SchedulerSimulator.simulate_sjf_non_preemptive(sample_processes)
    rr_res = SchedulerSimulator.simulate_round_robin(sample_processes, time_quantum=2)

    results = [fcfs_res, sjf_res, rr_res]

    output_lines = [
        "=" * 78,
        "CAPSTONE 13: CPU SCHEDULING SIMULATION ENGINE BENCHMARK",
        "=" * 78,
        "\nInput Benchmark Workload:",
        "  P1 -> Arrival Time: 0 | Burst Time: 5",
        "  P2 -> Arrival Time: 1 | Burst Time: 3",
        "  P3 -> Arrival Time: 2 | Burst Time: 8",
        "  P4 -> Arrival Time: 3 | Burst Time: 6",
        "\n"
    ]

    for res in results:
        output_lines.append(f"### Algorithm: {res.algorithm_name}")
        output_lines.append("\nGantt Chart Timeline:")
        output_lines.append(Visualizer.render_ascii_gantt(res.gantt_chart, width_per_unit=3))
        output_lines.append("\nProcess Execution Metrics:")
        output_lines.append(Visualizer.render_process_table(res))
        output_lines.append(f"\n=> Avg Turnaround Time (TAT): {res.avg_turnaround_time} ms")
        output_lines.append(f"=> Avg Waiting Time (WT):       {res.avg_waiting_time} ms")
        output_lines.append(f"=> Avg Response Time (RT):      {res.avg_response_time} ms")
        output_lines.append(f"=> CPU Utilization:             {res.cpu_utilization}%\n")
        output_lines.append("-" * 78)

    output_lines.append("\n### Cross-Algorithm Comparative Analysis Summary")
    output_lines.append(Visualizer.render_comparison_summary(results))
    output_lines.append("\n" + "=" * 78)

    full_output = "\n".join(output_lines)
    return results, full_output


if __name__ == "__main__":
    _, report = run_capstone_benchmark()
    print(report)
