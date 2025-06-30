import constantes as C
import joblib
import streamlit as st
import pandas as pd
from utils import text_to_number


@st.cache_data
def load_pipeline():
    return joblib.load("pipeline_model.pkl")


def predict(pipeline_loaded, info):
    """
    Predecir dato
    """
    # Dar las columnas como corresponde
    columns = [
        "tiempo_respuesta",
        "es_superhost",
        "tipo_propiedad",
        "capacidad",
        "puntaje_promedio_comunicación",
        "puntaje_promedio_localización",
        "servicio_tv_cable",
        "servicio_aire_acondicionado",
    ]

    # Construir DataFrame con los datos y columnas
    df_test = pd.DataFrame([info], columns=columns)

    # Clasificar obteniendo la probabilidad por clase
    predictions = pipeline_loaded.predict_proba(df_test)
    return {
        "classes": pipeline_loaded.classes_,
        "probabilities": predictions[0],
        "result": pipeline_loaded.predict(df_test)[0],
    }


def ml_zone(pipeline):
    """
    Sección para modelo de ML
    """
    column_1, column_2 = st.columns(2)

    column_1.subheader("Datos de entrada")

    respuesta_box = column_1.selectbox("Tiempo de respuesta", C.TIEMPO_RESPUESTA)
    superhost_box = column_1.selectbox("Es superhost", C.SI_NO)
    propiedad_box = column_1.selectbox("Tipo Propiedad", C.TIPO_PROPIEDAD)
    capacidad_slider = column_1.slider("Capacidad", min_value=0, max_value=16, value=5, step=1)
    comunicacion_slider = column_1.slider("Puntaje Comunicación", min_value=0, max_value=10,
                                          value=5, step=1)

    localizacion_slider = column_1.slider("Puntaje Localización", min_value=0, max_value=10,
                                          value=5, step=1)

    tv_cable_box = column_1.selectbox("Tiene TV Cable", C.SI_NO)
    aire_box = column_1.selectbox("Tiene Aire Acondicionado", C.SI_NO)

    column_2.subheader("Predicción")

    if column_1.button("Predecir", use_container_width=True):
        info = [
            respuesta_box,
            text_to_number(superhost_box),
            propiedad_box,
            capacidad_slider,
            comunicacion_slider,
            localizacion_slider,
            text_to_number(tv_cable_box),
            text_to_number(aire_box),
        ]
        resultado = predict(pipeline, info)
        df = pd.DataFrame([resultado["probabilities"]], columns=resultado["classes"])

        column_2.write(f'Resultado: {resultado["result"]}')
        column_2.write(df)
