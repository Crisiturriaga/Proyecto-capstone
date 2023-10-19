import gurobipy as gp
from gurobipy import GRB

# Crear el modelo
model = gp.Model("Optimización de Calidad de Lotes")

# Conjuntos
S = ...  # Conjunto de lotes comprados con spot
F = ...  # Conjunto de lotes comprados con forward
L = ...  # Conjunto de todos los lotes

# Parámetros
r = ...  # Rendimiento del lote l
d = ...  # Día óptimo de cosecha del lote l
d_c = ...  # Cantidad de cepa c requerida
u_c = ...  # Umbral de industrialización de cepa c
h = ...  # 1 si el lote l es de cepa c
M = ...  # Un valor grande que actúa como cota superior

# Variables de decisión
x = {}  # 1 si el lote l es enviado a la planta en el período t
xd = {}  # 1 si el lote l es desechado en el período t
y = {}  # 1 si el lote l se cosecha en el período t
z = {}  # 1 si la calidad del lote l es mayor al umbral u_l
v = {}  # 1 si la calidad del lote l es menor al umbral u_l
q = {}  # Calidad del lote l en el período t

# Crear variables de decisión en el modelo
for l in L:
    for t in T:
        x[l, t] = model.addVar(vtype=GRB.BINARY, name=f"x_{l}_{t}")
        xd[l, t] = model.addVar(vtype=GRB.BINARY, name=f"xd_{l}_{t}")
        y[l, t] = model.addVar(vtype=GRB.BINARY, name=f"y_{l}_{t}")
        z[l] = model.addVar(vtype=GRB.BINARY, name=f"z_{l}")
        v[l] = model.addVar(vtype=GRB.BINARY, name=f"v_{l}")
        q[l, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"q_{l}_{t}")

# Actualizar el modelo para agregar las variables
model.update()

# Restricciones
for l in S:
    model.addConstr(d[l] - d_c[l] == 2, name=f"Rest1_{l}")

for l in F:
    model.addConstr(d[l] - d_c[l] >= 5, name=f"Rest2_{l}")

for l in L:
    model.addConstr(gp.quicksum(x[l, t] + xd[l, t] for t in T) == 1, name=f"Rest3_{l}")

model.addConstr(gp.quicksum(y[l, t] for l in L for t in T) == 290, name="Rest4")

for c in C:
    for t in T:
        model.addConstr(
            gp.quicksum(y[l, t] * r[l] * h[l, c] * z[l] for l in L) == w[c, t], name=f"Rest5_{c}_{t}"
        )

for c in C:
    model.addConstr(
        gp.quicksum(x[l, t] * h[l, c] for l in L for t in T) >= d_c[c], name=f"Rest6_{c}"
    )

for l in L:
    model.addConstr(
        (u_c * h[l, c] - q[l, d_c[l]]) * z[l] >= 0, name=f"Rest7_{l}"
    )

for l in L:
    model.addConstr(
        v[l] * M >= z[l], name=f"Rest8_{l}"
    )

for c in C:
    for t in T:
        model.addConstr(
            gp.quicksum(y[l, t] * r[l] * h[l, c] * v[l] for l in L) == xd[l, t], name=f"Rest9_{c}_{t}"
        )

for l in L:
    for t in T:
        model.addConstr(
            q[l, t] == gp.max_(gp.min_(at[t] ** 2 + bt[t] + c[t], 1), 0), name=f"Rest10_{l}_{t}"
        )

# Función objetivo
model.setObjective(gp.quicksum(q[l, t] for l in L for t in T), GRB.MAXIMIZE)

# Optimizar el modelo
model.optimize()
