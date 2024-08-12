# CRON Expression Parser
A Python CLI tool to parse CRON expressions into human readable outputs.

## Requirements
This code-base requires the following to run:
- [Python](https://www.python.org/downloads/) 3.12.4
- [pyenv](https://github.com/pyenv/pyenv) 2.4.7+

## Setup
1. Ensure correct version of python is being used
```
 pyenv local 3.12.4
```

## Usage
```
python3 main.py "{command}"
```

e.g.
```
python3 main.py "*/15 0 1,15 * 1-5 /usr/bin/find"
```

## Testing
To run unit tests, run
```
python3 -m unittest discover
```

## Edge cases considered
- CRON expression with the incorrect number of fields
- Values out of range for field (i.e. 35,36,37 for day of month, or 1-100 for day of week)
- intervals larger than available options (i.e. */100 for days of the week)

## Improvements
- Testing for table.py
- Store ranges for each field options in constants rather than in code
- More edge cases (negative inputs, valid days of months for different months)
- Validate command input