from collections import defaultdict
from unittest.mock import patch

from ddt import data, ddt, unpack

from examscheduler.course import Course
from examscheduler.graphbuilder import GraphBuilder
from tests.case import TestCase


class TestGraphBuilderInit(TestCase):
    def test_graphbuilder_init(self):
        slots = self.fake.random_int()
        schedule_path = self.fake.file_path(depth=3)
        courses_path = self.fake.file_path(depth=3)

        gb = GraphBuilder(slots, schedule_path, courses_path)

        self.assertEqual(gb.slots, slots)
        self.assertEqual(gb.schedule_path, schedule_path)
        self.assertEqual(gb.courses_path, courses_path)

        self.assertListEqual(gb.courses, [])
        self.assertListEqual(gb.courses_ids, [])


class TestGraphBuilderReadCourses(TestCase):
    def setUp(self) -> None:
        super().setUp()

        slots = self.fake.random_int()
        schedule_path = self.fake.file_path(depth=3)
        courses_path = self.fake.file_path(depth=3)

        self.gb = GraphBuilder(slots, schedule_path, courses_path)

    @patch("examscheduler.graphbuilder.read_file", return_value=[])
    def test_read_courses_no_lines(self, *args):
        courses = self.gb._read_courses()

        self.assertEqual(0, len(courses))
        self.assertDictEqual(defaultdict(list), courses)

    @patch("examscheduler.graphbuilder.read_file")
    def test_read_courses_one_line(self, mock_read_file):
        mock_read_file.return_value = ["1901204	LogicDesign 			2       3"]
        courses = self.gb._read_courses()

        # One level has been created
        self.assertEqual(1, len(courses))
        # One course has been added to the level
        self.assertEqual(1, len(courses[2]))
        self.assertEqual("1901204", courses[2][0].key)
        self.assertEqual("LogicDesign", courses[2][0].name)
        self.assertEqual(2, courses[2][0].level)
        self.assertEqual(3, courses[2][0].sections)

    @patch("examscheduler.graphbuilder.read_file")
    def test_read_courses_multiple_lines(self, mock_read_file):
        mock_read_file.return_value = [
            "1901204	LogicDesign 			2       3",
            "1901351	Numerical   			3       5",
            "1904232	MIS         			2       2",
        ]
        courses = self.gb._read_courses()

        # Two levels has been created
        self.assertEqual(2, len(courses))

        # Two courses have been added to level 2
        self.assertEqual(2, len(courses[2]))
        # One courses have been added to level 3
        self.assertEqual(1, len(courses[3]))

        self.assertEqual("1901204", courses[2][0].key)
        self.assertEqual("1904232", courses[2][1].key)
        self.assertEqual("1901351", courses[3][0].key)


class TestGraphBuilderReadSchedule(TestCase):
    def setUp(self) -> None:
        super().setUp()

        slots = self.fake.random_int()
        schedule_path = self.fake.file_path(depth=3)
        courses_path = self.fake.file_path(depth=3)

        self.gb = GraphBuilder(slots, schedule_path, courses_path)

    def _add_courses(self):
        keys = {
            "1921425",
            "1901472",
            "1921422",
            "1921411",
        }

        for key in keys:
            Course(
                key,
                self.fake.random_digit_not_null(),
                self.fake.random_digit_not_null(),
                self.fake.random_digit_not_null(),
            )

    @patch("examscheduler.graphbuilder.read_file", return_value=[])
    def test_read_schedule_no_lines(self, *args):
        schedules = self.gb._read_schedule()

        self.assertEqual(0, len(schedules))
        self.assertListEqual([], schedules)

    @patch("examscheduler.graphbuilder.read_file")
    def test_read_schedule_no_courses_discovered(self, mock_read_file):
        mock_read_file.return_value = [
            "0125897         1921425     1921411     1901472",
        ]

        self.assertEqual(0, len(Course._all_courses))
        schedules = self.gb._read_schedule()

        # One schedule has been processed
        self.assertEqual(0, len(schedules))
        self.assertEqual(0, len(Course._all_courses))

    @patch("examscheduler.graphbuilder.read_file")
    def test_read_schedule_one_line(self, mock_read_file):
        self._add_courses()

        mock_read_file.return_value = [
            "0125897         1921425     1921411     1901472",
        ]
        schedules = self.gb._read_schedule()

        # One schedule has been processed
        self.assertEqual(1, len(schedules))

        # 3 Courses must be added to the schedule
        self.assertEqual(3, len(schedules[0]))

        student = "0125897"
        keys = {"1921425", "1921411", "1901472"}

        for course in schedules[0]:
            self.assertIn(course.key, keys)
            self.assertEqual(student, course._students[0].key)

            # Three registered courses
            self.assertEqual(3, len(course._students[0]._registered_courses))
            for c in course._students[0]._registered_courses:
                self.assertIn(c.key, keys)

    @patch("examscheduler.graphbuilder.read_file")
    def test_read_schedule_multiple_lines(self, mock_read_file):
        self._add_courses()

        mock_read_file.return_value = [
            "0125897         1921425     1921411     1901472",
            "0325887         1921422     1901466",
        ]
        schedules = self.gb._read_schedule()

        # Two schedules have been processed
        self.assertEqual(2, len(schedules))

        # 1 Course must be added to the second student's schedule (The
        # second course is not in the approved courses for listing).
        self.assertEqual(1, len(schedules[1]))

        student = "0325887"
        keys = {"1921422"}

        for course in schedules[1]:
            self.assertIn(course.key, keys)
            self.assertEqual(student, course._students[0].key)

            # One registered course
            self.assertEqual(1, len(course._students[0]._registered_courses))
            for c in course._students[0]._registered_courses:
                self.assertIn(c.key, keys)


