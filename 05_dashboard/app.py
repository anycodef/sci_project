import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import numpy as np

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
        df = pd.read_csv("data/processed_data.csv")
        # Ensure 'periodo' is sorted correctly for visualizations
        df['periodo'] = pd.Categorical(df['periodo'], categories=sorted(df['periodo'].unique()), ordered=True)
        return df
    except FileNotFoundError:
        st.error("El archivo `data/processed_data.csv` no fue encontrado. Por favor, ejecute `data_prep.py` primero.")
        return pd.DataFrame()

df = load_data()

# --- Model Loading ---
@st.cache_resource
def load_model():
    """Loads the trained model from the pickle file."""
    try:
        with open("informality_model.pickle", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("El archivo del modelo `informality_model.pickle` no fue encontrado.")
        return None

model = load_model()

# --- Sidebar Filters ---
st.sidebar.header("Filtros Interactivos")

if not df.empty:
    # Periodo Filter
    periodos_disponibles = sorted(df['periodo'].unique())
    periodo_seleccionado = st.sidebar.multiselect(
        "Seleccione Periodo(s):",
        options=periodos_disponibles,
        default=periodos_disponibles
    )

    # Sexo Filter
    sexo_disponible = sorted(df['Sexo'].unique())
    sexo_seleccionado = st.sidebar.multiselect(
        "Seleccione Sexo:",
        options=sexo_disponible,
        default=sexo_disponible
    )

    # Nivel Educativo Filter
    nivel_educativo_disponible = sorted(df['Nivel_Educativo'].dropna().unique())
    nivel_educativo_seleccionado = st.sidebar.multiselect(
        "Seleccione Nivel Educativo:",
        options=nivel_educativo_disponible,
        default=nivel_educativo_disponible
    )

    # Filtering Data
    df_filtrado = df[
        df['periodo'].isin(periodo_seleccionado) &
        df['Sexo'].isin(sexo_seleccionado) &
        df['Nivel_Educativo'].isin(nivel_educativo_seleccionado)
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
        # KPIs
        col1, col2, col3 = st.columns(3)

        # KPI 1: Ingreso Promedio Mensual
        ingreso_promedio = df_filtrado['Ingreso_Mensual'].mean()
        col1.metric(
            label="Ingreso Promedio Mensual (S/.)",
            value=f"{ingreso_promedio:,.2f}"
        )

        # KPI 2: Tasa de Informalidad
        tasa_informalidad = (df_filtrado['es_informal'].mean()) * 100
        col2.metric(
            label="Tasa de Informalidad (%)",
            value=f"{tasa_informalidad:.2f}%"
        )

        # KPI 3: Total de Encuestados
        total_encuestados = len(df_filtrado)
        col3.metric(
            label="Total de Encuestados",
            value=f"{total_encuestados:,}"
        )

        st.markdown("---")

        # Charts
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("Distribución por Nivel Educativo")
            educacion_counts = df_filtrado['Nivel_Educativo'].value_counts().reset_index()
            educacion_counts.columns = ['Nivel_Educativo', 'count']
            fig_donut = px.pie(
                educacion_counts,
                names='Nivel_Educativo',
                values='count',
                hole=0.4,
                title="Proporción de Encuestados por Nivel Educativo"
            )
            fig_donut.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_donut, use_container_width=True)

        with col_chart2:
            st.subheader("Distribución por Tipo de Ocupación")
            ocupacion_counts = df_filtrado['Tipo_Ocupacion'].value_counts().reset_index()
            ocupacion_counts.columns = ['Tipo_Ocupacion', 'count']
            fig_bar = px.bar(
                ocupacion_counts,
                x='Tipo_Ocupacion',
                y='count',
                title="Número de Encuestados por Tipo de Ocupación",
                labels={'count': 'Número de Encuestados', 'Tipo_Ocupacion': 'Tipo de Ocupación'},
                color='Tipo_Ocupacion'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para la selección actual.")


# --- Tab 2: Temporal Analysis ---
with tab2:
    st.header("Evolución de Indicadores Clave a lo Largo del Tiempo")

    if not df_filtrado.empty:
        # Line Chart: Evolution of Average Monthly Income
        st.subheader("Evolución del Ingreso Promedio Mensual (S/.)")
        ingreso_temporal = df_filtrado.groupby('periodo')['Ingreso_Mensual'].mean().reset_index()
        fig_line_ingreso = px.line(
            ingreso_temporal,
            x='periodo',
            y='Ingreso_Mensual',
            title="Ingreso Promedio Mensual por Trimestre",
            markers=True,
            labels={'Ingreso_Mensual': 'Ingreso Promedio (S/.)', 'periodo': 'Trimestre'}
        )
        fig_line_ingreso.update_layout(xaxis_title="Trimestre", yaxis_title="Ingreso Promedio (S/.)")
        st.plotly_chart(fig_line_ingreso, use_container_width=True)

        # Grouped Bar Chart: Evolution of Informality Rate by Sex
        st.subheader("Evolución de la Tasa de Informalidad (%) por Sexo")
        informalidad_temporal = df_filtrado.groupby(['periodo', 'Sexo'])['es_informal'].mean().reset_index()
        informalidad_temporal['Tasa_Informalidad'] = informalidad_temporal['es_informal'] * 100

        fig_bar_informalidad = px.bar(
            informalidad_temporal,
            x='periodo',
            y='Tasa_Informalidad',
            color='Sexo',
            barmode='group',
            title="Tasa de Informalidad por Sexo y Trimestre",
            labels={'Tasa_Informalidad': 'Tasa de Informalidad (%)', 'periodo': 'Trimestre'}
        )
        fig_bar_informalidad.update_layout(xaxis_title="Trimestre", yaxis_title="Tasa de Informalidad (%)")
        st.plotly_chart(fig_bar_informalidad, use_container_width=True)
    else:
        st.warning("No hay datos disponibles para la selección actual.")

# --- Tab 3: Predictive Model ---
with tab3:
    st.header("Modelo Predictivo de Informalidad Laboral")

    if model and not df.empty:
        # Sub-tab: Batch Prediction
        st.subheader("Predicción en Lote (Ejemplo)")
        st.write("A continuación se muestra una muestra de los datos con la probabilidad de informalidad predicha por el modelo.")

        if not df_filtrado.empty:
            sample_df = df_filtrado.sample(min(50, len(df_filtrado))).copy()

            # Features the model expects (raw categorical data)
            features = ['Grupo_Edad', 'Sexo', 'Nivel_Educativo']
            X_predict = sample_df[features].copy()

            # Fill NaNs with a placeholder string to prevent errors in the pipeline
            for col in features:
                X_predict[col] = X_predict[col].astype(str).replace('nan', 'Desconocido')

            # Predict probabilities
            pred_probs = model.predict_proba(X_predict)[:, 1]

            # Display results
            sample_df['Probabilidad_Informalidad'] = np.round(pred_probs * 100, 2)
            st.dataframe(sample_df[['Sexo', 'Edad', 'Nivel_Educativo', 'Probabilidad_Informalidad']].style.format({'Probabilidad_Informalidad': '{:.2f}%'}))
        else:
            st.warning("No hay datos en la selección actual para mostrar un ejemplo de predicción.")

        st.markdown("---")

        # Sub-tab: Interactive Classifier
        st.subheader("Clasificador Interactivo")
        st.write("Ingrese los datos de un perfil para predecir su probabilidad de ser informal.")

        with st.form("prediction_form"):
            # Input fields for model features
            grupo_edad_input = st.selectbox("Grupo de Edad:", options=sorted(df['Grupo_Edad'].dropna().unique()))
            sexo_input = st.selectbox("Sexo:", options=sorted(df['Sexo'].unique()))
            nivel_educativo_input = st.selectbox("Nivel Educativo:", options=sorted(df['Nivel_Educativo'].dropna().unique()))

            submit_button = st.form_submit_button("Clasificar")

            if submit_button:
                # Create a DataFrame from the inputs
                input_data = pd.DataFrame({
                    'Grupo_Edad': [grupo_edad_input],
                    'Sexo': [sexo_input],
                    'Nivel_Educativo': [nivel_educativo_input]
                })

                # The model pipeline expects raw categorical data. No get_dummies needed.
                prediction = model.predict_proba(input_data)[0, 1]
                prob_percent = prediction * 100

                # Display result
                if prob_percent >= 50:
                    st.warning(f"Este perfil tiene una {prob_percent:.2f}% de probabilidad de ser informal.")
                else:
                    st.success(f"Este perfil tiene una {prob_percent:.2f}% de probabilidad de ser informal.")
    else:
        st.error("No se pudo cargar el modelo o los datos, la funcionalidad de predicción está deshabilitada.")
