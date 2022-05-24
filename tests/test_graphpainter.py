from unittest.mock import patch

from ddt import data, ddt, unpack

from examscheduler.color import Color
from examscheduler.course import Course
from examscheduler.graph import Graph
from examscheduler.graphpainter import GraphPainter
from examscheduler.student import Student
from tests.case import TestCase as TestsTestCase


class TestCase(TestsTestCase):
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


@ddt
class TestGraphPainterInit(TestCase):
    @patch.object(GraphPainter, "_generate_colors_matrix")
    def test_graphpainter_init(self, mock_generate_colors_matrix):
        gp = GraphPainter(self.graph, self.days, self.slots, self.fairness)

        self.assertEqual(gp.current_courses, self.graph.adj_list)

        self.assertEqual(gp.days, self.days)
        self.assertEqual(gp.slots, self.slots)
        self.assertEqual(gp.fairness, self.fairness)

        mock_generate_colors_matrix.assert_called_once_with()
        gp.colors = mock_generate_colors_matrix.return_value

    @data(
        {"days": 2, "slots": 1},
        {"days": 2, "slots": 2},
        {"days": 2, "slots": 3},
        {"days": 5, "slots": 3},
    )
    @unpack
    def test_generate_colors_matrix(self, days, slots):
        gp = GraphPainter(self.graph, days, slots, self.fairness)

        colors = gp._generate_colors_matrix()

        rows = len(colors)
        columns = len(colors[0])

        self.assertEqual(rows, days)
        self.assertEqual(columns, slots)

        counter = 1
        for day in range(days):
            for slot in range(slots):
                color = colors[day][slot]

                self.assertEqual(color.key, counter)
                self.assertEqual(color.day, day)
                self.assertEqual(color.slot, slot)
                self.assertEqual(color.available_instances, days)

                counter += 1


class TestGraphPainterIsFairToSchedule(TestCase):
    def test_is_fair_to_schedule_fair_no_students(self):
        self.course._students = []

        self.assertTrue(
            self.gp._is_fair_to_schedule(self.course, self.fake.random_digit_not_null())
        )

    def test_is_fair_to_schedule_fair_no_slots(self):
        self.course._students = [
            "1",
            "2",
        ]
        self.gp.slots = 0

        self.assertTrue(
            self.gp._is_fair_to_schedule(self.course, self.fake.random_digit_not_null())
        )

    def test_is_fair_to_schedule_fair_different_students_same_slot(self):
        """
        This should fail becuase two courses are scheduled in the same
        slot.
        """
        slot = 0
        day = 0
        self.gp.fairness = 2

        student1 = Student(self.fake.bothify(text="#######"))
        student2 = Student(self.fake.bothify(text="#######"))
        course1 = self._create_course()
        course2 = self._create_course()

        course1._students.append(student1)
        course2._students.append(student2)

        self.gp.colors[day][slot].colored_courses = [course1, course2]

        self.assertTrue(self.gp._is_fair_to_schedule(course1, day))

    def test_is_fair_to_schedule_not_fair_two_courses_same_slot(self):
        """
        This should fail becuase two courses are scheduled in the same
        slot.
        """
        slot = 0
        day = 0
        self.gp.fairness = 3

        student = Student(self.fake.bothify(text="#######"))
        course1 = self._create_course()
        course2 = self._create_course()

        course1._students.append(student)
        course2._students.append(student)

        self.gp.colors[day][slot].colored_courses = [course1, course2]

        self.assertFalse(self.gp._is_fair_to_schedule(course1, day))

    def test_is_fair_to_schedule_not_fair_two_courses_same_day(self):
        """
        This should fail becuase two courses are scheduled in the same
        day which is not fair for the student.
        """
        slot = 0
        day = 0
        fairness = 2

        gp = GraphPainter(self.graph, day + 5, slot + 5, fairness)

        student = Student(self.fake.bothify(text="#######"))
        course1 = self._create_course()
        course2 = self._create_course()

        course1._students.append(student)
        course2._students.append(student)

        gp.colors[day][slot].colored_courses = [course1]
        gp.colors[day][slot + 1].colored_courses = [course2]

        self.assertFalse(gp._is_fair_to_schedule(course1, day))

    def test_is_fair_to_schedule_not_fair_three_courses_same_day(self):
        """
        This should fail becuase three courses are scheduled in the same
        day which is not fair for the student.
        """
        slot = 0
        day = 0
        fairness = 3
        gp = GraphPainter(self.graph, day + 5, slot + 5, fairness)

        student = Student(self.fake.bothify(text="#######"))
        course1 = self._create_course()
        course2 = self._create_course()
        course3 = self._create_course()

        course1._students.append(student)
        course2._students.append(student)
        course3._students.append(student)

        gp.colors[day][slot].colored_courses = [course1]
        gp.colors[day][slot + 1].colored_courses = [course2]
        gp.colors[day][slot + 2].colored_courses = [course3]

        self.assertFalse(gp._is_fair_to_schedule(course1, day))


