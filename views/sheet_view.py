import polars as pl
import streamlit as st
import streamlit_antd_components as sac
from actionsheets.sheet import ActionsheetView
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from streamlit_extras.row import row
from streamlit_extras.stylable_container import stylable_container

from data import get_sheet_info, get_sheet
from sidebar import sheet_toc

formatter = HtmlFormatter(style='monokai', linenos=False)


def generate_sheet_view():
    sheet_data = get_sheet(st.session_state['sheet'])

    _init()
    _generate_sheet_header(sheet_data)
    _generate_sections(sheet_data, section='')


def generate_filtered_sheet_view():
    if 'filtered_sheet_data' not in st.session_state:
        sac.result(
            label=f'No filtered sheet data for sheet {st.session_state["sheet"]}',
            status='error'
        )
    all_sheet_data: ActionsheetView = get_sheet(st.session_state['sheet'])
    sheet_data: ActionsheetView = st.session_state['filtered_sheet_data']
    assert type(sheet_data) is ActionsheetView

    _init()
    _generate_sheet_header(sheet_data)

    if sheet_data.data.height:
        _generate_sections(sheet_data, section='')
    else:
        sac.result(label=f'No snippets found', status='warning')


def _init():
    st.html('<style>' + formatter.get_style_defs('.highlight') + '</style>')


def _generate_sheet_header(sheet_data: ActionsheetView):
    sheet_info = get_sheet_info(st.session_state['sheet'])
    sheet_path = sheet_info['sheet'].split(sep='.')
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
            sheet=sheet_data,
            parent_section=''
        )


def _generate_sections(view: ActionsheetView, section: str):
    for section_id in view.entries(type='section', parent=section, nested=False):
        _generate_section(view, section=section_id)


def _generate_section(view: ActionsheetView, section: str):
    info = view.section_info(section=section)

    depth = section.count('.')
    h = 2 + depth if depth < 6 else 6

    st.html(f'<h{h} class="section"><a id={section}></a> {info["title"]} </h2>')
    if info['description']:
        st.markdown(info['description'])

    _generate_section_snippets(view, section)

    # Render subsections
    _generate_sections(view, section=section)


def _generate_section_snippets(view: ActionsheetView, section: str):
    data = view.section_snippets(section=section)
    if data.height:
        return _generate_snippets(data)


def _generate_snippets(data: pl.DataFrame):
    assert data.height > 0

    lexer = get_lexer_by_name('Python')

    def html_code(code) -> str:
        return highlight(code, lexer, formatter)

    pretty_data = data.select(
        pl.col('title').alias('Action'),
        pl.col('code').alias('Code'),
        pl.col('details').alias('Details')
    ).with_columns(
        pl.col('Code').map_elements(html_code, return_dtype=pl.String)
    )

    st.html(
        pretty_data.to_pandas().to_markdown(index=False, tablefmt='unsafehtml')
    )
