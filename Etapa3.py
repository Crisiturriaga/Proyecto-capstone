import gurobipy as gp
from gurobipy import GRB

# Crear un modelo
model = gp.Model("Optimización_de_Cosecha")

# Conjuntos
S = [1, 2, 3]  # Ejemplo de conjunto S
F = [4, 5, 6]  # Ejemplo de conjunto F
L = S + F
T = [1, 2, 3]  # Ejemplo de conjunto T
C = [1, 2]  # Ejemplo de conjunto de cepas

# Parámetros
# Define tus parámetros aquí

# Variables de decisión
x = {}  # Variable binaria, 1 si el lote l es enviado a la planta en el periodo t
xd = {}  # Variable binaria, 1 si el lote l es desechado en el periodo t
y = {}  # Variable binaria, 1 si el lote l se cosecha en el periodo t
z = {}  # Variable binaria, 1 si la calidad del lote l es mayor al umbral ul
dc = {}  # Día de aviso de cosecha del lote l
wc = {}  # Cantidad de cepa c enviada a la planta en el periodo t
ql = {}  # Calidad del lote l en el periodo t

for l in L:
    for t in T:
        x[l, t] = model.addVar(vtype=GRB.BINARY, name=f'x_{l}_{t}')
        xd[l, t] = model.addVar(vtype=GRB.BINARY, name=f'xd_{l}_{t}')
        y[l, t] = model.addVar(vtype=GRB.BINARY, name=f'y_{l}_{t}')
        ql[l, t] = model.addVar(lb=0.0, ub=1.0, name=f'ql_{l}_{t}')

for l in L:
    z[l] = model.addVar(vtype=GRB.BINARY, name=f'z_{l}')
    dc[l] = model.addVar(lb=0, vtype=GRB.INTEGER, name=f'dc_{l}')

for c in C:
    for t in T:
        wc[c, t] = model.addVar(lb=0.0, name=f'wc_{c}_{t}')

# Restricciones
# Restricciones
# 1. Restricción de igualdad para lotes comprados con spot (S)
for l in S:
    model.addConstr(dc[l] - dl == 2, name=f'restriccion1_{l}')

# 2. Restricción de desigualdad para lotes comprados con forward (F)
for l in F:
    model.addConstr(dc[l] - dl >= 5, name=f'restriccion2_{l}')

# 3. Restricción de asignación de lotes a un período
for l in L:
    model.addConstr(sum(x[l, t] + xd[l, t] for t in T) == 1, name=f'restriccion3_{l}')

# 4. Restricción de cantidad total de lotes a cosechar
model.addConstr(sum(y[l, t] for l in L for t in T) == 290, name='restriccion4')

# 5. Restricción de cantidad de cepa enviada a la planta
for c in C:
    for t in T:
        model.addConstr(sum(y[l, t] * rl * z[l] * x[l, t] * hl_c for l in L) == wc[c, t], name=f'restriccion5_{c}_{t}')

# 6. Restricción de umbral de industrialización
for c in C:
    model.addConstr(sum(x[l, t] * hl_c for l in L for t in T) >= dc[c], name=f'restriccion6_{c}')

# 7. Restricción de umbral de calidad de lote
for l in L:
    model.addConstr((ul - ql[l, t]) * z[l] >= 0, name=f'restriccion7_{l}')

# Define tus restricciones aquí

# Función objetivo
# Define tu función objetivo aquí
model.setObjective(
    gp.quicksum(ql[l, t] * y[l, t] for l in L for t in T),
    GRB.MAXIMIZE
)

# Actualizar el modelo para reflejar los cambios
model.update()

# Resolver el modelo
model.optimize()