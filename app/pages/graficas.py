# ---- Import libraries ----
import streamlit as st
import plotly.express as px


# ---- Functions ----
def app(df):
    st.markdown("<h1 style='text-align: center;'> Gráficas </h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    df1 = df.groupby(['date','category']).sum()
    df1.reset_index(inplace=True)
    #st.dataframe(df1)
    
    fig1 = px.line(df1, x='date', y="count", 
                  labels={'count':'Casos','date':'Fecha','category':'Categoría'},
                  line_group='category',
                  color='category',
                  color_discrete_map={
                 'Confirmed': '#F1C40F',
                 'Deaths': '#E74C3C',
                 'Recovered': '#2ECC71'
             })
    

    
    df2 = df.groupby(['country_region','category']).sum()
    df2.reset_index(inplace=True)

    
    fig2 = px.bar(df2, x='count', y="country_region", 
                  labels={'count':'Casos','country_region':'Región','category':'Categoría'},
                  color='category',
                  orientation='h',
                  color_discrete_map={
                 'Confirmed': '#F1C40F',
                 'Deaths': '#E74C3C',
                 'Recovered': '#2ECC71'
             })
    
    fig3 = px.pie(df2, values='count', names='category',
                  labels={'count':'Casos','country_region':'Región','category':'Categoría'},
                  color='category',
                  color_discrete_map={
                 'Confirmed': '#F1C40F',
                 'Deaths': '#E74C3C',
                 'Recovered': '#2ECC71'
             })
    
    fig4 = px.histogram(df1, x="count",
                        labels={'count':'Casos','country_region':'Región','category':'Categoría'},
                        color='category',
                        color_discrete_map={
                       'Confirmed': '#F1C40F',
                       'Deaths': '#E74C3C',
                       'Recovered': '#2ECC71'
                   })
    
    with col1:
        st.markdown("<h1 style='text-align: center;'> Casos por dia </h1>", unsafe_allow_html=True)
        st.plotly_chart(fig1)
        st.markdown("<h1 style='text-align: center;'> Casos por categoria </h1>", unsafe_allow_html=True)
        st.plotly_chart(fig3)
    with col2:
        st.markdown("<h1 style='text-align: center;'> Casos por región </h1>", unsafe_allow_html=True)
        st.plotly_chart(fig2)
        st.markdown("<h1 style='text-align: center;'> Histograma de Casos por Día </h1>", unsafe_allow_html=True)
        st.plotly_chart(fig4)
        

    