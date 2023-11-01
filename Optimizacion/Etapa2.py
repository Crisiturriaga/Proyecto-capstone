import gurobipy as gp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

archivo_excel = 'info-vinos_2023_v2.xlsx'  
df = pd.read_excel(archivo_excel, sheet_name=1)


# Lista para almacenar lotes
lotes = []

for index, row in df.iterrows():
    lista_lote = row.tolist()

    lotes.append(lista_lote)

def calcular_probabilidad_lluvia(P_seco_a_lluvioso, P_lluvioso_a_lluvioso):
    # Inicializar probabilidades iniciales según el estado inicial deseado
    P_dia_seco = 1
    P_dia_lluvioso = 0
    dias = 7

    # Calcular probabilidades de estado para cada día
    for _ in range(dias):
        P_dia_seco_nuevo = (P_dia_seco * (1 - P_seco_a_lluvioso) + P_dia_lluvioso * (1 - P_lluvioso_a_lluvioso))
        P_dia_lluvioso_nuevo = (P_dia_seco * P_seco_a_lluvioso + P_dia_lluvioso * ( P_lluvioso_a_lluvioso))
        P_dia_seco, P_dia_lluvioso = P_dia_seco_nuevo, P_dia_lluvioso_nuevo

    porcentaje_lluvia = P_dia_lluvioso 
    
    return porcentaje_lluvia



#Se crea ua funcion que nos entregue una lista que corresponde a la cantidad de lluvia maxima tolerada por cada una de las cepas
#Esta funcion se puede alterar dependiendo de que % de lotes se quiere comprar con compra spot
def tolerancia_cepa(lotes):
    cepas = ["C1","C2","C3","C4","C5","C6"]
    tolerancia = []

    penalizaciones = {'C1': [0.03, 0.02, 0.01, 0.005],
                        'C2': [0.025, 0.012, 0.004, 0.002],
                        'C3': [0.03, 0.02, 0.01, 0.005],
                        'C4': [0.025, 0.012, 0.01, 0.002],
                        'C5': [0.03, 0.02, 0.01, 0.005],
                        'C6': [0.025, 0.012, 0.004, 0.002]
                        }
    #Se hacen dos litas por cada cepa, donde una corresponde a la calidad o ponterador de calidad obtenido en base a una de las partes de la ecuacion de calidad
    #(la parte que pensaliza por la presencia de lluvias en cada uno de los dias previos)
    #Luego de eso se determina un porcentaje de los lotes que será comprado con contrato spot (Ej: el 20 porciento que contenga a los lotes con peor calidad)
    lluvias_cepa = []
    ponderador_cepa = []
    for cepa in cepas:
        valores_lluvia = []
        valores_calidad = []
        for lote in lotes:
            porcentaje_lluvia = lote[8]
            lote_cepa = lote[2]
            if cepa == lote_cepa:
                calidad = ((1-penalizaciones[cepa][0]*porcentaje_lluvia) *
                    (1-penalizaciones[cepa][1]*porcentaje_lluvia) *
                    (1-penalizaciones[cepa][2]*porcentaje_lluvia) *
                    (1-penalizaciones[cepa][3]*porcentaje_lluvia) *
                    (1-penalizaciones[cepa][3]*porcentaje_lluvia) *
                    (1-penalizaciones[cepa][3]*porcentaje_lluvia) *
                    (1-penalizaciones[cepa][3]*porcentaje_lluvia) *
                    (1-penalizaciones[cepa][3]*porcentaje_lluvia)
                    )
                valores_lluvia.append(porcentaje_lluvia)
                valores_calidad.append(calidad)
        lluvias_cepa.append(valores_lluvia)
        ponderador_cepa.append(valores_calidad)
        
        #Se ordenan las listas de mayor a menor para luego poder obtener que valor corresponde al % deseado
        valores_lluvia.sort(reverse = True)
        valores_calidad.sort()

        #En este caso el 0.2 es porque buscamos la calidad en el 20% mas bajo y con su posicion encontraremos la lluvia que genera la calidad del 20% mas bajo
        posicion_porcentaje = int(len(valores_calidad) * 0.01)
        valor_calidad = valores_calidad[posicion_porcentaje]
        valor_lluvia = valores_lluvia[posicion_porcentaje]
        tolerancia.append(valor_lluvia)
    return tolerancia, lluvias_cepa, ponderador_cepa       


