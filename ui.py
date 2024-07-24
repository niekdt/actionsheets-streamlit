import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from streamlit_extras.stylable_container import stylable_container


def stylable_metric(
        label: str,
        value: str | int | float,
        background_color: str
) -> DeltaGenerator:
    component = stylable_container(
            key=label.replace(' ', ''),
            css_styles=f'''
            div[data-testid="stMetric"] {{
                background-color: {background_color};
                border-radius: 20px;
                padding-left: 20px;
                padding-top: 5px;
            }}
            label[data-testid="stMetricLabel"] > div > div > p {{
                font-size: 18pt;
            }}
            div[data-testid="stMetricValue"] > div {{
            display: inline;
                font-size: 36pt;
                font-weight: bold;
                margin-top: -5px;
                padding-left: 10px;
            }}
            '''
    )
    with component:
        st.metric(label=label, value=value)

    return component
