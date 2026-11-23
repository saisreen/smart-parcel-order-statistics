# Assignment 6: Medians, Order Statistics and Elementary Data Structures
## A Smart Parcel Processing Case Study

**Student:** [Enter your name]  
**Course:** [Enter course name]  
**Date:** [Enter submission date]

## 1. Introduction
In a parcel sorting center, some packages need to be processed earlier than others. We can give each parcel a number based on its priority or waiting time. If the manager wants the middle waiting time, there is no need to sort every value. Selection algorithms can directly find the required rank. In the same center, arrays keep parcel information, matrices show shelf positions, stacks support reversing recent scanning actions, queues maintain arrival order, and linked lists maintain changing delivery routes. This example connects the two parts of the assignment. The code is a learning model, not a complete delivery application.

## 2. Part 1: Selection algorithms
The kth smallest value means the value at position k after sorting from smallest to largest. In this implementation k starts at 1. For example, in [7, 2, 7, 4], the third smallest value is 7. Repeated values count as separate positions. Both functions reject an empty list and invalid ranks, and neither changes the caller's original list.

### 2.1 Deterministic selection: Median of Medians
The algorithm splits the values into small groups of up to five. It sorts each small group and collects its middle value. It then finds a pivot from these middle values. Using this pivot, it separates the input into smaller, equal and greater values. If the requested rank falls in the smaller group, it continues there. If the rank is within the equal group, the pivot is the answer. Otherwise, it continues in the greater group after adjusting k.

**Why groups of five?** They provide a pivot with a proven balance guarantee. The algorithm does not depend on luck to avoid a very poor pivot. Small groups are cheap to sort because their size is bounded by five.

**Worst-case time:** The group medians take O(n) work to produce, choosing their median costs T(ceil(n/5)), and the larger remaining side has at most about 7n/10 elements, apart from small rounding terms. The recurrence is T(n) <= T(ceil(n/5)) + T(7n/10 + O(1)) + O(n). Since 1/5 + 7/10 = 9/10 < 1, this gives **O(n) worst-case time**. Best and average time are also O(n) in asymptotic terms for this implementation.

**Space:** This readable implementation copies lists during partitioning and builds median lists. Peak auxiliary memory is O(n) (plus O(log n) recursive stack depth for median computation). A carefully written in-place version could reduce memory overhead, but is more difficult to understand and maintain.

### 2.2 Randomized Quickselect
Randomized Quickselect picks a random element as the pivot and separates the input into smaller, equal and greater groups. It continues only in the group that contains the required rank. The equal group is important because many parcels may have the same priority. Without careful duplicate handling, a partition algorithm can do unnecessary work or calculate ranks incorrectly.

**Expected time:** Partitioning a list of n values takes O(n). A random pivot is reasonably balanced often enough that the expected total work across all rounds is O(n). An informal recurrence is E[T(n)] = O(n) + average remaining-subproblem cost, which solves to **O(n) expected time**. Its worst case is **O(n²)** if pivots repeatedly leave almost all elements on one side. Random choice makes that unlikely, but does not remove the possibility.

**Space:** This implementation makes new partition lists, so peak auxiliary space is O(n), with additional small control variables. An in-place partitioning version would have lower auxiliary memory use. The random number generator also has a small overhead.

### 2.3 Empirical experiment
I tested both methods on random, sorted, reverse-sorted, and duplicate-heavy inputs. The input sizes were 100, 1,000, 5,000 and 10,000. For each case I selected the lower median using k = (n+1)//2. Each measurement was repeated nine times and the median runtime was recorded in milliseconds. A fixed seed creates reproducible input and randomized pivot sequences. The experiment uses Python's perf_counter_ns clock. The full 32-row results are saved in `benchmark_results.csv`.

| Size | Distribution | Median of Medians (ms) | Randomized Quickselect (ms) |
|---:|---|---:|---:|
| 1,000 | Random | 0.23378 | 0.22601 |
| 1,000 | Sorted | 1.94963 | 0.11949 |
| 10,000 | Random | 2.18905 | 1.64359 |
| 10,000 | Sorted | 3.87329 | 1.58163 |
| 10,000 | Reverse | 1.53174 | 1.58438 |
| 10,000 | Duplicates | 1.77849 | 0.88725 |

**What I observed:** The randomized algorithm was faster for most selected cases. The deterministic method sometimes spent extra time forming groups and finding a careful pivot. A sorted list is not automatically the worst case for randomized selection because its pivot is selected randomly, not always from the first or last position. For duplicate-heavy values, three-way partitioning can finish quickly when k falls in the equal group. The deterministic method was slightly faster in the 10,000-element reverse case, showing that results can vary by input and runtime conditions.

**Limits of this experiment:** Timings depend on Python version, machine load, and the small number of trials. The data are generated rather than taken from a real parcel company. These measurements show practical behavior but cannot prove a time-complexity bound. Theoretical analysis provides the guarantee.

## 3. Part 2: Elementary data structures
### 3.1 Array and matrix
`ParcelArray` supports insertion, deletion, and indexed access using a Python list as the underlying array. An array is useful when the parcel records need direct access by position. `ParcelMatrix` represents shelf positions using rows and columns. It supports cell access and updates, plus inserting and deleting whole rows. This is a fixed-width rectangular matrix, and invalid row widths are rejected. Python lists are dynamic arrays, so this is an array-based educational implementation rather than a low-level fixed-capacity memory array.

### 3.2 Stack
`ParcelStack` uses a list with push, pop, and peek. The most recently added value is removed first (LIFO). In a parcel system, a stack could store the recent scanning actions for an undo feature. An empty pop or peek raises an error.

### 3.3 Queue
`ParcelQueue` uses a circular array with a head index and automatic resizing. Parcels leave in the same order they arrive (FIFO). Unlike deleting the first item of a normal Python list, the circular design avoids shifting every remaining item on each dequeue. It grows when full and shrinks when mostly empty. It clears removed references to avoid keeping unused objects in memory.

### 3.4 Singly linked list
`ParcelLinkedList` uses nodes containing a value and a pointer to the next node. It supports adding to the front or end, deleting the first matching value, and traversal. It keeps both head and tail pointers. A linked list is useful when delivery stops change regularly, although searching for a particular stop still takes linear time.

## 4. Operation complexity comparison

| Structure | Operation | Time | Extra explanation |
|---|---|---|---|
| Array | Indexed access | O(1) | Direct position lookup |
| Array | Insert/delete at arbitrary position | O(n) | Later elements may shift |
| Array | Append | Amortized O(1) | Occasionally resizes |
| Matrix | Access/update a cell | O(1) | Two indices |
| Matrix | Insert/delete row | O(r) | Row references may shift; copying a new row also costs O(c) |
| Stack | Push | Amortized O(1) | Array append |
| Stack | Pop/peek | O(1) | Last position |
| Circular queue | Enqueue/dequeue | Amortized O(1) | Occasional O(n) resizing |
| Circular queue | Peek | O(1) | Head position |
| Linked list | Prepend | O(1) | Change head pointer |
| Linked list | Append | O(1) | Tail pointer is maintained |
| Linked list | Delete by value | O(n) | Must search for the node |
| Linked list | Traverse | O(n) | Visits each node |

Here r is the number of matrix rows and c is the number of columns. An array holding n items needs O(n) memory. A matrix needs O(rc) memory. A stack and queue each need O(n) memory. A linked list needs O(n) memory plus a next-pointer reference per node.

## 5. Arrays versus linked lists
For a stack, a dynamic array is usually a good option. Push and pop at the end are fast, and items are stored compactly. A linked-list stack can also push and pop at the head in O(1), but every node needs extra memory for a pointer and object storage.

For a queue, a plain dynamic array that deletes index zero is less suitable because it shifts elements, giving O(n) dequeue time. A circular array solves this and gives amortized O(1) operations. A linked-list queue with head and tail pointers also offers O(1) enqueue and dequeue, but has more per-node memory overhead. If the queue has a stable or predictable size, a circular array is often simple and memory-efficient. If records are frequently inserted or removed in the middle and their nodes are already known, a linked list can avoid array shifting; finding those nodes still takes O(n).

## 6. Practical uses and design decisions
A parcel center can use an array to store a daily list of parcels and a matrix to track shelf locations. A stack can undo a recently recorded scan. A FIFO queue can process packages in arrival order. A linked list can represent a sequence of stops that may be updated. For selecting the middle delivery wait time, randomized Quickselect is attractive when fast average performance is the main goal. Median of Medians is useful when predictable worst-case time matters more than implementation overhead.

This case study also shows that one data structure should not be used for every job. The best choice depends on whether the program needs fast indexing, frequent changes, FIFO or LIFO order, predictable runtime, or lower memory overhead.

## 7. Testing and correctness
The unit tests check the smallest and largest ranks, single-element inputs, negative numbers, duplicate values, random lists, sorted and reverse-sorted lists, invalid ranks, empty stacks and queues, circular queue resizing, and linked-list deletion at the head, middle, and tail. The tests also check row insertion and deletion in the matrix. All six test groups passed in the recorded run. The benchmark additionally checks every selected result against Python's sorted reference answer.

## 8. Conclusion
Both selection algorithms find an order statistic without fully sorting the input. Median of Medians provides O(n) worst-case time, while Randomized Quickselect provides O(n) expected time and may be simpler and faster in practical tests. The parcel example helped me understand that arrays, matrices, stacks, queues, and linked lists have different strengths. The right structure depends on the operation we need most often.

## 9. References
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., and Stein, C. *Introduction to Algorithms*, 4th ed., MIT Press, 2022. Chapters on selection and elementary data structures.
- Python Software Foundation. *Python 3 Documentation*: `random`, `time`, `unittest`, and built-in list behavior. https://docs.python.org/3/

**Reproducibility note:** Run `python -m unittest -v` and `python benchmark.py` from the repository root to verify the code and regenerate measured results. Review and replace the student information before submission.
