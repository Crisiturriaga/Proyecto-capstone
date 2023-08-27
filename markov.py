import pandas as pd
import numpy as np

# Paso 1: Leer los datos desde el archivo CSV
data = pd.read_csv('promedios_tipo_uva.csv')

# Paso 2: Truncar los valores del día óptimo
data['Dia optimo cosecha estimado inicialmente'] = data['Dia optimo cosecha estimado inicialmente'].astype(int)

# Paso 3: Crear una cadena de Markov de dos etapas

# Función para generar secuencia de estados basada en las probabilidades
def generate_weather_sequence(probability_dry_to_rain, probability_rain_to_rain, length):
    sequence = [0]  # Comenzar con día seco
    for _ in range(1, length):
        prev_state = sequence[-1]
        if prev_state == 0:
            transition_probs = [1 - probability_dry_to_rain, probability_dry_to_rain]
        else:
            transition_probs = [1 - probability_rain_to_rain, probability_rain_to_rain]
        new_state = np.random.choice([0, 1], p=transition_probs)
        sequence.append(new_state)
    return sequence

weather_sequences = {}
for index, row in data.iterrows():
    uva_type = row['Tipo Uva']
    optimal_day = row['Dia optimo cosecha estimado inicialmente']
    probability_dry_to_rain = row['Prob de lluvia (seca a lluvia)']
    probability_rain_to_rain = row['Prob de lluvia (lluvia a lluvia)']
    
    sequence = generate_weather_sequence(probability_dry_to_rain, probability_rain_to_rain, optimal_day)
    weather_sequences[uva_type] = sequence

# Paso 5: Tomar solo los últimos 7 días de cada lote
last_7_days_sequences = {uva_type: sequence[-7:] for uva_type, sequence in weather_sequences.items()}

# Imprimir el diccionario con las secuencias de los últimos 7 días para cada tipo de uva
for uva_type, sequence in last_7_days_sequences.items():
    print(f"Tipo de Uva: {uva_type}, Últimos 7 días: {sequence}")
