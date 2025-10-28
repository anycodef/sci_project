import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página y Estilos ---
st.set_page_config(layout="wide", page_title="Análisis del Mercado Laboral de Lima")

# Estilo CSS para un diseño más profesional
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    .stMetric {
        border-radius: 10px;
        padding: 15px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
    }
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #007bff;
        color: #007bff;
    }
    .stButton>button:hover {
        border-color: #0056b3;
        color: #0056b3;
    }
</style>
""", unsafe_allow_html=True)

# --- Constantes y Mapeos ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', '02_preparacion_y_limpieza')
MODEL_DIR = os.path.join(BASE_DIR, '..', '05_modelado')
REG_MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_regresion_lima', 'modelo_regresion.joblib')
CLASS_MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_clasificacion_lima', 'modelo_clasificacion.joblib')

EDUCATION_MAP = {
    'Sin nivel': 1, 'Educ. Inicial': 2, 'Primaria Incompleta': 3, 'Primaria Completa': 4,
    'Secundaria Incompleta': 5, 'Secundaria Completa': 6, 'Básica Especial': 7,
    'Superior No Univ. Incompleta': 8, 'Superior No Univ. Completa': 9,
    'Superior Univ. Incompleta': 10, 'Superior Univ. Completa': 11, 'Maestría/Doctorado': 12
}
EDUCATION_LABELS = list(EDUCATION_MAP.keys())

ETHNICITY_MAP = {
    1: 'Quechua', 2: 'Aymara', 3: 'Nativo/Indígena Amazonía', 4: 'Otro Pueblo Indígena',
    5: 'Afroperuano', 6: 'Blanco', 7: 'Mestizo', 8: 'Otro', 9: 'No Sabe/No Responde'
}
INSURANCE_MAP = {
    1: 'ESSALUD', 2: 'Seguro Privado', 3: 'Ambos', 4: 'Otro',
    5: 'Seguro Integral (SIS)', 6: 'No Afiliado'
}

# --- Funciones de Carga de Datos y Modelos ---
@st.cache_data
def load_data():
    """Carga, unifica y prepara los datos limpios."""
    def extract_period_from_filename(filename):
        match = re.search(r'Trim ([A-Za-z-]+)(\d{2})', filename)
        if match:
            month_map = {
                'Ene-Feb-Mar': 'Q1', 'Abr-May-Jun': 'Q2', 'Jul-Ago-Set': 'Q3',
                'Set-Oct-Nov': 'Q4', 'Mar-Abr-May': 'Q2'
            }
            months, year = match.groups()
            quarter = month_map.get(months, 'Q_Unk')
            return f"20{year}-{quarter}"
        return "Periodo_Desconocido"

    try:
        files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith('lima_cleaned_')])
    except FileNotFoundError:
        st.error(f"El directorio de datos no fue encontrado en la ruta: {DATA_DIR}")
        return pd.DataFrame() # Retorna un DataFrame vacío para evitar más errores

    df_list = []
    for f in files:
        df = pd.read_csv(os.path.join(DATA_DIR, f), low_memory=False)
        df['periodo'] = extract_period_from_filename(f)
        df_list.append(df)

    master_df = pd.concat(df_list, ignore_index=True)

    master_df['C207'] = master_df['C207'].map({1: 'Hombre', 2: 'Mujer'})
    master_df['OCUP300_label'] = master_df['OCUP300'].map({1: 'Ocupado', 2: 'Desocupado', 3: 'Desocupado', 4: 'Inactivo'})
    master_df['es_informal'] = np.where((master_df['OCUP300'] == 1) & (master_df['C361_1'] == 2), 1, 0)
    master_df['C377_label'] = master_df['C377'].map(ETHNICITY_MAP)
    master_df['SEGURO1_label'] = master_df['SEGURO1'].map(INSURANCE_MAP)

    for col in ['INGTOT', 'C208', 'factor_expansion', 'whoraT', 'C366']:
        master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

    return master_df

@st.cache_resource
def load_model(path):
    """Carga un modelo desde un archivo .joblib."""
    return joblib.load(path)

def get_weighted_kpis(data):
    if data.empty or data['factor_expansion'].sum() == 0:
        return {'avg_income': 0, 'avg_age': 0, 'informality_rate': 0}
    income_data = data.dropna(subset=['INGTOT', 'factor_expansion'])
    avg_income = np.average(income_data['INGTOT'], weights=income_data['factor_expansion']) if not income_data.empty else 0
    age_data = data.dropna(subset=['C208', 'factor_expansion'])
    avg_age = np.average(age_data['C208'], weights=age_data['factor_expansion']) if not age_data.empty else 0
    ocupados = data[data['OCUP300_label'] == 'Ocupado'].dropna(subset=['es_informal', 'factor_expansion'])
    informality_rate = (np.average(ocupados['es_informal'], weights=ocupados['factor_expansion']) * 100) if not ocupados.empty else 0
    return {'avg_income': avg_income, 'avg_age': avg_age, 'informality_rate': informality_rate}

# --- Construcción de la Interfaz ---
def main():
    # Cargar datos y modelos
    df = load_data()
    reg_model = load_model(REG_MODEL_PATH)
    class_model = load_model(CLASS_MODEL_PATH)

    # --- Sidebar ---
    with st.sidebar:
        st.title("Panel de Control")
        st.write("Use este panel para explorar los datos del mercado laboral de Lima.")
        period_list = ['Todos'] + sorted(df['periodo'].unique().tolist())
        selected_period = st.selectbox("Seleccione un Trimestre:", period_list)

    # Filtrar datos según el período seleccionado
    if selected_period == 'Todos':
        df_filtered = df
    else:
        df_filtered = df[df['periodo'] == selected_period]

    # --- Contenido Principal ---
    st.title("Análisis del Mercado Laboral de Lima (2024-2025)")

    tab1, tab2, tab3, tab4 = st.tabs(["Explorador de Lima", "Modelos Predictivos", "Conclusiones y Evolución", "Acerca de"])

    with tab1:
        st.header("Análisis Exploratorio Interactivo")
        if selected_period == 'Todos':
            st.subheader("Mostrando datos para todos los períodos")
        else:
            st.subheader(f"Mostrando datos para: {selected_period}")

        kpis = get_weighted_kpis(df_filtered)
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingreso Promedio Mensual", f"S/. {kpis['avg_income']:,.2f}")
        col2.metric("Edad Promedio", f"{kpis['avg_age']:.1f} años")
        col3.metric("Tasa de Informalidad", f"{kpis['informality_rate']:.1f}%")

        st.markdown("---")
        st.markdown("### Visualizaciones Principales")
        col1_fig, col2_fig = st.columns(2)

        with col1_fig:
            st.write("**Distribución de Género**")
            gender_dist = df_filtered.groupby('C207')['factor_expansion'].sum()
            if not gender_dist.empty:
                fig, ax = plt.subplots()
                ax.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
                ax.axis('equal')
                st.pyplot(fig)

        with col2_fig:
            st.write("**Condición de Actividad**")
            status_dist = df_filtered.groupby('OCUP300_label')['factor_expansion'].sum()
            if not status_dist.empty:
                fig, ax = plt.subplots()
                sns.barplot(x=status_dist.index, y=status_dist.values, ax=ax, palette="viridis")
                ax.set_ylabel("Población Estimada")
                plt.xticks(rotation=45)
                st.pyplot(fig)

        st.markdown("### Análisis Demográfico Adicional")
        with st.expander("Ver Distribución por Etnia y Seguro de Salud"):
            col1_demo, col2_demo = st.columns(2)
            with col1_demo:
                st.write("**Autoidentificación Étnica**")
                ethnic_dist = df_filtered.groupby('C377_label')['factor_expansion'].sum().sort_values(ascending=False)
                if not ethnic_dist.empty:
                    fig, ax = plt.subplots()
                    sns.barplot(y=ethnic_dist.index, x=ethnic_dist.values, ax=ax, orient='h', palette="plasma")
                    ax.set_xlabel("Población Estimada")
                    st.pyplot(fig)
                    st.markdown("**Interpretación:** El gráfico muestra la composición étnica, donde 'Mestizo' es predominante, reflejando la diversidad cultural de Lima.")
            with col2_demo:
                st.write("**Tipo de Seguro de Salud**")
                seguro_dist = df_filtered.groupby('SEGURO1_label')['factor_expansion'].sum().sort_values(ascending=False)
                if not seguro_dist.empty:
                    fig, ax = plt.subplots()
                    sns.barplot(y=seguro_dist.index, x=seguro_dist.values, ax=ax, orient='h', palette="magma")
                    ax.set_xlabel("Población Estimada")
                    st.pyplot(fig)
                    st.markdown("**Interpretación:** La cobertura de seguros de salud es un indicador clave. Una alta proporción de 'No Afiliado' puede ser un indicio de informalidad laboral.")

    with tab2:
        st.header("Interacción con Modelos Predictivos")
        st.subheader("1. Predicción de Ingreso Mensual (Regresión)")
        with st.expander("Use el modelo para predecir ingresos"):
            # ... (código del modelo de regresión sin cambios)
            pred_c208_reg = st.slider("Edad", 14, 80, 40)
            pred_whoraT_reg = st.slider("Horas trabajadas por semana", 0, 100, 48)
            pred_c207_reg = st.selectbox("Sexo (Regresión)", df['C207'].dropna().unique())
            pred_c366_label_reg = st.selectbox("Nivel Educativo (Regresión)", options=EDUCATION_LABELS, index=5)
            pred_periodo_reg = st.selectbox("Período (Regresión)", sorted(df['periodo'].unique()))
            if st.button("Predecir Ingreso"):
                pred_c366_reg = EDUCATION_MAP[pred_c366_label_reg]
                input_data_reg = pd.DataFrame({
                    'C207': [pred_c207_reg], 'C366': [pred_c366_reg], 'periodo': [pred_periodo_reg],
                    'C208': [pred_c208_reg], 'whoraT': [pred_whoraT_reg]
                })
                predicted_income = reg_model.predict(input_data_reg)[0]
                st.success(f"El ingreso mensual predicho es: **S/. {predicted_income:,.2f}**")

        st.subheader("2. Predicción de Riesgo de Informalidad (Clasificación)")
        with st.expander("Use el modelo para predecir informalidad"):
            # ... (código del modelo de clasificación sin cambios)
            pred_c208_class = st.slider("Edad ", 14, 80, 40)
            pred_whoraT_class = st.slider("Horas trabajadas por semana ", 0, 100, 48)
            pred_c207_class = st.selectbox("Sexo (Clasificación)", df['C207'].dropna().unique())
            pred_c366_label_class = st.selectbox("Nivel Educativo (Clasificación)", options=EDUCATION_LABELS, index=5)
            pred_periodo_class = st.selectbox("Período (Clasificación)", sorted(df['periodo'].unique()))
            if st.button("Predecir Informalidad"):
                pred_c366_class = EDUCATION_MAP[pred_c366_label_class]
                input_data_class = pd.DataFrame({
                    'C207': [pred_c207_class], 'C366': [pred_c366_class], 'periodo': [pred_periodo_class],
                    'C208': [pred_c208_class], 'whoraT': [pred_whoraT_class]
                })
                prediction = class_model.predict(input_data_class)[0]
                prediction_proba = class_model.predict_proba(input_data_class)[0][1]
                if prediction == 1:
                    st.warning(f"Predicción: **ALTO RIESGO de ser informal** (Probabilidad: {prediction_proba:.2%})")
                else:
                    st.success(f"Predicción: **BAJO RIESGO de ser informal** (Probabilidad de ser informal: {prediction_proba:.2%})")

    with tab3:
        st.header("Conclusiones y Tendencias Observadas")
        st.markdown("""
        Este análisis revela tendencias clave en el mercado laboral de Lima (2024-2025):
        - **Temporalidad como Factor Clave:** El trimestre es un predictor significativo.
        - **Dinámica del Ingreso:** Fluctuación notable en el ingreso promedio.
        - **Persistencia de la Informalidad:** Un desafío estructural persistente.
        - **Análisis Ponderado:** Todos los cálculos usan el `factor_expansion` para asegurar la validez.
        """)
        st.subheader("Evolución General del Ingreso Ponderado")
        temporal_income_data = df.dropna(subset=['INGTOT', 'factor_expansion'])
        if not temporal_income_data.empty:
            temporal_income = temporal_income_data.groupby('periodo').apply(
                lambda x: np.average(x['INGTOT'], weights=x['factor_expansion'])
            ).sort_index()
            st.line_chart(temporal_income)
            st.caption("Evolución del ingreso promedio mensual ponderado.")

    with tab4:
        st.header("Acerca del Proyecto")
        st.markdown("""
        **Objetivo del Dashboard:**
        Este dashboard interactivo es una herramienta diseñada para explorar y analizar los datos de la Encuesta Permanente de Empleo Nacional (EPEN),
        enfocándose en el mercado laboral de Lima Metropolitana durante el período 2024-2025. El objetivo es proporcionar una visión clara y accesible
        de los indicadores clave, las tendencias y las características demográficas de la fuerza laboral.

        **Fuente de Datos:**
        Los datos utilizados provienen de la **Encuesta Permanente de Empleo Nacional (EPEN)**, realizada por el Instituto Nacional de Estadística e Informática (INEI) de Perú.
        Esta encuesta recopila información detallada sobre la situación laboral, los ingresos y las características sociodemográficas de la población.

        **Metodología:**
        El análisis se basa en datos ponderados utilizando el `factor_expansion` proporcionado en la encuesta para asegurar que los resultados sean representativos
        de la población total de Lima. El dashboard incluye:
        - **Análisis Exploratorio:** Visualizaciones interactivas de indicadores como ingresos, edad, género, y más.
        - **Modelos Predictivos:** Herramientas para estimar el ingreso y el riesgo de informalidad basados en características seleccionadas.
        - **Análisis de Tendencias:** Gráficos que muestran la evolución de indicadores clave a lo largo del tiempo.

        **Desarrollado por:** [Tu Nombre/Nombre del Equipo]
        """)

if __name__ == '__main__':
    main()
