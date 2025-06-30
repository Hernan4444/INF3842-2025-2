import altair as alt
import streamlit as st
import pandas as pd
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from ml import load_pipeline, ml_zone
from utils import number_to_text


@st.cache_data
def load_data(data_path):
    print("Cargando datos")
    df = pd.read_csv(data_path)
    df.es_superhost = df.es_superhost.map(number_to_text)
    df.servicio_aire_acondicionado = df.servicio_aire_acondicionado.map(number_to_text)
    return df


def add_title_and_description():
    """
    Añadir textos iniciales a la demo
    """
    st.title("Airbnb Demo")


def show_airbnb_dataframe(df):
    """
    Mostrar dataframe
    """
    st.write("Ver datos")


def country_filter(df):
    """
    Filtrar dataset
    """
    st.subheader("Filtrar por país")


def show_airbnb_in_map(df, is_all_data):
    """
    Mapa de los airbnb
    """
    st.subheader("Mapa de todos los Airbnb")


def plot_days_of_week(df, column):
    """
    Visualizaciones con altair
    """
    column.subheader("Anfitriones por tiempo de respuesta")


def plot_airbnb_by_superhost(df, column):
    """
    Visualizaciones con altair
    """
    column.subheader("Airbnb por superhost")


def interactive_view(df):
    """
    Visualizaciones interactivas con altair
    """
    st.subheader("Propiedad y servicio de aire acondicionado")


if __name__ == "__main__":
    print("Cargando streamlit")
    df = load_data("Airbnb_Locations.csv")

    # Textos y filtros
    add_title_and_description()
    show_airbnb_dataframe(df)

    # Descomentar a medida que avancemos
    filtered_df = country_filter(df)
    st.write(filtered_df)

    # Gráficos
    # show_airbnb_in_map(filtered_df, filtered_df.shape == df.shape)
    # column_1, column_2 = st.columns(2)
    # plot_days_of_week(filtered_df, column_1)
    # plot_airbnb_by_superhost(filtered_df, column_2)
    # interactive_view(filtered_df)

    # Parte ML [Esto viene listo para usar]
    # pipeline = load_pipeline()
    # ml_zone(pipeline)
