"""A custom min-heap using the assignment's urgency scale of 1 through 10."""


class Patient:
    def __init__(self, name, urgency):
        if not isinstance(name, str) or not name.strip():
            raise ValueError('Patient name must be a nonempty string.')
        if type(urgency) is not int or not 1 <= urgency <= 10:
            raise ValueError('Urgency must be an integer from 1 to 10.')
        self.name = name
        self.urgency = urgency


class MinHeap:
    def __init__(self):
        self.data = []

    def heapify_up(self, index):
        """Move a newly appended patient toward the root as needed."""
        while index > 0:
            parent = (index - 1) // 2
            if self.data[parent].urgency <= self.data[index].urgency:
                break
            self.data[parent], self.data[index] = self.data[index], self.data[parent]
            index = parent

    def heapify_down(self, index):
        """Swap with the more urgent child until the heap is restored."""
        size = len(self.data)
        while 2 * index + 1 < size:
            left = 2 * index + 1
            right = left + 1
            smallest = left
            if right < size and self.data[right].urgency < self.data[left].urgency:
                smallest = right
            if self.data[index].urgency <= self.data[smallest].urgency:
                break
            self.data[index], self.data[smallest] = self.data[smallest], self.data[index]
            index = smallest

    def insert(self, patient):
        if not isinstance(patient, Patient):
            raise TypeError('Only Patient objects can be inserted.')
        self.data.append(patient)
        self.heapify_up(len(self.data) - 1)

    def peek(self):
        """Return None when no patients are waiting."""
        return self.data[0] if self.data else None

    def remove_min(self):
        if not self.data:
            return None
        urgent = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self.heapify_down(0)
        return urgent

    def print_heap(self):
        """Display internal heap order, which is not a fully sorted list."""
        print('Current Queue:')
        for patient in self.data:
            print(f'- {patient.name} ({patient.urgency})')


if __name__ == '__main__':
    heap = MinHeap()
    for name, urgency in [('Jordan', 3), ('Taylor', 1), ('Avery', 5)]:
        heap.insert(Patient(name, urgency))
    heap.print_heap()
    next_up = heap.peek()
    print('Next:', next_up.name, next_up.urgency)
    print('Served:', heap.remove_min().name)
    heap.print_heap()
