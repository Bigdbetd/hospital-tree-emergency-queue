# Doctor Reporting Tree and Emergency Queue

Completed COMPSV Assignment 7 using Python's standard library.

## Files

- `doctor_tree.py`: recursive parent lookup and preorder, inorder, postorder traversals.
- `emergency_queue.py`: Patient objects and a custom array-backed min-heap.
- `design_memo.txt`: 200–300 word explanation of the design and trade-offs.
- `test_hospital.py`: example, validation, empty structure, and randomized heap tests.

## Run

```bash
python3 doctor_tree.py
python3 emergency_queue.py
python3 -m unittest -v
```

All 7 tests passed locally, including 500 randomized interleaved heap operations.

## Behavior and complexity

Set `tree.root = DoctorNode("Dr. Croft")`, then call
`tree.insert(parent_name, employee_name, "left" or "right")`.
Insertion returns a boolean and prints errors for invalid requests. Names must
be unique. Traversals accept a node, return a list, and return `[]` for `None`.
The hierarchy is a binary tree, not an alphabetically ordered search tree.
Insertion takes O(n) time; traversal takes O(n) time, O(n) result storage,
and O(h) recursion space for height h. A deeply skewed hierarchy can reach
Python's recursion limit.

Urgency is an integer from 1 to 10, with 1 most urgent. `peek()` and
`remove_min()` return `None` when empty. Heap insert/remove take O(log n)
time for reordering; Python list append is amortized O(1) and may occasionally
resize in O(n). Peek takes O(1), printing O(n), and total queue storage O(n).
Printed heap order is not fully sorted. Equal urgencies have no guaranteed
arrival order. Do not modify a queued patient's urgency directly, because that
can invalidate heap order. No `heapq` or sorting is used in the implementation.

The provided demos reproduce the assignment's example outputs.
