import sqlite3
import random
import numpy as np
import openpyxl



wb = openpyxl.Workbook()
ws = wb.active


# Crear una conexión a la base de datos
conn = sqlite3.connect('vinos.db')
c = conn.cursor()

# parametros cosecha
periodo_ideal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
calidades = [[0.85, 0.95],[0.92, 0.93],[0.91, 0.87],[0.95, 0.95],[0.85, 0.85],[0.93, 0.94]]
umbrales = [0.8, 0.75, 0.8, 0.7, 0.8, 0.7]

# parametros fermentacion
plantas = [[1600, 1840, 1840],[1500, 1725, 1725],[1800, 2070, 2070]]
cap_plantas = 600
tanques_x_planta = 24
cap_tanque = 25000
uso_plantas = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
litros_restantes_uvas = [0, 0, 0, 0, 0, 0]
litros_vino_uvas = [0, 0, 0, 0, 0, 0]
# planta 2 tarmo 1 = uso_plantas[1][0]

# Función para predecir el clima con markov
def predecir_clima(dia_optimo, prob_seco_lluvia, prob_lluvia_lluvia):
    clima_prediccion = []  # Lista para almacenar la predicción
    tipo_3 = []
    
    # Inicializar el primer día como seco
    clima_prediccion.append(0)
    
    # Calcular predicciones para los siguientes 18 días (13 días previos + 5 días de desviación)
    for _ in range(7):
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
    
def litros_restantes_uva(litros_restantes, uva):
    if uva == 'C1':
        litros_restantes_uvas[0] += litros_restantes
    elif uva == 'C2':
        litros_restantes_uvas[1] += litros_restantes
    elif uva == 'C3':
        litros_restantes_uvas[2] += litros_restantes
    elif uva == 'C4':
        litros_restantes_uvas[3] += litros_restantes
    elif uva == 'C5':
        litros_restantes_uvas[4] += litros_restantes
    elif uva == 'C6':
        litros_restantes_uvas[5] += litros_restantes

def litros_vino(litros_uva, uva):
    if uva == 'C1':
        litros_vino_uvas[0] += litros_uva
    elif uva == 'C2':
        litros_vino_uvas[1] += litros_uva
    elif uva == 'C3':
        litros_vino_uvas[2] += litros_uva
    elif uva == 'C4':
        litros_vino_uvas[3] += litros_uva
    elif uva == 'C5':
        litros_vino_uvas[4] += litros_uva
    elif uva == 'C6':
        litros_vino_uvas[5] += litros_uva
    
def calcular_duracion_vinificacion():
    duracion_aleatoria = random.uniform(7, 9)
    dia_exacto = round(duracion_aleatoria)
    return dia_exacto

def conversion_lt_tanque(litros_vino):
    tanques = 0
    while litros_vino >= 25000:
        litros_vino -= 25000
        tanques += 1
    return litros_vino, tanques

def uso_tanques(tanques_utilizar):
    tanques_a_fermentar = tanques_utilizar
    while tanques_utilizar > 0:
        if uso_plantas[1][0] < 24:
            uso_plantas[1][0] += 1
            tanques_utilizar -= 1
        elif uso_plantas[0][0] < 24:
            uso_plantas[0][0] += 1
            tanques_utilizar -= 1
        elif uso_plantas[1][1] < 24:
            uso_plantas[1][1] += 1
            tanques_utilizar -= 1
        elif uso_plantas[1][2] < 24:
            uso_plantas[1][2] += 1
            tanques_utilizar -= 1
        elif uso_plantas[2][0] < 24:
            uso_plantas[2][0] += 1
            tanques_utilizar -= 1
        elif uso_plantas[0][1] < 24:
            uso_plantas[0][1] += 1
            tanques_utilizar -= 1
        elif uso_plantas[0][2] < 24:
            uso_plantas[0][2] += 1
            tanques_utilizar -= 1
        elif uso_plantas[2][1] < 24:
            uso_plantas[2][1] += 1
            tanques_utilizar -= 1
        elif uso_plantas[2][2] < 24:
            uso_plantas[2][2] += 1
            tanques_utilizar -= 1
        else:
            '''litros_restantes = tanques_utilizar*25000
            litros_restantes_uva(litros_restantes, uva)'''
            tanques_a_fermentar -= tanques_utilizar
            return tanques_a_fermentar, tanques_utilizar
    return tanques_a_fermentar, tanques_utilizar
