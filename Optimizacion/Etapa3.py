from gurobipy import Model, GRB
from Etapa1 import Requerimientos,prop
from Etapa2 import lotes_finales_ordenados, lote_info
import numpy as np

# Creación del modelo
m = Model("OptimizacionCosechaLotes")

# Índices
S = []  # Conjunto de lotes comprados con spot
F = [] # Conjunto de lotes comprados con forward
for i in lotes_finales_ordenados:
    if i[15] == 1:
        S.append(i[0])
    elif i[16] == 1:
        F.append(i[0])
print("S",S)
print("F",F)
Conjunto_final = {}
L = range(1, 291)

T = list(range(1, 151)) # Periodos
Cepas = ["C1", "C2", "C3", "C4", "C5", "C6"]

calidades = {'C1': [0.85, 0.95], 'C2': [0.92, 0.93], 'C3': [0.91, 0.87], 'C4': [0.95, 0.95], 'C5': [0.85, 0.85],
             'C6': [0.93, 0.94]}

Dl = [6674412, 16173750, 12480000, 12592500, 14337206, 2002133]



# Parámetros
r = {} #riesgo por lote
requerimientos = {} #requerimientos por cepa
kg = {} #kilogramos por lote
d_optimo = {} #dia optimo por lote
lote_cepa = {} #cepa de cada lote
umbral = {} #umbral de cada lote
umbrales = {
    "C1": 0.8,
    "C2": 0.75,
    "C3": 0.8,
    "C4": 0.7,
    "C5": 0.8,
    "C6": 0.7
} #definido solo para asignar umbral por lote

for l, lote_info in enumerate(lotes_finales_ordenados, start=1):
    kg[l] = lote_info[3]*1000 #Kilogramos de uva por lote
    d_optimo = lote_info[4] #dia optimo de cosecha por lote
    r[l] = lote_info[9] #riesgo por lote
    #c[l] = lote_info[7] #costo por kg
    #q_expec[l] = lote_info[14]
    lote_cepa[l] = lote_info[2] #cepa de cada lote
    umbral[l] = umbrales[lote_info[2]] #umbral industrializacion de cada lote

indice = 0
for cepa in Cepas:
    requerimientos[cepa] = Requerimientos[indice]
    indice += 1



q_lt = {} # Calidad del lote l en el periodo t
M = 1 #parametro grande considernado

#Actualizar los dias optimos de cada lote incluyendo variabilidad

def dia_estimado():
    optimal_day = np.random.normal(0, 2)
    return int(round(optimal_day))

for clave, valor in d_l.items():
    d_l[clave] = valor + dia_estimado()


def obtener_coeficientes(tipo_uva):
    q_t_minus = calidades[tipo_uva][0]
    q_t_plus = calidades[tipo_uva][1]
    t_minus = -7
    t_plus = 7
    A = np.array([
        [t_minus ** 2, t_minus, 1],
        [0, 0, 1],
        [t_plus ** 2, t_plus, 1]])
    b = np.array([q_t_minus, 1, q_t_plus])
    coefficients = np.linalg.solve(A, b)
    a, b, c = coefficients
    return a, b, c


def funcion_cuadratica_calidad(tipo_uva, t,l):
    a, b, c = obtener_coeficientes(tipo_uva)
    x = a * t ** 2 + b * t + c
    calidad = max(min(x*lotes_finales_ordenados[l][12], 1),0)
    return calidad


for l in range(0,len(L)):
    tipo_uva = L[l][(len(L[l]) - 2):len(L[l])]
    tipo_uva_con_comillas = "'" + tipo_uva + "'"
    for t in T:
        if (d_l[L[l]] - 7) <= t <= (d_l[L[l]]) + 7:
            calidad_dia_final = funcion_cuadratica_calidad(tipo_uva, (t - (d_l[L[l]])), l)
            q_lt[L[l], t] = calidad_dia_final
        else:
            q_lt[L[l], t] = 0


# Variables de Decisión
x_lt = m.addVars(L, T, vtype=GRB.BINARY, name="x")
y_lt = m.addVars(L, T, vtype=GRB.BINARY, name="x")
xd_lt = m.addVars(L, T, vtype=GRB.BINARY, name="xd")
z_lt = m.addVars(L,T, vtype=GRB.BINARY, name="z")
dc_l = m.addVars(L, vtype=GRB.CONTINUOUS, name="dc")
w_ct = m.addVars(C, T, vtype=GRB.CONTINUOUS, name="w")

# Función Objetivo
m.setObjective(sum(q_lt[l, t]*x_lt[l, t] - M*riesgo_l[l]  for l in L for t in T), GRB.MAXIMIZE)

# Restricciones
for l in S:
    #Aviso de cosecha para los lotes de tipo forward (que aviso se emita dos dias antes)
    m.addConstr(d_l[l] - dc_l[l] == 2, name=f"restr1_{l}")

for l in F:
    #Aviso de cosecha para los lotes de tipo spot (aviso tiene que ser 5 dias antes)
    m.addConstr(d_l[l] - dc_l[l] >= 5, name=f"restr2_{l}")

for l in L:
    #Sumatoria a lo largo de los periodos que dice que un lote debe ser enviado a la planta o debe ser desechado
    m.addConstr(sum(x_lt[l, t] + xd_lt[l, t] for t in T) == 1, name=f"restr3_{l}")

for f in C:
    for t in T:
        m.addConstr(sum(z_lt[l, t] * r_cl[f,l] for c, l in r_cl if l in L and  c == f) == w_ct[f, t], name=f"restr5_{f}_{t}")

for f in C:
    m.addConstr(sum(z_lt[l, t] * r_cl[f,l]  for c, l in r_cl if l in L and  c == f for t in T) >= d_c[f], name=f"restr6_{f}")

# Agrega restricciones para calcular la calidad en función del día de cosecha --------
#----------------------------------

for l in L:
    for t in T:
        m.addConstr(0 <= (q_lt[l, t] - u_l[l])* z_lt[l,t])

# Suponiendo que 'm' es el modelo de Gurobi
for l in L:
    for t in T:
        m.addConstr(y_lt[l, t] <= x_lt[l, t], name=f"Restriction_y_x_{l}_{t}")

for l in L:
    m.addConstr(sum(z_lt[l,t] for t in T) <= 1, name=f"restr3_{l}")


# Suponiendo que 'm' es el modelo de Gurobi
for l in L:
    for t in T:
        m.addConstr(y_lt[l, t] >= z_lt[l,t], name=f"Restriction_y_z_{l}_{t}")

# Suponiendo que 'm' es el modelo de Gurobi
for l in L:
    for t in T:
        m.addConstr(y_lt[l, t] >= x_lt[l, t] + z_lt[l,t] - 1, name=f"Restriction_y_x_z_{l}_{t}")

# Resolver el modelo
m.optimize()

# Imprimir solución (esto es opcional)
if m.status == GRB.OPTIMAL:
    for l in L:
        for t in T:
            if x_lt[l, t].x == 1:
                Conjunto_final[f"x_{l}"] = t
                print(f"x_{l}_{t}:", x_lt[l, t].x, f"Cosechado el dia", t , f" Cantidad de kilo del lote, pta no alcanze a definirlo se podria sacar de forma manual desde r_cl")

print(Conjunto_final)



