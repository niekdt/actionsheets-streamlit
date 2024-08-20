import itertools
from os import path
from typing import Literal

import streamlit as st
import polars as pl
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container
from importlib.metadata import version

from data import get_all_sheets
from sidebar import sheet_toc
from views.home_view import generate_landing_view
from views.sheet_view import generate_sheet_view, generate_filtered_sheet_view
from views.sheets_view import generate_sheets_results
from views.structure_view import generate_structure_view

st.set_page_config(
    page_title='Actionsheets',
    page_icon='📄',
    initial_sidebar_state='expanded',
    layout='wide'
)

print('\n== INIT APP ==')
active_lang: str = 'Python'
active_sheet_id: str = ''
active_view: Literal[
    'home',
    'sheets', 'sheets_result',
    'sheet', 'sheet_result',
] = 'home'
static = st.session_state['static'] if 'static' in st.session_state else False
print('STATIC: ', static)

if 'lang' not in st.session_state:
    # new session; set default language
    st.session_state['lang'] = active_lang
    st.session_state['view'] = active_view
    static = True
else:
    active_lang = st.session_state['lang']
    active_view = st.session_state['view']

if 'sheet' not in st.session_state:
    st.session_state['sheet'] = ''
else:
    active_sheet_id = st.session_state['sheet']

print(f'\tView: {active_view}')
print(f'\tLang: {active_lang}')
print(f'\tSheet: {active_sheet_id}')

sheets = get_all_sheets()

# Import CSS file
with open(path.join('.streamlit', 'style.css')) as f:
    st.sidebar.html(f'<style>{f.read()}</style><div id="top"/>')

# Sidebar
with st.sidebar:
    def on_click_home():
        st.session_state['view'] = 'home'
        st.session_state['static'] = True

    def on_click_struct():
        st.session_state['view'] = 'struct'
        st.session_state['static'] = True


    with stylable_container(
            key='home',
            css_styles=[
                'div {float: left; width: 100%; text-align: left;}',
                'button {border-style: none; background-color: transparent; float:left;}',
                'button:hover {color: inherit}',
                'button:focus {color: inherit}',
                'p {font-size: 24pt; font-weight: bold;}'
            ]
    ):
        st.button(
            label='Actionsheets',
            use_container_width=True,
            on_click=on_click_home
        )

    with stylable_container(
            key='nav',
            css_styles=[
                'div {float: left; width: 100%; text-align: left; gap: 0;}',
                'button {border-style: none; background-color: transparent; float:left;}',
                'button:hover {background-color: gray; color: inherit;}',
                'button:focus {background-color: gray; color: inherit}'
            ]
    ):
        with st.container():
            st.button(
                key='home_nav',
                label='🏠 Home',
                on_click=on_click_home,
                use_container_width=True
            )

            st.button(
                key='struc_nav',
                label='📄 Sheet structure',
                on_click=on_click_struct,
                use_container_width=True
            )

    sac.divider('Programming language', color='blue', size='xl')


    def on_select_language():
        lang = st.session_state['lang_select']
        print('CHANGE TO LANGUAGE: ', lang)
        st.session_state['lang'] = lang
        st.session_state['view'] = 'sheet'  # TODO: implement "sheets" view
        st.session_state['sheet'] = lang.lower()
        st.session_state['search_sheet'] = ''


    langs = sorted(sheets.sheets_data.filter(pl.col('sheet_parent') == '')['title'])
    st.selectbox(
        key='lang_select',
        label='Programming language',
        placeholder='Select proglang',
        index=0,
        options=langs,
        label_visibility='collapsed',
        on_change=on_select_language
    )