lotes_def = []
for lote in lotes:
    tipo_uva = lote[2]
    prob_seca_lluvia = lote[5]
    prob_lluvia_lluvia = lote[6]

    lluvia_dias = calcular_probabilidad_lluvia(prob_seca_lluvia, prob_lluvia_lluvia)
    lote.append(lluvia_dias)

tolerancia_lluvias = tolerancia_cepa(lotes)

#Funcion que normaliza los datos pero entrega valores dados dentro de un rango definido por nosotros para que funcione como penalizacion
def normalizar (lista, a, b):

    minimo = min(lista)
    maximo = max(lista)

    if minimo == maximo:
        return [a] * len(lista)

    normalized_list = [(x - minimo) / (maximo - minimo) * (b - a) + a for x in lista]
    return normalized_list

lluvias_c1 = tolerancia_lluvias[1][0]
lluvias_c2 = tolerancia_lluvias[1][1]
lluvias_c3 = tolerancia_lluvias[1][2]
lluvias_c4 = tolerancia_lluvias[1][3]
lluvias_c5 = tolerancia_lluvias[1][4]
lluvias_c6 = tolerancia_lluvias[1][5]

ponderador_c1 = tolerancia_lluvias[2][0]
ponderador_c2 = tolerancia_lluvias[2][1]
ponderador_c3 = tolerancia_lluvias[2][2]
ponderador_c4 = tolerancia_lluvias[2][3]
ponderador_c5 = tolerancia_lluvias[2][4]
ponderador_c6 = tolerancia_lluvias[2][5]





#Se hacen penalizaciones dentro de cada cepa ya que los lotes se afectan de forma diferente segun la cepa
a =0.2
b =0.6
c1_normalizada = normalizar(lluvias_c1, a, b)
c2_normalizada = normalizar(lluvias_c2, a, b)
c3_normalizada = normalizar(lluvias_c3, a, b)
c4_normalizada = normalizar(lluvias_c4, a, b)
c5_normalizada = normalizar(lluvias_c5, a, b)
c6_normalizada = normalizar(lluvias_c6, a, b)

lotes_c1 = []
lotes_c2 = []
lotes_c3 = []
lotes_c4 = []
lotes_c5 = []
lotes_c6 = []

for lote in lotes:
    if lote[2] == "C1":
        lotes_c1.append(lote)
    if lote[2] == "C2":
        lotes_c2.append(lote)
    if lote[2] == "C3":
        lotes_c3.append(lote)
    if lote[2] == "C4":
        lotes_c4.append(lote)
    if lote[2] == "C5":
        lotes_c5.append(lote)
    if lote[2] == "C6":
        lotes_c6.append(lote)

lotes_c1 = sorted(lotes_c1, key=lambda x: x[8], reverse=True)
lotes_c2 = sorted(lotes_c2, key=lambda x: x[8],reverse=True)
lotes_c3 = sorted(lotes_c3, key=lambda x: x[8],reverse=True)
lotes_c4 = sorted(lotes_c4, key=lambda x: x[8],reverse=True)
lotes_c5 = sorted(lotes_c5, key=lambda x: x[8],reverse=True)
lotes_c6 = sorted(lotes_c6, key=lambda x: x[8],reverse=True)


#se vincula cada lote especifico con su penalizador calculado mediante la funcion
#para esto se ordenaron los lotes de manera decreciente, para poder entregar el penalizador mas alto al lote con mas lluvias
#y el mas bajo al con menos lluvias
lotes_finales = []
contador_1 = 0
for lote in lotes_c1:
    lote.append (c1_normalizada[contador_1])
    contador_1 += 1
    lotes_finales.append(lote)

contador_2 = 0
for lote in lotes_c2:
    lote.append (c2_normalizada[contador_2])
    contador_2 += 1
    lotes_finales.append(lote)

contador_3 = 0
for lote in lotes_c3:
    lote.append (c3_normalizada[contador_3])
    contador_3 += 1
    lotes_finales.append(lote)

contador_4 = 0
for lote in lotes_c4:
    lote.append (c4_normalizada[contador_4])
    contador_4 += 1
    lotes_finales.append(lote)

contador_5 = 0
for lote in lotes_c5:
    lote.append (c5_normalizada[contador_5])
    contador_5 += 1
    lotes_finales.append(lote)

contador_6 = 0
for lote in lotes_c6:
    lote.append (c6_normalizada[contador_6])
    contador_6 += 1
    lotes_finales.append(lote)

