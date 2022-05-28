from collections import defaultdict
from unittest.mock import patch

from examscheduler.graph import Graph, GraphIterator
from tests.case import TestCase


class TestGraphInit(TestCase):
    def test_graph_init_not_directed(self):
        g = Graph(directed=False)

        self.assertFalse(g.directed)
        self.assertEqual(0, len(g.adj_list))
        self.assertEqual(g.adj_list, defaultdict(set))

    def test_graph_init_directed(self):
        g = Graph(directed=True)

        self.assertTrue(g.directed)
        self.assertEqual(0, len(g.adj_list))
        self.assertEqual(g.adj_list, defaultdict(set))


class TestGraphDunderMethods(TestCase):
    def test_len(self):
        g = Graph()

        self.assertEqual(0, len(g))

        g.adj_list = [1, 2]
        self.assertEqual(2, len(g))

    def test_repr(self):
        g = Graph()
        self.assertEqual(f"<Graph: {id(g)} courses={len(g.adj_list)}>", repr(g))

    def test_iter(self):
        g = Graph()
        g.adj_list = list(range(self.fake.random_digit_not_null()))

        self.assertIsInstance(iter(g), GraphIterator)
        self.assertEqual(iter(g).adj_list, g.adj_list)

    def test_str(self):
        g = Graph()
        g.adj_list = defaultdict(set)

        for i in range(self.fake.random_digit_not_null()):
            g.adj_list[f"key-{i}"] = [
                f"value-{j}" for j in range(self.fake.random_digit_not_null())
            ]

        expected = ""
        for course in g.adj_list.keys():
            expected += f"course {course}: {g.adj_list[course]} \n"

        self.assertEqual(expected, str(g))


