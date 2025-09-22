import csv
import json

csv_file = 'data.csv'
json_file = 'data.json'

data = []
with open(csv_file, 'r') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        # Only select a few columns to keep the file size small
        # and filter out rows with "No Aplica"
        if row['periodo'] != 'No Aplica' and row['INGTOT'] != 'No Aplica':
            selected_row = {
                'periodo': row['periodo'],
                'sexo': row['C207'],
                'nivel_educativo': row['C366'],
                'ingreso': float(row['INGTOT']) if row['INGTOT'] else 0,
                'informal': int(row['es_informal']),
                'ocupacion': row['OCUP300'],
                'grupo_edad': row['grupo_edad'],
                'horas_trabajadas': int(float(row['whoraT'])) if row['whoraT'] else 0,
            }
            data.append(selected_row)

with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f'Successfully converted {csv_file} to {json_file}')
