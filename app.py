from os import path
from typing import Literal

import streamlit as st

import polars as pl
import streamlit_antd_components as sac
from streamlit_antd_components import MenuItem
from streamlit_extras.stylable_container import stylable_container

from data import get_all_sheets
from sidebar import generate_actionsheets_items, sheet_toc, get_sheet_title
from views.home_view import generate_landing_view
from views.sheet_view import generate_sheet_view, generate_filtered_sheet_view
from views.sheets_view import generate_sheets_results

print('\n== INIT APP ==')
active_lang: str = 'Python'
active_sheet_id: str = ''
active_view: Literal[
    'home',
    'sheets', 'sheets_result',
    'sheet', 'sheet_result',
] = 'home'
static = st.session_state['static'] if 'static' in st.session_state else False

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


    with stylable_container(
            key='home',
            css_styles=[
                'div {float: left; width: 100%; text-align: left;}',
                'button {border-style: none; background-color: transparent; float:left;}',
                'button:hover {color: inherit}',
                'p {font-size: 24pt; font-weight: bold;}'
            ]
    ):
        st.button(
            label='Actionsheets',
            use_container_width=True,
            on_click=on_click_home
        )

    sac.divider('Programming language', color='blue', size='xl')


    def on_select_language():
        lang = st.session_state['lang_select']
        print('CHANGE TO LANGUAGE: ', lang)
        st.session_state['lang'] = lang
        st.session_state['view'] = 'sheets'
        st.session_state['sheet'] = ''
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
        search_results = sheets.find_snippets(query)

        st.session_state['view'] = 'sheets_result'

        if search_results.count_snippets() > 0:
            st.session_state['quick_search'] = ''
            st.session_state['filtered_sheets_data'] = search_results
        else:
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
        sheet_id = sheets.find_sheet(query=query)

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

    sheet_items = list(generate_actionsheets_items(active_lang.lower()))

    def get_menu_ids(items: list[MenuItem]) -> list[str]:
        for item in items:
            yield item.label
            if item.children:
                yield from get_menu_ids(item.children)


    sheet_item_ids = list(get_menu_ids(sheet_items))
    active_sheet_index = sheet_item_ids.index(active_sheet_id) if \
        active_sheet_id and active_sheet_id in sheet_item_ids else 0

    if 'actionsheets_menu' in st.session_state and \
            st.session_state['actionsheets_menu'] not in sheet_item_ids:
        st.session_state['actionsheets_menu'] = sheet_item_ids[0]

    # NOTE: sac.menu callback doesn't work
    # NOTE: an item must be selected, otherwise the component does not expand correctly
    # NOTE: changing the index causes complete reloading of the component, so use sparingly!
    # NOTE: don't use st.rerun(), as it causes random reload/selection issues
    actionsheets_menu = sac.menu(
        key='actionsheets_menu',
        items=sheet_items,
        index=0,
        indent=10,
        open_all=False,
        size='sm',
        color='green',
        format_func=get_sheet_title
    )

    if not static and (not active_sheet_id or active_sheet_id != actionsheets_menu):
        print('SHEET MENU SELECTION: ', actionsheets_menu)
        active_sheet_id = actionsheets_menu
        active_view = 'sheet'
        st.session_state['view'] = 'sheet'
        st.session_state['sheet'] = active_sheet_id

has_sheet = sheets.has_sheet(active_sheet_id)

with (st.sidebar):
    sac.divider(label='Actionsheet sections', color='yellow', size='md')

    def on_search_snippet():
        print('SEARCH SNIPPET')
        query = st.session_state['search_snippet']

        active_sheet = sheets.sheet_view(active_sheet_id)
        snippets = active_sheet.find_snippets(query=query)['entry'].to_list()

        if snippets:
            search_view = active_sheet.filter_view(snippets)

            st.session_state['view'] = 'sheet_result'
            st.session_state['search_snippet'] = ''
            st.session_state['filtered_sheet_data'] = search_view
        else:
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
            sac.MenuItem('Actionsheets package', disabled=True),
            sac.MenuItem('Github', icon='github', href='https://github.com/niekdt/actionsheets'),
            sac.MenuItem(
                label='Submit an issue / snippet',
                icon='question-circle',
                href='https://github.com/niekdt/actionsheets/issues'
            ),
            sac.MenuItem('Streamlit website', disabled=True),
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
