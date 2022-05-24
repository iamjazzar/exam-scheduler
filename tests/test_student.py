from examscheduler.student import Student
from tests.case import TestCase


class TestStudentInit(TestCase):
    def test_key_and_registered_courses(self):
        key = self.fake.random_int()
        student = Student(key)
        self.assertEqual(student.key, key)
        self.assertSetEqual(student._registered_courses, set())

    def test_all_students(self):
        self.assertEqual(0, len(Student._all_students))

        key_1 = "test-key-1"
        Student(key_1)

        self.assertIn(key_1, Student._all_students)
        self.assertEqual(1, len(Student._all_students))

        key_2 = "test-key-2"
        Student(key_2)

        self.assertIn(key_2, Student._all_students)
        self.assertEqual(2, len(Student._all_students))

    def test_student_same_key(self):
        key = self.fake.random_int()
        Student(key)

        with self.assertRaises(AttributeError):
            Student(key)

        self.assertIn(key, Student._all_students)
        self.assertEqual(1, len(Student._all_students))


class TestStudentAddCourse(TestCase):
    def test_registered_courses_and_courses(self):
        student = Student(1234)
        self.assertSetEqual(student._registered_courses, set())

        student._registered_courses = [1, 2, 3]
        self.assertListEqual(student.courses, [1, 2, 3])

    def test_add_course(self):
        student = Student(1234)

        student.add_course(1)
        student.add_course(2)
        student.add_course(3)

        self.assertSetEqual(student.courses, {1, 2, 3})
