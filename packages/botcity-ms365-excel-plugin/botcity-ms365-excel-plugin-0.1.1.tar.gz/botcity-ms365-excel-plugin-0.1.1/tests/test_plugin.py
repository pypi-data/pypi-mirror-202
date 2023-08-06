import pytest
from botcity.plugins.ms365.excel import MS365ExcelPlugin
from O365.excel import WorkBook, WorkSheet


reference = [
    ['Name', 'Mana', 'Price', 'Mana/Price', 'Where to Buy'],
    ['Small Mana Potion', '150', '4', '37.5', 'Ginkgo'],
    ['Strong Mana Potion', '300', '12', '25', 'Bicheon'],
    ['Great Mana Potion', '600', '36', '16.66666667', 'Snake Pit']
]


def test_get_excel_file(bot: MS365ExcelPlugin):
    bot.get_excel_file(file_or_path="/Test-Plugin.xlsx")
    assert isinstance(bot.excel_file, WorkBook)
    assert isinstance(bot.active_sheet, WorkSheet)


@pytest.mark.depends(name="test_get_excel_file")
def test_create_sheet(bot: MS365ExcelPlugin):
    try:
        bot.remove_sheet("New Sheet")
    except:
        pass

    bot.create_sheet("New Sheet")
    created_sheet = bot.get_worksheet("New Sheet")
    assert isinstance(created_sheet, WorkSheet)


@pytest.mark.depends(name="test_create_sheet")
def test_add_row(bot: MS365ExcelPlugin):
    bot.set_active_sheet("New Sheet")
    bot.clear()
    assert bot.as_list() == []

    for row in reference:
        bot.add_row(row_values=row[:3])
    assert bot.as_list() == [row[:3] for row in reference]


@pytest.mark.depends(name="test_add_row")
def test_add_column(bot: MS365ExcelPlugin):
    bot.add_column(column_values=[row[3] for row in reference])
    bot.add_column(column_values=[row[4] for row in reference])
    assert bot.as_list() == reference


@pytest.mark.depends(name="test_add_column")
def test_get_values(bot: MS365ExcelPlugin):
    assert bot.get_cell(column="D", row=3) == "25"
    assert bot.get_row(row=3) == reference[2]
    assert bot.get_column(column="C") == [row[2] for row in reference]
    assert bot.get_range(range_="B2:C4") == [row[1:3] for row in reference[1:4]]


def test_set_values(bot: MS365ExcelPlugin):
    bot.clear()
    bot.set_range(range_="A1:E4", values=reference)
    assert bot.as_list() == reference

    bot.set_cell(column="F", row=1, value="Level")
    assert bot.get_cell(column="F", row=1) == "Level"


@pytest.mark.depends(name="test_set_values")
def test_remove_values(bot: MS365ExcelPlugin):
    bot.set_active_sheet("New Sheet")
    bot.clear(range_="A1:C1")
    assert bot.get_row(row=1) == ['', '', '', 'Mana/Price', 'Where to Buy', 'Level']

    bot.remove_row(row=1)
    assert bot.as_list() == reference[1:]

    bot.remove_rows(rows=[1, 2])
    assert bot.as_list() == [reference[3]]

    bot.remove_column(column="A")
    assert bot.as_list() == [reference[3][1:]]

    bot.remove_columns(columns=["C", "D"])
    assert bot.as_list() == [reference[3][1:3]]

    bot.clear(only_values=False)
    assert bot.as_list() == []


def test_list_sheets(bot: MS365ExcelPlugin):
    sheets = bot.list_sheets()
    bot.active_sheet = sheets[-1]
    assert len(sheets) == 2

    bot.remove_sheet("New Sheet")
    sheets = bot.list_sheets()
    assert len(sheets) == 1
