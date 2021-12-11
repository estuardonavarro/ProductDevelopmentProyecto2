# ---- Import libraries ----
import streamlit as st
import database

# ---- formato de la pagina ----
st.set_page_config(layout="wide")

# ---- Custom imports -----
from multipage import MultiPage
from pages import tablas, graficas, mapa

# ---- Connect to data base ----
@st.cache(allow_output_mutation=True)
def getData():
    df = database.connect_to_database("select * from  covid")
    return df
df = getData()
df["count"][df["count"]<0] = 0
#df =df[df["count"]>=0]
print(df)
if df.empty:
    st.text("Por favor, cargue la base de datos primero.")
else:    
    # ---- Create an instance of the app ----
    app = MultiPage.filter(df)

    # ---- Add all your application ----

    app.add_page("Mapa",mapa.app)
    app.add_page("Tablas",tablas.app)
    app.add_page("Gráficas",graficas.app)


    # ---- The main app ----
    app.run()