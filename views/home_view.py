import polars as pl
import streamlit as st
import streamlit_antd_components as sac

from streamlit_extras.grid import grid
from ui import stylable_metric
from data import get_all_sheets


def generate_landing_view():
    all_sheets = get_all_sheets()

    st.title('Actionsheets')

    all_langs = sorted(['Julia', 'Python', 'R', 'MATLAB', 'Stan'])
    langs = all_sheets.sheets_data.filter(pl.col('sheet_parent') == '')['title']

    sac.segmented(
        key='lang_segmented',
        items=[
            sac.SegmentedItem(label=lang, disabled=lang not in langs) for lang in all_langs
        ],
        label='',
        align='start',
        color='blue',
        size='xl',
        divider=False,
        index=None,  # index=all_langs.index(st.session_state.lang),
        disabled=True,
        use_container_width=True
    )

    metric_grid = grid(3)
    with metric_grid.container():
        stylable_metric(
            label='Programming languages',
            value=f'{len(all_sheets.sheets(nested=False)):,d}',
            icon=r'\e13e',
            background_color='var(--lang-color)'
        )

    with metric_grid.container():
        stylable_metric(
            label='Actionsheets',
            value=f'{all_sheets.sheets_data.height:,d}',
            icon=r'\F388',
            background_color='var(--sheet-color)'
        )

    with metric_grid.container():
        stylable_metric(
            label='Code snippets',
            value=f'{all_sheets.count_snippets():,d}',
            icon=r'\e86f',
            background_color='var(--section-color)'
        )

    st.markdown('''
    **Actionsheets** is an open-source (hobby) project with a different take on cheatsheets. 
    Standard cheatsheets are great for getting started, but don't get into the details for advanced or complex use cases.
    This is where actionsheets come in.
    
    #### Getting started
    Use the sidebar to select a programming language, and then select or search an actionsheets. 
    Sheets can be searched to generate a filtered view of code snippets.
    
    
    #### How do actionsheets differ from cheatsheets?
    - Actionsheets are expressed in terms of a desired *action* or result, and the code snippet(s) to achieve it.
      - This is a more natural way to look up code snippets. Especially useful for beginners.
    - Actions may be complex or comprise multiple steps.
      - Actions are not limited to the direct functionality provided by the package API. 
      - Cheatsheets typically lack more advanced compound use cases.
    - Code snippets are data; enabling dynamic generation of sheets depending on user queries
      - Sheets can therefore be more feature-complete, as they do not need fit on a single page.
        
    This way of organizing sheets is especially useful for packages or functions with powerful versatile functionality, where merely listing the API does not cover the full capabilities. 
    
    #### Contributing
    This website is a front-end for the [actionsheets](https://github.com/niekdt/actionsheets) package.
    Actionsheets are defined using [TOML](https://toml.io/) files. 
    This makes it very easy to define a hierarchy of code snippets in a readable way.
    
    Defining a code snippet belonging to the _Create_ section of the respective actionsheet file is as simple as:
    ```toml
    [create.list]
    action = "Define a list"
    code = "x = ['apple', 'pear', 'banana']"
    details = "You can define as many items as you like"
    ```
    
    For submitting code snippets or complete actionsheets, submit a PR to [actionsheets on Github](https://github.com/niekdt/actionsheets).
    
    #### Motivation
    My motivation for building this curated database of code snippet is out of frustration of the worsening state of the internet in quickly finding short answers to straightforward queries.
    
    - Many website have the code snippet(s) buried between tons of irrelevant text just for SEO optimization.
    - The quality of (accepted) answers on Stackoverflow is severely lacking for some programming languages:
      - Answers are out of date
      - Answers are overly complicated or inefficient (contributions by beginners)
      - For the future, this also means that the answers by any LLM are going to have the same issues. 
    - The answer on the site was for a different question
    - The answer on the site was for a more narrow question
    - With the increasing usage of LLMs, the problem of bloated low-quality answer results will only get worse.
     
    ''')

    # sac.tabs([
    #     sac.TabsItem(label='Create', tag="10"),
    #     sac.TabsItem(label='Test'),
    #     sac.TabsItem(label='Extract', icon='github'),
    #     sac.TabsItem(label='Update'),
    #     sac.TabsItem(label='Derive'),
    #     sac.TabsItem(label='Convert'),
    # ], position='right', variant='outline', use_container_width=True, return_index=True)

    # card(
    #     title="datetime",
    #     text="Some description",
    #     styles={"card": {"background-color": "blue"}},
    # )
    # card(
    #     title="str",
    #     text="Some description",
    #     styles={"card": {"background-color": "tomato"}},
    # )
