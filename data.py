import streamlit as st
from actionsheets.sheets import Actionsheets, default_sheets


@st.cache_data
def get_all_sheets() -> Actionsheets:
    return default_sheets()
