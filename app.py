from os import path

import streamlit as st

import polars as pl
import streamlit_antd_components as sac
from streamlit_extras.stylable_container import stylable_container

from data import get_all_sheets, get_active_sheet_id
from sidebar import generate_actionsheets_items, sheet_toc, get_sheet_title
from views.home_view import generate_landing_view
from views.sheet_view import generate_sheet_view

if 'lang' not in st.session_state:
    st.session_state.lang = 'Python'

if 'sheet_id' not in st.session_state:
    st.session_state.sheet_id = ''

sheets = get_all_sheets()

# Import CSS file
with open(path.join('.streamlit', 'style.css')) as f:
    st.sidebar.html(f'<style>{f.read()}</style>')

freeze = False

# Sidebar
with st.sidebar:
    with stylable_container(
            key='home',
            css_styles=[
                'div {float: left; width: 100%; text-align: left;}',
                'button {border-style: none; background-color: transparent; float:left;}',
                'button:hover {color: inherit}',
                'p {font-size: 24pt; font-weight: bold;}'
            ]
    ):
        home_button = st.button('Actionsheets', use_container_width=True)

    if home_button:
        st.session_state.sheet_id = ''

    sac.divider('Programming language', color='blue', size='xl')
    langs = sorted(sheets.sheets_data.filter(pl.col('sheet_parent') == '')['title'])

    lang_select = st.selectbox(
        key='lang_select',
        label='Programming language',
        placeholder='Select proglang',
        index=langs.index(st.session_state.lang),
        options=langs,
        label_visibility='collapsed'
    )

    print(lang_select)
    if not home_button and lang_select and st.session_state.lang != lang_select:
        print('SELECT LANG')
        st.session_state.lang = lang_select
        st.session_state.sheet_id = ''
        freeze = True


with st.sidebar:
    general_search = st.text_input(
        label='Search all',
        placeholder='Quick search',
        label_visibility='collapsed',
        disabled=True
    )

    sac.divider(f'{lang_select} actionsheets', color='green', size='lg')
    actionsheets_menu = sac.menu(
        items=generate_actionsheets_items(st.session_state.lang),
        index=0,  # an item must be selected, otherwise the component does not expand correctly
        indent=10,
        open_all=False,
        size='sm',
        color='green',
        format_func=get_sheet_title
    )

    if not home_button and len(actionsheets_menu) > 0:
        if actionsheets_menu in sheets.sheets_data['sheet_id']:
            st.session_state.sheet_id = actionsheets_menu

        print(f'Selected sheet: {st.session_state.sheet_id}')

    search_sheet = st.text_input(
        label='Search sheet',
        placeholder='Search sheet',
        label_visibility='collapsed',
        disabled=True
    )


if get_active_sheet_id() in sheets.sheets_data['sheet_id']:
    print('Show sheet')
    sheet_name = sheets.sheet_info(st.session_state.sheet_id)['title']
    generate_sheet_view(get_active_sheet_id())
elif len(get_active_sheet_id()) > 0:
    sheet_name = ''
    sac.result('Not found')
else:
    sheet_name = ''
    generate_landing_view()

with st.sidebar:
    sac.divider(
        f'{sheet_name} sections' if sheet_name else 'Sections',
        color='yellow',
        size='md'
    )

    if len(get_active_sheet_id()) > 0:
        sheet_toc(
            sheet=sheets.sheet_view(id=get_active_sheet_id()),
            parent_section=''
        )

    search_snippet = st.text_input(
        label='Search snippet',
        placeholder='Search snippet',
        label_visibility='collapsed',
        disabled=True
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
