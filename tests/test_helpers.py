from unittest.mock import mock_open, patch

from ddt import data, ddt

from palatable.helpers import calculate_distance, read_file
from tests.case import TestCase


@ddt
class TestReadFile(TestCase):
    def test_read_file_none(self):
        results = read_file(None)

        with self.assertRaises(TypeError):
            list(results)

    @data("", "/some/random/file.txt")
    def test_read_file_not_found(self, value):
        results = read_file(value)

        with self.assertRaises(FileNotFoundError):
            list(results)

    def test_one_line(self):
        read_data = "some text goes in file"
        path = "/some/path.txt"

        with patch("builtins.open", mock_open(read_data=read_data)) as mock_file:
            results = list(read_file(path))
            mock_file.assert_called_with(path, "r")

        self.assertEqual(1, len(results), msg="Expecting one line to be yielded.")

    def test_one_line_comment(self):
        read_data = "# some comment"
        path = "/some/path.txt"

        with patch("builtins.open", mock_open(read_data=read_data)) as mock_file:
            results = list(read_file(path))
            mock_file.assert_called_with(path, "r")

        self.assertListEqual(results, [])

    def test_multiple_lines(self):
        read_data = "some before\nsome after"
        path = "/some/path.txt"

        with patch("builtins.open", mock_open(read_data=read_data)) as mock_file:
            results = list(read_file(path))
            mock_file.assert_called_with(path, "r")

        self.assertEqual(2, len(results), msg="Expecting two rows!")
        self.assertIn("some before\n", results)
        self.assertIn("some after", results)

    def test_multiple_lines_comment(self):
        comment_line = "# some comment"
        read_data = f"some before\n{comment_line}\nsome after"
        path = "/some/path.txt"

        with patch("builtins.open", mock_open(read_data=read_data)) as mock_file:
            results = list(read_file(path))
            mock_file.assert_called_with(path, "r")

        self.assertNotIn(comment_line, results)
        self.assertEqual(2, len(results), msg="Expecting two rows!")


class TestCalculateDistance(TestCase):
    def test_calculate_distance_first_second(self):
        result = calculate_distance(3, 2)
        self.assertEqual(3 - 2, result)

    def test_calculate_distance_second_first(self):
        result = calculate_distance(2, 4)
        self.assertEqual(4 - 2, result)
