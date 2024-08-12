from src.table import Table
import unittest


class TestTable(unittest.TestCase):
    def test_format(self):
        result = Table([
            ("minute", [0,15,30,45]),
            ("hour", [0]),
            ("day of month", [1,2,3]),
            ("month", [1,2,3,4,5,6,7,8,9,10,11,12]),
            ("day of week", [1,2,3,4,5]),
            ("command", "/usr/bin/find")
        ]).format()

        expected = """minute          0 15 30 45
hour            0
day of month    1 2 3
month           1 2 3 4 5 6 7 8 9 10 11 12
day of week     1 2 3 4 5
command         /usr/bin/find"""
        self.assertEqual(result, expected)

    