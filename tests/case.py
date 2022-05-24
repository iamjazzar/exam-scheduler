from unittest import TestCase as UnittestTestCase

from faker import Faker

from examscheduler.course import Course
from examscheduler.student import Student


class TestCase(UnittestTestCase):
    def setUp(self) -> None:
        self.fake = Faker()

    def tearDown(self) -> None:
        Student._all_students = set()
        Course._all_courses = {}
