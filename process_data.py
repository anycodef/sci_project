import pandas as pd
import numpy as np
import os

def get_recode_maps():
    """Returns dictionaries for recoding variables based on the data dictionary."""
    maps = {
        'REGION': {1: 'Lima Metropolitana', 2: 'Resto Urbano', 3: 'Rural'},
        'C203': {
            1: 'Jefe/a', 2: 'Esposo/a o compañero/a', 3: 'Hijo/a o hijastro/a',
            4: 'Yerno o Nuera', 5: 'Nieto/a', 6: 'Padre / madre / suegro/a',
            7: 'Hermano/a', 8: 'Otro pariente', 9: 'Trabajador/a del hogar',
            10: 'Pensionista', 11: 'Otro no pariente', 98: 'No residente'
        },
        'C207': {1: 'Hombre', 2: 'Mujer'},
        'C310': {
            1: 'Empleador o patrono', 2: 'Trabajador independiente', 3: 'Empleado u obrero',
            4: 'Ayudante en un negocio de la familia', 5: 'Ayudante en el empleo de un familiar',
            6: 'Trabajador del hogar', 7: 'Aprendiz/practicante remunerado',
            8: 'Practicante sin remuneración', 9: 'Ayudante en un negocio de la familia de otro hogar',
            10: 'Ayudante en el empleo de un familiar de otro hogar'
        },
        'C311': {
            1: 'Fuerzas Armadas, Policía Nacional del Perú (militares)',
            2: 'Administración pública', 3: 'Empresa pública',
            4: 'Empresas especiales de servicios (SERVICE)', 5: 'Empresa o patrono privado',
            6: 'Otra'
        },
        'C312': {
            1: 'Persona jurídica (Sociedad Anónima SRL, Sociedad Civil, EIRL o Asociación, etc.)',
            2: 'Persona Natural con RUC (RUS, RER, u otro régimen)',
            3: 'NO ESTA REGISTRADO (no tiene RUC)', 4: 'NO SABE (solo para dependientes)'
        },
        'C366': {
            1: 'Sin nivel', 2: 'Educación Inicial', 3: 'Primaria incompleta',
            4: 'Primaria completa', 5: 'Secundaria incompleta', 6: 'Secundaria completa',
            7: 'Básica especial', 8: 'Superior no universitaria incompleta',
            9: 'Superior no universitaria completa', 10: 'Superior universitaria incompleta',
            11: 'Superior universitaria completa', 12: 'Maestria/Doctorado'
        },
        'OCUP300': {
            0: 'Sin información', 1: 'Ocupado', 2: 'Desocupado abierto', 3: 'Desocupado oculto', 4: 'Inactivo pleno'
        }
    }
    return maps

def process_data():
    # --- Phase 1: Data Loading and Unification ---
    files = [f for f in os.listdir('Empleabilidad') if f.endswith('.csv')]
    quarters = {
        'Trim Ene-Feb-Mar24.csv': '2024-Q1', 'Trim Abr-May-Jun24.csv': '2024-Q2',
        'Trim Jul-Ago-Set24.csv': '2024-Q3', 'Trim Set-Oct-Nov24.csv': '2024-Q4',
        'Trim Ene-Feb-Mar25.csv': '2025-Q1', 'Trim Mar-Abr-May25.csv': '2025-Q2'
    }

    df_list = []
    for file in files:
        df = pd.read_csv(os.path.join('Empleabilidad', file), low_memory=False)
        df['periodo'] = quarters[file]
        df_list.append(df)

    master_df = pd.concat(df_list, ignore_index=True)

    # --- Data Type Conversion ---
    master_df['C208'] = pd.to_numeric(master_df['C208'], errors='coerce')
    fa_cols = [col for col in master_df.columns if col.startswith('fa_')]
    for col in fa_cols:
        master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

    # --- Unify and Adjust Expansion Factor ---
    master_df['factor_expansion'] = master_df[fa_cols].sum(axis=1)
    master_df['factor_ajustado'] = master_df['factor_expansion'] / len(files)
    master_df.drop(columns=fa_cols, inplace=True)

    # --- Phase 2: Data Segregation ---
    master_df.dropna(subset=['C208'], inplace=True)
    poblacion_trabajo_df = master_df[master_df['C208'] >= 14].copy()
    poblacion_no_trabajo_df = master_df[master_df['C208'] < 14].copy()

    # --- Phase 3: Cleaning poblacion_trabajo_df ---
    maps = get_recode_maps()
    for var, mapping in maps.items():
        if var in poblacion_trabajo_df.columns:
            poblacion_trabajo_df[var] = poblacion_trabajo_df[var].map(mapping)

    # Handle Nulls with 'No Aplica'
    not_employed_condition = poblacion_trabajo_df['OCUP300'] != 'Ocupado'

    cols_to_fill = []
    for col in poblacion_trabajo_df.columns:
        if col.startswith('C3'):
            try:
                if int(col.split('_')[0][1:]) >= 308:
                    cols_to_fill.append(col)
            except ValueError:
                continue # Skip columns like C300n

    cols_to_fill.extend([col for col in poblacion_trabajo_df.columns if col.startswith('I3') or col.startswith('D3')])
    cols_to_fill.extend(['INGTOT', 'INGTOTP', 'ingtrabw', 'whoraT'])
    for col in cols_to_fill:
        if col in poblacion_trabajo_df.columns:
            poblacion_trabajo_df.loc[not_employed_condition, col] = 'No Aplica'

    # Feature Engineering: grupo_edad
    bins = [14, 18, 25, 35, 45, 55, 65, np.inf]
    labels = ['14-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    poblacion_trabajo_df['grupo_edad'] = pd.cut(poblacion_trabajo_df['C208'], bins=bins, labels=labels, right=False)

    # Feature Engineering: es_informal
    poblacion_trabajo_df['es_informal'] = 0
    poblacion_trabajo_df.loc[(poblacion_trabajo_df['OCUP300'] == 'Ocupado') & (poblacion_trabajo_df['C361_1'] == 2), 'es_informal'] = 1

    # --- Phase 4: Cleaning poblacion_no_trabajo_df ---
    # Prune irrelevant columns
    try:
        c300n_index = list(poblacion_no_trabajo_df.columns).index('C300n')
        cols_to_keep = list(poblacion_no_trabajo_df.columns[:c300n_index])
        cols_to_keep.extend(['periodo', 'factor_expansion', 'factor_ajustado'])
        poblacion_no_trabajo_df = poblacion_no_trabajo_df[cols_to_keep]
    except ValueError:
        pass # C300n not found

    for var, mapping in maps.items():
        if var in poblacion_no_trabajo_df.columns and var != 'OCUP300':
            poblacion_no_trabajo_df[var] = poblacion_no_trabajo_df[var].map(mapping)

    # --- Final Output ---
    poblacion_trabajo_df.to_csv('datos_limpios_poblacion_trabajo.csv', index=False)
    poblacion_no_trabajo_df.to_csv('datos_limpios_poblacion_no_trabajo.csv', index=False)

if __name__ == '__main__':
    process_data()
