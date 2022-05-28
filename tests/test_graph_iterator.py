from collections import defaultdict

from examscheduler.graph import GraphIterator
from tests.case import TestCase


class TestGraphIterator(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.adj_list = list(range(self.fake.random_digit_not_null()))

    def test_init(self):
        gi = GraphIterator(self.adj_list)

        self.assertEqual(0, gi.idx)
        self.assertEqual(self.adj_list, gi.adj_list)

    def test_iter(self):
        gi = GraphIterator(self.adj_list)
        self.assertEqual(gi, iter(gi))


class TestGraphIteratorNext(TestCase):
    def test_iter_list(self):
        adj_list = list(range(self.fake.random_digit_not_null()))
        gi = GraphIterator(adj_list)

        for item in adj_list:
            self.assertEqual(item, next(gi))

    def test_iter_defaultdict(self):
        adj_list = defaultdict(int)
        for i in range(10):
            adj_list[f"key-{i}"] = f"value-{i}"

        gi = GraphIterator(adj_list)

        for key, _ in adj_list.items():
            self.assertEqual(key, next(gi))

    def test_iter_stopiteration_greater_index(self):
        adj_list = list(range(self.fake.random_digit_not_null()))
        gi = GraphIterator(adj_list)
        gi.idx = 2 * len(adj_list)

        with self.assertRaises(StopIteration):
            next(gi)

        self.assertIsNone(gi.idx)

    def test_iter_stopiteration_none_index(self):
        adj_list = list(range(self.fake.random_digit_not_null()))
        gi = GraphIterator(adj_list)
        gi.idx = None

        with self.assertRaises(StopIteration):
            next(gi)

        self.assertIsNone(gi.idx)
