import polars as pl
import streamlit as st
import streamlit_antd_components as sac
from actionsheets.sheets import Actionsheets

from views.sheet_view import _generate_snippets, _init


def generate_sheets_results():
    st.title('Quick search results')

    if 'filtered_sheets_data' not in st.session_state:
        sac.result(
            label=f'No results for query<br>"{st.session_state["quick_search"]}"',
            status='warning'
        )
        return

    results: Actionsheets = st.session_state['filtered_sheets_data']

    def on_click_sheet(id):
        print('JUMP TO SHEET: ', id)
        st.session_state['view'] = 'sheet'
        st.session_state['sheet'] = id
        st.session_state['static'] = True

    _init()
    for sheet in results.sheets():
        sheet_view = results.sheet_view(sheet)
        if not sheet_view:
            continue

        with st.expander(sheet_view.info['title'], expanded=True):
            st.button(
                key=f'goto_{sheet}_button',
                label='Open sheet',
                args=[sheet],
                on_click=on_click_sheet
            )
            _generate_snippets(sheet_view.data)
