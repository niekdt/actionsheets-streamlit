import streamlit as st
from actionsheets.sheet import ActionsheetView
from actionsheets.sheets import Actionsheets, default_sheets


# configure here because use of st.cache_data counts as calling streamlit before page config
st.set_page_config(
    page_title='Actionsheets',
    page_icon='🧪',
    initial_sidebar_state='expanded',
    layout='wide'
)


def get_all_sheets() -> Actionsheets:
    return default_sheets()


def get_sheet_info(sheet: str) -> dict:
    return get_all_sheets().sheet_info(sheet)


def get_sheet(sheet: str) -> ActionsheetView:
    return get_all_sheets().sheet_view(sheet)
