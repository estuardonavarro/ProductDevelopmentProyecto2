# ---- Import libraries ----
import streamlit as st
import datetime

# ---- Define the multipage class to manage the multiple apps in our program ----
class MultiPage: 

    # ---- Contrucctor de la clase ----
    def __init__(self,filter_country,filter_category,df) -> None:
        self.pages = []
        self.filter_country = filter_country
        self.filter_category = filter_category
        self.df = df
    
    # ---- Metodo para agregar paginas al proyecto ----
    def add_page(self, title, func) -> None: 
        self.pages.append(
            {
                "title": title, 
                "function": func
            }
        )
    # ---- Funcion principal run
    def run(self):
        # ---- Drodown to select the page to run ----
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )
        # ---- run the app function ----
        page['function'](self.df)
    
    # ---- Decorador ----
    @classmethod
    def filter(cls,df):
        # ---- Filtro por pais ----
        all_countries = st.sidebar.checkbox(
            "All Countries",
            value=True,
            key="all_countries",
        )
        country = st.sidebar.multiselect(
            'Country filter',
            df["country_region"].unique()
        )
        # ---- Filtro por categoria -----
        category = st.sidebar.multiselect(
            "Category filter",
            df["category"].unique(),
            default=df["category"].unique()
        )
        # ---- Filtro por fecha ----
        start_date = st.sidebar.date_input(
            "Start date",
            min_value= min(df["date"]),
            value= datetime.date(2020,1,23),
        )
        end_date = st.sidebar.date_input(
            "End date",
            min_value= min(df["date"])
        )
        st.sidebar.text(start_date)
        
        if all_countries:
            df_filtered = df[df["category"].isin(category)]
        else:
            df_filtered = df[df["category"].isin(category) &
            df["country_region"].isin(country)
            ]
        df_filtered = df_filtered[(df_filtered["date"].dt.date > start_date) &
                                (df_filtered["date"].dt.date < end_date)]
        return cls(country,category,df_filtered)


    