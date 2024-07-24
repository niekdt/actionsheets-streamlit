from actionsheets.sheet import ActionsheetView
from actionsheets.sheets import Actionsheets, default_sheets


def get_all_sheets() -> Actionsheets:
    return default_sheets()


def get_sheet_info(sheet: str) -> dict:
    return get_all_sheets().sheet_info(sheet)


def get_sheet(sheet: str) -> ActionsheetView:
    return get_all_sheets().sheet_view(sheet)
