from actionsheets.sheet import ActionsheetView
import streamlit as st

from data import get_all_sheets

all_sheets = get_all_sheets()


def sheet_toc(sheet: ActionsheetView, parent_section: str):
    html_content = generate_sections_list_html(sheet, parent_section=parent_section)

    st.html(f'<ul class="toc">{html_content}</ul>')


def generate_sections_list_html(sheet: ActionsheetView, parent_section: str) -> str:
    ids = sheet.entries(type='section', parent=parent_section, nested=False)

    def generate_section_entry(section: str):
        info = sheet.section_info(section)

        depth = section.count('.')

        return '''
        <li class="toc-{depth}">
            <a class="toc-{depth}" href=#{id}>{title}</a>
            <ul class="toc-{depth}">{content}</ul>
        </li>'''.format(
            id=section,
            title=info['title'],
            depth=depth,
            content=generate_sections_list_html(sheet, parent_section=section)
        )

    return ''.join(map(generate_section_entry, ids))
