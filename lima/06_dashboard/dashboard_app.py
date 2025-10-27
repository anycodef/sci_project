import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Análisis del Mercado Laboral de Lima")

# --- Constants and Paths ---
DATA_PATH = '../02_preparacion_y_limpieza/lima_cleaned_unified.csv'
# NOTE: Model paths are placeholders until models are retrained.
# MODEL_DIR = '../05_modelado'
# REG_MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_regresion_lima', 'modelo_regresion.joblib')
# CLASS_MODEL_PATH = os.path.join(MODEL_DIR, 'modelo_clasificacion_lima', 'modelo_clasificacion.joblib')

# --- Data Loading and Caching ---
@st.cache_data
def load_and_prepare_data(path):
    """Loads the unified and cleaned dataset and prepares it for the dashboard."""
    if not os.path.exists(path):
        st.error(f"Error: El archivo de datos no se encontró en la ruta: {path}")
        return pd.DataFrame()

    df = pd.read_csv(path, low_memory=False)

    # --- Data Recoding for Visualization ---
    df['sexo'] = df['c207'].map({1: 'Hombre', 2: 'Mujer'}).astype('category')

    # Define employment status, including a category for underemployment
    # ocup300 -> 1:Ocupado, 2:Desocupado, 4:Inactivo
    # p209h -> 1:Sí (quiere y puede trabajar más horas), 2:No
    df['condicion_actividad'] = df['ocup300'].map({
        1: 'Ocupado', 2: 'Desocupado', 3: 'Desocupado', 4: 'Inactivo'
    }).astype('category')

    # Define informality (simplified: not contributing to ESSALUD)
    # c361_1 -> 1:Sí afiliado a ESSALUD, 2:No
    df['es_informal'] = np.where((df['condicion_actividad'] == 'Ocupado') & (df['c361_1'] == 2), 1, 0)

    # Convert key columns to numeric, coercing errors
    numeric_cols = ['ingtot', 'c208', 'factor_expansion', 'whorat']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.rename(columns={'c208': 'edad'}, inplace=True)

    return df

# Load the data
master_df = load_and_prepare_data(DATA_PATH)

# --- UI Layout ---
st.title("Dashboard de Análisis del Mercado Laboral de Lima (2024-2025)")

if master_df.empty:
    st.warning("No se pudieron cargar los datos. El dashboard no puede continuar.")
