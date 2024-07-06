from actionsheets.sheet import ActionsheetView
import streamlit as st
from streamlit_antd_components import TreeItem

from data import get_all_sheets

sheets = get_all_sheets()


def generate_actionsheets_tree_items(parent: str) -> list[TreeItem]:
    ids = sheets.ids(parent_id=parent.lower())

    return [
        TreeItem(
            label=sheets.sheet_info(sheet_id)['title'],
            children=generate_actionsheets_tree_items(sheet_id)
        ) for sheet_id in ids
    ]


def generate_actionsheets_tree_lookup(parent: str) -> list[str]:
    ids = sheets.ids(parent_id=parent.lower())

    out = []
    for sheet_id in ids:
        out += [sheet_id] + generate_actionsheets_tree_lookup(sheet_id)
    return out


def sheet_toc(sheet: ActionsheetView, parent_section: str):
    html_content = generate_sections_list_html(sheet, parent_section=parent_section)

    st.html('''
    <style>
        ul[class="toc"] li ul li a {
            text-decoration: inherit;
            color: inherit;
        }
        ul[class="toc"] a {
            text-decoration: inherit;
            color: var(--section-color);
            padding-left: 0px;
            padding-right: 2px;
        }
        ul[class="toc"] li {
            list-style: none;
            margin-left: 5px;
            line-height: 130%;
        }
        ul[class="toc"] li ul li {
            list-style: none;
            margin-left: 5px;
        }
        ul[class="toc"] li ul li ul li {
            list-style: none;
            margin-left: 15px;
            font-size: 9pt;
            color: silver;
        }
        ul[class="toc"] li ul > li:before {
          content: "·";
        }
        ul[class="toc"] a:hover {
            background-color: #505158;
            border-radius: 5px;
        }
    </style>''')
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