def eliminar_tanques(tanques_utilizar, tipo_uva):
    litros_uva = tanques_utilizar*25000
    litros_vino(litros_uva, tipo_uva)
    while tanques_utilizar > 0:
        if uso_plantas[1][0] > 0:
            uso_plantas[1][0] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[0][0] > 0:
            uso_plantas[0][0] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[1][1] > 0:
            uso_plantas[1][1] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[1][2] > 0:
            uso_plantas[1][2] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[2][0] > 0:
            uso_plantas[2][0] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[0][1] > 0:
            uso_plantas[0][1] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[0][2] > 0:
            uso_plantas[0][2] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[2][1] > 0:
            uso_plantas[2][1] -= 1
            tanques_utilizar -= 1
        elif uso_plantas[2][2] > 0:
            uso_plantas[2][2] -= 1
            tanques_utilizar -= 1
        else:
            break

def sacar_tanques(lista, t):
    indices_a_eliminar = []

    for i, iteracion in enumerate(lista):
        if t == iteracion[1]:
            indices_a_eliminar.append(i)
            tanques_utilizar = iteracion[0]
            tipo_uva = iteracion[2]
            eliminar_tanques(tanques_utilizar, tipo_uva)

    # Eliminar sublistas en orden inverso para evitar problemas con los índices
    for index in reversed(indices_a_eliminar):
        lista.pop(index)

    return lista


### Para calcular los coeficientes llamar a la funcion "calcular_coeficientes_parabola(q_t_minus, q_t_plus)" siendo
### el q_t_minus = q[t-7] y el otro q[t+7].
### Para obtener la calidad simplemente llamar a calidad(q_t_minus, q_t_plus, a, b, c), usando los coeficientes de
### la funcion anterior.

