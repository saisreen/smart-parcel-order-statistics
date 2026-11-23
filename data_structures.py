"""Small educational data structures built using Python lists and nodes."""
from collections.abc import Iterable


class ParcelArray:
    def __init__(self, items=()):
        self.items = list(items)

    def insert(self, index, value):
        if not 0 <= index <= len(self.items):
            raise IndexError('Invalid insertion index')
        self.items.insert(index, value)

    def delete(self, index):
        return self.items.pop(index)

    def access(self, index):
        return self.items[index]


class ParcelMatrix:
    def __init__(self, rows, columns, default=None):
        if rows <= 0 or columns <= 0:
            raise ValueError('Matrix dimensions must be positive')
        self.grid = [[default for _ in range(columns)] for _ in range(rows)]

    def access(self, row, column):
        return self.grid[row][column]

    def update(self, row, column, value):
        self.grid[row][column] = value

    def insert_row(self, index, values):
        if len(values) != len(self.grid[0]):
            raise ValueError('Row width must match matrix')
        if not 0 <= index <= len(self.grid):
            raise IndexError('Invalid row index')
        self.grid.insert(index, list(values))

    def delete_row(self, index):
        if len(self.grid) == 1:
            raise ValueError('Cannot remove final row')
        return self.grid.pop(index)


class ParcelStack:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)

    def pop(self):
        if not self.items:
            raise IndexError('Stack is empty')
        return self.items.pop()

    def peek(self):
        if not self.items:
            raise IndexError('Stack is empty')
        return self.items[-1]


class ParcelQueue:
    """Circular array queue with amortized O(1) enqueue and dequeue."""
    def __init__(self):
        self._buffer = [None] * 4
        self._head = 0
        self._size = 0

    def __len__(self):
        return self._size

    def _resize(self, capacity):
        old = self._buffer
        self._buffer = [old[(self._head + i) % len(old)] for i in range(self._size)] + [None] * (capacity - self._size)
        self._head = 0

    def enqueue(self, value):
        if self._size == len(self._buffer):
            self._resize(len(self._buffer) * 2)
        self._buffer[(self._head + self._size) % len(self._buffer)] = value
        self._size += 1

    def dequeue(self):
        if not self._size:
            raise IndexError('Queue is empty')
        value = self._buffer[self._head]
        self._buffer[self._head] = None
        self._head = (self._head + 1) % len(self._buffer)
        self._size -= 1
        if len(self._buffer) > 4 and self._size <= len(self._buffer) // 4:
            self._resize(max(4, len(self._buffer) // 2))
        return value

    def peek(self):
        if not self._size:
            raise IndexError('Queue is empty')
        return self._buffer[self._head]


class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class ParcelLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def prepend(self, value):
        self.head = Node(value, self.head)
        if self.tail is None:
            self.tail = self.head

    def delete(self, value):
        previous, current = None, self.head
        while current:
            if current.value == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                return True
            previous, current = current, current.next
        return False

    def traverse(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


if __name__ == '__main__':
    a = ParcelArray(['P1', 'P3'])
    a.insert(1, 'P2')
    print('Array:', a.items, 'Access:', a.access(1), 'Removed:', a.delete(0))
    m = ParcelMatrix(2, 2, 0)
    m.update(0, 1, 5)
    m.insert_row(2, [7, 8])
    print('Matrix:', m.grid, 'Access:', m.access(0, 1), 'Removed:', m.delete_row(2))
    s = ParcelStack()
    s.push('scan'); s.push('label')
    print('Stack peek/pop:', s.peek(), s.pop())
    q = ParcelQueue()
    q.enqueue('P1'); q.enqueue('P2')
    print('Queue peek/dequeue:', q.peek(), q.dequeue())
    linked = ParcelLinkedList()
    linked.append('P2'); linked.prepend('P1'); linked.append('P3')
    print('Linked list:', linked.traverse(), 'Delete P2:', linked.delete('P2'), linked.traverse())
