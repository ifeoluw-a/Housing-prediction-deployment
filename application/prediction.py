import streamlit as st
import pandas as pd

df = pd.read_csv("clean_data.csv")


def pred_page():
    with st.expander("Dataframe")
    st.info("This is a cleaned dataframe")
    st.dataframe(df)