lista_unida = ponderador_c1 + ponderador_c2 + ponderador_c3 + ponderador_c4 + ponderador_c5 + ponderador_c6

for lote in lotes_finales:
    lote.append(lista_unida[0])
    lista_unida.pop(0)
    tipo_3 = lote[6]*0.05
    lote.append(tipo_3)
    q = (1-tipo_3) * lote[10]
    lote.append(q)
print(lotes_finales[0])
calidades =  {'C1': [0.85, 0.95], 'C2': [0.92, 0.93], 'C3': [0.91, 0.87], 'C4': [0.95, 0.95], 'C5': [0.85, 0.85], 'C6': [0.93, 0.94]}

def obtener_coeficientes(tipo_uva):
    q_t_minus = calidades[tipo_uva][0]
    q_t_plus = calidades[tipo_uva][1]
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

def funcion_cuadratica_calidad(tipo_uva):
    a, b, c = obtener_coeficientes(tipo_uva)
    def dia_estimado():
        optimal_day = np.random.normal(0, 2)
        return int(round(optimal_day))
    t = dia_estimado()
    calidad = max(min(a * t**2 + b * t + c, 1), 0)
    return calidad

for lote in lotes_finales:
    tipo_uva = lote[2]
    calidad = funcion_cuadratica_calidad(tipo_uva)
    lote.append(calidad)

## NOTAR QUE EL ULTIMO VALOR ES LA PARTE CUADRATICA
print(lotes_finales[0])

#En lotes_finales tendremos cada uno de los lotes, donde la ultima columna corresponde a la penalizacion que este tiene

# Creacion modelo
model = gp.Model()

# Índices
L = range(1, 291)
T = range(1, 6)  # Hay que cambiar por periodos reales

# Parámetros
kg = {}  # Kilogramos de uva por lote
q_expec = {}  # Calidad esperada del lote por lote y período
r = {}  # Medida de riesgo por lote
c = {} #costo por lote
# Poblando los parametros con la lista de lotes obtenida mas arriba
for l, lote_info in enumerate(lotes_finales, start=1):
    kg[l] = lote_info[3]*1000 
    r[l] = lote_info[9] 
    c[l] = lote_info[7] #costo por kg
    q_expec[l] = lote_info[12]


###print(lotes_finales)
#Hay que agregar las calidades para un periodo especifico
#Creo que va a tener que ser una lista de listas que vaya por cada uno de los lotes 
#y dentro tenga las calidades que tendría este lote para los diferentes posibles días

    #for t in T:
        #q_expec[l, t] = lote_info[1][t - 1]  # Calidad esperada del lote por período



# Definir los parámetros kg, q_expec y r aquí

# Variables de decisión
x_spot = {}  # Variable binaria: 1 si el lote l se compra con contrato spot, 0 en otro caso
x_fwd = {}  # Variable binaria: 1 si el lote l se compra con contrato forward, 0 en otro caso

for l in L:
    for t in T:
        x_spot[l, t] = model.addVar(vtype=gp.GRB.BINARY, name=f'x_spot_{l}_{t}')
    x_fwd[l] = model.addVar(vtype=gp.GRB.BINARY, name=f'x_fwd_{l}')

# Función Objetivo
model.setObjective(
    gp.quicksum((x_spot[j] * kg[j] * q_expec[j]*c[j] + x_fwd[j] * kg[j] * c[j] * 0.8) / (1 - r[j] + 0.0000001) for t in T),
    sense=gp.GRB.MINIMIZE
)

# Restricciones
# Restricción: Un lote se compra una sola vez
for j in L:
    model.addConstr(gp.quicksum(x_spot[j, t] for t in T) + x_fwd[j] == 1, name=f'restriccion_compra_{j}')

# Restricción: Atender el requerimiento de cepas (debes definirlo)
# Supongamos que el requerimiento está definido en un diccionario req_cepas, donde req_cepas[j] es la cantidad requerida del lote j.
for j in L:
    model.addConstr(gp.quicksum(x_spot[j, t] for t in T) * kg[j] >= req_cepas[j], name=f'restriccion_req_cepas_{j}')

# Resolver el modelo
model.optimize()

# Obtener los resultados
for j in L:
    for t in T:
        print(f"Lote {j}, Periodo {t}: Compra con contrato spot = {x_spot[j, t].x}")
    print(f"Lote {j}: Compra con contrato forward = {x_fwd[j].x}")

# Obtener el valor óptimo de la función objetivo
print(f"Valor óptimo: {model.objVal}")
