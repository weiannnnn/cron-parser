from src.cron_expression import CronExpression
import unittest
import datetime


class TestCronExpression(unittest.TestCase):
    # --------------------
    # Class attributes stored correctly
    # --------------------
    def test_store_input(self):
        instance = CronExpression("*/15 0 1,2,3 * 1-5 /usr/bin/find")
        self.assertEqual(instance.raw_input, "*/15 0 1,2,3 * 1-5 /usr/bin/find")

    def test_command_with_year(self):
        instance = CronExpression("*/15 0 1,2,3 * 1-5 2007,2008 python3 command1 command2")
        self.assertEqual(instance.field_inputs.year, "2007,2008")
        self.assertEqual(instance.field_inputs.command, "python3 command1 command2")
    
    def test_command_with_whitespaces(self):
        instance = CronExpression("*/15 0 1,2,3 * 1-5 python3 command1 command2")
        self.assertEqual(instance.field_inputs.command, "python3 command1 command2")

    def test_split_field_inputs(self):
        instance = CronExpression( "*/15 0 1,2,3 * 1-5 /usr/bin/find")
        self.assertEqual(instance.field_inputs.minute, "*/15")
        self.assertEqual(instance.field_inputs.hour, "0")
        self.assertEqual(instance.field_inputs.day_of_month, "1,2,3")
        self.assertEqual(instance.field_inputs.month, "*")
        self.assertEqual(instance.field_inputs.day_of_week, "1-5")
        self.assertEqual(instance.field_inputs.command, "/usr/bin/find")

    def test_field_options(self):
        instance = CronExpression( "*/15 0 1,2,3 * 1-5 /usr/bin/find")
        self.assertEqual(instance.field_options.minute, [0,15,30,45])
        self.assertEqual(instance.field_options.hour, [0])
        self.assertEqual(instance.field_options.day_of_month, [1,2,3])
        self.assertEqual(instance.field_options.month, [1,2,3,4,5,6,7,8,9,10,11,12])
        self.assertEqual(instance.field_options.day_of_week, [1,2,3,4,5])
        self.assertEqual(instance.field_options.command, "/usr/bin/find")

    def test_empty_list_default(self):
        instance = CronExpression("null null null null null null")
        self.assertEqual(instance.field_options.minute, [])
        self.assertEqual(instance.field_options.hour, [])
        self.assertEqual(instance.field_options.day_of_month, [])
        self.assertEqual(instance.field_options.month, [])
        self.assertEqual(instance.field_options.day_of_week, [])
        self.assertEqual(instance.field_options.command, "null")

    # --------------------
    # Format for table
    # --------------------

    def test_format_for_table(self):
        instance = CronExpression("*/15 0 1,2,3 * 1-5 /usr/bin/find")
        self.assertEqual(instance.format_for_table(), [
            ("minute", [0,15,30,45]),
            ("hour", [0]),
            ("day of month", [1,2,3]),
            ("month", [1,2,3,4,5,6,7,8,9,10,11,12]),
            ("day of week", [1,2,3,4,5]),
            ("command", "/usr/bin/find")
        ])

    # --------------------
    # Input validation
    # --------------------
    def test_insufficient_fields_throw_error(self):
        with self.assertRaises(ValueError):
            CronExpression("")
        with self.assertRaises(ValueError):
            CronExpression("*/15 0 1,2,3 * 1-5")

    # --------------------
    # Expression evaluation
    # --------------------
    
    def test_any_exp(self):
        instance = CronExpression("null null null * null null")
        self.assertEqual(instance.field_options.month, [1,2,3,4,5,6,7,8,9,10,11,12])

    def test_separator_exp(self):
        instance = CronExpression("null null 1,2,3 null null null")
        self.assertEqual(instance.field_options.day_of_month, [1,2,3])
    
    def test_separator_exceed_limit_exp_raise_error(self):
        with self.assertRaises(ValueError):
            CronExpression("null null null null 9,10 null")
    
    def test_interval__exp(self):
        instance = CronExpression("null null null null 1-5 null")
        self.assertEqual(instance.field_options.day_of_week, [1,2,3,4,5])
    
    def test_interval_exp_lower_more_than_upper_raises_error(self):
        with self.assertRaises(ValueError):
            CronExpression("null null null null 5-1 null")
    
    def test_interval_not_in_range_raises_error(self):
        with self.assertRaises(ValueError):
            CronExpression("null null null null 20-25 null")
    
    def test_step_values_expression(self):
        instance = CronExpression("*/15 null null null null null")
        self.assertEqual(instance.field_options.minute, [0, 15, 30, 45])

    def test_step_expression_step_larger_than_range(self):
        with self.assertRaises(ValueError):
            CronExpression("*/70 null null null null null")
    
    def test_field_ranges(self):
        instance = CronExpression("* * * * * * some-command")

        print("YEAR INPUT", instance.field_inputs.year)
        self.assertEqual(instance.field_options.minute, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59])
        self.assertEqual(instance.field_options.hour, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
        self.assertEqual(instance.field_options.day_of_month, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31])
        self.assertEqual(instance.field_options.month, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        self.assertEqual(instance.field_options.day_of_week, [1, 2, 3, 4, 5, 6, 7]),
        self.assertEqual(instance.field_options.year, [2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033])
        self.assertEqual(instance.field_options.command, "some-command")

    def test_complex(self):
        # 1,2,4-5,10-20/2
        print("")

if __name__ == '__main__':
    unittest.main()