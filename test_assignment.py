"""Run with python -m unittest -v."""
import random
import unittest
from selection_algorithms import deterministic_select, randomized_select
from data_structures import ParcelArray, ParcelMatrix, ParcelStack, ParcelQueue, ParcelLinkedList


class SelectionTests(unittest.TestCase):
    def test_all_ranks_and_distributions(self):
        rng = random.Random(42)
        for values in ([5], [4, 4, 4], [-5, 0, -5, 8], list(range(30)), list(range(30, 0, -1)),
                       [rng.randrange(-20, 20) for _ in range(101)]):
            for k in range(1, len(values) + 1):
                expected = sorted(values)[k - 1]
                self.assertEqual(deterministic_select(values, k), expected)
                self.assertEqual(randomized_select(values, k, rng), expected)

    def test_invalid_ranks(self):
        for algorithm in (deterministic_select, randomized_select):
            for values, k in [([], 1), ([1], 0), ([1], 2)]:
                with self.assertRaises(ValueError):
                    algorithm(values, k)


class StructureTests(unittest.TestCase):
    def test_array_matrix(self):
        a = ParcelArray([1, 3]); a.insert(1, 2)
        self.assertEqual(a.access(1), 2)
        self.assertEqual(a.delete(0), 1)
        m = ParcelMatrix(2, 2, 0); m.update(1, 1, 8)
        self.assertEqual(m.access(1, 1), 8)
        m.insert_row(2, [3, 4]); self.assertEqual(m.delete_row(2), [3, 4])
        with self.assertRaises(ValueError): m.insert_row(0, [1])

    def test_stack(self):
        s = ParcelStack()
        with self.assertRaises(IndexError): s.pop()
        s.push(1); s.push(2)
        self.assertEqual((s.peek(), s.pop(), s.pop()), (2, 2, 1))

    def test_queue_wrap_resize(self):
        q = ParcelQueue()
        with self.assertRaises(IndexError): q.dequeue()
        for i in range(100): q.enqueue(i)
        for i in range(70): self.assertEqual(q.dequeue(), i)
        for i in range(100, 160): q.enqueue(i)
        self.assertEqual([q.dequeue() for _ in range(len(q))], list(range(70, 160)))

    def test_linked_list(self):
        l = ParcelLinkedList()
        self.assertFalse(l.delete('missing'))
        l.append('b'); l.prepend('a'); l.append('c')
        self.assertEqual(l.traverse(), ['a', 'b', 'c'])
        self.assertTrue(l.delete('a')); self.assertTrue(l.delete('c'))
        self.assertTrue(l.delete('b')); self.assertEqual(l.traverse(), [])
        l.append('again'); self.assertEqual(l.traverse(), ['again'])


if __name__ == '__main__':
    unittest.main()
