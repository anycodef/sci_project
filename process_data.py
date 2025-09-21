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

    # --- Phase 2.A: Identification and Mapping of Special Codes (Outlier Sanitization) ---
    codes_to_nan = {
        'C208': [99],
        'C301_DIA': [99],
        'C301_MES': [99],
        'C301_ANIO': [9999],
        'C303': [9],
        'C304': [9],
        'C305': [9],
        'C308_COD': [9999],
        'C309_COD': [9999],
        'C317A': [9999],
        'C318_1': [99], 'C318_2': [99], 'C318_3': [99], 'C318_4': [99],
        'C318_5': [99], 'C318_6': [99], 'C318_7': [99], 'C318_T': [99],
        'C328_T': [99],
        'whoraT': [99],
        'C331': [999],
        'C339_1': [999999], 'I339_1': [999999],
        'C341_T': [999999], 'D341_T': [999999],
        'C342': [999999], 'I342': [999999],
        'C344': [999999], 'D344': [999999],
        'C345_1': [999999], 'I345_1': [999999],
        'C347_T': [999999], 'D347_T': [999999],
        'C348': [999999], 'I348': [999999],
        'C350': [999999], 'D350': [999999],
        'C366_1': [99],
        'C366_2': [99],
        'INGTOT': [999999],
        'INGTOTP': [999999],
        'INGTRABW': [999999]
    }

    for column, codes in codes_to_nan.items():
        if column in master_df.columns:
            master_df[column] = master_df[column].replace(codes, np.nan)

    # --- Data Type Conversion ---
    numeric_columns = [
        'C208', 'C301_DIA', 'C301_MES', 'C301_ANIO', 'C308_COD', 'C309_COD',
        'C317A', 'C318_1', 'C318_2', 'C318_3', 'C318_4', 'C318_5', 'C318_6',
        'C318_7', 'C318_T', 'C328_T', 'whoraT', 'C331', 'C339_1', 'I339_1',
        'C341_T', 'D341_T', 'C342', 'I342', 'C344', 'D344', 'C345_1', 'I345_1',
        'C347_T', 'D347_T', 'C348', 'I348', 'C350', 'D350', 'C366_1', 'C366_2',
        'INGTOT', 'INGTOTP', 'INGTRABW'
    ]
    fa_cols = [col for col in master_df.columns if col.startswith('fa_')]
    numeric_columns.extend(fa_cols)

    for col in numeric_columns:
        if col in master_df.columns:
            master_df[col] = pd.to_numeric(master_df[col], errors='coerce')

    # --- Unify and Adjust Expansion Factor ---
    master_df['factor_expansion'] = master_df[fa_cols].sum(axis=1)
    master_df['factor_ajustado'] = master_df['factor_expansion'] / len(files)
    master_df.drop(columns=fa_cols, inplace=True)

    # --- Phase 2: Data Segregation ---
    # Note: We don't need to explicitly drop rows with NaN in 'C208' because
    # the filtering conditions below (`>= 14` and `< 14`) will not be met
    # for NaN values, so these rows are automatically excluded from both
    # `poblacion_trabajo_df` and `poblacion_no_trabajo_df`.
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