else:
    tab1, tab2, tab3 = st.tabs(["Explorador de Lima", "Modelos Predictivos (Platzhalter)", "Análisis Temporal y Conclusiones"])

    # --- Tab 1: Interactive Explorer ---
    with tab1:
        st.header("Análisis Exploratorio Interactivo")

        period_list = ['Todos'] + sorted(master_df['trimestre'].unique().tolist())
        selected_period = st.selectbox("Seleccione un Trimestre para analizar:", period_list)

        df_filtered = master_df if selected_period == 'Todos' else master_df[master_df['trimestre'] == selected_period]

        st.markdown("### Indicadores Clave Ponderados")

        def get_weighted_kpis(data):
            # Safe division helper
            def safe_avg(values, weights):
                return np.average(values, weights=weights) if not values.empty and weights.sum() > 0 else 0

            # Filter data for valid calculations
            income_data = data.dropna(subset=['ingtot', 'factor_expansion'])
            age_data = data.dropna(subset=['edad', 'factor_expansion'])
            activity_data = data.dropna(subset=['condicion_actividad', 'factor_expansion'])

            # Calculate KPIs
            total_pop = activity_data['factor_expansion'].sum()
            ocupados_pop = activity_data[activity_data['condicion_actividad'] == 'Ocupado']['factor_expansion'].sum()
            desocupados_pop = activity_data[activity_data['condicion_actividad'] == 'Desocupado']['factor_expansion'].sum()

            pea_pop = ocupados_pop + desocupados_pop
            tasa_desempleo = (desocupados_pop / pea_pop * 100) if pea_pop > 0 else 0

            informal_data = data[(data['condicion_actividad'] == 'Ocupado')].dropna(subset=['es_informal', 'factor_expansion'])
            tasa_informalidad = safe_avg(informal_data['es_informal'], informal_data['factor_expansion']) * 100

            return {
                'ingreso_promedio': safe_avg(income_data['ingtot'], income_data['factor_expansion']),
                'edad_promedio': safe_avg(age_data['edad'], age_data['factor_expansion']),
                'tasa_desempleo': tasa_desempleo,
                'tasa_informalidad': tasa_informalidad
            }

        kpis = get_weighted_kpis(df_filtered)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Ingreso Promedio", f"S/. {kpis['ingreso_promedio']:,.2f}")
        col2.metric("Edad Promedio", f"{kpis['edad_promedio']:.1f} años")
        col3.metric("Tasa de Desempleo", f"{kpis['tasa_desempleo']:.1f}%")
        col4.metric("Tasa de Informalidad", f"{kpis['tasa_informalidad']:.1f}%")

        st.markdown("### Visualizaciones Demográficas y Educativas")
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.write("Distribución de Edad (Ponderada)")
            age_dist_data = df_filtered.dropna(subset=['edad', 'factor_expansion'])
            fig, ax = plt.subplots()
            sns.histplot(data=age_dist_data, x='edad', weights='factor_expansion', bins=20, kde=True, ax=ax)
            ax.set_title("Distribución de Edad en la Población")
            st.pyplot(fig)

        with fig_col2:
            st.write("Distribución por Nivel Educativo (Ponderado)")
            edu_dist_data = df_filtered.dropna(subset=['nivel_educativo_agrupado', 'factor_expansion'])
            edu_dist = edu_dist_data.groupby('nivel_educativo_agrupado')['factor_expansion'].sum().sort_values()
            fig, ax = plt.subplots()
            sns.barplot(y=edu_dist.index, x=edu_dist.values, ax=ax, orient='h')
            ax.set_title("Población por Nivel Educativo")
            ax.set_xlabel("Población Estimada")
            st.pyplot(fig)

    # --- Tab 2: Predictive Models (Placeholder) ---
    with tab2:
        st.header("Interacción con Modelos Predictivos")
        st.info("Los modelos de predicción se integrarán en esta pestaña una vez que se hayan reentrenado con el conjunto de datos unificado y mejorado.")
        st.markdown("""
        **Funcionalidades Planeadas:**
        - **Predicción de Ingreso Mensual:** Un formulario interactivo para estimar el ingreso de una persona basado en su edad, sexo, nivel educativo y horas de trabajo.
        - **Predicción de Riesgo de Informalidad:** Una herramienta para evaluar la probabilidad de que un perfil laboral sea informal.
        """)

    # --- Tab 3: Temporal Analysis and Conclusions ---
    with tab3:
        st.header("Análisis Temporal y Conclusiones")

        # Prepare temporal data
        temporal_data = master_df.groupby('trimestre').apply(get_weighted_kpis).apply(pd.Series).reset_index()

        st.subheader("Evolución de Indicadores Clave (2024-2025)")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Plot unemployment and informality rates
        ax1.plot(temporal_data['trimestre'], temporal_data['tasa_desempleo'], marker='o', linestyle='-', label='Tasa de Desempleo (%)')
        ax1.plot(temporal_data['trimestre'], temporal_data['tasa_informalidad'], marker='s', linestyle='--', label='Tasa de Informalidad (%)')
        ax1.set_title("Evolución de Tasas de Desempleo e Informalidad")
        ax1.set_ylabel("Tasa (%)")
        ax1.legend()
        ax1.grid(True)

        # Plot average income
        ax2.plot(temporal_data['trimestre'], temporal_data['ingreso_promedio'], marker='^', linestyle='-', color='green', label='Ingreso Promedio (S/.)')
        ax2.set_title("Evolución del Ingreso Promedio Mensual")
        ax2.set_ylabel("Ingreso (S/.)")
        ax2.legend()
        ax2.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.subheader("Comparación: Primer vs. Último Trimestre")
        first_quarter = temporal_data.iloc[0]
        last_quarter = temporal_data.iloc[-1]

        comp_df = pd.DataFrame({
            'Indicador': ['Ingreso Promedio', 'Tasa de Desempleo', 'Tasa de Informalidad'],
            'Primer Trimestre': [first_quarter['ingreso_promedio'], first_quarter['tasa_desempleo'], first_quarter['tasa_informalidad']],
            'Último Trimestre': [last_quarter['ingreso_promedio'], last_quarter['tasa_desempleo'], last_quarter['tasa_informalidad']]
        }).set_index('Indicador')

        st.table(comp_df.style.format("{:.2f}"))

        st.markdown("""
        ### Conclusiones Preliminares
        - **Dinámicas Temporales:** Se observa una clara variación en los indicadores clave a lo largo de los trimestres, subrayando la importancia del análisis temporal.
        - **Desafíos Persistentes:** La informalidad y el desempleo muestran fluctuaciones, pero se mantienen como características estructurales del mercado laboral de Lima.
        - **Impacto de la Educación:** El análisis exploratorio sugiere una fuerte correlación entre el nivel educativo y los ingresos, un área que los modelos predictivos explorarán más a fondo.
        """)

