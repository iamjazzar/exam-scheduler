from examscheduler.color import Color
from examscheduler.course import Course
from examscheduler.student import Student
from tests.case import TestCase


class TestCourseInit(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.key = self.fake.bothify(text="#######")
        self.name = self.fake.random_digit_not_null()
        self.level = self.fake.random_digit_not_null()
        self.sections = self.fake.random_digit_not_null()

    def test_init(self):
        course = Course(self.key, self.name, self.level, self.sections)

        self.assertEqual(self.key, course.key)
        self.assertEqual(self.name, course.name)
        self.assertEqual(self.level, course.level)
        self.assertEqual(self.sections, course.sections)

        self.assertEqual(self.sections, course.concurrency_level)
        self.assertListEqual([], course._students)
        self.assertListEqual([], course.weight_matrix)
        self.assertEqual(0, course.degree)
        self.assertEqual(0, course.largest_weight)

        self.assertIsNone(course.color)
        self.assertIsNone(course.time_slot)

    def test_course_same_key(self):
        Course(self.key, self.name, self.level, self.sections)

        with self.assertRaises(AttributeError):
            Course(self.key, self.name, self.level, self.sections)

        self.assertIn(self.key, Course._all_courses)
        self.assertEqual(1, len(Course._all_courses))

    def test_all_courses(self):
        self.assertEqual(0, len(Course._all_courses))

        key_1 = self.fake.bothify(text="#######")
        Course(key_1, self.name, self.level, self.sections)

        self.assertIn(key_1, Course._all_courses)
        self.assertEqual(1, len(Course._all_courses))

        key_2 = self.fake.bothify(text="#######")
        Course(key_2, self.name, self.level, self.sections)

        self.assertIn(key_2, Course._all_courses)
        self.assertEqual(2, len(Course._all_courses))


class TestCourseIsColored(TestCase):
    def setUp(self) -> None:
        super().setUp()

        key = self.fake.bothify(text="#######")
        name = self.fake.random_digit_not_null()
        level = self.fake.random_digit_not_null()
        sections = self.fake.random_digit_not_null()

        self.course = Course(key, name, level, sections)

    def test_not_colored(self):
        self.course.color = None

        self.assertFalse(self.course.is_colored)

    def test_colored(self):
        self.course.color = Color(self.fake.random_int())

        self.assertTrue(self.course.is_colored)


class TestCourseExistsGet(TestCase):
    def test_exists(self):
        key = self.fake.bothify(text="#######")
        name = self.fake.random_digit_not_null()
        level = self.fake.random_digit_not_null()
        sections = self.fake.random_digit_not_null()

        Course(key, name, level, sections)

        self.assertTrue(Course.exists(key))

    def test_get(self):
        key = self.fake.bothify(text="#######")
        name = self.fake.random_digit_not_null()
        level = self.fake.random_digit_not_null()
        sections = self.fake.random_digit_not_null()

        actual = Course(key, name, level, sections)
        retrieved = Course.get(key)

        self.assertEqual(actual, retrieved)

    def test_does_not_exists(self):
        key = self.fake.bothify(text="#######")
        name = self.fake.random_digit_not_null()
        level = self.fake.random_digit_not_null()
        sections = self.fake.random_digit_not_null()

        Course(key, name, level, sections)

        self.assertFalse(Course.exists("should-not-exist"))

    def test_get_does_not_exists(self):
        key = self.fake.bothify(text="#######")
        name = self.fake.random_digit_not_null()
        level = self.fake.random_digit_not_null()
        sections = self.fake.random_digit_not_null()

        Course(key, name, level, sections)

        self.assertIsNone(Course.get("should-not-exist"))


class TestCourseStudents(TestCase):
    def setUp(self) -> None:
        super().setUp()

        key = self.fake.bothify(text="#######")
        name = self.fake.random_digit_not_null()
        level = self.fake.random_digit_not_null()
        sections = self.fake.random_digit_not_null()

        self.course = Course(key, name, level, sections)

    def test_add_student(self):
        self.assertListEqual([], self.course._students)

        student1 = Student(self.fake.random_int())
        self.course.add_student(student1)

        self.assertEqual(1, len(self.course._students))
        self.assertListEqual([student1], self.course._students)

        student2 = Student(self.fake.random_int())
        self.course.add_student(student2)

        self.assertEqual(2, len(self.course._students))
        self.assertListEqual([student1, student2], self.course._students)

    def test_students(self):
        self.assertListEqual([], self.course._students)

        self.course._students = [1, 2, 3, 4]
        self.assertListEqual([1, 2, 3, 4], self.course.students)

        self.course._students = [1, 2]
        self.assertListEqual([1, 2], self.course.students)


class TestCourseDunderMethods(TestCase):
    def setUp(self) -> None:
        super().setUp()

        key = self.fake.bothify(text="#######")
        name = self.fake.random_digit_not_null()
        level = self.fake.random_digit_not_null()
        sections = self.fake.random_digit_not_null()

        self.course = Course(key, name, level, sections)

    def test_course_hash_method(self):
        self.assertEqual(id(self.course), hash(self.course))

    def test_course_str_method(self):
        self.assertEqual(self.course.key, str(self.course))

    def test_course_repr_method(self):
        self.assertEqual(f"<Course: {self.course.key}>", repr(self.course))


class TestCourseComparsionsDegree(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.course = Course(
            self.fake.bothify(text="#######"),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
        )
        self.other_course = Course(
            self.fake.bothify(text="#######"),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
        )

    def test_course_lt(self):
        self.course.degree = 1
        self.other_course.degree = 2

        self.assertTrue(self.course < self.other_course)

    def test_course_not_lt(self):
        self.course.degree = 2
        self.other_course.degree = 1

        self.assertFalse(self.course < self.other_course)

    def test_course_gt(self):
        self.course.degree = 2
        self.other_course.degree = 1

        self.assertTrue(self.course > self.other_course)

    def test_course_not_gt(self):
        self.course.degree = 1
        self.other_course.degree = 2

        self.assertFalse(self.course > self.other_course)


class TestCourseComparsionsLargestWeight(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.course = Course(
            self.fake.bothify(text="#######"),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
        )
        self.other_course = Course(
            self.fake.bothify(text="#######"),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
        )

        self.course.degree = 1
        self.other_course.degree = 1

    def test_course_lt(self):
        self.course.largest_weight = 1
        self.other_course.largest_weight = 2

        self.assertTrue(self.course < self.other_course)

    def test_course_not_lt(self):
        self.course.largest_weight = 2
        self.other_course.largest_weight = 1

        self.assertFalse(self.course < self.other_course)

    def test_course_gt(self):
        self.course.largest_weight = 2
        self.other_course.largest_weight = 1

        self.assertTrue(self.course > self.other_course)

    def test_course_not_gt(self):
        self.course.largest_weight = 1
        self.other_course.largest_weight = 2

        self.assertFalse(self.course > self.other_course)


class TestCourseComparsionsKey(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.course = Course(
            self.fake.bothify(text="#######"),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
        )
        self.other_course = Course(
            self.fake.bothify(text="#######"),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
            self.fake.random_digit_not_null(),
        )

        self.course.degree = 1
        self.other_course.degree = 1
        self.course.largest_weight = 2
        self.other_course.largest_weight = 2

    def test_course_lt(self):
        self.course.key = 1
        self.other_course.key = 2

        self.assertTrue(self.course < self.other_course)

    def test_course_not_lt(self):
        self.course.key = 2
        self.other_course.key = 1

        self.assertFalse(self.course < self.other_course)

    def test_course_gt(self):
        self.course.key = 2
        self.other_course.key = 1

        self.assertTrue(self.course > self.other_course)

    def test_course_not_gt(self):
        self.course.key = 1
        self.other_course.key = 2

        self.assertFalse(self.course > self.other_course)
