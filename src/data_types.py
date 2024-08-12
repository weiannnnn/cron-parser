import typing
from enum import Enum
from dataclasses import dataclass

class CronFields(Enum):
    minute = "minute"
    hour = "hour"
    day_of_month = "day of month"
    month = "month"
    day_of_week = "day of week"
    year = "year"
    command = "command"


@dataclass
class FieldInputs:
    """
    Commands for each CRON field parsed from CLI input
    """
    minute: str
    hour: str
    day_of_month: str
    month: str
    day_of_week: str
    year: typing.Optional[str]
    command: str


@dataclass
class FieldOptions:
    """
    Options for each CRON field, calculated from CLI input
    e.g. { minute: [1, 5, 30], day_of_month: [1, 3, 12]...}
    """
    minute: typing.List[int]
    hour: typing.List[int]
    day_of_month: typing.List[int]
    month: typing.List[int]
    day_of_week: typing.List[int]
    year: typing.Optional[typing.List[int]]
    command: str


TableData: typing.TypeAlias = typing.List[typing.Tuple[CronFields, typing.Union[str, typing.List[int]]]]