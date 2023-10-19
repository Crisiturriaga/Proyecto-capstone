import gurobipy as gp
from gurobipy import GRB

# Crear el modelo
model = gp.Model("Producción de Vino y Gestión de Barricas")

# Conjuntos
C = ...  # Conjunto de cepas
V = ...  # Conjunto de tipos de vinos
M = ...  # Conjunto de mercados
X = ...  # Conjunto de recetas
B = ...  # Conjunto de todas las barricas
T = ...  # Periodo de tiempo en días a optimizar

# Parámetros
cf = ...  # Costo de fermentación de 1 litro de vino
r = ...  # Cantidad de cepa c requerida para hacer receta x del vino v
d = ...  # Variable binaria: 1 si cepa c requerida para hacer receta x del vino v, 0 e.o.c
L = ...  # Litros de vino de la cepa c que vienen del estanque e
D = ...  # Demanda en el mercado m para el vino de tipo t
P = ...  # Precio de venta del vino de tipo v en el mercado m

# Variables de decisión
Y = {}  # Variable binaria: 1 si el tipo de vino v se produce en el mercado m en el día t
Dv = {}  # Cantidad en litros de vino del tipo v destinado al mercado m en el día t
O = {}  # Variable binaria: 1 si la barrica b está ocupada en el período t
X = {}  # Cantidad de litros de cepa c utilizado para la receta x en el período t
A = {}  # Variable binaria para verificar si el vino v en la barrica b ha excedido el tiempo de 10 días en el día t

# Crear variables de decisión en el modelo
for v in V:
    for m in M:
        for t in T:
            Y[v, m, t] = model.addVar(vtype=GRB.BINARY, name=f"Y_{v}_{m}_{t}")
            Dv[v, m, t] = model.addVar(vtype=GRB.CONTINUOUS, name=f"Dv_{v}_{m}_{t}")

for c in C:
    for x in X:
        for t in T:
            for b in B:
                X[c, x, t, b] = model.addVar(vtype=GRB.CONTINUOUS, name=f"X_{c}_{x}_{t}_{b}")

for b in B:
    for t in T:
        O[b, t] = model.addVar(vtype=GRB.BINARY, name=f"O_{b}_{t}")
        for v in V:
            A[v, b, t] = model.addVar(vtype=GRB.BINARY, name=f"A_{v}_{b}_{t}")

# Actualizar el modelo para agregar las variables
model.update()

# Restricciones
for v in V:
    for m in M:
        for t in T:
            for x in X:
                model.addConstr(Dv[v, m, t] <= D[v, m] * Y[v, m, t], f"Rest1_{v}_{m}_{t}_{x}")

for c in C:
    for x in X:
        for t in T:
            for b in B:
                model.addConstr(X[c, x, t, b] >= r[c, x, v] * O[b, t], f"Rest2_{c}_{x}_{t}_{b}")

for x in X:
    for c in C:
        model.addConstr(
            quicksum(X[c, x, t, b] for t in T for b in B) == quicksum(L[c, p] for p in P),
            f"Rest3_{x}_{c}"
        )

for x in X:
    for b in B:
        model.addConstr(
            quicksum(X[c, x, t, b] for t in T) >= 160 * O[b, t], f"Rest4_{x}_{b}"
        )

for b in B:
    for t in T[1:]:
        model.addConstr(O[b, t] >= O[b, t - 1], f"Rest5_{b}_{t}")

for b in B:
    for t in T:
        model.addConstr(
            quicksum(O[b, t_prime] for t_prime in T if t_prime <= t) >= 10 * A[b, t], f"Rest6_{b}_{t}"
        )

for b in B:
    model.addConstr(
        quicksum(O[b, t] for t in T) <= 10, f"Rest7_{b}"
    )

# Función objetivo
obj = gp.quicksum(
    (cf * Dv[v, m, t] + gp.quicksum(d[c, x, v] * X[c, x, t, b] for c in C for x in X) for x in X)
    for v in V for m in M for t in T
) + gp.quicksum(P[v, m] * A[v, b, t] for b in B for t in T for v in V)
model.setObjective(obj, GRB.MINIMIZE)

# Optimizar el modelo
model.optimize()
