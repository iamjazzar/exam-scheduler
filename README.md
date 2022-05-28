# Palatable [![Tests](https://github.com/iamjazzar/palatable/actions/workflows/ci.yml/badge.svg)](https://github.com/iamjazzar/palatable/actions/workflows/ci.yml) [![PyPI version](https://badge.fury.io/py/djangomako.svg)](https://badge.fury.io/py/djangomako)

A Fast, reliable Exam Scheduling Algorithm Using Graph Coloring.


## About

This package presents a graph-coloring-based algorithm for the exam scheduling application, with the objective of achieving fairness, accuracy, and optimal exam time period. Through the work, we consider few assumptions and constraints, closely related to the general exam scheduling problem, and mainly driven from accumulated experience at various universities. The performance of the algorithm is also a major concern of this package.


## Getting started

```bash
pip install palatable
```

## Usage
The simplest way to use the package is using this command.
```bash
palatable -d files/schedule.txt -c files/courses.txt
```

For a list of all available options

```bash
palatable -h

usage: palatable [-h] [--slots SLOTS] [--days DAYS] [--fairness FAIRNESS] --schedule SCHEDULE --courses COURSES

optional arguments:
  -h, --help            show this help message and exit
  --slots SLOTS, -s SLOTS
                        Number of exam time slots in a given day (determined by the registrar and/or the faculty)
  --days DAYS, -y DAYS  The number of concurrent exam sessions. Bounded by available halls, and the availability of faculty to conduct the exams.
  --fairness FAIRNESS, -f FAIRNESS
                        An Exam schedule should avoid conflicts, in the sense that no two or more exams (this value) for the same student are scheduled at the same time.
  --schedule SCHEDULE, -d SCHEDULE
                        The path of the file for students' enrollments.
  --courses COURSES, -c COURSES
                        The path of the file that hosts courses' data.
```

## Upcoming
We are currently supporting text formatted courses and schedules tables. CSV support is coming up soon.

## References
This package is an implementation of the algorithm presented in the paper: [A New Exam Scheduling Algorithm Using Graph Coloring](https://www.researchgate.net/publication/220413840_A_New_Exam_Scheduling_Algorithm_Using_Graph_Coloring_) by [Mohammad Malkawi](https://www.researchgate.net/profile/Mohammad-Malkawi?_sg%5B0%5D=TEcNNzOft5bBstNFqBqpYNwlD33_i9hbPHM_VdM0ejEl9yLb0r3YiUfqNtuxs_Y_uhAnkis.hSKhfAlXAl3NayTteLeLyY8t6RSx4OY5b15bypYXrJ3un9Ua903F6jrnI7jd0JeCZ67_0fPe98qwQFfo3CHCCg&_sg%5B1%5D=S4XZH5xnJVzEZyFwfdiGPXYnO8827e3_7iQA-5Oslvj7kvxED8NPQBvgVdTnw2ZP_ntRNds.wtaWc_JUa6TzSo4B6VynSf39MvaGXV2dvYT6cXE2Lgmm9gJ95GS9FPHvt43RTIR5WjJU7XUw52NZlV_QmVvgvg), [Mohammad Al-Haj Hassan](https://www.researchgate.net/scientific-contributions/Mohammad-Al-Haj-Hassan-70934694?_sg%5B0%5D=TEcNNzOft5bBstNFqBqpYNwlD33_i9hbPHM_VdM0ejEl9yLb0r3YiUfqNtuxs_Y_uhAnkis.hSKhfAlXAl3NayTteLeLyY8t6RSx4OY5b15bypYXrJ3un9Ua903F6jrnI7jd0JeCZ67_0fPe98qwQFfo3CHCCg&_sg%5B1%5D=S4XZH5xnJVzEZyFwfdiGPXYnO8827e3_7iQA-5Oslvj7kvxED8NPQBvgVdTnw2ZP_ntRNds.wtaWc_JUa6TzSo4B6VynSf39MvaGXV2dvYT6cXE2Lgmm9gJ95GS9FPHvt43RTIR5WjJU7XUw52NZlV_QmVvgvg), and [Osama Al-Haj Hassan](https://www.researchgate.net/profile/Osama-Al-Haj-Hassan?_sg%5B0%5D=TEcNNzOft5bBstNFqBqpYNwlD33_i9hbPHM_VdM0ejEl9yLb0r3YiUfqNtuxs_Y_uhAnkis.hSKhfAlXAl3NayTteLeLyY8t6RSx4OY5b15bypYXrJ3un9Ua903F6jrnI7jd0JeCZ67_0fPe98qwQFfo3CHCCg&_sg%5B1%5D=S4XZH5xnJVzEZyFwfdiGPXYnO8827e3_7iQA-5Oslvj7kvxED8NPQBvgVdTnw2ZP_ntRNds.wtaWc_JUa6TzSo4B6VynSf39MvaGXV2dvYT6cXE2Lgmm9gJ95GS9FPHvt43RTIR5WjJU7XUw52NZlV_QmVvgvg).
