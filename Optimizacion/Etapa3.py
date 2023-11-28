import gurobipy as gp
from Etapa1 import Requerimientos,prop, lista
from Etapa2 import lotes_finales_ordenados, lote_info
import numpy as np

# Creación del modelo
m = gp.Model()

# Índices
L = range(1, 291)

T = range(0,150) # Periodos
K = range(0,159)

F = range(1, 291)
Cepas = ["C1", "C2", "C3", "C4", "C5", "C6"]

calidades = {'C1': [0.85, 0.95], 'C2': [0.92, 0.93], 'C3': [0.91, 0.87], 'C4': [0.95, 0.95], 'C5': [0.85, 0.85],
             'C6': [0.93, 0.94]}

Dl = [6674412, 16173750, 12480000, 12592500, 14337206, 2002133]

optimos = []
for lote in lotes_finales_ordenados:
    optimo = lote[4]
    optimos.append(optimo)


def dia_estimado():
    optimal_day = np.random.normal(0, 2)
    return int(round(optimal_day))

optimos_2 = []
for dia in optimos:
    optimo = dia + dia_estimado()
    optimos_2.append(optimo)

lote_counter = 0
for optimo in optimos_2:
    lotes_finales_ordenados[lote_counter].append(optimo)
    lote_counter += 1


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

for lote in lotes_finales_ordenados:
    calidad_dias = []
    tipo_uva = lote[2]
    for t in T:
        if lote[17]-7 <= t <= lote[17]+7:
            calidad_dia_final = funcion_cuadratica_calidad(tipo_uva,(t-lote[17]),1)
            calidad_dias.append(calidad_dia_final)
        else:
            calidad_dias.append(0)
    lote.append(calidad_dias)

# Parámetros
x_spot = {} #binaria correspondiente a si se compra con contrato spot
x_fwd = {} #binaria correspondiente a si lote se compra con contrato forward
kg = {} #kilogramos por lote
d_optimo = {} #dia optimo por lote
requerimientos = {} #requerimientos por cepa
umbral = {} #umbral de cada lote
costo = {} #costo por kg del lote
r = {} #riesgo por lote
lote_cepa = {} #cepa de cada lote
umbral = {} #umbral de cada lote
q = {}
umbrales = {
    "C1": 0.8,
    "C2": 0.75,
    "C3": 0.8,
    "C4": 0.7,
    "C5": 0.8,
    "C6": 0.7
} #definido solo para asignar umbral por lote

for l, lote_info in enumerate(lotes_finales_ordenados, start=1):
    x_spot[l] = lote_info[15]
    x_fwd[l] = lote_info[16]
    kg[l] = lote_info[3]*1000 #Kilogramos de uva por lote
    d_optimo[l] = lote_info[4] #dia optimo de cosecha por lote
    r[l] = lote_info[9] #riesgo por lote
    costo[l] = lote_info[7] #costo por kg
    #q_expec[l] = lote_info[14]
    lote_cepa[l] = lote_info[2] #cepa de cada lote
    umbral[l] = umbrales[lote_info[2]] #umbral industrializacion de cada lote
    q[l] = lote_info[18] #lista de la calidad para cada día en cada lote

indice = 0
for cepa in Cepas:
    requerimientos[cepa] = Requerimientos[indice]
    indice += 1




# Variables de Decisión
x_compra = m.addVars(L, T, vtype=gp.GRB.BINARY, name="Eleccion de compra")
y = m.addVars(L, F, K, vtype=gp.GRB.BINARY, name="AsignacionTanque")
o = m.addVars(F, K, vtype=gp.GRB.BINARY, name="Ocupacion de tanque")

#Función Objetivo

m.setObjective(
    gp.quicksum(gp.quicksum(kg[l]*costo[l]*(x_spot[l] * q[l][t] + x_fwd[l] * 0.8)*r[l]*x_compra[l, t] for t in T) for l in L ), 
    sense = gp.GRB.MINIMIZE
)

#Restricciones
for c in Cepas:
    m.addConstr(gp.quicksum(kg[l]* x_compra[l, t] for l in L for t in T if lote_cepa[l] == c) >= requerimientos[c], name=f"restriccion_requerimientos_{c}")

#for t in T
for l in L:
    for t in T:
        m.addConstr(x_compra[l, t] * q[l][t] >= umbral[l] * x_compra[l, t], name=f"restriccion_cosechar_sobre_umbral_{l}")

for l in L:
    m.addConstr(gp.quicksum(x_compra[l, t]for t in T)<= 1, name = f"restriccion comprar solo en un periodo")

for t in T:
    for l in L:
        m.addConstr(x_compra[l, t] * kg[l] * 0.5 <= gp.quicksum(y[l, f, t] * 25000 for f in F))

for t in T:
    for f in F:
        m.addConstr(gp.quicksum(y[l, f, t] for l in L)*7 <= o[f, t+1] + o[f, t+2] + o[f, t+3] + o[f, t+4] + o[f, t+5] + o[f, t+6] + o[f, t+7])

for f in F:
    for t in T:
        m.addConstr(gp.quicksum(y[l,f,t] for l in L) <= 1)

for f in F:
    for t in T:
        m.addConstr(gp.quicksum(y[l,f,t] for l in L) + o[f,t] <= 1)


m.setParam(gp.GRB.Param.MIPGap, 0.9) 


m.optimize()

# Imprimir solución
if m.status == gp.GRB.OPTIMAL:
    # Imprimir valor de la función objetivo
    print(f"Valor de la función objetivo: {m.objVal}")

    # Imprimir variables de decisión
    listita = 0
    ce1 = 0
    ce2 = 0
    ce3 = 0
    ce4 = 0
    ce5 = 0
    ce6 = 0
    diias = 500
    days = 0
    for l in L:
        for t in T:
            valor_x_compra = x_compra[l, t].x
            if valor_x_compra>0:
                lotes_finales_ordenados[l-1].append(valor_x_compra)
                lotes_finales_ordenados[l-1].append(t)
                listita += 1
                print(f"x_compra[{l}, {t}] = {valor_x_compra}")
                if t >= days:
                    days = t
                if t <= diias:
                    diias = t
                if lote_cepa[l] == "C1":
                    ce1 += kg[l]
                if lote_cepa[l] == "C2":
                    ce2 += kg[l]
                if lote_cepa[l] == "C3":
                    ce3 += kg[l]
                if lote_cepa[l] == "C4":
                    ce4 += kg[l]
                if lote_cepa[l] == "C5":
                    ce5 += kg[l]
                if lote_cepa[l] == "C6":
                    ce6 += kg[l]

    print(listita)
    print(ce1,requerimientos["C1"])
    print(ce2,requerimientos["C2"])
    print(ce3,requerimientos["C3"])
    print(ce4,requerimientos["C4"])
    print(ce5,requerimientos["C5"])
    print(ce6,requerimientos["C6"])
    print(diias)
    print(days)

else:
    print("El modelo no tiene solución óptima.")

print (len(lotes_finales_ordenados[288]))
for lote in lotes_finales_ordenados:
    if len(lote) <20:
        lote.append(0)
        lote.append(-1)
print(lotes_finales_ordenados[289])

#La lista que se debe importar a la etapa 4 es "lotes_finales_ordenados"
#El atributo lote[19] es una binaria que entrega un 1 si se cosecha el lote, cero si no se cosecha
#El atributo lote[20] entrega el dia en que se debe cosechar el lote, si no se cosecha, el valor del atributo es (-1)