with st.sidebar:
    def on_quicksearch():
        query = st.session_state['quick_search']
        print('QUICK SEARCH query: ', query)
        search_results = sheets.filter(active_lang.lower()).find_snippets(query)

        st.session_state['view'] = 'sheets_result'

        if search_results.count_snippets() > 0:
            st.session_state['quick_search'] = ''
            st.session_state['filtered_sheets_data'] = search_results
        else:
            st.warning('No sheets found')
            if 'filtered_sheets_data' not in st.session_state:
                del st.session_state['filtered_sheets_data']


    st.text_input(
        key='quick_search',
        label='Search all',
        placeholder='Quick snippet search',
        label_visibility='collapsed',
        on_change=on_quicksearch
    )

    sac.divider(label='Actionsheets', color='green', size='lg')


    def on_search_sheet():
        query = st.session_state['search_sheet']
        print('SEARCH SHEET FOR QUERY: ', query)
        sheet_id = sheets.filter(active_lang.lower()).find_sheet(query=query)

        print('RESULT: ', sheet_id)
        st.session_state['view'] = 'sheet'
        st.session_state['static'] = True

        if sheet_id:
            st.session_state['sheet'] = sheet_id
            st.session_state['actionsheets_menu'] = sheet_id
            st.session_state['search_sheet'] = ''
        else:
            st.session_state['view'] = 'sheets_result'


    st.text_input(
        key='search_sheet',
        label='Search sheet',
        placeholder='Search sheet',
        label_visibility='collapsed',
        on_change=on_search_sheet
    )

    def get_child_sheets(id: str) -> list[str]:
        return sheets.sheets_data.filter(
            pl.col('sheet_parent') == id
        ).sort('rank')['sheet'].to_list()

    def get_nested_child_sheets(id: str) -> list[str]:
        # get children in sorted order
        child_ids = get_child_sheets(id)

        ids = list()
        ids.append(id)
        for child_id in child_ids:
            ids += get_nested_child_sheets(child_id)
        return ids

    sheet_ids = get_nested_child_sheets(active_lang.lower())

    df_sheet = pl.DataFrame(pl.Series('sheet', sheet_ids))

    sheets_data = df_sheet.join(sheets.sheets_data, on='sheet', how='left')

    def on_select_sheet(id: str):
        print('OPEN SHEET: ', id)
        st.session_state['view'] = 'sheet'
        st.session_state['sheet'] = id

    with stylable_container(
            key='sheets_menu',
            css_styles=[
                'div {float: left; width: 100%; text-align: left; gap: 0;}',
                '''button {
                    border-style: none; 
                    background-color: transparent; 
                    color: var(--sheet-color); 
                    float:left; 
                    min-height: 0; 
                    padding: 0; 
                    margin: -2px; 
                    padding-left: 5px;
                }''',
                'button:hover {background-color: gray; color: inherit;}',
                'button:focus {background-color: gray; color: inherit}'
            ]
    ):
        with st.container():
            for sheet, title, depth in zip(
                    sheets_data['sheet'], sheets_data['title'], sheets_data['depth']
            ):
                st.button(
                    key=f'sheet_{sheet}',
                    label='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' * (depth - 1) + ('▫️' if depth > 0 else '') + title,
                    use_container_width=True,
                    on_click=on_select_sheet,
                    args=(sheet,)
                )

has_sheet = sheets.has_sheet(active_sheet_id)

with st.sidebar:
    sac.divider(label='Actionsheet sections', color='yellow', size='md')

    def on_search_snippet():
        print('SEARCH SNIPPET')
        query = st.session_state['search_snippet']

        active_sheet = sheets.sheet_view(active_sheet_id)
        snippets = active_sheet.find_snippets(query=query)['entry'].to_list()

        if snippets:
            search_view = active_sheet.filter(snippets)

            st.session_state['view'] = 'sheet_result'
            st.session_state['search_snippet'] = ''
            st.session_state['filtered_sheet_data'] = search_view
        else:
            st.warning('No snippets found')
            if 'filtered_sheet_data' in st.session_state:
                del st.session_state['filtered_sheet_data']


    st.text_input(
        key='search_snippet',
        label='Search snippets',
        placeholder='Search snippet',
        label_visibility='collapsed',
        disabled=not has_sheet,
        on_change=on_search_snippet
    )

    if sheets.has_sheet(active_sheet_id):
        sheet_toc(
            sheet=sheets.sheet_view(active_sheet_id),
            parent_section=''
        )

    sac.menu(
        items=[
            sac.MenuItem(type='divider'),
            sac.MenuItem(
                label='Actionsheets package',
                disabled=True,
                tag=sac.Tag(
                    label=f'v{version("actionsheets")}',
                    link=f'https://github.com/niekdt/actionsheets/releases/tag/v{version("actionsheets")}'
                ),
            ),
            sac.MenuItem('Github', icon='github', href='https://github.com/niekdt/actionsheets'),
            sac.MenuItem(
                label='Submit an issue / snippet',
                icon='question-circle',
                href='https://github.com/niekdt/actionsheets/issues'
            ),
            sac.MenuItem('Streamlit actionsheets app', disabled=True),
            sac.MenuItem('Github', icon='github',
                         href='https://github.com/niekdt/actionsheets-streamlit'),
            sac.MenuItem(
                label='Submit an issue',
                icon='question-circle',
                href='https://github.com/niekdt/actionsheets/issues'
            ),
            sac.MenuItem('Copyright © 2024 Niek Den Teuling', disabled=True)
        ],
        size='xs',
        indent=10
    )

if active_view:
    if active_view == 'home':
        generate_landing_view()
    elif active_view == 'struct':
        generate_structure_view()
    elif active_view == 'sheet':
        if has_sheet:
            generate_sheet_view()
        else:
            sac.result(label=f'Sheet "{active_sheet_id}" is undefined', status='error')
    elif active_view == 'sheet_result':
        if has_sheet:
            generate_filtered_sheet_view()
        else:
            sac.result(label=f'Sheet "{active_sheet_id}" is undefined', status='error')
    elif active_view == 'sheets_result':
        generate_sheets_results()
    else:
        sac.result(label=f'undefined view: {active_view}', status='error')
else:
    sac.result(label=f'no defined view', status='error')

st.session_state['static'] = False