@ddt
class TestGraphBuilderProcessNodes(TestCase):
    def setUp(self) -> None:
        super().setUp()

        slots = self.fake.random_int()
        schedule_path = self.fake.file_path(depth=3)
        courses_path = self.fake.file_path(depth=3)

        self.gb = GraphBuilder(slots, schedule_path, courses_path)
        self._add_courses()
        self.schedules = [
            [
                Course.get("1921425"),
                Course.get("1901472"),
                Course.get("1921422"),
            ],
            [
                Course.get("1921411"),
                Course.get("1901472"),
            ],
        ]

    def _add_courses(self):
        keys = {
            "1921425",
            "1901472",
            "1921422",
            "1921411",
        }

        for key in keys:
            Course(
                key,
                self.fake.random_digit_not_null(),
                self.fake.random_digit_not_null(),
                self.fake.random_digit_not_null(),
            )

    def test_process_nodes_undirected_graph(self):
        graph = self.gb._process_nodes(self.schedules)
        self.assertFalse(graph.directed)

    @data(
        {"key1": "1921425", "key2": "1901472"},  # First schedule
        {"key1": "1921425", "key2": "1921422"},  # First schedule
        {"key1": "1901472", "key2": "1921422"},  # First schedule
        {"key1": "1921411", "key2": "1901472"},  # Second schedule
        {"key1": "1901472", "key2": "1921411"},  # Second schedule
    )
    @unpack
    def test_process_nodes_edges(self, key1, key2):
        graph = self.gb._process_nodes(self.schedules)

        # First schedule edges
        self.assertTrue(graph.contains_edge(Course.get(key1), Course.get(key2)))

    @data(
        {"key1": "1921425", "key2": "1901472"},  # First schedule
        {"key1": "1921425", "key2": "1921422"},  # First schedule
        {"key1": "1901472", "key2": "1921422"},  # First schedule
        {"key1": "1921411", "key2": "1901472"},  # Second schedule
        {"key1": "1901472", "key2": "1921411"},  # Second schedule
    )
    @unpack
    def test_process_nodes_weights_ones(self, key1, key2):
        graph = self.gb._process_nodes(self.schedules)

        self.assertEqual(1, graph.get_weight(Course.get(key1), Course.get(key2)))

    def test_process_nodes_weights_more_than_one(self):
        graph = self.gb._process_nodes(
            [
                [
                    Course.get("1921425"),
                    Course.get("1901472"),
                    Course.get("1921422"),
                ],
                [
                    Course.get("1921425"),
                    Course.get("1901472"),
                ],
            ]
        )

        # Weight must be two since it appears in two schedules
        self.assertEqual(
            2, graph.get_weight(Course.get("1921425"), Course.get("1901472"))
        )

    @data(
        {"key": "1921425", "degree": 2},  # Connected to two different courses
        {"key": "1901472", "degree": 3},  # Connected to three different courses
        {"key": "1921422", "degree": 2},  # Connected to two different courses
        {"key": "1921411", "degree": 1},  # Connected to one course
    )
    @unpack
    def test_process_nodes_degree(self, key, degree):
        graph = self.gb._process_nodes(self.schedules)

        self.assertEqual(degree, graph.get_degree(Course.get(key)))
        self.assertEqual(degree, Course.get(key).degree)

    @data(
        {"key": "1921425"},  # Appears in one schedule
        {"key": "1901472"},  # Appears in two schedules
        {"key": "1921422"},  # Appears in one schedule
        {"key": "1921411"},  # Appears in one schedule
    )
    @unpack
    def test_process_nodes_largest_weight_ones(self, key):
        graph = self.gb._process_nodes(self.schedules)

        self.assertEqual(1, graph.get_largest_weight(Course.get(key)))
        self.assertEqual(1, Course.get(key).largest_weight)

    @data(
        {"key": "1921425", "weight": 2},  # Connected to 1901472 twice
        {"key": "1901472", "weight": 2},  # Connected to 1921425 twice
        {"key": "1921422", "weight": 1},  # Appears in one schedule
        {"key": "1921411", "weight": 0},  # No weights here
    )
    @unpack
    def test_process_nodes_largest_weight_more_than_one(self, key, weight):
        graph = self.gb._process_nodes(
            [
                [
                    Course.get("1921425"),
                    Course.get("1901472"),
                    Course.get("1921422"),
                ],
                [
                    Course.get("1921425"),
                    Course.get("1901472"),
                ],
            ]
        )

        self.assertEqual(weight, graph.get_largest_weight(Course.get(key)))
        self.assertEqual(weight, Course.get(key).largest_weight)


class TestGraphBuilderBuild(TestCase):
    @patch.object(GraphBuilder, "_read_courses")
    @patch.object(GraphBuilder, "_read_schedule")
    @patch.object(GraphBuilder, "_process_nodes")
    def test_build(self, mock_process_nodes, mock_read_schedule, mock_read_courses):
        slots = self.fake.random_int()
        schedule_path = self.fake.file_path(depth=3)
        courses_path = self.fake.file_path(depth=3)

        gb = GraphBuilder(slots, schedule_path, courses_path)
        expected = gb.build()

        mock_read_courses.assert_called_once_with()
        mock_read_schedule.assert_called_once_with()
        mock_process_nodes.assert_called_once_with(mock_read_schedule.return_value)

        self.assertEqual(expected, mock_process_nodes.return_value)
