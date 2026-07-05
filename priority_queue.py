"""
A binary-heap min-priority-queue implemented from scratch.

Python's heapq would do this in one line, but the point of AlgoPath is to
demonstrate the underlying data structure, so the heap operations
(sift-up / sift-down) are written out explicitly, including support for
"decrease-key" via lazy deletion (a common approach used in real Dijkstra
implementations).
"""


class PriorityQueue:
    def __init__(self):
        self._heap: list[tuple[float, int, str]] = []
        self._counter = 0  # tie-breaker so equal-priority items don't compare node names

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def push(self, priority: float, item: str) -> None:
        entry = (priority, self._counter, item)
        self._counter += 1
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def pop_min(self):
        if not self._heap:
            raise IndexError("pop_min from an empty priority queue")
        self._swap(0, len(self._heap) - 1)
        priority, _, item = self._heap.pop()
        if self._heap:
            self._sift_down(0)
        return priority, item

    def __len__(self):
        return len(self._heap)

    # -- internal heap mechanics -------------------------------------------------

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i] < self._heap[parent]:
                self._swap(i, parent)
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._heap)
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            smallest = i
            if left < n and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < n and self._heap[right] < self._heap[smallest]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest
