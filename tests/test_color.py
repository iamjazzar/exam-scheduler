from palatable.color import Color
from tests.case import TestCase


class TestColorInit(TestCase):
    def test_init(self):
        key = self.fake.random_int()
        day = self.fake.random_digit_not_null()
        slot = self.fake.random_digit_not_null()
        instances = self.fake.random_digit_not_null()

        color = Color(key, day=day, slot=slot, instances=instances)

        self.assertEqual(key, color.key)
        self.assertIsInstance(color.name, str)

        self.assertEqual(day, color.day)
        self.assertEqual(slot, color.slot)

        self.assertIsNone(color._weight)
        self.assertListEqual([], color.colored_courses)
        self.assertEqual(instances, color.available_instances)

    def test_init_defaults(self):
        key = self.fake.random_int()
        color = Color(key)

        self.assertEqual(key, color.key)
        self.assertIsInstance(color.name, str)

        self.assertEqual(0, color.day)
        self.assertEqual(0, color.slot)

        self.assertIsNone(color._weight)
        self.assertListEqual([], color.colored_courses)
        self.assertEqual(0, color.available_instances)


class TestCalculateWeight(TestCase):
    def test_calculate_weight_formula(self):
        key = self.fake.random_int()
        day = self.fake.random_digit_not_null()
        slot = self.fake.random_digit_not_null()

        color = Color(key, day=day, slot=slot)

        slots = self.fake.random_digit_not_null()
        expected = ((day - 1) * slots) + slot
        self.assertEqual(expected, color.calculate_weight(slots))

    def test_calculate_weight_setting_weight(self):
        key = self.fake.random_int()
        day = self.fake.random_digit_not_null()
        slot = self.fake.random_digit_not_null()

        color = Color(key, day=day, slot=slot)

        slots = self.fake.random_digit_not_null()
        actual = color.calculate_weight(slots)
        self.assertEqual(color._weight, actual)


class TestColorStrRepr(TestCase):
    def test_color_str(self):
        color = Color(self.fake.random_int())

        self.assertEqual(color.name, str(color))

    def test_color_repr(self):
        color = Color(self.fake.random_int())

        self.assertEqual(f"<Color: {color.key}>", repr(color))
