import os
import sys
import unittest
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import orders  # noqa: E402


class TestOrders(unittest.TestCase):
    def test_each_persona_sees_every_stimulus_once(self):
        result = orders.make_orders(["A", "B", "C", "D"], 12, seed=7)
        self.assertEqual(len(result), 12)
        for order in result.values():
            self.assertEqual(sorted(order), ["A", "B", "C", "D"])

    def test_persona_ids_are_zero_padded(self):
        result = orders.make_orders(["A", "B"], 3, seed=1)
        self.assertEqual(list(result), ["P01", "P02", "P03"])

    def test_same_seed_gives_same_orders(self):
        self.assertEqual(
            orders.make_orders(["A", "B", "C"], 9, seed=3),
            orders.make_orders(["A", "B", "C"], 9, seed=3),
        )

    def test_first_position_is_balanced(self):
        result = orders.make_orders(["A", "B", "C", "D"], 10, seed=5)
        firsts = Counter(order[0] for order in result.values())
        self.assertEqual(set(firsts), {"A", "B", "C", "D"})
        self.assertLessEqual(max(firsts.values()) - min(firsts.values()), 1)

    def test_rejects_duplicate_ids(self):
        with self.assertRaises(ValueError):
            orders.make_orders(["A", "A"], 4, seed=1)


if __name__ == "__main__":
    unittest.main()
