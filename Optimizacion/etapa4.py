import gurobipy as gp
from gurobipy import GRB

# Crear el modelo
model = gp.Model("Optimizacion de Tanques y Lotes")

# Conjuntos
P = ...  # Conjunto de plantas disponibles
E = ...  # Conjunto de tanques disponibles en cada planta
T = ...  # Conjunto de los días a optimizar
J = ...  # Conjunto de lotes aptos para la industrialización
E_ad = ...  # Conjunto de tanques adicionales que se pueden contratar

# Parámetros
u = ...  # Cantidad de uva de lote j a recibir en día t
h = ...  # 1 si el lote j es de cepa c
C = ...  # Capacidad máxima de tanque e en planta p
Cmin = ...  # Capacidad mínima para que se active el tanque e en planta p
T_promedio = ...  # Tiempo promedio de fermentación del tanque e
q = ...  # Calidad de la uva de lote j por recibir en t
C1 = ...  # Costo por arrendar tanques adicionales durante la temporada
B = ...  # Umbral de calidad de uva que no requiere rectificar
C_trans = ...  # Costo de almacenamiento en transporte por día
C_rect = ...  # Costo de rectificación de un tanque
U = ...  # Capacidad de almacenamiento en planta p (litros de vino)
R = ...  # Pérdida de calidad de la uva por día de espera en camión en el día t
H = ...  # Cantidad de uva en kg por lote j
D = ...  # Día en que lote j está listo para ser recibido
C_ad = ...  # Define la capacidad de los tanques adicionales que se pueden contratar en cada planta p
C_jt = ...  # Costo de desechar un lote j en base a la calidad t

# Variables de decisión
t = {}  # Variable binaria: 1 si lote j se guarda en transporte para el día t, 0 e.o.c
s = {}  # Variable binaria: 1 si lote j se recibe para el día t, 0 e.o.c
r = {}  # Variable binaria: 1 si se rectifica el tanque e en el día t
e = {}  # Variable binaria: 1 si se contrata un tanque adicional en la planta p en el día t
y = {}  # Variable binaria: 1 si el tanque e está lleno o no en el día t
v = {}  # Cantidad de vino de lote j enviado a la planta p y al tanque e en día t
d = {}  # Día en que el lote j entra a tanque t
b = {}  # Variable binaria: 1 si el contenido de la planta p del tanque e se rectifica en el día t
x = {}  # Cantidad de uva del lote j enviada a la planta p en el tanque e en el día t
ql = {}  # Calidad en planta p en el tanque e en el día t
Q = {}  # Calidad final del lote j al entrar a procesamiento en el día t
z = {}  # Variable binaria: 1 si el lote j de la cepa c se almacena en el tanque e en la planta p en el día t

# Crear variables de decisión en el modelo
for j in J:
    for t in T:
        t[j, t] = model.addVar(vtype=GRB.BINARY, name=f"t_{j}_{t}")
        s[j, t] = model.addVar(vtype=GRB.BINARY, name=f"s_{j}_{t}")
        Q[j, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"Q_{j}_{t}")

for e in E:
    for t in T:
        r[e, t] = model.addVar(vtype=GRB.BINARY, name=f"r_{e}_{t}")
        y[e, t] = model.addVar(vtype=GRB.BINARY, name=f"y_{e}_{t}")

for p in P:
    for t in T:
        e[p, t] = model.addVar(vtype=GRB.BINARY, name=f"e_{p}_{t}")

for j in J:
    for p in P:
        for e in E:
            for t in T:
                v[j, p, e, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"v_{j}_{p}_{e}_{t}")
                d[j, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"d_{j}_{t}")
                x[j, p, e, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"x_{j}_{p}_{e}_{t}")
                ql[p, e, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"ql_{p}_{e}_{t}")

for c in C:
    for j in J:
        for t in T:
            z[j, c, p, e, t] = model.addVar(vtype=GRB.BINARY, name=f"z_{j}_{c}_{p}_{e}_{t}")

# Actualizar el modelo para agregar las variables
model.update()

# Restricciones
for j in J:
    for t in T:
        model.addConstr(Q[j, t] == q[j, t] - (d[j, t] - D[j]) * R[t], f"Rest1_{j}_{t}")

for j in J:
    for t in T:
        model.addConstr(t[j, t] + s[j, t] <= 1, f"Rest2_{j}_{t}")

for p in P:
    for j in J:
        for t in T:
            for c in C:
                model.addConstr(
                    quicksum(x[j, p, e, t] * h[j, c] for e in E) == u[j, t], f"Rest3_{p}_{j}_{t}_{c}"
                )

for j in J:
    for t in T:
        model.addConstr(
            0.5 * quicksum(x[j, p, e, t] for p in P for e in E) == quicksum(v[j, p, e, t] for p in P for e in E),
            f"Rest4_{j}_{t}",
        )

for p in P:
    for e in E:
        for t in T:
            model.addConstr(quicksum(z[j, c, p, e, t] for j in J for c in C) == 1, f"Rest5_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            model.addConstr(
                quicksum(v[j, p, e, t] for j in J for c in C) <= C[e, p] * y[e, t], f"Rest6_{p}_{e}_{t}"
            )

for p in P:
    for e in E:
        for t in T:
            model.addConstr(
                quicksum(v[j, p, e, t] for j in J for c in C) >= Cmin[e, p] * y[e, t], f"Rest7_{p}_{e}_{t}"
            )

for p in P:
    for e in E:
        for t in T:
            model.addConstr(y[e, t] <= quicksum(v[j, p, e, t] for j in J for c in C), f"Rest8_{p}_{e}_{t}")

for p in P:
    for j in J:
        for t in T:
            model.addConstr(quicksum(v[j, p, e, t] for e in E for c in C) <= U[p], f"Rest9_{p}_{j}_{t}")

for p in P:
    for e in E:
        for t in T:
            model.addConstr(
                ql[p, e, t]
                == (quicksum(x[j, p, e, t] * Q[j, t] for j in J) / quicksum(x[j, p, e, t] for j in J)),
                f"Rest10_{p}_{e}_{t}",
            )

for p in P:
    for e in E:
        for t in T:
            model.addConstr(ql[p, e, t] <= B + M * (1 - r[e, t]), f"Rest11_{p}_{e}_{t}")

for p in P:
    for t in T:
        model.addConstr(
            quicksum(C[e, p] * y[e, t] for e in E) + quicksum(C_ad[e_ad] * e[p, t] for e_ad in E_ad) >=
            quicksum(v[j, p, e, t] for j in J),
            f"Rest12_{p}_{t}",
        )

# Función objetivo
obj = (
        quicksum(
            C_rect * r[e, t] for e in E for t in T
        )
        + quicksum(
    C1 * e[p, t] for p in P for t in T
)
        + quicksum(
    C_trans * t[j, t] * H[j] for j in J for t in T
)
        + quicksum(
    C_desecho * (1 - t[j, t]) for j in J for t in T
)
)
model.setObjective(obj, GRB.MINIMIZE)

# Optimizar el modelo
model.optimize()
