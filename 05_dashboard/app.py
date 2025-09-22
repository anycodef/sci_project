import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import numpy as np
import os

# --- Path setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "informality_model.pickle")


# --- Page Configuration ---
st.set_page_config(
    page_title="Dashboard de Empleabilidad",
    page_icon="📊",
    layout="wide"
)

# --- Header ---
st.markdown("""
    <div style="background-color:#1428A0; padding:10px; border-radius:10px;">
        <h1 style="color:white; text-align:center;">Samsung Innovation Campus - Grupo 3</h1>
    </div>
""", unsafe_allow_html=True)
st.title("Dashboard de Análisis del Mercado Laboral")

# --- Data Loading ---
@st.cache_data
def load_data():
    """Loads the processed data from the CSV file."""
    try:
        df = pd.read_csv(DATA_PATH)
        df['periodo'] = pd.Categorical(df['periodo'], categories=sorted(df['periodo'].unique()), ordered=True)
        return df
    except FileNotFoundError:
        st.error(f"El archivo `{DATA_PATH}` no fue encontrado. Por favor, ejecute `data_prep.py` primero.")
        return pd.DataFrame()

df = load_data()

# --- Model Loading ---
@st.cache_resource
def load_model():
    """Loads the trained model from the pickle file."""
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error(f"El archivo del modelo `{MODEL_PATH}` no fue encontrado.")
        return None

model = load_model()

# --- Sidebar Filters ---
st.sidebar.header("Filtros Interactivos")

if not df.empty:
    periodos_disponibles = sorted(df['periodo'].unique())
    periodo_seleccionado = st.sidebar.multiselect(
        "Seleccione Periodo(s):",
        options=periodos_disponibles,
        default=periodos_disponibles
    )

    sexo_disponible = sorted(df['Sexo'].unique())
    sexo_seleccionado = st.sidebar.multiselect(
        "Seleccione Sexo:",
        options=sexo_disponible,
        default=sexo_disponible
    )

    nivel_educativo_disponible = sorted(df['Nivel Educativo'].dropna().unique())
    nivel_educativo_seleccionado = st.sidebar.multiselect(
        "Seleccione Nivel Educativo:",
        options=nivel_educativo_disponible,
        default=nivel_educativo_disponible
    )

    df_filtrado = df[
        df['periodo'].isin(periodo_seleccionado) &
        df['Sexo'].isin(sexo_seleccionado) &
        df['Nivel Educativo'].isin(nivel_educativo_seleccionado)
    ]
else:
    st.warning("No hay datos para mostrar. Verifique la carga de datos.")
    df_filtrado = pd.DataFrame()


# --- Main Content Tabs ---
tab1, tab2, tab3 = st.tabs(["Análisis General y KPIs", "Análisis Temporal", "Modelo Predictivo de Informalidad"])

# --- Tab 1: General Analysis & KPIs ---
with tab1:
    st.header("Análisis General para la Selección Actual")

    if not df_filtrado.empty:
        col1, col2, col3 = st.columns(3)
        ingreso_promedio = df_filtrado['Ingreso_Mensual'].mean()
        col1.metric(label="Ingreso Promedio Mensual (S/.)", value=f"{ingreso_promedio:,.2f}")

        tasa_informalidad = (df_filtrado['es_informal'].mean()) * 100
        col2.metric(label="Tasa de Informalidad (%)", value=f"{tasa_informalidad:.2f}%")

        total_encuestados = len(df_filtrado)
        col3.metric(label="Total de Encuestados", value=f"{total_encuestados:,}")

        st.markdown("---")
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("Distribución por Nivel Educativo")
            educacion_counts = df_filtrado['Nivel Educativo'].value_counts().reset_index()
            fig_donut = px.pie(educacion_counts, names='Nivel Educativo', values='count', hole=0.4, title="Proporción por Nivel Educativo")
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_chart2:
            st.subheader("Distribución por Tipo de Ocupación")
            ocupacion_counts = df_filtrado['Tipo de Ocupación'].value_counts().reset_index()
            fig_bar = px.bar(ocupacion_counts, x='Tipo de Ocupación', y='count', title="Encuestados por Tipo de Ocupación", color='Tipo de Ocupación')
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para la selección actual.")

