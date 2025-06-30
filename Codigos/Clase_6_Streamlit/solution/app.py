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
    st.write("Este dashboard muestra información sobre diferentes Airbnb en 10 ciudades.")


def show_airbnb_dataframe(df):
    """
    Mostrar dataframe
    """
    st.write("Ver datos")
    capacidad_slider = st.slider("Capacidad", min_value=0, max_value=17, value=2, step=1)
    filtrado = df[df.capacidad >= capacidad_slider]
    if len(filtrado) > 0:
        st.write(filtrado)
    else:
        st.write("Te quedaste sin datos :c")


def country_filter(df):
    """
    Filtrar dataset
    """
    st.subheader("Filtrar por país")
    opciones = ["Todos"] + list(df["pais"].unique())
    option_box = st.selectbox("Selecciona un pais", opciones)
    if option_box and option_box != "Todos":
        filtered_df = df[df["pais"] == option_box]
        return filtered_df
    return df


def show_airbnb_in_map(df, is_all_data):
    """
    Mapa de los airbnb
    """
    st.subheader("Mapa de todos los Airbnb")
    positions = df[["latitud", "longitud"]]
    if is_all_data:
        center = [positions.latitud.mean(), positions.longitud.mean()]
        f_map = folium.Map()

        # Extra: Cuando usamos folium necesitamos
        # restrigir el tamaño con CSS por un bug que todavía no corrigen
        st.markdown(
            "<style>iframe[title='streamlit_folium.st_folium'] {height: 500px;}</style>",
            unsafe_allow_html=True,
        )

        st_folium(
            f_map,
            feature_group_to_add=[FastMarkerCluster(positions)],
            center=center,
            zoom=2,
            width=1200,
            height=500,
            use_container_width=True,
            returned_objects=[],
        )
    else:
        st.map(data=df, latitude="latitud", longitude="longitud")


def plot_days_of_week(df, column):
    """
    Visualizaciones con altair
    """
    column.subheader("Anfitriones por tiempo de respuesta")

    grupo_contado = (
        df.groupby("tiempo_respuesta")["anfitrión/a"]
        .nunique()  # Cuantos datos hay sin considerar repetidos
        .reset_index(name="Cantidad")
    )

    tiempo_respuesta = (
        alt.Chart(grupo_contado)
        .mark_bar()
        .encode(
            x="Cantidad",
            y=alt.Y("tiempo_respuesta:N", axis=alt.Axis(labelLimit=200)),
        )
    ).properties(height=300)

    column.altair_chart(tiempo_respuesta, use_container_width=True)


def plot_airbnb_by_superhost(df, column):
    """
    Visualizaciones con altair
    """
    column.subheader("Airbnb por superhost")
    pie = (
        alt.Chart(df)
        .mark_arc()
        .encode(
            theta="count()",
            color=alt.Color("es_superhost:N", scale=alt.Scale(scheme="set2")),
        )
    ).properties(height=300)

    column.altair_chart(pie)


def interactive_view(df):
    """
    Visualizaciones interactivas con altair
    """
    st.subheader("Propiedad y servicio de aire acondicionado")
    selection = alt.selection_point(fields=["servicio_aire_acondicionado"], bind="legend")

    pie = (
        alt.Chart(df)
        .mark_arc()
        .encode(
            theta="count()",
            color=alt.Color(
                "servicio_aire_acondicionado:N",
                legend=alt.Legend(title="Aire"),
                scale=alt.Scale(scheme="set2"),
            ),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.2)),
        )
        .add_params(selection)
        .properties(width=200)
    )

    bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x="count()",
            y=alt.Y("tipo_propiedad:N", axis=alt.Axis(labelLimit=200)),
        )
        .add_params(selection)
        .transform_filter(selection)
        .properties(height=300, width=200)
    )
    juntos = bar | pie
    st.altair_chart(juntos)


if __name__ == "__main__":
    print("Cargando streamlit")
    df = load_data("Airbnb_Locations.csv")

    # Textos y filtros
    add_title_and_description()
    show_airbnb_dataframe(df)

    filtered_df = country_filter(df)
    st.write(filtered_df)

    # Gráficos
    show_airbnb_in_map(filtered_df, filtered_df.shape == df.shape)
    column_1, column_2 = st.columns(2)
    plot_days_of_week(filtered_df, column_1)
    plot_airbnb_by_superhost(filtered_df, column_2)
    interactive_view(filtered_df)

    # Parte ML
    pipeline = load_pipeline()
    ml_zone(pipeline)
