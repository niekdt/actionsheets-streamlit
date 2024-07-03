import itertools

from streamlit_antd_components import TreeItem

from data import get_all_sheets

sheets = get_all_sheets()


def generate_actionsheets_tree_items(parent: str) -> list[TreeItem]:
    ids = sheets.ids(parent_id=parent.lower())

    return [
        TreeItem(
            label=sheets.sheet_info(sheet_id)['title'],
            children=generate_actionsheets_tree_items(sheet_id)
        ) for sheet_id in ids
    ]


def generate_actionsheets_tree_lookup(parent: str) -> list[str]:
    ids = sheets.ids(parent_id=parent.lower())

    out = []
    for sheet_id in ids:
        out += [sheet_id] + generate_actionsheets_tree_lookup(sheet_id)
    return out
