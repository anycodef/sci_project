import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración y Carga de Datos/Modelos ---
st.set_page_config(layout="wide", page_title="Análisis del Mercado Laboral de Lima")

DATA_DIR = '../02_preparacion_y_limpieza'
MODEL_DIR = '../05_modelado'
REG_MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_regresion_lima', 'modelo_regresion.joblib')
CLASS_MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_clasificacion_lima', 'modelo_clasificacion.joblib')

# Mapeo de Nivel Educativo para la UI
EDUCATION_MAP = {
    'Sin nivel': 1, 'Educ. Inicial': 2, 'Primaria Incompleta': 3, 'Primaria Completa': 4,
    'Secundaria Incompleta': 5, 'Secundaria Completa': 6, 'Básica Especial': 7,
    'Superior No Univ. Incompleta': 8, 'Superior No Univ. Completa': 9,
    'Superior Univ. Incompleta': 10, 'Superior Univ. Completa': 11, 'Maestría/Doctorado': 12
}
EDUCATION_LABELS = list(EDUCATION_MAP.keys())

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

    files = sorted([f for f in os.listdir(DATA_DIR) if f.startswith('lima_cleaned_')])
    df_list = []
    for f in files:
        df = pd.read_csv(os.path.join(DATA_DIR, f), low_memory=False)
        df['periodo'] = extract_period_from_filename(f)
        df_list.append(df)

    master_df = pd.concat(df_list, ignore_index=True)

    # Recodificación
    master_df['C207'] = master_df['C207'].map({1: 'Hombre', 2: 'Mujer'})
    master_df['OCUP300_label'] = master_df['OCUP300'].map({1: 'Ocupado', 2: 'Desocupado', 3: 'Desocupado', 4: 'Inactivo'})
    master_df['es_informal'] = np.where((master_df['OCUP300'] == 1) & (master_df['C361_1'] == 2), 1, 0)

    # Conversión a numérico
    for col in ['INGTOT', 'C208', 'factor_expansion', 'whoraT', 'C366']:
        master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

    return master_df

@st.cache_resource
def load_model(path):
    """Carga un modelo desde un archivo .joblib."""
    return joblib.load(path)

# Cargar todo al inicio
df = load_data()
reg_model = load_model(REG_MODEL_PATH)
class_model = load_model(CLASS_MODEL_PATH)

# --- UI del Dashboard ---
st.title("Dashboard de Análisis del Mercado Laboral de Lima (2024-2025)")

tab1, tab2, tab3 = st.tabs(["Explorador de Lima", "Modelos Predictivos", "Conclusiones y Evolución"])

# --- Pestaña 1: Explorador de Lima ---
with tab1:
    st.header("Análisis Exploratorio Interactivo")

    period_list = ['Todos'] + sorted(df['periodo'].unique().tolist())
    selected_period = st.selectbox("Seleccione un Trimestre para analizar:", period_list)

    if selected_period == 'Todos':
        df_filtered = df
        st.subheader("Mostrando datos para todos los períodos")
    else:
        df_filtered = df[df['periodo'] == selected_period]
        st.subheader(f"Mostrando datos para el período: {selected_period}")

    st.markdown("### Indicadores Clave Ponderados")

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

    kpis = get_weighted_kpis(df_filtered)

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingreso Promedio Mensual", f"S/. {kpis['avg_income']:,.2f}")
    col2.metric("Edad Promedio", f"{kpis['avg_age']:.1f} años")
    col3.metric("Tasa de Informalidad (Ocupados)", f"{kpis['informality_rate']:.1f}%")

    st.markdown("### Visualizaciones")
    col1_fig, col2_fig = st.columns(2)

    with col1_fig:
        st.write("Distribución de Género (Ponderada)")
        gender_dist = df_filtered.groupby('C207')['factor_expansion'].sum()
        if not gender_dist.empty:
            fig, ax = plt.subplots()
            ax.pie(gender_dist, labels=gender_dist.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

    with col2_fig:
        st.write("Distribución de Condición de Actividad (Ponderada)")
        status_dist = df_filtered.groupby('OCUP300_label')['factor_expansion'].sum()
        if not status_dist.empty:
            fig, ax = plt.subplots()
            sns.barplot(x=status_dist.index, y=status_dist.values, ax=ax)
            ax.set_ylabel("Población Estimada")
            plt.xticks(rotation=45)
            st.pyplot(fig)


# --- Pestaña 2: Modelos Predictivos ---
with tab2:
    st.header("Interacción con Modelos Predictivos")

    st.subheader("1. Predicción de Ingreso Mensual (Regresión)")
    with st.expander("Use el modelo para predecir ingresos"):
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

# --- Pestaña 3: Conclusiones y Evolución ---
with tab3:
    st.header("Conclusiones y Tendencias Observadas")

    st.markdown("""
    Este análisis del mercado laboral de Lima para el período 2024-2025 revela varias tendencias clave:
    - **Temporalidad como Factor Clave:** El análisis demuestra que el trimestre (`periodo`) es un predictor significativo.
    - **Dinámica del Ingreso:** Se observa una fluctuación notable en el ingreso promedio ponderado a lo largo de los trimestres.
    - **Persistencia de la Informalidad:** La tasa de informalidad se mantiene como un desafío estructural.
    - **Importancia del Análisis Ponderado:** Todos los cálculos utilizan el `factor_expansion` para asegurar la validez de las conclusiones.
    """)

    st.subheader("Evolución General del Ingreso Ponderado")
    temporal_income_data = df.dropna(subset=['INGTOT', 'factor_expansion'])
    if not temporal_income_data.empty:
        temporal_income = temporal_income_data.groupby('periodo').apply(
            lambda x: np.average(x['INGTOT'], weights=x['factor_expansion'])
        ).sort_index()
        st.line_chart(temporal_income)
        st.caption("Gráfico de la evolución del ingreso promedio mensual ponderado a lo largo de los 6 trimestres analizados.")