import pandas as pd
from gurobipy import Model, GRB, quicksum
from Etapa3 import lotes_finales_ordenados
import math

# Crear el modelo
m = Model("FermentacionDeUva")

# Leer datos del archivo CSV
df = pd.read_csv('datos.csv')

#El atributo lote[19] es una binaria que entrega un 1 si se cosecha el lote, cero si no se cosecha
#El atributo lote[20] entrega el dia en que se debe cosechar el lote, si no se cosecha, el valor del atributo es (-1)

L = []  # Lista de los primeros 10 lotes
Dia = {}
Vol = {}  # Volumen de cada lote
Cepa = {}
Calidad = {}  # Calidad fija para todos los lotes
# Conjuntos
for i in range(0,len(lotes_finales_ordenados)):
    if lotes_finales_ordenados[i][19] == 1:
        L.append(lotes_finales_ordenados[i][0])
        Dia[lotes_finales_ordenados[i][0]] = lotes_finales_ordenados[i][20]
        Vol[lotes_finales_ordenados[i][0]] = lotes_finales_ordenados[i][3]*1000
        Cepa[lotes_finales_ordenados[i][0]]= lotes_finales_ordenados[i][2]
        lista_calidad = lotes_finales_ordenados[i][18]
        Calidad[lotes_finales_ordenados[i][0]] = lista_calidad[lotes_finales_ordenados[i][20]] #calidad del dia de cosecha segun etapa 3
C = ["C1","C2","C3","C4","C5","C6"]  # Lista de cepas
T = range(216)  # 216 tanques disponibles
D = range(df['Dia optimo cosecha estimado inicialmente'].min(),
          df['Dia optimo cosecha estimado inicialmente'].max() + 1)  # Horizonte de planificación

# Parámetros
Cap = {t: 25000 for t in T}  # Capacidad de cada tanque t

Dur = 8  # Duración promedio de la fermentación
Costo = 1600  # Costo promedio por cada 24 tanques utilizados

# Variables de decisión
x = m.addVars(L, T, D, vtype=GRB.BINARY, name="x")
ocupado = m.addVars(T, D, vtype=GRB.BINARY, name="ocupado")
tanques_usados = m.addVars(D, vtype=GRB.INTEGER, name="tanques_usados")
calidad_tanque = m.addVars(T, vtype=GRB.CONTINUOUS, name="calidad_tanque")

# Variables de decisión adicionales (auxiliar)
grupos_tanques = m.addVars(D, vtype=GRB.INTEGER, name="grupos_tanques")

# Función objetivo
m.setObjective(quicksum(grupos_tanques[d] * Costo for d in D), GRB.MINIMIZE)

# Ajustar parámetros de Gurobi
m.setParam(GRB.Param.Heuristics, 0.5)  # Aumentar el uso de heurísticas
m.setParam(GRB.Param.TimeLimit, 120)  # Establecer un límite de tiempo de 2 minutos
m.setParam(GRB.Param.MIPGap, 0.30)  # Aceptar una brecha de optimalidad del 5%

# Restricciones
# 1. Asignación de lotes
for l in L:
    m.addConstr(quicksum(x[l, t, d] for t in T for d in D) == 1)

# 2. Capacidad de tanques
for l in L:
    for t in T:
        for d in D:
            m.addConstr(Vol[l] * x[l, t, d] <= Cap[t])

# 3. Mínimo de llenado
for l in L:
    for t in T:
        for d in D:
            m.addConstr(Vol[l] * x[l, t, d] >= 0.3 * Cap[t] * x[l, t, d])

# 4. Disponibilidad de tanques
for t in T:
    for d in D:
        m.addConstr(quicksum(x[l, t, d] for l in L) <= ocupado[t, d])

# 5. Respetar fechas de inicio
for l in L:
    for t in T:
        for d in D:
            if d < Dia[l]:
                m.addConstr(x[l, t, d] == 0)

# 6. Duración de la fermentación
for l in L:
    for t in T:
        for d in D:
            # Limitar el rango de días para evitar exceder el horizonte de planificación
            limite_superior = min(d + Dur, max(D) + 1)
            m.addConstr(quicksum(ocupado[t, d_prime] for d_prime in range(d, limite_superior)) >= Dur * x[l, t, d])

# 7. No mezclar cepas en un tanque
for t in T:
    for c in C:
        for d in D:
            m.addConstr(quicksum(x[l, t, d] for l in L if Cepa[l] != c) == 0)

# 8. Conteo de tanques usados
for d in D:
    m.addConstr(tanques_usados[d] == quicksum(ocupado[t, d] for t in T))

# 9. Cálculo de la calidad del vino en cada tanque
for t in T:
    suma_calidad = quicksum(Calidad[l] * Vol[l] * x[l, t, d] for l in L for d in D)
    suma_volumen = quicksum(Vol[l] * x[l, t, d] for l in L for d in D)
    m.addConstr(calidad_tanque[t] * suma_volumen == suma_calidad)
# Restricciones adicionales para definir los grupos de tanques
for d in D:
    m.addConstr(grupos_tanques[d] >= (tanques_usados[d] + 23) / 24)

# Optimizar el modelo
m.optimize()