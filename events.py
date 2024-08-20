import streamlit as st

from data import get_all_sheets

sheets = get_all_sheets()


def on_select_sheet(id: str):
    print('OPEN SHEET: ', id)
    st.session_state['view'] = 'sheet'
    st.session_state['sheet'] = id


def on_clear_snippet_search():
    on_select_sheet(st.session_state['sheet'])


def on_search_snippet(key: str = 'search_snippet'):
    query = st.session_state[key]
    print(f'SEARCH SNIPPET: "{query}"')
    if not query:
        on_clear_snippet_search()
        return

    st.session_state['last_search_snippet'] = query

    active_sheet = sheets.sheet_view(st.session_state['sheet'])
    snippets = active_sheet.find_snippets(query=query)['entry'].to_list()

    if snippets:
        search_view = active_sheet.filter(snippets)

        st.session_state['view'] = 'sheet_result'
        st.session_state['search_snippet'] = ''
        st.session_state['search_snippet2'] = ''
        st.session_state['filtered_sheet_data'] = search_view
    else:
        st.warning(f'No snippets found for query "{query}"')
        if 'filtered_sheet_data' in st.session_state:
            del st.session_state['filtered_sheet_data']
        on_clear_snippet_search()
