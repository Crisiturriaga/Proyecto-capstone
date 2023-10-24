from gurobipy import Model, GRB

# Creación del modelo
m = Model("OptimizacionCompraLotes")

# Índices
L = [...]  # Debes definir los elementos del conjunto de lotes
T = [...]  # Debes definir los elementos del conjunto de periodos

# Parámetros
q_lt = {...}  # Debes definir los valores para cada l y t
c_l = {...}   # Debes definir los valores para cada l
r_l = {...}   # Debes definir los valores para cada l

# Variables de Decisión
x_spot_l = m.addVars(L, vtype=GRB.BINARY, name="x_spot")
x_forward_l = m.addVars(L, vtype=GRB.BINARY, name="x_forward")

# Función Objetivo
m.setObjective(sum(c_l[l] * (x_spot_l[l] * q_lt[l, t] + x_forward_l[l] * 0.8 * r_l[l]) for l in L for t in T), GRB.MINIMIZE)

# Restricciones
for l in L:
    m.addConstr(x_spot_l[l] + x_forward_l[l] == 1, name=f"restr1_{l}")

# Resolver el modelo
m.optimize()

# Imprimir solución (esto es opcional)
if m.status == GRB.OPTIMAL:
    for l in L:
        print(f"x_spot_{l}:", x_spot_l[l].x)
        print(f"x_forward_{l}:", x_forward_l[l].x)