# Simulación de toma de decisiones y restricciones
def simular():
    conn = sqlite3.connect('vinos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM lotes')
    lotes = c.fetchall()
    contador = 0
    litros_totales = 0
    litros_C1 = 0
    litros_C2 = 0
    litros_C3 = 0
    litros_C4 = 0
    litros_C5 = 0
    litros_C6 = 0
    columna = 0
    lista_fermentacion = []
    tipo_33 = []
    for t in range(50, 150):
        uva_C1_hoy = 0
        uva_C2_hoy = 0
        uva_C3_hoy = 0
        uva_C4_hoy = 0
        uva_C5_hoy = 0
        uva_C6_hoy = 0
        lista_fermentacion = sacar_tanques(lista_fermentacion, t)
        for lote in lotes:
            lote_id, lote_cod, lote_numero, lote_tipo_uva, lote_toneladas, lote_dia_optimo, lote_prob_seco_lluvia, lote_prob_lluvia_lluvia, lote_precio_usd = lote
            if t == lote_dia_optimo:
                clima_prediccion, tipo_3 = predecir_clima(lote_dia_optimo, lote_prob_seco_lluvia, lote_prob_lluvia_lluvia)
                tipo_33.append(tipo_3)
                contador += 1
                calidad_lote = uva(lote_tipo_uva)
                q_menos_7 = calidad_lote[0]
                q_mas_7 = calidad_lote[1]
                calidad_lote, t_optimal = calidad_final(q_menos_7, q_mas_7)
                #print(f'lote: {lote_cod}')
                #print(f't = {t}')
                lote_dia_optimo += t_optimal
                umbral_calidad_uva = umbral_uva(lote_tipo_uva)
                if calidad_lote >= umbral_calidad_uva:
                    #Calidad en buen estado, pasa a fermentacion
                    kilos_lote = lote_toneladas*1000
                    litros_vin = kilos_lote*0.5
                    litros_totales += litros_vin
                    litros_restantes, tanques_utilizar = conversion_lt_tanque(litros_vin)
                    litros_restantes_uva(litros_restantes, lote_tipo_uva)
                    #print(litros_restantes_uvas)
                    tanques_utilizar, tanques_espera = uso_tanques(tanques_utilizar)
                    #print(uso_plantas)
                    dias_tanque = t + calcular_duracion_vinificacion()
                    if tanques_utilizar > 0:
                        lista_fermentacion.append([tanques_utilizar, dias_tanque, lote_tipo_uva])
                    litros_sobrantes = 25000*tanques_espera
                    litros_vino(litros_sobrantes, lote_tipo_uva)
                    ### supuesto: cuando no hay espacio en fermentación, y cuando en un lote sobran litros de uva que no 
                    ### pueden ser introducidos a un tanque, estas sobras no se consideran en la simulación.
                    if lote_tipo_uva == "C1":
                        litros_C1 += litros_vin
                        botellas_C1 = litros_C1/0.75
                        uva_C1_hoy += litros_vin

                    elif lote_tipo_uva == "C2":
                        litros_C2 += litros_vin
                        botellas_C2 = litros_C2/0.75
                        uva_C2_hoy += litros_vin

                    elif lote_tipo_uva == "C3":
                        litros_C3 += litros_vin
                        botellas_C3 = litros_C3/0.75
                        uva_C3_hoy += litros_vin

                    elif lote_tipo_uva == "C4":
                        litros_C4 += litros_vin
                        botellas_C4 = litros_C4/0.75
                        uva_C4_hoy += litros_vin

                    elif lote_tipo_uva == "C5":
                        litros_C5 += litros_vin
                        botellas_C5 = litros_C5/0.75
                        uva_C5_hoy += litros_vin

                    elif lote_tipo_uva == "C6":
                        litros_C6 += litros_vin
                        botellas_C6 = litros_C6/0.75
                        uva_C6_hoy += litros_vin
                    


                    



                    


                elif umbral_calidad_uva > calidad_lote >= 0.5:
                    # Calidad piola, se recupera 30%
                    pass
                elif 0.5> calidad_lote:
                    # calidad mala, se recupera el 5%
                    pass
                
            else:
                pass
        lista_diaria = [uva_C1_hoy,uva_C2_hoy,uva_C3_hoy,uva_C4_hoy,uva_C5_hoy,uva_C6_hoy]
        columna += 1
        for index, value in enumerate(lista_diaria, start=1):
            ws.cell(row=index, column=columna, value=value)
        '''wb.save('archivo_excel.xlsx')'''

    print(f'litros vino por cepa (C1, ..., C6): {litros_vino_uvas}')
    print(f'litros sobrantes por cepa: {litros_restantes_uvas}')
    suma = sum(litros_vino_uvas) + sum(litros_restantes_uvas)
    print(f'litros totales de vino: {suma}')
    print(f'litros que se usarán:{sum(litros_vino_uvas)}')
    print(f'litros que sobraron:{sum(litros_restantes_uvas)}')
    botellas_mercado_A = botellas_C5
    botellas_mercado_B = botellas_C3 + botellas_C1
    botellas_mercado_C = botellas_C2
    botellas_mercado_D = botellas_C4 + botellas_C6
    print(f"la cantidad de litros será {litros_totales}")
    botellas = litros_totales/0.75
    print(f"la cantidad de botellas totales a producir es {botellas}")
    print(f"para C1 hay {litros_C1} litros y {botellas_C1} botellas")
    print(f"para C2 hay {litros_C2} litros y {botellas_C2} botellas")
    print(f"para C3 hay {litros_C3} litros y {botellas_C3} botellas")
    print(f"para C4 hay {litros_C4} litros y {botellas_C4} botellas")
    print(f"para C5 hay {litros_C5} litros y {botellas_C5} botellas")
    print(f"para C6 hay {litros_C6} litros y {botellas_C6} botellas")
    print(f"para el mercado A se tiene {botellas_mercado_A}, para el mercado B se tiene {botellas_mercado_B}")
    print(f"para el C tenemos {botellas_mercado_C} y finalmente para el mercado D se logra producir{botellas_mercado_D}")
<<<<<<< HEAD
    print(f'contador: {contador}')'''
    dias_perdidos = 0
    for lote in tipo_33:
        if sum(lote)>0:
            dias_perdidos += 1
    print(f'lotes perdidos: {dias_perdidos}')

=======
    print(f'contador: {contador}')
>>>>>>> 09ff58c7e1f1ad245cdd2d65888d982e7649c614
    conn.close()

# Ejecutar la simulación
simular()