from .data_types import TableData

class Table:
    """
    Class to store table data and format it in CLI output
    """
    def __init__(
            self,
            table_data: TableData,
            column_size: int = 15 # at least 12 characters to account for longest CRON field name
    ):
        self.data = table_data
        self.column_size = column_size

    def format(self) ->  str:
        """
        Format table data into a table for printing to console
        """
        out = ""
        for name, value in self.data:
            if isinstance(value, list):
                value = " ".join([str(x) for x in value])
            if value != "":
                row = f"{self._create_padding(name=name, col_length=self.column_size)} {value}\n"
                out += row
        return out.rstrip()
    
    def _create_padding(self, name: str, col_length: int) -> str:
        """
        Helper fn to create consistent padding, regardless of name length
        """
        return name + " " * (col_length - len(name))