from os import path

import streamlit as st

import polars as pl
import streamlit_antd_components as sac

from data import get_all_sheets, get_active_sheet_id
from sidebar import generate_actionsheets_tree_items, generate_actionsheets_tree_lookup, sheet_toc
from views.landing import generate_landing_view
from views.sheet import generate_sheet_view

if 'lang' not in st.session_state:
    st.session_state.lang = 'Python'

if 'sheet_id' not in st.session_state:
    st.session_state.sheet_id = ''

sheets = get_all_sheets()

# Import CSS file
with open(path.join('.streamlit', 'style.css')) as f:
    st.sidebar.html(f'<style>{f.read()}</style>')

# Sidebar
with st.sidebar:
    st.title('Actionsheets')

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

    if lang_select:
        st.session_state.lang = lang_select
        st.session_state.sheet_id = ''

    general_search = st.text_input(
        label='Search all',
        placeholder='Quick search',
        label_visibility='collapsed',
        disabled=True
    )

    sac.divider(f'{lang_select} actionsheets', color='green', size='lg')
    actionsheets_tree_lookup = generate_actionsheets_tree_lookup(st.session_state.lang)
    actionsheets_tree = sac.tree(
        items=generate_actionsheets_tree_items(st.session_state.lang),
        label='',
        index=-1,
        open_all=True,
        size='sm',
        color='green',
        show_line=False,
        return_index=True
    )

    if len(actionsheets_tree_lookup) > 0 and type(actionsheets_tree) is int:
        if actionsheets_tree == -1:
            st.session_state.sheet_id = st.session_state.lang.lower()
        else:
            st.session_state.sheet_id = actionsheets_tree_lookup[actionsheets_tree]

        print(f'Selected index: {actionsheets_tree}, sheet id: {st.session_state.sheet_id}')

    search_sheet = st.text_input(
        label='Search sheet',
        placeholder='Search sheet',
        label_visibility='collapsed',
        disabled=True
    )


if get_active_sheet_id() in sheets.sheets_data['sheet_id']:
    sheet_name = sheets.sheet_info(st.session_state.sheet_id)['title']
    generate_sheet_view(get_active_sheet_id())
else:
    sheet_name = ''
    generate_landing_view()

with st.sidebar:
    sac.divider(
        f'{sheet_name} sections' if sheet_name else 'Sections',
        color='yellow',
        size='md'
    )

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

    sac.menu(items=[
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
    ], size='xs', indent=10)
