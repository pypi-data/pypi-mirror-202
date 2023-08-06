from typing import List, Union

from O365.excel import EXCEL_XLSX_MIME_TYPE, File, WorkBook, WorkSheet

from botcity.plugins.ms365.credentials import MS365CredentialsPlugin


class MS365ExcelPlugin:
    def __init__(self, service_account: MS365CredentialsPlugin) -> None:
        """
        MS365ExcelPlugin.

        Args:
            service_account (MS365CredentialsPlugin): The authenticated Microsoft365 account.
                The authentication process must be done through the credentials plugin.
        """
        self._excel_file = None
        self._active_sheet = None
        self._service = service_account.ms365_account

    @property
    def excel_file(self) -> WorkBook:
        """
        The Workbook element referencing the Excel file.

        You can use this property to access Excel functionality.
        """
        return self._excel_file

    @excel_file.setter
    def excel_file(self, drive_file: File):
        """
        Set the Workbook element referencing the Excel file.

        You can use this property to access Excel functionality.
        """
        self._excel_file = WorkBook(file_item=drive_file)

    @property
    def active_sheet(self) -> WorkSheet:
        """
        The reference to the active Worksheet.

        You can use this property to perform operations directly on this worksheet.
        """
        return self._active_sheet

    @active_sheet.setter
    def active_sheet(self, worksheet: WorkSheet):
        """
        Set the reference to the active Worksheet.

        You can use this property to perform operations directly on this worksheet.
        """
        self._active_sheet = worksheet

    def get_excel_file(self, file_or_path: Union[File, str], active_sheet: str = ""):
        """
        Get the Excel file using the File object or the file path in Drive.

        The file path must be used in the pattern: /path/to/file

        Args:
            file_or_path (File | str): The file path to fetch or the File object.
            active_sheet (str, optional): The name of the worksheet to be used by default.
                Defaults to the first sheet.
        """
        drive_item = file_or_path
        if isinstance(drive_item, str):
            default_drive = self._service.storage().get_default_drive()
            drive_item = default_drive.get_item_by_path(file_or_path)

        if not drive_item.is_file or drive_item.mime_type != EXCEL_XLSX_MIME_TYPE:
            raise ValueError("No Excel file found using this file or path.")
        self.excel_file = drive_item
        self.set_active_sheet(sheet_name=active_sheet)

    def set_active_sheet(self, sheet_name: str = ""):
        """
        Set the active worksheet that will be used by default.

        If no worksheet is informed, the first worksheet in the file will be considered.

        Args:
            sheet_name (str, optional): The name of the worksheet to be used.
        """
        if not sheet_name:
            self._active_sheet = self.excel_file.get_worksheets()[0]
        else:
            worksheet = self.get_worksheet(sheet_name=sheet_name)
            self._active_sheet = worksheet

    def create_sheet(self, sheet_name: str):
        """
        Create a new worksheet.

        Args:
            sheet_name (str): The name of the worksheet to be created.
        """
        self.excel_file.add_worksheet(name=sheet_name)

    def remove_sheet(self, sheet_name: str):
        """
        Remove a worksheet.

        Keep in mind that if you remove the active_sheet, you must set another sheet as active.

        Args:
            sheet_name (str): The name of the worksheet to be removed.
        """
        worksheet = self.get_worksheet(sheet_name=sheet_name)
        worksheet.delete()

    def list_sheets(self):
        """
        Return a list with the Worksheet object for each worksheet in the file.

        Returns:
            List[Worksheet]: A list of Worksheet objects.
        """
        return self.excel_file.get_worksheets()

    def get_worksheet(self, sheet_name: str):
        """
        Get a Worksheet object using it's name.

        You can use this object to set the active sheet.

        Args:
            sheet_name (str): The name of the worksheet to be fetched.

        Returns:
            Worksheet: The Worksheet object.
        """
        worksheet = None
        for ws in self.excel_file.get_worksheets():
            if ws.name == sheet_name:
                worksheet = ws
                break
        if not worksheet:
            raise ValueError("No sheets found in Excel file using this sheet name.")
        return worksheet

    def clear(self, range_: str = "", only_values=True, sheet: WorkSheet = None):
        """
        Clear a specific range or the entire worksheet content.

        Args:
            range_ (str, optional): The range to be cleared, in A1 format. Example: 'A1:B2'.
                If no range is informed, the entire worksheet content will be considered.
            only_values(bool, optional): If True, only the values will be removed and the sheet formatting will remain.
                If False, values and formatting will be removed.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        ws = sheet or self.active_sheet

        apply_to = "contents"
        if not only_values:
            apply_to = "all"

        if range_:
            content = ws.get_range(address=range_)
        else:
            content = ws.get_used_range()
        content.clear(apply_to=apply_to)

    def as_list(self, sheet: WorkSheet = None):
        """
        Return the contents of an entire sheet in a list of lists format.

        Args:
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.

        Returns:
            List[List[object]]: A list of rows. Each row is a list of cell values.
        """
        ws = sheet or self.active_sheet
        content = ws.get_used_range()
        values = self._format_values(content.text)
        return values

    def set_cell(self, column: str, row: int, value: object, sheet: WorkSheet = None):
        """
        Insert a value in a single cell.

        Args:
            column (str): The cell's letter-indexed column name ('a', 'A', 'AA').
            row (int): The cell's 1-indexed row number.
            value (object): The value to be entered into the cell.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        ws = sheet or self.active_sheet
        column = self._get_column_index(column)
        cell = ws.get_cell(row=row - 1, column=column)
        cell.values = value
        cell.update()

    def get_cell(self, column: str, row: int, sheet: WorkSheet = None):
        """
        Return the value of a single cell.

        Args:
            column (str): The cell's letter-indexed column name ('a', 'A', 'AA').
            row (int): The cell's 1-indexed row number.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.

        Returns:
            object: The cell's value.
        """
        ws = sheet or self.active_sheet
        column = self._get_column_index(column)
        cell = ws.get_cell(row=row - 1, column=column)
        return cell.text[0][0]

    def set_range(self, range_: str, values: List[List[object]], sheet: WorkSheet = None):
        """
        Insert values in a given range.

        Args:
            range_ (str): The range to be used, in A1 format. Example: 'A1:B2'.
            values (List[List[object]]): A list of rows. Each row is a list of cell values.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        ws = sheet or self.active_sheet
        content = ws.get_range(address=range_)
        content.values = values
        content.update()

    def get_range(self, range_: str, sheet: WorkSheet = None):
        """
        Return the contents of a specific range.

        Args:
            range_ (str): The range to be used, in A1 format. Example: 'A1:B2'.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.

        Returns:
            List[List[object]]: A list of rows. Each row is a list of cell values.
        """
        ws = sheet or self.active_sheet
        content = ws.get_range(address=range_)
        values = self._format_values(content.text)
        return values

    def add_row(self, row_values: List[object], row_range: str = "", sheet: WorkSheet = None):
        """
        Add a new row to the worksheet.

        You can add a new row at the end of the worksheet or at a specific range.

        Args:
            row_values (List[object]): A list with the cell values.
            row_range (str, optional): The row range to be used, in A1 format. Example: 'A3:D3'.
                If no range is specified, the new row will be added at the end.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        ws = sheet or self.active_sheet

        if not row_range:
            last_row = ws.get_used_range().get_last_row()

            row_index = last_row.row_index + 2
            if last_row.row_index == 0 and last_row.values[0] == ['']:
                row_index = last_row.row_index + 1

            start_column = self._get_column_name(last_row.column_index)
            final_column = self._get_column_name(last_row.column_index + len(row_values) - 1)
            row_range = f"{start_column}{row_index}:{final_column}{row_index}"

        new_row = ws.get_range(address=row_range)
        new_row.values = [row_values]
        new_row.update()

    def get_row(self, row: int, sheet: WorkSheet = None):
        """
        Return the contents of an entire row in a list format.

        Args:
            row (int): The 1-indexed row number.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.

        Returns:
            List[object]: The values of all cells within the row.
        """
        ws = sheet or self.active_sheet
        content = ws.get_used_range()
        col_index = self._get_column_name(column_index=content.column_count - 1)

        rows_range = f"A{row}:{col_index}{row}"
        content = ws.get_range(address=rows_range)
        return self._format_row_values(row_content=content.text[0])

    def remove_row(self, row: int, sheet: WorkSheet = None):
        """
        Remove a single row from the worksheet.

        Args:
            row (int): The 1-indexed row number.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        self.remove_rows(rows=[row], sheet=sheet)

    def remove_rows(self, rows: List[int], sheet: WorkSheet = None):
        """
        Remove rows from the sheet.

        Args:
            rows (List[int]): A list of the 1-indexed numbers of the rows to be removed.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        ws = sheet or self.active_sheet
        content = ws.get_used_range()
        col_index = self._get_column_name(column_index=content.column_count - 1)

        rows.sort(reverse=True)
        for row_index in rows:
            row_range = f"A{row_index}:{col_index}{row_index}"
            row_content = ws.get_range(address=row_range)
            row_content.delete(shift='up')

    def add_column(self, column_values: List[object], col_range: str = "", sheet: WorkSheet = None):
        """
        Add a new column to the worksheet.

        You can add a new column at the right end of the worksheet or at a specific range.

        Args:
            column_values (List[object]): A list with the cell values.
            col_range (str, optional): The column range to be used, in A1 format. Example: 'B1:B10'.
                If no range is specified, the new column will be added at the right end.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        ws = sheet or self.active_sheet

        if not col_range:
            last_column = ws.get_used_range().get_last_column()

            next_index = last_column.column_index + 1
            if last_column.column_index == 0 and last_column.values[0] == ['']:
                next_index = last_column.column_index

            col_index = self._get_column_name(column_index=next_index)
            start_row = last_column.row_index + 1
            final_row = start_row + (len(column_values) - 1)
            col_range = f"{col_index}{start_row}:{col_index}{final_row}"

        new_col = ws.get_range(address=col_range)
        values = [[value] for value in column_values]
        new_col.values = values
        new_col.update()

    def get_column(self, column: str, sheet: WorkSheet = None):
        """
        Return the contents of an entire column in a list format.

        Args:
            column (str): The letter-indexed column name ('a', 'A', 'AA').
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.

        Returns:
            List[object]: The values of all cells within the column.
        """
        ws = sheet or self.active_sheet
        column_index = self._get_column_index(column)
        column_content = ws.get_used_range().get_column(column_index)
        values = [value[0] for value in column_content.text]
        return values

    def remove_column(self, column: str, sheet: WorkSheet = None):
        """
        Remove a single column from the worksheet.

        Args:
            column (str): The letter-indexed column name ('a', 'A', 'AA').
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        self.remove_columns(columns=[column], sheet=sheet)

    def remove_columns(self, columns: List[str], sheet: WorkSheet = None):
        """
        Remove columns from the sheet.

        Args:
            columns (List[str]): A list of the letter-indexed names of the columns to be removed.
            sheet (Worksheet, optional): If a worksheet is provided, it'll be used
                by this method instead of the active_sheet. Defaults to None.
        """
        ws = sheet or self.active_sheet
        content = ws.get_used_range()

        columns.sort(reverse=True)
        for col in columns:
            column_index = self._get_column_index(col)
            column_content = content.get_column(column_index)
            column_content.delete('left')

    def _get_column_name(self, column_index: int):
        name = chr(65 + column_index % 26)

        column_index //= 26
        while column_index > 0:
            name = chr(65 + (column_index - 1) % 26) + name
            column_index //= 26
        return name

    def _get_column_index(self, column_name: str):
        place = 0
        number = 0
        column_name = column_name.upper()

        for letter in reversed(column_name):
            number += (ord(letter) - ord('A') + 1) * (26 ** place)
            place += 1
        return number - 1

    def _format_row_values(self, row_content: List[object]):
        if all('' == cell for cell in row_content):
            return []
        return row_content

    def _format_values(self, content: List[List[object]]):
        values = []
        for row in content:
            values.append(self._format_row_values(row))
        if all([] == row for row in values):
            return []
        return values
