# CAPSTONE 13 — Operating Systems Concepts Explainer Pack 🖥️

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Target Audience](https://img.shields.io/badge/Target-3rd--Semester%20CSE-emerald.svg)](#)
[![Simulation Accuracy](https://img.shields.io/badge/Simulation%20Accuracy-100%25%20Verified-brightgreen.svg)](#)
[![Capstone Weightage](https://img.shields.io/badge/Weightage-100%20Marks-purple.svg)](#)

> **Author:** Jerushlin W  
> **Course:** Computer Science and Engineering (CSE) — Operating Systems Core Curriculum  
> **Project Title:** CAPSTONE 13 — Operating Systems Concepts Explainer Pack  
> **Target Audience:** 3rd-Semester B.Tech / B.E. Computer Science & Engineering Students  

---

## 📌 Executive Summary

Undergraduate students encountering Operating Systems for the first time in their 3rd semester often struggle to bridge the gap between abstract textbook mathematics (CPU scheduling formulas, page table lookups, deadlock graph cycles) and real-world system behavior. 

**CAPSTONE 13** solves this pedagogical bottleneck by providing a cohesive, production-ready educational ecosystem comprising:
1. **Engaging Real-Life Analogies & Deep Notes:** Deconstructs 6 core OS concepts (Scheduling, Contiguous vs. Non-Contiguous Memory, Paging & MMU, Coffman Deadlocks, Demand Paging, and Semaphores vs. Mutex) into everyday mental models.
2. **Deterministic Python Simulation Engine (`scheduler_sim.py`):** Implements FCFS, Non-Preemptive SJF, and Round Robin scheduling with ASCII Gantt charts and automated turnaround/waiting time computation.
3. **Automated Documentation Utility (`scheduler_automation.py`):** Parses JSON workloads and generates formatted Markdown reports for lab assignments.
4. **Interactive Single-Page Web Laboratory (`index.html`):** A responsive, dark-mode web application featuring real-time interactive Gantt rendering, an address translation MMU visualizer, a Coffman deadlock state inspector, an interactive 6-slide presentation deck, and a 12-question quiz engine.
5. **Responsible AI Verification & Hallucination Audit:** Rigorous verification comparing simulated outputs against manual hand calculations and documenting 3 common AI hallucination pitfalls in OS education with authoritative citations.

---

## 📂 Repository Structure

```text
capstone13-os-explainer-pack/
│
├── index.html                    # Interactive Single-Page Web Application & Visualizer
├── scheduler_sim.py              # Core Python CPU Scheduling Simulation Engine
├── scheduler_automation.py       # Automated JSON-to-Markdown Workload Runner
├── test_scheduler.py             # Unit Test Suite & Mathematical Hand-Verification
│
├── data/
│   └── sample_processes.json     # Sample Workloads (Canonical, Convoy Effect, Idle Gaps)
│
├── docs/
│   ├── AUTOMATED_SCHEDULING_REPORT.md   # Auto-generated Lab Benchmark Report
│   └── CAPSTONE_13_FINAL_REPORT.md      # Comprehensive 100-Mark Capstone Report
│
└── README.md                     # Repository Guide & Documentation
```

---

## 🚀 Quick Start Guide

### 1. Launch the Interactive Web Application
No build tools, Node.js, or complex web servers required. Simply open `index.html` in any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Brave):
```powershell
# Double-click index.html or launch via command line:
Start-Process "index.html"
```

### 2. Run the Python Simulation Engine
Execute the standalone CPU scheduler benchmark:
```powershell
python scheduler_sim.py
```
This runs the canonical 4-process workload ($P_1, P_2, P_3, P_4$) across FCFS, SJF, and Round Robin, outputting ASCII Gantt charts and cross-algorithm metric comparisons.

### 3. Run Automated Workload Reports
Parse process workload files from JSON and generate formatted Markdown tables:
```powershell
python scheduler_automation.py --input data/sample_processes.json --output docs/AUTOMATED_SCHEDULING_REPORT.md
```

### 4. Run Unit Tests & Mathematical Verification
Validate simulated metrics against known hand calculations:
```powershell
python test_scheduler.py
```

---

## 🧮 Canonical Benchmark Workload

The engine comes pre-configured with the standard 4-process verification workload:

| Process | Arrival Time ($AT$) | Burst Time ($BT$) |
|:-------:|:------------------:|:----------------:|
| **P1**  | 0 ms               | 5 ms             |
| **P2**  | 1 ms               | 3 ms             |
| **P3**  | 2 ms               | 8 ms             |
| **P4**  | 3 ms               | 6 ms             |

### Comparative Benchmark Results

| Algorithm | Avg Turnaround Time ($TAT$) | Avg Waiting Time ($WT$) | Avg Response Time ($RT$) | Schedule Duration |
|:---|:---:|:---:|:---:|:---:|
| **FCFS** | 11.25 ms | 5.75 ms | 5.75 ms | 22 ms |
| **SJF (Non-Preemptive)** | **10.75 ms** | **5.25 ms** | 5.25 ms | 22 ms |
| **Round Robin ($Q=2$)** | 15.25 ms | 9.75 ms | **2.00 ms** | 22 ms |

*Note: SJF achieves the minimum average turnaround and waiting times, while Round Robin provides the highest responsiveness (lowest average response time of 2.00 ms).*

---

## 🛡️ Responsible AI & Ethical Verification

This project adheres strictly to responsible AI principles:
- **Zero Variance Guarantee:** Simulation outputs were verified cell-by-cell against manual algebraic hand calculations. Error rate: **0.000%**.
- **AI Hallucination Audit:** Identifies and documents 3 widespread AI errors in OS theory:
  1. *Arrival-time blindness in Non-Preemptive SJF*.
  2. *Confusing internal vs. external fragmentation in Paging*.
  3. *Recommending spinlocks on uniprocessor architectures*.
- **Authoritative Textbooks Cited:** All corrections are backed by Silberschatz et al. (*Operating System Concepts*, 10th Ed.), Tanenbaum (*Modern Operating Systems*, 4th Ed.), and the official Linux Kernel Documentation.

---

## 📜 License
Distributed under the MIT License. Open for educational and classroom use.
