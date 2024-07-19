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
from views.sheet_view import generate_sheet_view

print('\n== INIT APP ==')
active_lang: str = 'Python'
active_sheet_id: str = ''
active_view: Literal['', 'home', 'sheets', 'sheet', 'snippets'] = 'home'

if 'lang' not in st.session_state:
    # new session; set default language
    st.session_state.lang = active_lang
    st.session_state.view = active_view
else:
    active_lang = st.session_state.lang
    active_view = st.session_state.view

if 'sheet_id' not in st.session_state:
    st.session_state.sheet_id = ''
else:
    active_sheet_id = st.session_state.sheet_id

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
        st.session_state.view = 'home'


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
        st.session_state.lang = lang
        st.session_state.view = 'sheets'
        st.session_state.sheet_id = ''
        st.session_state.search_sheet = ''


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
    st.text_input(
        label='Search all',
        placeholder='Quick snippet search',
        label_visibility='collapsed',
        disabled=True
    )

    sac.divider(f'{active_lang} actionsheets', color='green', size='lg')


    def on_search_sheet():
        query = st.session_state.search_sheet
        print('SEARCH SHEET FOR QUERY: ', query)
        sheet_id = sheets.find_sheet(query=query)
        print('RESULT: ', sheet_id)
        st.session_state.sheet_id = sheet_id
        st.session_state['actionsheets_menu'] = sheet_id


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

    if st.session_state['actionsheets_menu'] not in sheet_item_ids:
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

    if not active_sheet_id or active_sheet_id != actionsheets_menu:
        print('SHEET MENU SELECTION: ', actionsheets_menu)
        active_sheet_id = actionsheets_menu
        active_view = 'sheets'
        st.session_state.view = 'sheet'
        st.session_state.sheet_id = active_sheet_id

if active_view:
    if active_view == 'home':
        generate_landing_view()
    elif active_view == 'sheets' or active_view == 'sheet':
        if sheets.has_sheet(active_sheet_id):
            generate_sheet_view(active_sheet_id)
        else:
            sac.result(label=f'Sheet "{active_sheet_id}" is undefined', status='error')
    else:
        sac.result(label=f'undefined view: {active_view}', status='error')
else:
    sac.result(label=f'no defined view', status='error')

with (st.sidebar):
    sheet_name = sheets.sheet_info(active_sheet_id)['title'] if \
        sheets.has_sheet(active_sheet_id) else ''

    sac.divider(
        f'{sheet_name} sections' if sheet_name else 'Sections',
        color='yellow',
        size='md'
    )

    st.text_input(
        label='Search snippet',
        placeholder='Search snippet',
        label_visibility='collapsed',
        disabled=True
    )

    if sheets.has_sheet(active_sheet_id):
        sheet_toc(
            sheet=sheets.sheet_view(id=active_sheet_id),
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
