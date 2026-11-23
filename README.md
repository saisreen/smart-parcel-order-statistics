# Assignment 6 — Smart Parcel Processing

This project demonstrates deterministic Median of Medians, randomized Quickselect, and elementary data structures through a parcel-sorting example. Written in Python 3 with no external packages.

## Repository files
- `selection_algorithms.py` — kth-smallest selection (1-based rank)
- `data_structures.py` — arrays, matrix, stack, circular queue, singly linked list
- `benchmark.py` — reproducible runtime experiment
- `benchmark_results.csv` — actual recorded timing results
- `test_assignment.py` — correctness and edge-case tests
- `REPORT.md` — full report, recurrence analysis, results, and applications
- `benchmark_console.txt` — raw benchmark output

## Run instructions
Install Python 3.9 or later. Open a terminal in this repository folder and run:

```bash
python selection_algorithms.py
python data_structures.py
python -m unittest -v
python benchmark.py
```

The benchmark writes a new `benchmark_results.csv`. Results may change on another machine. `k` is 1-based, and duplicate values count toward ranks.

## Summary
Median of Medians guarantees O(n) worst-case time; randomized Quickselect has O(n) expected time and O(n²) worst-case time. The implementation uses three-way partitions to handle duplicates. Arrays provide fast indexed access, stacks give LIFO order, circular queues give FIFO order, and linked lists support flexible node insertion.

## Academic submission
Read and understand the implementation, add your student information to the report, run the code yourself, and follow your institution's rules about AI assistance.
