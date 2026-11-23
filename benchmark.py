"""Reproducible performance experiment; writes results to CSV."""
import csv
import random
import statistics
import time
from selection_algorithms import deterministic_select, randomized_select

SIZES = [100, 1000, 5000, 10000]
DISTRIBUTIONS = ['random', 'sorted', 'reverse', 'duplicates']
REPEATS = 9


def make_data(size, distribution):
    rng = random.Random(2026 + size)
    if distribution == 'random':
        return [rng.randrange(size * 10) for _ in range(size)]
    if distribution == 'sorted':
        return list(range(size))
    if distribution == 'reverse':
        return list(range(size, 0, -1))
    return [rng.randrange(10) for _ in range(size)]


def main():
    rows = []
    for size in SIZES:
        for distribution in DISTRIBUTIONS:
            values = make_data(size, distribution)
            k = (size + 1) // 2
            expected = sorted(values)[k - 1]
            for name, algorithm in [('median_of_medians', deterministic_select), ('randomized_quickselect', randomized_select)]:
                durations = []
                for trial in range(REPEATS):
                    rng = random.Random(1000 + trial)
                    start = time.perf_counter_ns()
                    result = algorithm(values, k) if name == 'median_of_medians' else algorithm(values, k, rng)
                    durations.append((time.perf_counter_ns() - start) / 1_000_000)
                    assert result == expected
                row = {'size': size, 'distribution': distribution, 'algorithm': name,
                       'median_ms': round(statistics.median(durations), 5),
                       'min_ms': round(min(durations), 5), 'max_ms': round(max(durations), 5)}
                rows.append(row)
                print(row)
    with open('benchmark_results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print('Saved benchmark_results.csv')


if __name__ == '__main__':
    main()
