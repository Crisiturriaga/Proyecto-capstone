import sqlite3
import random
import numpy as np

# Crear una conexión a la base de datos
conn = sqlite3.connect('vinos.db')
c = conn.cursor()

periodo_ideal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Función para predecir el clima con markov
def predecir_clima(dia_optimo, prob_seco_lluvia, prob_lluvia_lluvia):
    clima_prediccion = []  # Lista para almacenar la predicción
    
    # Inicializar el primer día como seco
    clima_prediccion.append(0)
    
    # Calcular predicciones para los siguientes 18 días (13 días previos + 5 días de desviación)
    for _ in range(18):
        if clima_prediccion[-1] == 0:  # Si el día anterior fue seco
            clima_prediccion.append(0 if random.random() < prob_seco_lluvia else 1)
        else:  # Si el día anterior fue lluvioso
            clima_prediccion.append(0 if random.random() < prob_lluvia_lluvia else 1)
    
    return clima_prediccion

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

def calidad(q_t_minus, q_t_plus, a, b, c):
    # Entrega la calidad
    def dia_estimado():
        # Funcion que estima el dia de cosecha con media 0 y desv est 2
        optimal_day = np.random.normal(0, 2)
        return int(round(optimal_day))
    t_optimal = dia_estimado()
    def funcion_calidad(a, b, c, t):
        # funcion de calidad bajo el supuesto que no llueve, para modificar en el futuro
        return max(min(a * t**2 + b * t + c, 1), 0)
    a, b, c = calcular_coeficientes_parabola(q_t_minus, q_t_plus)
    q_t_optimal = funcion_calidad(a, b, c, t_optimal)
    return q_t_optimal

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

    for lote in lotes:
        lote_id, lote_cod, lote_numero, lote_tipo_uva, lote_toneladas, lote_dia_optimo, lote_prob_seco_lluvia, lote_prob_lluvia_lluvia, lote_precio_usd = lote
        
        # Tomar decisiones aqui
        

        '''
        # Calcular predicción climática
        dia_optimo_prediccion = predecir_clima(lote_dia_optimo, lote_prob_seco_lluvia, lote_prob_lluvia_lluvia)
        
        # Imprimir resultados
        print(f"Lote: {lote_cod}")
        # en dia_optimo_prediccion[12] está el día óptimo
        print(f"Predicción climática: {dia_optimo_prediccion}")
        '''


    conn.close()

# Ejecutar la simulación
simular()