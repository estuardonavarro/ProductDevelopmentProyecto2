# ---- Importacion de librerias ----
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

# ---- Funciones ----
def app(df2):
    df2.drop("province_state", axis=1, inplace=True)
    st.title("Mapa de COVID-19")
    try:
        df_grouped = df2.groupby(['lon','lat',"category","country_region"]).sum().reset_index().drop(0)
        #df_grouped = df_grouped[df_grouped.count >= 0]
        df_grouped_catetory = df_grouped.category.unique()
        # --- Use pandas to calculate additional data for each point ---
        df_grouped["radius"] =  df_grouped["count"]/df_grouped["count"].max()* 80000
        #df_grouped =  df_grouped[df_grouped.radius > 0]
    except:
        pass

    # --- Define a layer to display on a map ---
    lista = []
    try:
        Confirmed = pdk.Layer(
            "ScatterplotLayer",
            df_grouped[df_grouped["category"] == "Confirmed"],
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="[lon, lat]",
            get_radius="radius",
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
        )
        lista.append(Confirmed)
    except:
        pass
    try:
        Deaths = pdk.Layer(
            "ScatterplotLayer",
            df_grouped[df_grouped["category"] == "Deaths"],
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="[lon, lat]",
            get_radius="radius",
            get_fill_color=[255, 0, 0],
            get_line_color=[0, 0, 0],
        )
        lista.append(Deaths)
    except:
        pass
    try:
        Recovered = pdk.Layer(
            "ScatterplotLayer",
            df_grouped[df_grouped["category"] == "Recovered"],
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="[lon, lat]",
            get_radius="radius",
            get_fill_color=[0, 255, 0],
            get_line_color=[0, 0, 0],
        )
        lista.append(Recovered)
    except:
        pass

        # --- Set the viewport location and zoom level ---
    try:
        view_state = pdk.ViewState(
            latitude=df_grouped.lat.mean(),
            longitude=df_grouped.lon.mean(),
            zoom=2,
            bearing=0,
            pitch=0
        )
    except:
        pass

        # --- Render the map to the page ---
    try:
        r = pdk.Deck(
            layers=lista,
            initial_view_state=view_state,
            tooltip={"text": "{count} cases\n{category}\n {country_region}"},
        )
    except:
        pass
    try:
        st.pydeck_chart(r)
    except:
        view_state = pdk.ViewState(
            latitude= 14.61,
            longitude=-90.51,
            zoom=5,
            bearing=0,
            pitch=0
        )
        r2 = pdk.Deck(
            
            initial_view_state=view_state,
        )
        st.pydeck_chart(r2)