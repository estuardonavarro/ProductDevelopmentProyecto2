# ---- Import libraries ----
import streamlit as st

def app(df):
    st.markdown("<h1 style='text-align: center;'> Tablas </h1>", unsafe_allow_html=True)
    st.dataframe(df)
    st.download_button(
       "Descargar tabla",
       df.to_csv(),
       "DATA.csv",
       "text/csv",
       key='download-csv'
       )