from actionsheets.sheet import ActionsheetView
import streamlit as st
from streamlit_antd_components import MenuItem

from data import get_all_sheets

all_sheets = get_all_sheets()


def generate_actionsheets_items(parent: str) -> list[MenuItem]:
    sheet_info = all_sheets.sheet_info(sheet=parent)
    show_sheet = (not sheet_info['sheet_parent']
                  or sheet_info['description']
                  or all_sheets.sheet_view(parent).snippets().height)
    if show_sheet:
        yield MenuItem(label=parent, icon='journal-code')

    ids = all_sheets.sheets(parent=parent.lower(), nested=False)
    for id in ids:
        child_ids = all_sheets.sheets(parent=id, nested=False)
        if child_ids:
            child_items = list(generate_actionsheets_items(id))
            yield MenuItem(label=id.upper(), children=child_items)
        else:
            yield MenuItem(label=id, icon='file-earmark-code')


def get_sheet_title(section: str) -> str:
    if section:
        return all_sheets.sheet_info(sheet=section.lower())['title']
    else:
        return ''


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
