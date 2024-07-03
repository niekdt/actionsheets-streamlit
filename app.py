from os import path

import streamlit as st
import polars as pl
import streamlit_antd_components as sac

from data import get_all_sheets
from views.landing import generate_landing_view

if 'config' not in st.session_state:
    st.set_page_config(
        page_title='Actionsheets',
        page_icon='🧪',
        initial_sidebar_state='expanded',
        layout='wide'
    )
    st.session_state.config = True

sheets = get_all_sheets()

# Import CSS file
with open(path.join('.streamlit', 'style.css')) as f:
    st.sidebar.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if 'new' not in st.session_state:
    generate_landing_view()

# Sidebar
with st.sidebar:
    st.title('Actionsheets')

    sac.divider('Programming language', color='blue', size='xl')
    proglang_select = st.selectbox(
        label='Programming language',
        placeholder='Select proglang',
        index=0,
        options=sorted(sheets.sheets_data.filter(pl.col('sheet_parent') == '')['title']),
        label_visibility='collapsed'
    )

    general_search = st.text_input(
        label='Search all',
        placeholder='Quick search',
        label_visibility='collapsed',
        disabled=True
    )

    sac.divider(f'{proglang_select} actionsheets', color='green', size='lg')
    sac.tree(items=[
        sac.TreeItem('Scalars', children=[
            sac.TreeItem('datetime'),
            sac.TreeItem('numeric'),
            sac.TreeItem('str'),
        ], tooltip='item tooltip'),
        sac.TreeItem('Collections', children=[
            sac.TreeItem('tuple'),
            sac.TreeItem('list'),
            sac.TreeItem('dict'),
        ]),
    ], label='', index=-1, size='md', color='green', show_line=False, return_index=True)

    search_sheet = st.text_input(
        label='Search sheet',
        placeholder='Search sheet',
        label_visibility='collapsed',
        disabled=True
    )

    sac.divider('Tuple sections', color='yellow', size='md')
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