class TestGraphPainterGetFirstcourseColor(TestCase):
    def test_get_first_course_color_no_days_is_none(self):
        gp = GraphPainter(self.graph, 0, 0, 2)

        self.assertIsNone(gp._get_first_course_color(self.course))

    def test_get_first_course_color_no_slots_is_none(self):
        gp = GraphPainter(self.graph, 10, 0, 2)

        self.assertIsNone(gp._get_first_course_color(self.course))

    def test_get_first_course_color_sections_cannot_be_accomadated(self):
        gp = GraphPainter(self.graph, 3, 3, 2)
        self.course.sections = float("inf")

        self.assertIsNone(gp._get_first_course_color(self.course))

    def test_get_first_course_color_sections_can_be_accomadated(self):
        expected = Color(3, 1, 0, instances=10)

        gp = GraphPainter(self.graph, 2, 2, 2)
        gp.colors = [
            [
                Color(1, 0, 0, instances=0),
                Color(2, 0, 1, instances=0),
            ],
            [
                expected,
                Color(4, 1, 1, instances=0),
            ],
        ]

        self.course.sections = 10

        actual = gp._get_first_course_color(self.course)
        self.assertIsNotNone(actual)
        self.assertEqual(expected, actual)


class TestGraphPainterGetSmallestAvailableColor(TestCase):
    def test_get_smallest_available_color_no_days_is_none(self):
        gp = GraphPainter(self.graph, 0, self.slots, self.fairness)
        self.assertIsNone(gp._get_smallest_available_color(self.course))

    def test_get_smallest_available_color_no_slots_is_none(self):
        gp = GraphPainter(self.graph, self.days, 0, self.fairness)
        self.assertIsNone(gp._get_smallest_available_color(self.course))

    @patch.object(Graph, "get_adjacency_list")
    def test_get_smallest_available_color_no_neighbors_first_color(
        self, mock_get_adjacency_list
    ):
        mock_get_adjacency_list.return_value = set()

        # First color should be selected since we have no neighbors to process.
        expected = self.gp.colors[0][0]
        actual = self.gp._get_smallest_available_color(self.course)

        self.assertIsNotNone(actual)
        self.assertEqual(expected, actual)

    @patch.object(GraphPainter, "_is_color_valid")
    @patch.object(Graph, "get_adjacency_list")
    def test_get_smallest_available_color_neighbor_not_same_day_and_time(
        self, mock_get_adjacency_list, mock_is_color_valid
    ):
        neighbor = self._create_course()
        neighbor.color = Color(
            self.fake.random_digit_not_null(), day=0, slot=0, instances=10
        )
        mock_get_adjacency_list.return_value = {(neighbor, 0)}

        self.gp._get_smallest_available_color(self.course)
        mock_is_color_valid.assert_called_once()

    @patch.object(GraphPainter, "_is_color_valid")
    @patch.object(Graph, "get_adjacency_list")
    def test_get_smallest_available_color_neighbor_same_day_and_time(
        self, mock_get_adjacency_list, mock_is_color_valid
    ):
        self.gp.slots = 1
        self.gp.days = 1

        neighbor = self._create_course()
        neighbor.color = Color(
            self.fake.random_digit_not_null(), day=0, slot=0, instances=10
        )
        mock_get_adjacency_list.return_value = {(neighbor, 0)}

        self.gp._get_smallest_available_color(self.course)
        mock_is_color_valid.assert_not_called()

    @patch.object(GraphPainter, "_is_color_valid")
    @patch.object(Graph, "get_adjacency_list")
    def test_get_smallest_available_color_neighbor_not_colored(
        self, mock_get_adjacency_list, mock_is_color_valid
    ):
        self.gp.slots = 1
        self.gp.days = 1

        neighbor = self._create_course()
        neighbor.color = None
        mock_get_adjacency_list.return_value = {(neighbor, 0)}

        expected = self.gp.colors[0][0]
        actual = self.gp._get_smallest_available_color(self.course)
        self.assertEqual(expected, actual)

        mock_is_color_valid.assert_not_called()


