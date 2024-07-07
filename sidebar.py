from actionsheets.sheet import ActionsheetView
import streamlit as st
from streamlit_antd_components import MenuItem

from data import get_all_sheets

sheets = get_all_sheets()


def generate_actionsheets_items(parent: str) -> list[MenuItem]:
    ids = sheets.ids(parent_id=parent.lower())

    def generate_children(sheet_id: str) -> MenuItem:
        child_items = generate_actionsheets_items(sheet_id)

        if child_items:
            sheet_info = sheets.sheet_info(id=sheet_id)

            self_item = MenuItem(label=sheet_id, icon='journal-code')
            if len(sheet_info['description']) > 0:
                child_items.insert(0, self_item)
            return MenuItem(label=sheet_id.upper(), children=child_items)
        else:
            return MenuItem(label=sheet_id, icon='file-earmark-code')

    return list(map(generate_children, ids))


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
