#streamlit web file
import streamlit as st
from streamlit_option_menu import option_menu
from home import Home

st.set_page_config(
    layout= "wide", 
    initial_sidebar_state= "expanded",
    page_title= "Predict Price"
)

with st.sidebar:
    selected= option_menu(
        menu_title= None,
        options=["Home", "Prediction", "Dashboard"],
        icons=["house","",""],
        menu_icon= "cast",
        default_index= 0
)


if selected == "Home":
    Home()
elif selected == "Prediction":
    pred_page()

