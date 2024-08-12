import typing
import re
from datetime import datetime

from .data_types import CronFields, FieldInputs, FieldOptions, TableData


class CronExpression:
    """
    Parse, store, and format CRON expression from CLI input string
    Provides CRON expression in three formats
    - raw_input (string input by user in CLI tool)
    - field_inputs: FieldInputs
    - field_options: FieldOptions
    And function to format data for ingestion into Table class
    """
    
    def __init__(
        self,
        raw_input: str
    ) -> None:
        self.raw_input: str = raw_input
        self.field_inputs: FieldInputs = self._split_fields_inputs(self.raw_input)
        self.field_options: FieldOptions = self._field_options(self.field_inputs)

    def format_for_table(self) -> TableData:
        return [
            (CronFields.minute.value, self.field_options.minute),
            (CronFields.hour.value, self.field_options.hour),
            (CronFields.day_of_month.value, self.field_options.day_of_month),
            (CronFields.month.value, self.field_options.month),
            (CronFields.day_of_week.value, self.field_options.day_of_week),
            (CronFields.year.value, self.field_options.year),
            (CronFields.command.value, self.field_options.command),
        ]

    def _split_fields_inputs(self, raw_input: str) -> FieldInputs:
        """
        Converts raw input string into CRON expressions for each CRON field - <minute> <hour> <day-of-month> <month> <day-of-week> <command>
        e.g.
            split_input = CronExpression(...)._split_fields_inputs(""*/15 0 1,15 * 5-1 /usr/bin/find")
            split_input.minute = "*/15"
            split_input.command = "/usr/bin/find"
        """
        split_arr: typing.List[str] = raw_input.split(" ")

        if len(split_arr) < 6:
            raise ValueError("Too few inputs to CRON expression")
        
        # "*/15 0 1,15 * 1-5 year /usr/bin/find"
        # command or year [year, /usr/bin/find] -> year and command
        # command or year [/user/bin/find, python3, ajkdasl] -> only command
        # assume command never starts with a number

        year, command = self._command_or_year(input_arr=split_arr[5:])

        return FieldInputs(
            minute=split_arr[0],
            hour=split_arr[1],
            day_of_month=split_arr[2],
            month=split_arr[3],
            day_of_week=split_arr[4],
            year=year,
            command=command
        )
    
    def _command_or_year(self, input_arr: typing.List[str]) -> tuple:
        if re.match(r"^\d", input_arr[0]) or input_arr[0] == "*":
            # assume that it is a year!
            return input_arr[0], ' '.join(input_arr[1:])

        return None, ' '.join(input_arr)

    
    def _field_options(self, field_inputs: FieldInputs) -> FieldOptions:
        """
        For each CRON field, return valid options based on constraints of field type (i.e. up to 31 days in a month) and field input (*, 1-5 etc)
        e.g.
            for minute, * should return [0,1,2,3......,59]
            for day of the week, */2 should return [1,3,5,7]
        """

        return FieldOptions(
            minute=self._eval(expression=field_inputs.minute, lower=0, upper=59),
            hour=self._eval(expression=field_inputs.hour, lower=0, upper=23),
            day_of_month=self._eval(expression=field_inputs.day_of_month, lower=1, upper=31), # EDGE CASE - different months have different number of days
            month=self._eval(expression=field_inputs.month, lower=1, upper=12),
            day_of_week=self._eval(expression=field_inputs.day_of_week, lower=1, upper=7),
            year=self._eval(expression=field_inputs.year, lower=datetime.now().year, upper=datetime.now().year + 9),
            command=field_inputs.command
        )
    
    def _eval(
            self,
            expression: typing.Optional[str],
            lower: int,
            upper: int
        ) -> typing.List[int]:
        """
        Evaluates expression and options provided, returns list of possible options
        # Logic
        # +------+----------------------+-------------------------------------+
        # | Char |     Description      | Example (for minute)                |    
        # +------+----------------------+-------------------------------------+
        # | *    | Any value            | Every minute of the hour            |
        # | ,    | Separator            | 10,20: the 10th and 20th minute     |
        # | -    | interval             | 10-25: from 10 until 25 past hour   |
        # | /    | Step                 | */5: every 5th minute               |
        # +------+----------------------+-------------------------------------+
        """

        if expression is None:
            return []

        if expression == "*":
            return list(range(lower, upper+1))

        separators: typing.List[str] = re.findall(r"^\d{1,2}(?:,\d{1,2})*$", expression)
        if separators:
            return self._separator_expand(input=separators, lower=lower, upper=upper)
        
        interval = re.search(r"^(\d{1,2})-(\d{1,2})$", expression)
        if interval:
            return self._interval_expand(input=interval, options_lower=lower, options_upper=upper)
    
        steps = re.search(r"^(\*|\d{1,2}-\d{1,2})/(\d{1,2})$", expression)
        if steps:
            return self._step_expand(input=steps, lower=lower, upper=upper)
        
        return []

    def _separator_expand(
        self,
        input: typing.List[str],
        lower: int,
        upper: int
    ) -> typing.List[int]:
        """
        ['1,15,30'] -> [1, 15, 30]
        """
        # Would not happen, but guard regardless
        if len(input) > 1:
            raise Exception("Invalid expression")
        expanded = [int(x) for x in input[0].split(",")]
        if min(expanded) < lower or max(expanded) > upper:
            raise ValueError("Invalid expression")
        return expanded

    def _interval_expand(
        self,
        input: re.Match,
        options_lower: int,
        options_upper: int
    ):
        """
        match='1-5' -> [1,2,3,4,5]
        """
        interval_lower, interval_upper = int(input.group(1)), int(input.group(2))
        if interval_lower > interval_upper or interval_lower<options_lower or interval_upper>options_upper:
            raise ValueError("Invalid expression")
        return list(range(interval_lower, interval_upper + 1))

    def _step_expand(
        self,
        input: re.Match,
        lower: int,
        upper: int
    ) -> typing.List[int]:
        step_options = self._eval(
            expression=input.group(1),
            lower=lower,
            upper=upper
        )
        interval = int(input.group(2))
        if interval > max(step_options):
            raise ValueError("Invalid expression")
        return step_options[::interval]