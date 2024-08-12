import sys

from src.cron_expression import CronExpression
from src.table import Table


def main():
    try:
        input = sys.argv[1]
    except IndexError:
        print('Error: unable to find CRON expression. Please execute command in the following pattern: python3 main.py "*/15 0 1,15 * 1-5 /usr/bin/find"')
        exit

    table_data = CronExpression(raw_input=input).format_for_table()
    print(Table(table_data=table_data).format())


if __name__ == "__main__":
    main()