class TestGetAdjacencyList(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.g = Graph()
        self.g.adj_list = defaultdict(set)

        for i in range(self.fake.random_digit_not_null()):
            self.g.adj_list[f"key-{i}"] = [
                f"value-{j}" for j in range(self.fake.random_digit_not_null())
            ]

    def test_get_adjacency_list(self):
        key = "key-0"

        self.assertEqual(self.g.adj_list[key], self.g.get_adjacency_list(key))


class TestCourseWeight(TestCase):
    def test_get_largest_weight(self):
        g = Graph()
        g.adj_list = {
            "a": {("b", 1), ("c", 2), ("d", 3)},
            "b": {("a", 6), ("c", 5), ("d", 4)},
            "d": {("a", 7), ("c", 9), ("b", 8)},
        }

        self.assertEqual(3, g.get_largest_weight("a"))
        self.assertEqual(6, g.get_largest_weight("b"))
        self.assertEqual(9, g.get_largest_weight("d"))

    def test_directed_get_weight_success(self):
        g = Graph(directed=True)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 6), ("c", 5), ("d", 4)},
            "d": {("a", 7)},
        }

        self.assertEqual(1, g.get_weight("a", "b"))
        self.assertEqual(6, g.get_weight("b", "a"))
        self.assertEqual(4, g.get_weight("b", "d"))
        self.assertEqual(7, g.get_weight("d", "a"))

    def test_not_directed_get_weight_success(self):
        g = Graph(directed=False)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 1)},
            "c": {("a", 2)},
        }

        self.assertEqual(1, g.get_weight("a", "b"))
        self.assertEqual(1, g.get_weight("b", "a"))

        self.assertEqual(2, g.get_weight("a", "c"))
        self.assertEqual(2, g.get_weight("c", "a"))

    def test_directed_get_weight_no_edge_courses_exist(self):
        g = Graph(directed=True)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 6), ("c", 5), ("d", 4)},
            "d": {("a", 7)},
        }

        self.assertEqual(7, g.get_weight("d", "a"))
        self.assertIsNone(g.get_weight("a", "d"))

        self.assertEqual(4, g.get_weight("b", "d"))
        self.assertIsNone(g.get_weight("d", "b"))

    def test_directed_get_weight_no_courses(self):
        g = Graph(directed=True)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 6), ("c", 5), ("d", 4)},
            "d": {("a", 7)},
        }

        self.assertIsNone(g.get_weight("f", "a"))
        self.assertIsNone(g.get_weight("a", "f"))
        self.assertIsNone(g.get_weight("g", "f"))

    def test_not_directed_get_weight_no_edge_courses_exist(self):
        g = Graph(directed=False)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 1)},
            "c": {("a", 2)},
        }

        self.assertIsNone(g.get_weight("b", "c"))
        self.assertIsNone(g.get_weight("c", "b"))

    def test_not_directed_get_weight_no_courses(self):
        g = Graph(directed=False)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 1)},
            "c": {("a", 2)},
        }

        self.assertIsNone(g.get_weight("b", "d"))
        self.assertIsNone(g.get_weight("d", "a"))
        self.assertIsNone(g.get_weight("e", "f"))

    def test_set_weight_directed_graph_no_courses(self):
        g = Graph(directed=True)

        with self.assertRaises(ValueError):
            g.set_weight("a", "b", 3)

        with self.assertRaises(ValueError):
            g.adj_list = {"a": {("b", 1)}}
            g.set_weight("b", "a", 3)

    def test_set_weight_not_directed_graph_no_courses(self):
        g = Graph(directed=False)

        with self.assertRaises(ValueError):
            g.set_weight("a", "b", 3)

        # This should pass
        g.adj_list = {
            "a": {("b", 1)},
            "b": {("a", 1)},
        }
        weight = g.set_weight("b", "a", 3)
        self.assertEqual(weight, 3)

    def test_set_weight_not_directed_graph(self):
        g = Graph(directed=False)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 1)},
            "c": {("a", 2)},
        }

        weight = g.set_weight("a", "b", 3)
        self.assertEqual(weight, 3)
        self.assertDictEqual(
            {
                "a": {("b", 3), ("c", 2)},
                "b": {("a", 3)},
                "c": {("a", 2)},
            },
            g.adj_list,
        )

        weight = g.set_weight("b", "a", 4)
        self.assertEqual(weight, 4)
        self.assertDictEqual(
            {
                "a": {("b", 4), ("c", 2)},
                "b": {("a", 4)},
                "c": {("a", 2)},
            },
            g.adj_list,
        )

    def test_set_weight_directed_graph(self):
        g = Graph(directed=True)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 3)},
            "c": {("a", 4)},
        }

        weight = g.set_weight("a", "b", 3)
        self.assertEqual(weight, 3)
        self.assertDictEqual(
            {
                "a": {("b", 3), ("c", 2)},
                "b": {("a", 3)},
                "c": {("a", 4)},
            },
            g.adj_list,
        )

        weight = g.set_weight("b", "a", 5)
        self.assertEqual(weight, 5)
        self.assertDictEqual(
            {
                "a": {("b", 3), ("c", 2)},
                "b": {("a", 5)},
                "c": {("a", 4)},
            },
            g.adj_list,
        )

    @patch.object(Graph, "_find_and_set_weight", side_effect=[5, 10])
    def test_set_weight_not_directed_mismatch(self, mock_find_and_set_weight):
        g = Graph(directed=False)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 3)},
            "c": {("a", 4)},
        }

        with self.assertRaises(RuntimeError):
            g.set_weight("a", "b", 3)

        self.assertEqual(2, mock_find_and_set_weight.call_count)

    @patch.object(Graph, "_find_and_set_weight", side_effect=[5])
    def test_set_weight_directed_called_once(self, mock_find_and_set_weight):
        g = Graph(directed=True)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 3)},
            "c": {("a", 4)},
        }

        g.set_weight("a", "b", 3)
        mock_find_and_set_weight.assert_called_once_with("a", "b", 3)

    def test_find_and_set_weight_none(self):
        g = Graph()
        self.assertIsNone(g._find_and_set_weight("a", "b", 2))

        g = Graph(directed=True)
        g.adj_list = {
            "b": {("a", 3)},
        }
        self.assertIsNone(g._find_and_set_weight("a", "b", 2))

    def test_find_and_set_weight_exists(self):
        g = Graph()
        g.adj_list = {
            "a": {("b", 3)},
            "b": {("a", 3)},
        }
        self.assertEqual(2, g._find_and_set_weight("a", "b", 2))
        self.assertDictEqual(
            g.adj_list,
            {
                "a": {("b", 2)},
                "b": {("a", 3)},
            },
        )


