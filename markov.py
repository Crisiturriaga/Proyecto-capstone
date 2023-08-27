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

# Diccionario para almacenar las secuencias climáticas
weather_sequences = {}
for index, row in data.iterrows():
    uva_type = row['Tipo Uva']
    optimal_day = row['Dia optimo cosecha estimado inicialmente']
    probability_dry_to_rain = row['Prob de lluvia (seca a lluvia)']
    probability_rain_to_rain = row['Prob de lluvia (lluvia a lluvia)']
    
    # Generar secuencia hasta el día de cosecha estimado
    sequence = generate_weather_sequence(probability_dry_to_rain, probability_rain_to_rain, optimal_day)
    
    # Generar secuencia para los próximos 7 días después del día de cosecha estimado
    future_sequence = generate_weather_sequence(probability_dry_to_rain, probability_rain_to_rain, 7)
    
    weather_sequences[uva_type] = {
        'Ultimos 7 días': sequence[-7:],
        'Próximos 7 días': future_sequence
    }

# Imprimir el diccionario con las secuencias climáticas
for uva_type, sequences in weather_sequences.items():
    print(f"Tipo de Uva: {uva_type}")
    print(f"Últimos 7 días: {sequences['Ultimos 7 días']}")
    print(f"Próximos 7 días: {sequences['Próximos 7 días']}\n")