# --- Tab 2: Temporal Analysis ---
with tab2:
    st.header("Evolución de Indicadores Clave a lo Largo del Tiempo")

    if not df_filtrado.empty:
        st.subheader("Evolución del Ingreso Promedio Mensual (S/.)")
        ingreso_temporal = df_filtrado.groupby('periodo')['Ingreso_Mensual'].mean().reset_index()
        fig_line_ingreso = px.line(ingreso_temporal, x='periodo', y='Ingreso_Mensual', title="Ingreso Promedio Mensual por Trimestre", markers=True)
        st.plotly_chart(fig_line_ingreso, use_container_width=True)

        st.subheader("Evolución de la Tasa de Informalidad (%) por Sexo")
        informalidad_temporal = df_filtrado.groupby(['periodo', 'Sexo'])['es_informal'].mean().reset_index()
        informalidad_temporal['Tasa_Informalidad'] = informalidad_temporal['es_informal'] * 100
        fig_bar_informalidad = px.bar(informalidad_temporal, x='periodo', y='Tasa_Informalidad', color='Sexo', barmode='group', title="Tasa de Informalidad por Sexo y Trimestre")
        st.plotly_chart(fig_bar_informalidad, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para la selección actual.")

# --- Tab 3: Predictive Model ---
with tab3:
    st.header("Modelo Predictivo de Informalidad Laboral")

    if model and not df.empty:
        # Define the full list of features the model expects
        model_features = ['grupo_edad', 'Sexo', 'Nivel Educativo', 'Tipo de Ocupación', 'whoraT']

        st.subheader("Predicción en Lote (Ejemplo)")
        st.write("A continuación se muestra una muestra de los datos con la probabilidad de informalidad predicha por el modelo.")

        if not df_filtrado.empty:
            sample_df = df_filtrado.sample(min(50, len(df_filtrado))).copy()
            X_predict = sample_df[model_features].copy()

            # Handle potential NaNs from sampling or filtering
            for col in X_predict.columns:
                if X_predict[col].dtype == 'object' or pd.api.types.is_categorical_dtype(X_predict[col]):
                    X_predict[col] = X_predict[col].astype(str).replace('nan', 'Desconocido')
                elif pd.api.types.is_numeric_dtype(X_predict[col]):
                    X_predict[col].fillna(X_predict[col].median(), inplace=True)

            pred_probs = model.predict_proba(X_predict)[:, 1]
            sample_df['Probabilidad_Informalidad'] = np.round(pred_probs * 100, 2)
            st.dataframe(sample_df[['Sexo', 'Edad', 'Nivel Educativo', 'Tipo de Ocupación', 'whoraT', 'Probabilidad_Informalidad']].style.format({'Probabilidad_Informalidad': '{:.2f}%', 'whoraT': '{:.0f}'}))
        else:
            st.warning("No hay datos en la selección actual para mostrar un ejemplo de predicción.")

        st.markdown("---")
        st.subheader("Clasificador Interactivo")
        st.write("Ingrese los datos de un perfil para predecir su probabilidad de ser informal.")

        with st.form("prediction_form"):
            # Create inputs for all model features
            grupo_edad_input = st.selectbox("Grupo de Edad:", options=sorted(df['grupo_edad'].dropna().unique()))
            sexo_input = st.selectbox("Sexo:", options=sorted(df['Sexo'].unique()))
            nivel_educativo_input = st.selectbox("Nivel Educativo:", options=sorted(df['Nivel Educativo'].dropna().unique()))
            tipo_ocupacion_input = st.selectbox("Tipo de Ocupación:", options=sorted(df['Tipo de Ocupación'].dropna().unique()))
            whoraT_input = st.number_input("Horas de Trabajo a la Semana:", min_value=0, max_value=100, value=40)

            submit_button = st.form_submit_button("Clasificar")

            if submit_button:
                input_data = pd.DataFrame({
                    'grupo_edad': [grupo_edad_input],
                    'Sexo': [sexo_input],
                    'Nivel Educativo': [nivel_educativo_input],
                    'Tipo de Ocupación': [tipo_ocupacion_input],
                    'whoraT': [whoraT_input]
                })

                prediction = model.predict_proba(input_data)[0, 1]
                prob_percent = prediction * 100

                if prob_percent >= 50:
                    st.warning(f"Este perfil tiene una {prob_percent:.2f}% de probabilidad de ser informal.")
                else:
                    st.success(f"Este perfil tiene una {prob_percent:.2f}% de probabilidad de ser informal.")
    else:
        st.error("No se pudo cargar el modelo o los datos, la funcionalidad de predicción está deshabilitada.")
