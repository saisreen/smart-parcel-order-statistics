"""Selection algorithms using 1-based ranks, including duplicate values."""
import random


def _validate(values, k):
    if not values:
        raise ValueError('Input cannot be empty')
    if not 1 <= k <= len(values):
        raise ValueError('k must be between 1 and the input length')


def _median_of_medians(values):
    if len(values) <= 5:
        ordered = sorted(values)
        return ordered[len(ordered) // 2]
    medians = []
    for start in range(0, len(values), 5):
        group = sorted(values[start:start + 5])
        medians.append(group[len(group) // 2])
    return _median_of_medians(medians)


def deterministic_select(values, k):
    """Return kth smallest value (k starts at 1); worst-case O(n)."""
    _validate(values, k)
    remaining = list(values)
    while True:
        if len(remaining) <= 5:
            return sorted(remaining)[k - 1]
        pivot = _median_of_medians(remaining)
        low = [x for x in remaining if x < pivot]
        equal = [x for x in remaining if x == pivot]
        high = [x for x in remaining if x > pivot]
        if k <= len(low):
            remaining = low
        elif k <= len(low) + len(equal):
            return pivot
        else:
            k -= len(low) + len(equal)
            remaining = high


def randomized_select(values, k, rng=None):
    """Return kth smallest value using randomized three-way partitioning."""
    _validate(values, k)
    rng = rng or random.Random()
    remaining = list(values)
    while True:
        pivot = rng.choice(remaining)
        low = [x for x in remaining if x < pivot]
        equal = [x for x in remaining if x == pivot]
        high = [x for x in remaining if x > pivot]
        if k <= len(low):
            remaining = low
        elif k <= len(low) + len(equal):
            return pivot
        else:
            k -= len(low) + len(equal)
            remaining = high


if __name__ == '__main__':
    priorities = [17, 3, 9, 9, 25, 1, 12]
    print('Parcel priority values:', priorities)
    print('4th smallest (deterministic):', deterministic_select(priorities, 4))
    print('4th smallest (randomized):', randomized_select(priorities, 4))
