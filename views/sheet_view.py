import polars as pl
import streamlit as st
from actionsheets.sheet import ActionsheetView
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from streamlit_extras.row import row
from streamlit_extras.stylable_container import stylable_container

from data import get_sheet, get_sheet_info, get_all_sheets
from sidebar import sheet_toc

formatter = HtmlFormatter(style='monokai', linenos=False)


def generate_sheet_view(sheet_id: str):
    st.html('<style>' + formatter.get_style_defs('.highlight') + '</style>')

    sheet_info = get_sheet_info(sheet_id)
    sheet = get_sheet(sheet_id)

    sheet_path = sheet_id.split(sep='.')
    if len(sheet_path) > 1:
        del sheet_path[-1]
    lang_html = f'<span style="color: var(--lang-color)">{sheet_path[0]}</span>'
    sheets_path_html = (
            '<span class="sheet">' +
            '</span> › <span class="sheet">'.join(sheet_path[1:])
    )
    st.html(f'''
        <div style="margin-top: 20px; font-size: 16pt">
            {lang_html}
             › 
            {sheets_path_html}
        </div>
        <h1 class="sheet" style="padding-top: 0px;"><em>{sheet_info["title"]}</em> actionsheet</h1>
    ''')

    with stylable_container(
            key='sheet-info',
            css_styles='''
    div[data-testid="stHorizontalBlock"] {
        background-color: var(--table-color); 
        border-radius: 10px;
        padding-left: 10px;
    }
    div[data-testid="column"]:first-child {
        border-right: solid;
        border-color: var(--bg-color);
        border-width: 10px;
    } 
    '''):
        sheet_info_row = row([2, 1], vertical_align='top')

    with sheet_info_row.container():
        st.html('<h4 class="sheet">Description</h4>')
        st.markdown(sheet_info['description'])

        if 'details' in sheet_info and sheet_info['details']:
            st.html('<h4 class="sheet">Details</h4>')
            st.markdown(sheet_info['details'])

    with sheet_info_row.container():
        st.html('<h4 class="sheet">Sections</h4>')
        sheet_toc(
            sheet=get_all_sheets().sheet_view(id=sheet_id),
            parent_section=''
        )

    generate_sections(sheet, section='')


def generate_sections(view: ActionsheetView, section: str):
    for section_id in view.child_ids(section=section, type='section'):
        generate_section(view, section=section_id)


def generate_section(view: ActionsheetView, section: str):
    info = view.section_info(section=section)

    depth = section.count('.')
    h = 2 + depth if depth < 6 else 6

    st.html(f'<h{h} class="section"><a id={section}></a> {info["title"]} </h2>')
    if info['description']:
        st.markdown(info['description'])

    generate_section_snippets(view, section)

    # Render subsections
    generate_sections(view, section=section)


def generate_section_snippets(view: ActionsheetView, section: str):
    data = view.section_snippets(section=section)
    if data.height:
        return generate_snippets(data)


def generate_snippets(data: pl.DataFrame):
    assert data.height > 0

    lexer = get_lexer_by_name('Python')

    def html_code(code) -> str:
        return highlight(code, lexer, formatter)

    pretty_data = data.select(
        pl.col('title').alias('What'),
        pl.col('code').alias('Code'),
        pl.col('details').alias('Details')
    ).with_columns(
        pl.col('Code').apply(html_code, return_dtype=pl.String)
    )

    st.html(
        pretty_data.to_pandas().to_markdown(index=False, tablefmt='unsafehtml')
    )