class TestCourseDegree(TestCase):
    def test_get_degree(self):
        g = Graph()
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 6), ("c", 5), ("d", 4)},
            "d": {("a", 7)},
        }

        self.assertEqual(2, g.get_degree("a"))
        self.assertEqual(3, g.get_degree("b"))
        self.assertEqual(1, g.get_degree("d"))


class TestEdge(TestCase):
    def test_directed_contains_edge(self):
        g = Graph(directed=True)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 6), ("c", 5), ("d", 4)},
            "d": {("a", 7)},
        }

        self.assertTrue(g.contains_edge("a", "b"))
        self.assertTrue(g.contains_edge("b", "a"))
        self.assertTrue(g.contains_edge("b", "d"))
        self.assertTrue(g.contains_edge("d", "a"))

    def test_not_directed_contains_edge(self):
        g = Graph(directed=False)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 1)},
            "c": {("a", 2)},
        }

        self.assertTrue(g.contains_edge("a", "b"))
        self.assertTrue(g.contains_edge("b", "a"))
        self.assertTrue(g.contains_edge("c", "a"))

    def test_directed_does_not_contain_edge(self):
        g = Graph(directed=True)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 6), ("c", 5), ("d", 4)},
            "d": {("a", 7)},
        }

        self.assertFalse(g.contains_edge("a", "d"))
        self.assertFalse(g.contains_edge("d", "c"))
        self.assertFalse(g.contains_edge("b", "e"))
        self.assertFalse(g.contains_edge("f", "a"))

    def test_not_directed_does_not_contain_edge(self):
        g = Graph(directed=False)
        g.adj_list = {
            "a": {("b", 1), ("c", 2)},
            "b": {("a", 1)},
            "c": {("a", 2)},
        }

        self.assertFalse(g.contains_edge("b", "c"))
        self.assertFalse(g.contains_edge("c", "b"))
        self.assertFalse(g.contains_edge("c", "f"))
        self.assertFalse(g.contains_edge("r", "a"))
        self.assertFalse(g.contains_edge("t", "u"))

    def test_add_edge_directed(self):
        g = Graph(directed=True)

        weight = g.add_edge("a", "b")
        self.assertEqual(weight, 1)
        expected = {"a": {("b", weight)}}
        self.assertDictEqual(expected, g.adj_list)

        weight = g.add_edge("b", "a", weight=3)
        self.assertEqual(weight, weight)
        expected = {"a": {("b", 1)}, "b": {("a", 3)}}
        self.assertDictEqual(expected, g.adj_list)

    def test_add_edge_not_directed(self):
        g = Graph(directed=False)

        weight = g.add_edge("a", "b")
        self.assertEqual(weight, 1)
        expected = {"a": {("b", weight)}, "b": {("a", weight)}}
        self.assertDictEqual(expected, g.adj_list)

        weight = g.add_edge("b", "c", weight=3)
        self.assertEqual(weight, 3)
        expected = {"a": {("b", 1)}, "b": {("c", 3), ("a", 1)}, "c": {("b", 3)}}
        self.assertDictEqual(expected, g.adj_list)

    def test_add_edge_directed_exists(self):
        g = Graph(directed=True)
        weight = g.add_edge("a", "b")
        self.assertEqual(weight, 1)

        with self.assertRaises(ValueError):
            g.add_edge("a", "b", weight=3)

        # (b, a) can be added as it's a directed graph
        weight = g.add_edge("b", "a", weight=3)
        self.assertEqual(weight, weight)
        expected = {"a": {("b", 1)}, "b": {("a", 3)}}
        self.assertDictEqual(expected, g.adj_list)

    def test_add_edge_not_directed_exists(self):
        g = Graph(directed=False)
        weight = g.add_edge("a", "b")
        self.assertEqual(weight, 1)

        with self.assertRaises(ValueError):
            g.add_edge("a", "b", weight=3)

        with self.assertRaises(ValueError):
            g.add_edge("b", "a", weight=3)
