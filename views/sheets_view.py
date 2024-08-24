import polars as pl
import streamlit as st
import streamlit_antd_components as sac
from actionsheets.sheets import Actionsheets

from events import on_quicksearch
from views.sheet_view import _generate_snippets, _init


def generate_sheets_results():
    st.text_input(
        key='quick_search3',
        label='Search all',
        placeholder=f'Quick search for {st.session_state["lang"]} snippets',
        label_visibility='collapsed',
        on_change=on_quicksearch,
        args=('quick_search3',)
    )

    st.title('Quick search results')
    results: Actionsheets = st.session_state['filtered_sheets_data']
    query = st.session_state["last_quick_search"]

    if results.count_snippets() == 0:
        sac.result(
            label=f'No results for query<br>"{query}"',
            status='warning'
        )
        return

    st.markdown(f'Query: "{query}"')

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
