import streamlit as st
from __init__ import wordcloud
# from custom_circle_plot import custom_circle_plot

st.set_page_config(layout="wide")


words = [{"text":"AML Compliance Manager.","value":1},{"text":"Agricultural Property Solicitor","value":2},{"text":"Agriculture Lawyer","value":1},{"text":"Associate Criminal Solicitor","value":1},{"text":"Banking & Finance Associate","value":1},{"text":"Banking & Finance Solicitor","value":1},{"text":"Banking Solicitor","value":1},{"text":"Banking and Finance Solicitor","value":1},{"text":"Casualty Solicitor","value":1},{"text":"Catastrophic Injury Lawyer","value":1}]

wordcloud(words=words, width="100%", height="100%", tooltip_data_fields={
    'text':'Titles', 'value':'Mentions'
}, paletteColorVer=False)
