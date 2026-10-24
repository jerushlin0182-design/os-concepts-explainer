"""
CAPSTONE 13 — Operating Systems Concepts Explainer Pack
Module: Scheduling Automation Utility Script
Author: Jerushlin W (Lead OS Engineer / Student Researcher)
Target Audience: 3rd-Semester CSE Students

Description:
  Automates the execution and Markdown report generation for process scheduling
  workloads loaded from JSON or Python dictionaries. Streamlines documentation,
  lab reports, and research papers.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List
from scheduler_sim import Process, SchedulerSimulator, Visualizer, SimulationResult


class SchedulingAutomationEngine:
    """
    Automated pipeline for evaluating and generating Markdown reports
    from structured process workload definitions.
    """

    def __init__(self, json_path: str = None, data_dict: Dict[str, Any] = None):
        self.test_cases = []
        if json_path:
            path = Path(json_path)
            if not path.exists():
                raise FileNotFoundError(f"JSON input file not found: {json_path}")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.test_cases = data.get("test_cases", [])
        elif data_dict:
            self.test_cases = data_dict.get("test_cases", [])
        else:
            raise ValueError("Either json_path or data_dict must be provided.")

    def run_all(self, output_markdown_path: str = None) -> str:
        """
        Executes simulations across all test cases and compiles a Markdown document.
        """
        md_lines = [
            "# CAPSTONE 13: Automated CPU Scheduling Performance Report",
            "**Target Audience:** 3rd-Semester CSE Operating Systems Lab & Theory Students  ",
            "**Author:** Jerushlin W  ",
            "**Engine:** Python High-Precision OS Scheduling Simulator  \n",
            "> [!NOTE]",
            "> This automated report compares FCFS, SJF (Non-preemptive), and Round Robin across multiple workload profiles.",
            "> All metrics are verified using standard formulas: $TAT = CT - AT$, $WT = TAT - BT$.\n",
            "---"
        ]

        for idx, tc in enumerate(self.test_cases, 1):
            name = tc.get("name", f"Test_Case_{idx}")
            desc = tc.get("description", "No description provided.")
            quantum = tc.get("time_quantum", 2)
            raw_procs = tc.get("processes", [])

            md_lines.append(f"## Test Case {idx}: {name}")
            md_lines.append(f"**Description:** {desc}  ")
            md_lines.append(f"**Configured Time Quantum (RR):** `{quantum}` units\n")

            # Input Table
            md_lines.append("### 1. Workload Specification")
            md_lines.append("| Process ID | Arrival Time (AT) | Burst Time (BT) |")
            md_lines.append("|:----------:|:-----------------:|:---------------:|")
            for p in raw_procs:
                md_lines.append(f"| **{p['pid']}** | {p['arrival_time']} ms | {p['burst_time']} ms |")
            md_lines.append("")

            # Convert to Process dataclasses
            proc_objs = [Process(pid=p["pid"], arrival_time=p["arrival_time"], burst_time=p["burst_time"]) for p in raw_procs]

            # Run simulations
            fcfs_res = SchedulerSimulator.simulate_fcfs(proc_objs)
            sjf_res = SchedulerSimulator.simulate_sjf_non_preemptive(proc_objs)
            rr_res = SchedulerSimulator.simulate_round_robin(proc_objs, time_quantum=quantum)
            results = [fcfs_res, sjf_res, rr_res]

            md_lines.append("### 2. Execution Breakdown & Metrics")
            for res in results:
                md_lines.append(f"#### {res.algorithm_name}")
                md_lines.append("```text")
                md_lines.append(Visualizer.render_ascii_gantt(res.gantt_chart, width_per_unit=3))
                md_lines.append("```")
                md_lines.append(Visualizer.render_process_table(res))
                md_lines.append("")

            # Summary Table
            md_lines.append("### 3. Summary Performance Comparison")
            md_lines.append(Visualizer.render_comparison_summary(results))
            
            # Winner determination
            best_tat = min(results, key=lambda r: r.avg_turnaround_time)
            best_wt = min(results, key=lambda r: r.avg_waiting_time)
            md_lines.append(f"\n- **Optimal for Turnaround Time:** `{best_tat.algorithm_name}` ({best_tat.avg_turnaround_time} ms)")
            md_lines.append(f"- **Optimal for Waiting Time:** `{best_wt.algorithm_name}` ({best_wt.avg_waiting_time} ms)\n")
            md_lines.append("---\n")

        full_md = "\n".join(md_lines)

        if output_markdown_path:
            out_file = Path(output_markdown_path)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(full_md)
            print(f"[SUCCESS] Automated Markdown report generated at: {out_file.resolve()}")

        return full_md


def main():
    parser = argparse.ArgumentParser(description="Automated Process Scheduling Table & Report Generator")
    parser.add_argument("--input", "-i", type=str, default="data/sample_processes.json", help="Path to input JSON file")
    parser.add_argument("--output", "-o", type=str, default="docs/AUTOMATED_SCHEDULING_REPORT.md", help="Path to output Markdown file")
    args = parser.parse_args()

    engine = SchedulingAutomationEngine(json_path=args.input)
    report_content = engine.run_all(output_markdown_path=args.output)
    print("\n--- SAMPLE REPORT PREVIEW (First 25 lines) ---")
    for line in report_content.splitlines()[:25]:
        print(line)


if __name__ == "__main__":
    main()
