import sqlite3
import random
import numpy as np

# Crear una conexión a la base de datos
conn = sqlite3.connect('vinos.db')
c = conn.cursor()

periodo_ideal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
calidades = [[0.85, 0.95],[0.92, 0.93],[0.91, 0.87],[0.95, 0.95],[0.85, 0.85],[0.93, 0.94]]
umbrales = [0.8, 0.75, 0.8, 0.7, 0.8, 0.7]

# Función para predecir el clima con markov
def predecir_clima(dia_optimo, prob_seco_lluvia, prob_lluvia_lluvia):
    clima_prediccion = []  # Lista para almacenar la predicción
    tipo_3 = []
    
    # Inicializar el primer día como seco
    clima_prediccion.append(0)
    
    # Calcular predicciones para los siguientes 18 días (13 días previos + 5 días de desviación)
    for _ in range(18):
        if clima_prediccion[-1] == 0:  # Si el día anterior fue seco
            clima_prediccion.append(1 if random.random() < prob_seco_lluvia else 0)
            tipo_3.append(0)
        else:  # Si el día anterior fue lluvioso
            clima_prediccion.append(1 if random.random() < prob_lluvia_lluvia else 0)
            if clima_prediccion[-1] == 1:
                tipo_3.append(1 if random.random() <= 0.05 else 0)
            
    
    return clima_prediccion, tipo_3

def calcular_coeficientes_parabola(q_t_minus, q_t_plus):
    # funcion que entrega los valores de a, b y c para utilizar en la ecuacion de calidad
    t_minus = -7
    t_plus = 7
    A = np.array([
        [t_minus**2, t_minus, 1],
        [0, 0, 1],
        [t_plus**2, t_plus, 1]])
    b = np.array([q_t_minus, 1, q_t_plus])
    coefficients = np.linalg.solve(A, b)
    a, b, c = coefficients
    return a, b, c

def dia_estimado():
        # Funcion que estima el dia de cosecha con media 0 y desv est 2
        optimal_day = np.random.normal(0, 2)
        return int(round(optimal_day))

def calidad(q_t_minus, q_t_plus, a, b, c):
    # Entrega la calidad
    t_optimal = dia_estimado()
    def funcion_calidad(a, b, c, t):
        # funcion de calidad bajo el supuesto que no llueve, para modificar en el futuro
        return max(min(a * t**2 + b * t + c, 1), 0)
    a, b, c = calcular_coeficientes_parabola(q_t_minus, q_t_plus)
    q_t_optimal = funcion_calidad(a, b, c, t_optimal)
    return q_t_optimal, t_optimal

def calidad_final(q_t_minus, q_t_plus):
    a, b, c = calcular_coeficientes_parabola(q_t_minus, q_t_plus)
    quality, t_optimal = calidad(q_t_minus, q_t_plus, a, b, c)
    return quality, t_optimal

def uva(uva):
    if uva == 'C1':
        return calidades[0]
    elif uva == 'C2':
        return calidades[1]
    elif uva == 'C3':
        return calidades[2]
    elif uva == 'C4':
        return calidades[3]
    elif uva == 'C5':
        return calidades[4]
    elif uva == 'C6':
        return calidades[5]
    
def umbral_uva(uva):
    if uva == 'C1':
        return umbrales[0]
    elif uva == 'C2':
        return umbrales[1]
    elif uva == 'C3':
        return umbrales[2]
    elif uva == 'C4':
        return umbrales[3]
    elif uva == 'C5':
        return umbrales[4]
    elif uva == 'C6':
        return umbrales[5]

### Para calcular los coeficientes llamar a la funcion "calcular_coeficientes_parabola(q_t_minus, q_t_plus)" siendo
### el q_t_minus = q[t-7] y el otro q[t+7].
### Para obtener la calidad simplemente llamar a calidad(q_t_minus, q_t_plus, a, b, c), usando los coeficientes de
### la funcion anterior.

# Funciones para tomar decisiones
def decidir_contrato(lote):
    # Implementa lógica para decidir tipo de contrato y cantidad a comprar
    pass

def asignar_lote_a_planta(lote):
    # Implementa lógica para asignar lote a planta y cantidad
    pass

def calcular_proporciones_vinos(lotes):
    # Implementa lógica para calcular proporciones de vinos
    pass

def decidir_arriendo_tanques():
    # Implementa lógica para decidir cuántos tanques alquilar
    pass

def decidir_almacenamiento_camion():
    # Implementa lógica para decidir cantidad a almacenar en camión
    pass

def almacenamiento_barricas(mezclas_vinos):
    # Implementa lógica para decidir almacenamiento en barricas
    pass

def gestion_calidad(lote):
    # Implementa lógica para tomar decisiones sobre corrección de calidad
    pass

# Función objetivo
def objetivo(decisiones):
    # Implementa cálculo del objetivo basado en decisiones tomadas
    pass
# Simulación de toma de decisiones y restricciones
def simular():
    conn = sqlite3.connect('vinos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM lotes')
    lotes = c.fetchall()
    contador = 0
    litros_totales = 0
    for t in range(50, 160):
        for lote in lotes:
            lote_id, lote_cod, lote_numero, lote_tipo_uva, lote_toneladas, lote_dia_optimo, lote_prob_seco_lluvia, lote_prob_lluvia_lluvia, lote_precio_usd = lote
            if t == lote_dia_optimo:
                contador += 1
                calidad_lote = uva(lote_tipo_uva)
                q_menos_7 = calidad_lote[0]
                q_mas_7 = calidad_lote[1]
                calidad_lote, t_optimal = calidad_final(q_menos_7, q_mas_7)
                print(f'lote: {lote_cod}')
                print(lote_dia_optimo)
                print(t_optimal)
                lote_dia_optimo += t_optimal
                print(lote_dia_optimo)
                print(calidad_lote)
                umbral_calidad_uva = umbral_uva(lote_tipo_uva)
                if calidad_lote >= umbral_calidad_uva:
                    #Calidad en buen estado, pasa a fermentacion
                    kilos_lote = lote_toneladas*1000
                    litros_vino = kilos_lote*0.5
                    litros_totales += litros_vino
                    

                    pass
                elif umbral_calidad_uva > calidad_lote >= 0.5:
                    # Calidad piola, se recupera 30%
                    pass
                elif 0.5> calidad_lote:
                    # calidad mala, se recupera el 5%
                    pass
                
            else:
                pass

        '''
        # Calcular predicción climática
        dia_optimo_prediccion, tipo_3 = predecir_clima(lote_dia_optimo, lote_prob_seco_lluvia, lote_prob_lluvia_lluvia)
        
        # Imprimir resultados
        print(f"Lote: {lote_cod}")
        # en dia_optimo_prediccion[12] está el día óptimo
        print(f"Predicción climática: {dia_optimo_prediccion}")
        print(f'prediccion tipo 3: {tipo_3}')'''

    print(litros_totales)
    botellas = litros_totales/0.75
    print(botellas)
    print(f'contador: {contador}')


    conn.close()

# Ejecutar la simulación
simular()