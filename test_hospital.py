"""Run with python3 -m unittest -v."""
import contextlib
import io
import random
import unittest
from doctor_tree import DoctorNode, DoctorTree
from emergency_queue import MinHeap, Patient


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.tree = DoctorTree()
        self.tree.root = DoctorNode('Dr. Croft')
        for parent, name, side in [('Dr. Croft', 'Dr. Goldsmith', 'right'),
                                   ('Dr. Croft', 'Dr. Phan', 'left'),
                                   ('Dr. Phan', 'Dr. Carson', 'right'),
                                   ('Dr. Phan', 'Dr. Morgan', 'left')]:
            self.assertTrue(self.tree.insert(parent, name, side))

    def test_traversals(self):
        self.assertEqual(self.tree.preorder(self.tree.root),
                         ['Dr. Croft', 'Dr. Phan', 'Dr. Morgan', 'Dr. Carson', 'Dr. Goldsmith'])
        self.assertEqual(self.tree.inorder(self.tree.root),
                         ['Dr. Morgan', 'Dr. Phan', 'Dr. Carson', 'Dr. Croft', 'Dr. Goldsmith'])
        self.assertEqual(self.tree.postorder(self.tree.root),
                         ['Dr. Morgan', 'Dr. Carson', 'Dr. Phan', 'Dr. Goldsmith', 'Dr. Croft'])

    def test_invalid_insertions_do_not_change_tree(self):
        before = self.tree.preorder(self.tree.root)
        with contextlib.redirect_stdout(io.StringIO()):
            for args in [('missing', 'new', 'left'), ('Dr. Croft', 'new', 'up'),
                         ('Dr. Croft', 'new', 'left'), ('Dr. Carson', 'Dr. Phan', 'left'),
                         ('Dr. Carson', '', 'left')]:
                self.assertFalse(self.tree.insert(*args))
        self.assertEqual(before, self.tree.preorder(self.tree.root))

    def test_empty_singleton_and_subtree(self):
        tree = DoctorTree()
        for traversal in (tree.preorder, tree.inorder, tree.postorder):
            self.assertEqual(traversal(None), [])
            self.assertEqual(traversal(DoctorNode('Only')), ['Only'])
        self.assertEqual(self.tree.preorder(self.tree.root.right), ['Dr. Goldsmith'])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(tree.insert('missing', 'new', 'left'))


class HeapTests(unittest.TestCase):
    def assert_heap(self, heap):
        for i in range(1, len(heap.data)):
            self.assertLessEqual(heap.data[(i-1)//2].urgency, heap.data[i].urgency)

    def test_example_and_peek(self):
        heap = MinHeap()
        for name, urgency in [('Jordan', 3), ('Taylor', 1), ('Avery', 5)]:
            heap.insert(Patient(name, urgency))
        self.assertEqual(heap.peek().name, 'Taylor')
        self.assertEqual(len(heap.data), 3)
        self.assertEqual(heap.remove_min().name, 'Taylor')
        self.assertEqual(heap.remove_min().name, 'Jordan')
        self.assertEqual(heap.remove_min().name, 'Avery')
        self.assertIsNone(heap.remove_min())
        self.assertIsNone(heap.peek())

    def test_randomized_interleaved_operations(self):
        rng = random.Random(42)
        heap, waiting = MinHeap(), []
        for i in range(500):
            if not waiting or rng.random() < .65:
                patient = Patient(str(i), rng.randint(1, 10))
                waiting.append(patient)
                heap.insert(patient)
            else:
                expected = min(p.urgency for p in waiting)
                served = heap.remove_min()
                self.assertEqual(served.urgency, expected)
                waiting.remove(served)
            self.assert_heap(heap)
            self.assertEqual(len(heap.data), len(waiting))
        scores = []
        while heap.data:
            scores.append(heap.remove_min().urgency)
            self.assert_heap(heap)
        self.assertEqual(scores, sorted(p.urgency for p in waiting))

    def test_validation(self):
        for urgency in [0, 11, True, 2.5, '2']:
            with self.assertRaises(ValueError):
                Patient('Test', urgency)
        with self.assertRaises(ValueError):
            Patient('', 1)
        with self.assertRaises(TypeError):
            MinHeap().insert('not a patient')

    def test_print_heap(self):
        heap = MinHeap()
        heap.insert(Patient('Taylor', 1))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            heap.print_heap()
        self.assertEqual(output.getvalue(), 'Current Queue:\n- Taylor (1)\n')


if __name__ == '__main__':
    unittest.main()