@ddt
class TestGraphPainterIsColorValid(TestCase):
    @data(
        {"slot1": 0, "slot2": 0},
        {"slot1": 1, "slot2": 1},
        {"slot1": 0, "slot2": 1},
        {"slot1": 1, "slot2": 0},
        {"slot1": 4, "slot2": 5},
    )
    @unpack
    def test_is_color_valid_same_day_not_valid(self, slot1, slot2):
        day = 0

        current_color = Color(1, day, slot1, instances=10)
        other_color = Color(2, day, slot2, instances=10)

        self.assertFalse(
            self.gp._is_color_valid(current_color, other_color, self.course)
        )

    @data(
        {"available_instances": 1, "sections": 1},
        {"available_instances": 1, "sections": 5},
        {"available_instances": 3, "sections": 4},
    )
    @unpack
    def test_is_color_valid_available_instances_not_valid(
        self, available_instances, sections
    ):
        current_color = Color(1, 1, 0, instances=10)
        other_color = Color(2, 2, 0, instances=10)

        current_color.available_instances = available_instances
        self.course.sections = sections

        self.assertFalse(
            self.gp._is_color_valid(current_color, other_color, self.course)
        )

    @patch.object(GraphPainter, "_is_fair_to_schedule")
    def test_is_color_valid_is_fair_to_schedule_not_valid(
        self, mock_is_fair_to_schedule
    ):
        current_color = Color(1, 1, 0, instances=10)
        other_color = Color(2, 2, 0, instances=10)

        current_color.available_instances = 10
        self.course.sections = 5

        mock_is_fair_to_schedule.return_value = False
        self.assertFalse(
            self.gp._is_color_valid(current_color, other_color, self.course)
        )

    @patch.object(GraphPainter, "_is_fair_to_schedule")
    def test_is_color_valid_valid(self, mock_is_fair_to_schedule):
        current_color = Color(1, 1, 0, instances=10)
        other_color = Color(2, 2, 0, instances=10)

        current_color.available_instances = 10
        self.course.sections = 5

        mock_is_fair_to_schedule.return_value = True
        self.assertTrue(
            self.gp._is_color_valid(current_color, other_color, self.course)
        )


class TestGraphPainterSetCourseColor(TestCase):
    def test_set_course_color(self):
        day = 0
        slot = 0
        instances = 100
        old_available_instances = self.gp.colors[day][slot].available_instances
        self.course.sections = 1

        self.assertNotIn(self.course, self.gp.colors[day][slot].colored_courses)

        # Set the color
        new_color = Color(
            self.fake.random_digit_not_null(), day=day, slot=slot, instances=instances
        )
        self.gp._set_course_color(self.course, new_color, day, slot)

        self.assertEqual(new_color, self.course.color)
        self.assertIn(self.course, self.gp.colors[day][slot].colored_courses)
        self.assertEqual(
            self.gp.colors[day][slot].available_instances,
            old_available_instances - self.course.sections,
        )

    def test_set_course_color_negative_available_instances(self):
        day = 0
        slot = 0
        instances = 0
        old_available_instances = self.gp.colors[day][slot].available_instances
        self.course.sections = 100

        self.assertNotIn(self.course, self.gp.colors[day][slot].colored_courses)

        # Set the color
        new_color = Color(
            self.fake.random_digit_not_null(), day=day, slot=slot, instances=instances
        )
        with self.assertRaises(ValueError):
            self.gp._set_course_color(self.course, new_color, day, slot)

        self.assertEqual(
            self.gp.colors[day][slot].available_instances,
            old_available_instances,
        )

        self.assertIsNone(self.course.color)
        self.assertNotIn(self.course, self.gp.colors[day][slot].colored_courses)


class TestGraphPainterAttemptCourseColor(TestCase):
    @patch.object(GraphPainter, "_set_course_color")
    @patch.object(GraphPainter, "_get_smallest_available_color")
    def test_attempt_course_color_no_color(
        self, mock_get_smallest_available_color, mock_set_course_color
    ):
        mock_get_smallest_available_color.return_value = None
        actual = self.gp._attempt_course_color(self.course, 0)

        self.assertEqual(0, actual)
        mock_get_smallest_available_color.assert_called_once_with(self.course)
        mock_set_course_color.assert_not_called()

        mock_get_smallest_available_color.return_value = Color(key=None)
        actual = self.gp._attempt_course_color(self.course, 0)

        self.assertEqual(0, actual)
        mock_get_smallest_available_color.assert_called_with(self.course)
        mock_set_course_color.assert_not_called()

    @patch.object(GraphPainter, "_set_course_color", return_value=None)
    @patch.object(GraphPainter, "_get_smallest_available_color")
    def test_attempt_course_color_no_color_valid_color(
        self, mock_get_smallest_available_color, mock_set_course_color
    ):
        mock_get_smallest_available_color.return_value = Color(key=1)

        actual = self.gp._attempt_course_color(self.course, 0)
        mock_set_course_color.assert_called_once()

        self.assertEqual(1, actual)


class TestGraphPainterPaint(TestCase):
    @patch.object(GraphPainter, "_get_first_course_color", return_value=None)
    def test_paint_empty_graph_impossible_scheduling(self, mock_get_first_course_color):
        with self.assertRaises(RuntimeError):
            self.gp.paint()

        mock_get_first_course_color.assert_called_once()

    def test_paint_empty_graph_all_colored(self):
        for course in self.graph:
            course.color = True

        self.assertEqual(0, self.gp.paint())

    def test_paint_empty_graph_none_colored(self):
        self.assertEqual(len(self.graph), self.gp.paint())

    def test_paint_empty_graph(self):
        self.gp.graph = Graph(directed=False)
        self.assertEqual(0, self.gp.paint())
