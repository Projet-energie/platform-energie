#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 21:37:41 2021

@author: vcaballero
"""
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


from urllib.error import URLError
#import plotly.figure_factory as ff
#import matplotlib.pyplot as plt


@st.cache
def load_data(nrows):
    data = pd.read_csv('df_nettoye_2.csv', sep=';', nrows=nrows)
    return data


st.sidebar.title('Analyses Projet Energie')
page = st.sidebar.radio("", options = ['Choix Région', 'Modélisation', 'Magic Command', 'Graph', 'DataFrame Demo', 'DataFrame Energie', 'Analyse Production', 'Carte de France', 'Carte Sources Energies de France', 'Consommation par Secteur'])



if page == 'Choix Région':
    
    
    st.sidebar.title('Choix Région')
    # Titre et sous-titre
    '''
    # Région choisie

    Voici la Région _choisie_.
    '''
    x = st.sidebar.slider('x')  # 👈 this is a widget
    st.write(x * x, 'est le carré de ', x)
    st.text("On remarque que lorsque l'on choisi une valeur pour 'x' on obtient le carré de 'x'.")


if page == 'Modélisation':
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

if page == 'Magic Command':
    # Titre et sous-titre
    '''
    # This is the document title

    This is some _markdown_.
    '''

    df = pd.DataFrame({'col1': [1,2,3]})
    df  # <-- Draw the dataframe

    x = 10
    'x', x  # <-- Draw the string 'x' and then the value of x

if page == 'Graph':
    # Titre et sous-titre
    '''
    # This is the document title

    This is some _markdown_.
    '''
    st.line_chart({"data": [1, 5, 2, 6, 2, 1]})
    with st.expander("Voir les explications"):
        st.write("""
                 Le graphique ci-dessus, bla bla bla..
                 On peu aussi ajouter une image.
                 """)
        st.image("https://static.streamlit.io/examples/dice.jpg")
        
        
if page == 'DataFrame Demo':
    @st.cache
    def get_UN_data():
        AWS_BUCKET_URL = "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
            )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
                )
            chart = (alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(x="year:T", y=alt.Y("Gross Agricultural Product ($B):Q", stack=None), color="Region:N",))
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
                st.error(
               """
               **This demo requires internet access.**

                Connection error: %s
                """
            % e.reason
            )
                
if page == 'DataFrame Energie':
    @st.cache
    def get_data_consommation():
        df = pd.read_csv('df_streamlit.csv')
        df = df.reset_index()
        return df.set_index("Libellé Région")

    try:
        df = get_data_consommation()
        region = st.multiselect(
            "Choisissez vos régions", list(df.index), ["Île-de-France", "Centre-Val de Loire"]
            )
        if not region:
            st.error("Merci de choisir une région.")
        else:
            data = df.loc[region]
            st.write("### Consommations électrique en MW", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "Annee", "value": "Consommation (MW)"}
                )
            chart = (alt.Chart(data)
                .mark_area(opacity=0.4)
                .encode(x="Annee:T", y=alt.Y("Consommation (MW):Q", stack=None), color="Libellé Région:N",))
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
                st.error(
               """
               **This demo requires internet access.**

                Connection error: %s
                """
            % e.reason
            )


if page == 'Analyse Production':
    @st.cache
    
    def get_data_consommation():
        df = pd.read_csv('df_streamlit.csv')
        df = df.reset_index()
        return df.set_index("Libellé Région")

    def get_data_production():
        df_prod = pd.read_csv('df_production.csv')
        df_prod = df_prod.reset_index()
        return df_prod.set_index("Libellé Région")

    try:
        df = get_data_consommation()
        df_prod = get_data_production()
        region = st.multiselect(
            "Choisissez vos régions", list(df_prod.index), ["Île-de-France", "Centre-Val de Loire"]
            )
        if not region:
            st.error("Merci de choisir une région.")
        else:
            
            # Traitement de la partie production
            data_prod = df_prod.loc[region]
            st.write("### Production électrique en MW", data_prod.sort_index())

            data_prod = data_prod.T.reset_index()
            data_prod = pd.melt(data_prod, id_vars=["index"]).rename(
                columns={"index": "Annee", "value": "Production (MW)"}
                )
            chart_prod = (alt.Chart(data_prod)
                .mark_area(opacity=0.4)
                .encode(x="Annee:T", y=alt.Y("Production (MW):Q", stack=None), color="Libellé Région:N",))
            st.altair_chart(chart_prod, use_container_width=True)
            
            # Traitement de la partie Consommation
            data = df.loc[region]
            st.write("### Consommations électrique en MW", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "Annee", "value": "Consommation (MW)"}
                )
            chart = (alt.Chart(data)
                .mark_area(opacity=0.4)
                .encode(x="Annee:T", y=alt.Y("Consommation (MW):Q", stack=None), color="Libellé Région:N",))
            st.altair_chart(chart, use_container_width=True)
            
    except URLError as e:
                st.error(
               """
               **This demo requires internet access.**

                Connection error: %s
                """
            % e.reason
            )


if page == 'Carte de France':
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from urllib.request import urlopen
    import json
    st.title('Visualisation géographique')
    with urlopen('http://france-geojson.gregoiredavid.fr/repo/regions.geojson') as response:
        regions = json.load(response)

    
    df = pd.read_csv("df_energie_2020.csv",
                   dtype={"Code INSEE région": str})




    fig = px.choropleth_mapbox(df, geojson=regions, locations='Libellé Région',             color='Production_totale',
                           featureidkey="properties.nom",
                           color_continuous_scale="Viridis",
                           range_color=(df['Production_totale'].min(), df['Production_totale'].max()),
                           mapbox_style="carto-positron",
                           zoom=4.5, center = {"lat": 47.000193, "lon": 2.209667},
                           opacity=0.5,
                           labels={'Production_totale':'Production Totale en MW'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    
if page == 'Carte Sources Energies de France':
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from urllib.request import urlopen
    import json
    st.title('Sources Energétiques de France en 2020')
    with urlopen('http://france-geojson.gregoiredavid.fr/repo/regions.geojson') as response:
        regions = json.load(response)

    
    df = pd.read_csv("df_energie_2020.csv",
                   dtype={"Code INSEE région": str})


    type_energie = st.selectbox("Choisissez une source d'énergie",['Thermique (MW)', 'Nucléaire (MW)','Hydraulique (MW)', 'Solaire (MW)', 'Eolien (MW)'])

    fig = px.choropleth_mapbox(df, geojson=regions, locations='Libellé Région',             color=type_energie,
                           featureidkey="properties.nom",
                           color_continuous_scale="Viridis",
                           range_color=(df[type_energie].min(), df[type_energie].max()),
                           mapbox_style="carto-positron",
                           zoom=4.5, center = {"lat": 47.000193, "lon": 2.209667},
                           opacity=0.5,
                           labels=type_energie
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)


if page == 'Consommation par Secteur':
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from urllib.request import urlopen
    import json
    st.title('Consommations par secteur d\'activité')
    with urlopen('http://france-geojson.gregoiredavid.fr/repo/regions.geojson') as response:
        regions = json.load(response)

    
    df = pd.read_csv("consommation_secteurs.csv",
                   dtype={"Code INSEE région": str})


    type_energie = st.selectbox("Choisissez un secteur d\'activité",[ 'Consommation Agriculture (MWh)',
       'Consommation Industrie (MWh)', 'Consommation Résidentiel  (MWh)', 
       'Consommation Tertiaire  (MWh)',])

    fig = px.choropleth_mapbox(df, geojson=regions, locations='Libellé Région',             color=type_energie,
                           featureidkey="properties.nom",
                           color_continuous_scale="Viridis",
                           range_color=(df[type_energie].min(), df[type_energie].max()),
                           mapbox_style="carto-positron",
                           zoom=4.5, center = {"lat": 47.000193, "lon": 2.209667},
                           opacity=0.5,
                           labels=type_energie
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
    
    with st.expander("Voir les explications"):
        if type_energie == 'Consommation Agriculture (MWh)':
            st.write("""
                 Les régions dont la consommation agricole est plus forte que les autres secteurs activités sont la Bretagne, la Nouvelle-Aquitaine et les Pays de la Loire.
                 """)
        if type_energie == 'Consommation Industrie (MWh)':
            st.write("""
                 Les régions dont la consommation industrielle est plus forte que les autres secteurs activités sont l’Auvergne- Rhône-Alpes, les Hauts-de-France et le Grand-Est.
                 """)
        if type_energie == 'Consommation Tertiaire  (MWh)':
            st.write("""
                 Les régions dont la consommation tertiaire est plus forte que les autres secteurs activités est l’Ile-de-France, l’Auvergne-Rhône-Alpes et la Provence-Alpes-Côte d’Azur.
                 """)
        if type_energie == 'Consommation Résidentiel  (MWh)':
            st.write("""
                 Les régions dont la consommation résidentielle est plus forte que les autres secteurs activités sont l’Ile-de-France, l’Auvergne-Rhône-Alpes et l’Occitanie.
                 """)