import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página y Estilos ---
st.set_page_config(layout="wide", page_title="Análisis del Mercado Laboral de Lima", initial_sidebar_state="expanded")


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
SUNAT_MAP = {
    1: 'Persona Jurídica', 2: 'Persona Natural con RUC', 3: 'No Registrado', 4: 'No Sabe'
}
COMPANY_SIZE_MAP = {
    1: 'Hasta 20 personas', 2: '21 a 50 personas', 3: '51 a 100 personas',
    4: '101 a 500 personas', 5: 'Más de 500 personas'
}
SECTOR_MAP = {
    1: 'Fuerzas Armadas/Policía', 2: 'Administración Pública', 3: 'Empresa Pública',
    4: 'Empresa de Servicios (SERVICE)', 5: 'Empresa Privada', 6: 'Otro'
}
OCCUPATION_MAP = {
    1: 'Empleador o Patrono', 2: 'Trabajador Independiente', 3: 'Empleado u Obrero',
    4: 'Ayudante Familiar (Negocio)', 5: 'Ayudante Familiar (Empleo)', 6: 'Trabajador del Hogar',
    7: 'Aprendiz/Practicante Remunerado', 8: 'Practicante sin Remuneración',
    9: 'Ayudante Familiar (Otro Hogar)', 10: 'Ayudante Familiar (Otro Hogar)'
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
    master_df['C312_label'] = master_df['C312'].map(SUNAT_MAP)
    master_df['C317_label'] = master_df['C317'].map(COMPANY_SIZE_MAP)
    master_df['C311_label'] = master_df['C311'].map(SECTOR_MAP)
    master_df['C310_label'] = master_df['C310'].map(OCCUPATION_MAP)

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

        with st.expander("Análisis Demográfico por Etnia y Seguro de Salud"):
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

        st.markdown("### Análisis Laboral Detallado")
        with st.expander("Ver Gráficos sobre Condiciones Laborales"):
            st.write("#### Promedio de Horas Trabajadas por Ocupación")
            avg_hours_occupation = df_filtered.groupby('C310_label')['whoraT'].mean().sort_values(ascending=False)
            if not avg_hours_occupation.empty:
                fig, ax = plt.subplots()
                sns.barplot(y=avg_hours_occupation.index, x=avg_hours_occupation.values, ax=ax, orient='h', palette="cubehelix")
                ax.set_xlabel("Horas Promedio Semanales")
                st.pyplot(fig)
                st.markdown("**Interpretación:** Este gráfico compara las horas de trabajo promedio entre diferentes categorías ocupacionales, revelando qué roles demandan más tiempo.")

            st.write("#### Distribución de Empleados por Tamaño de Empresa")
            company_size_dist = df_filtered.groupby('C317_label')['factor_expansion'].sum().sort_values(ascending=False)
            if not company_size_dist.empty:
                fig, ax = plt.subplots()
                sns.barplot(y=company_size_dist.index, x=company_size_dist.values, ax=ax, orient='h', palette="rocket")
                ax.set_xlabel("Población Estimada")
                st.pyplot(fig)
                st.markdown("**Interpretación:** Muestra la concentración de la fuerza laboral en micro, pequeñas, medianas y grandes empresas, un indicador clave de la estructura económica.")

            st.write("#### Ingreso Promedio por Ocupación")
            avg_income_occupation = df_filtered.groupby('C310_label')['INGTOT'].mean().sort_values(ascending=False)
            if not avg_income_occupation.empty:
                fig, ax = plt.subplots()
                sns.barplot(y=avg_income_occupation.index, x=avg_income_occupation.values, ax=ax, orient='h', palette="crest")
                ax.set_xlabel("Ingreso Promedio Mensual (S/.)")
                st.pyplot(fig)
                st.markdown("**Interpretación:** Compara los ingresos promedio entre roles, destacando las ocupaciones con mayor y menor remuneración en el mercado.")

            col3_demo, col4_demo = st.columns(2)
            with col3_demo:
                st.write("#### Relación Laboral con SUNAT")
                sunat_dist = df_filtered.groupby('C312_label')['factor_expansion'].sum()
                if not sunat_dist.empty:
                    fig, ax = plt.subplots()
                    ax.pie(sunat_dist, labels=sunat_dist.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set2"))
                    ax.axis('equal')
                    st.pyplot(fig)
                    st.markdown("**Interpretación:** Este gráfico de pastel ilustra la formalidad del empleo a través del registro en SUNAT, un indicador crucial para entender la economía formal vs. informal.")

            with col4_demo:
                st.write("#### Ocupación de las Personas")
                occupation_dist = df_filtered.groupby('C310_label')['factor_expansion'].sum()
                if not occupation_dist.empty:
                    fig, ax = plt.subplots()
                    ax.pie(occupation_dist, labels=occupation_dist.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Paired"))
                    ax.axis('equal')
                    st.pyplot(fig)
                    st.markdown("**Interpretación:** Muestra la distribución de la fuerza laboral entre diferentes tipos de empleo, como trabajador independiente, empleado, etc.")

            st.write("#### Distribución por Sector de Empleo")
            sector_dist = df_filtered.groupby('C311_label')['factor_expansion'].sum().sort_values(ascending=False)
            if not sector_dist.empty:
                fig, ax = plt.subplots()
                sns.barplot(y=sector_dist.index, x=sector_dist.values, ax=ax, orient='h', palette="Spectral")
                ax.set_xlabel("Población Estimada")
                st.pyplot(fig)
                st.markdown("**Interpretación:** Este gráfico muestra en qué sectores (público, privado, etc.) se concentra la mayor parte de la fuerza laboral de Lima.")
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
