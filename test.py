import unittest
import ltl

class test_ltl(unittest.TestCase):
    def test_get_optimal_load(self):
        self.assertEqual(ltl.get_optimal_load(2, [1, 2, 3]), [2])
        self.assertEqual(ltl.get_optimal_load(6, [1, 2, 3]), [1, 2, 3])
        self.assertEqual(ltl.get_optimal_load(0, []), [])

    def test_distribute_shipments(self):
        self.assertEqual(ltl.distribute_shipments([1, 2, 3, 4, 5, 6],[1, 2, 3, 4, 5, 6]), [[1], [2], [3], [4], [5], [6]])
        self.assertEqual(ltl.distribute_shipments([3, 7, 11], [11, 7, 3]), [[3], [7], [11]])
        self.assertEqual(ltl.distribute_shipments([],[]), [[]])

    def test_remove_loaded(self):
        self.assertEqual(ltl.remove_loaded([5, 1], [1, 2, 3, 4, 5, 6]), [2, 3, 4, 6])
        self.assertEqual(ltl.remove_loaded([], []), [] )

if __name__ == '__main__':
    unittest.main()