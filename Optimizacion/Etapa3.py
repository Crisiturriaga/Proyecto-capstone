import gurobipy as gp
from Etapa1 import Requerimientos,prop
from Etapa2 import lotes_finales_ordenados, lote_info
import numpy as np

# Creación del modelo
m = gp.Model()

# Índices
S = []  # Conjunto de lotes comprados con spot
F = [] # Conjunto de lotes comprados con forward
for i in lotes_finales_ordenados:
    if i[15] == 1:
        S.append(i[0])
    elif i[16] == 1:
        F.append(i[0])

Conjunto_final = {}
L = range(1, 291)

T = range(0, 150) # Periodos
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

#for clave, valor in d_l.items():
    #d_l[clave] = valor + dia_estimado()


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



#for l in range(0,len(L)):
    #tipo_uva = L[l][(len(L[l]) - 2):len(L[l])]
    #tipo_uva_con_comillas = "'" + tipo_uva + "'"
    #for t in T:
        #if (d_l[L[l]] - 7) <= t <= (d_l[L[l]]) + 7:
            #calidad_dia_final = funcion_cuadratica_calidad(tipo_uva, (t - (d_l[L[l]])), l)
            #q_lt[L[l], t] = calidad_dia_final
        #else:
            #q_lt[L[l], t] = 0


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



q_lt = {} # Calidad del lote l en el periodo t
M = 1 #parametro grande considernado

#Actualizar los dias optimos de cada lote incluyendo variabilidad



# Variables de Decisión
x_compra = m.addVars(L, T, vtype=gp.GRB.BINARY, name="Eleccion de compra")
#y_lt = m.addVars(L, T, vtype=GRB.BINARY, name="x")
#xd_lt = m.addVars(L, T, vtype=GRB.BINARY, name="xd")
#z_lt = m.addVars(L,T, vtype=GRB.BINARY, name="z")
#dc_l = m.addVars(L, vtype=GRB.CONTINUOUS, name="dc")
#w_ct = m.addVars(C, T, vtype=GRB.CONTINUOUS, name="w")

# Imprimir contenido de q para una clave específica (por ejemplo, la clave 1)



#Función Objetivo
# Agrega esto antes de la línea que genera el error

m.setObjective(
    gp.quicksum(gp.quicksum(kg[l]*costo[l]*(x_spot[l] * q[l][t] + x_fwd[l] * 0.8)*r[l]*x_compra[l, t] for t in T) for l in L ), 
    sense = gp.GRB.MINIMIZE
)


#m.setObjective(sum(q_lt[l, t]*x_lt[l, t] - M*riesgo_l[l]  for l in L for t in T), GRB.MAXIMIZE)

#Restricciones
for c in Cepas:
    m.addConstr(gp.quicksum(kg[l]* x_compra[l, t] for l in L for t in T) >= requerimientos[c], name=f"restriccion_requerimientos_{c}")


for l in L:
    m.addConstr(gp.quicksum(x_compra[l, t] * q[l][t] for t in T) >= umbral[l], name=f"restriccion_cosechar_sobre_umbral_{l}")

for l in L:
    m.addConstr(gp.quicksum(x_compra[l, t]for t in T)<= 1, name = f"restriccion comprar solo en un periodo")
#for l in S:
    #Aviso de cosecha para los lotes de tipo forward (que aviso se emita dos dias antes)
    #m.addConstr(d_l[l] - dc_l[l] == 2, name=f"restr1_{l}")

#for l in F:
    #Aviso de cosecha para los lotes de tipo spot (aviso tiene que ser 5 dias antes)
    #m.addConstr(d_l[l] - dc_l[l] >= 5, name=f"restr2_{l}")

#for l in L:
    #Sumatoria a lo largo de los periodos que dice que un lote debe ser enviado a la planta o debe ser desechado
    #m.addConstr(sum(x_lt[l, t] + xd_lt[l, t] for t in T) == 1, name=f"restr3_{l}")

#for f in C:
    #for t in T:
        #m.addConstr(sum(z_lt[l, t] * r_cl[f,l] for c, l in r_cl if l in L and  c == f) == w_ct[f, t], name=f"restr5_{f}_{t}")

#for f in C:
    #m.addConstr(sum(z_lt[l, t] * r_cl[f,l]  for c, l in r_cl if l in L and  c == f for t in T) >= d_c[f], name=f"restr6_{f}")

# Agrega restricciones para calcular la calidad en función del día de cosecha --------
#----------------------------------

#for l in L:
    #for t in T:
        #m.addConstr(0 <= (q_lt[l, t] - u_l[l])* z_lt[l,t])

# Suponiendo que 'm' es el modelo de Gurobi
#for l in L:
    #for t in T:
        #m.addConstr(y_lt[l, t] <= x_lt[l, t], name=f"Restriction_y_x_{l}_{t}")

#for l in L:
    #m.addConstr(sum(z_lt[l,t] for t in T) <= 1, name=f"restr3_{l}")


# Suponiendo que 'm' es el modelo de Gurobi
#for l in L:
    #for t in T:
        #m.addConstr(y_lt[l, t] >= z_lt[l,t], name=f"Restriction_y_z_{l}_{t}")

# Suponiendo que 'm' es el modelo de Gurobi
#for l in L:
    #for t in T:
        #m.addConstr(y_lt[l, t] >= x_lt[l, t] + z_lt[l,t] - 1, name=f"Restriction_y_x_z_{l}_{t}")

#Resolver el modelo
m.optimize()

# Imprimir solución
if m.status == gp.GRB.OPTIMAL:
    # Imprimir valor de la función objetivo
    print(f"Valor de la función objetivo: {m.objVal}")

    # Imprimir variables de decisión
    listita = 0
    for l in L:
        for t in T:
            valor_x_compra = x_compra[l, t].x
            if valor_x_compra>0:
                listita += 1
                print(f"x_compra[{l}, {t}] = {valor_x_compra}")
    print(listita)


    # Puedes agregar más variables de decisión según sea necesario

else:
    print("El modelo no tiene solución óptima.")


