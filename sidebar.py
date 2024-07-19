from actionsheets.sheet import ActionsheetView
import streamlit as st
from streamlit_antd_components import MenuItem

from data import get_all_sheets

sheets = get_all_sheets()


def generate_actionsheets_items(parent: str) -> list[MenuItem]:
    sheet_info = sheets.sheet_info(id=parent)
    show_sheet = not sheet_info['sheet_parent'] or sheet_info['description'] or sheets.sheet_view(parent).snippets().height
    if show_sheet:
        yield MenuItem(label=parent, icon='journal-code')

    ids = sheets.ids(parent_id=parent.lower(), nested=False)
    for id in ids:
        child_ids = sheets.ids(parent_id=id, nested=False)
        if child_ids:
            child_items = list(generate_actionsheets_items(id))
            yield MenuItem(label=id.upper(), children=child_items)
        else:
            yield MenuItem(label=id, icon='file-earmark-code')


def get_sheet_title(section: str) -> str:
    if section:
        return sheets.sheet_info(id=section.lower())['title']
    else:
        return ''


def sheet_toc(sheet: ActionsheetView, parent_section: str):
    html_content = generate_sections_list_html(sheet, parent_section=parent_section)

    st.html(f'<ul class="toc">{html_content}</ul>')


def generate_sections_list_html(sheet, parent_section: str) -> str:
    ids = sheet.child_ids(type='section', section=parent_section)

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
