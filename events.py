import streamlit as st

from data import get_all_sheets

sheets = get_all_sheets()


def on_click_home():
    st.session_state['view'] = 'home'
    st.session_state['static'] = True


def on_click_struct():
    st.session_state['view'] = 'struct'
    st.session_state['static'] = True


def on_select_language():
    lang = st.session_state['lang_select']
    print('CHANGE TO LANGUAGE: ', lang)
    st.session_state['lang'] = lang
    st.session_state['view'] = 'sheet'  # TODO: implement "sheets" view
    st.session_state['sheet'] = lang.lower()
    st.session_state['search_sheet'] = ''


def on_select_sheet(id: str):
    print('OPEN SHEET: ', id)
    st.session_state['view'] = 'sheet'
    st.session_state['sheet'] = id


def on_quicksearch():
    query = st.session_state['quick_search']
    print('QUICK SEARCH query: ', query)
    search_results = sheets.filter(st.session_state['lang'].lower()).find_snippets(query)

    st.session_state['view'] = 'sheets_result'

    if search_results.count_snippets() > 0:
        st.session_state['quick_search'] = ''
        st.session_state['filtered_sheets_data'] = search_results
    else:
        st.warning('No sheets found')
        if 'filtered_sheets_data' not in st.session_state:
            del st.session_state['filtered_sheets_data']


def on_search_sheet():
    query = st.session_state['search_sheet']
    print('SEARCH SHEET FOR QUERY: ', query)
    sheet_id = sheets.filter(st.session_state['lang'].lower()).find_sheet(query=query)

    print('RESULT: ', sheet_id)
    st.session_state['view'] = 'sheet'
    st.session_state['static'] = True

    if sheet_id:
        st.session_state['sheet'] = sheet_id
        st.session_state['actionsheets_menu'] = sheet_id
        st.session_state['search_sheet'] = ''
    else:
        st.session_state['view'] = 'sheets_result'


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
