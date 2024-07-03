from os import path

import streamlit as st

import polars as pl
import streamlit_antd_components as sac

from data import get_all_sheets
from sidebar import generate_actionsheets_tree_items, generate_actionsheets_tree_lookup
from views.landing import generate_landing_view

st.set_page_config(
    page_title='Actionsheets',
    page_icon='🧪',
    initial_sidebar_state='expanded',
    layout='wide'
)

if 'lang' not in st.session_state:
    st.session_state.lang = 'Python'

if 'sheet_id' not in st.session_state:
    st.session_state.sheet_id = ''

sheets = get_all_sheets()

# Import CSS file
with open(path.join('.streamlit', 'style.css')) as f:
    st.sidebar.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

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

    if st.session_state.sheet_id in sheets.sheets_data['sheet_id']:
        sheet_name = sheets.sheet_info(st.session_state.sheet_id)['title']
    else:
        sheet_name = 'UNDEFINED'

    sac.divider(f'{sheet_name} sections', color='yellow', icon='code', size='md')
    sac.tree(items=[
        sac.TreeItem('Create', children=[
            sac.TreeItem('datetime'),
            sac.TreeItem('numeric'),
            sac.TreeItem('str'),
        ], tooltip='item tooltip'),
        sac.TreeItem('Test', children=[
            sac.TreeItem('tuple'),
            sac.TreeItem('list'),
            sac.TreeItem('dict'),
        ]),
        sac.TreeItem('Extract'),
        sac.TreeItem('Update'),
        sac.TreeItem('Derive'),
        sac.TreeItem('Convert'),
    ], label='', index=-1, size='sm', color='yellow', show_line=False, return_index=True)

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
        sac.MenuItem('Github', icon='github', href='https://github.com/niekdt/actionsheets-streamlit'),
        sac.MenuItem(
            label='Submit an issue',
            icon='question-circle',
            href='https://github.com/niekdt/actionsheets/issues'
        ),
        sac.MenuItem('Copyright © 2024 Niek Den Teuling', disabled=True)
    ], size='xs', indent=10)

if 'new' not in st.session_state:
    generate_landing_view()