from unittest import TestCase as UnittestTestCase

from faker import Faker

from examscheduler.course import Course
from examscheduler.graph import Graph
from examscheduler.graphpainter import GraphPainter
from examscheduler.student import Student


class TestCase(UnittestTestCase):
    def setUp(self) -> None:
        self.fake = Faker()

    def tearDown(self) -> None:
        Student._all_students = set()
        Course._all_courses = {}


class GraphTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.graph = self._create_graph()

        self.gp = self._create_graphpainter()
        self.course = self._create_course()

    def _create_graph(self):
        g = Graph(directed=False)

        a = self._create_course()
        b = self._create_course()
        c = self._create_course()
        d = self._create_course()

        g.add_edge(a, b)
        g.add_edge(a, c, weight=2)
        g.add_edge(b, d)

        return g

    def _create_graphpainter(self):
        self.days = 10
        self.slots = 5
        self.fairness = 2

        return GraphPainter(self.graph, self.days, self.slots, self.fairness)

    def _create_course(self):
        key = self.fake.bothify(text="#######")
        name = self.fake.word()
        level = self.fake.random_digit_not_null()
        sections = 3

        return Course(key, name, level, sections)
