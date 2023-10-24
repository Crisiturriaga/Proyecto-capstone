from gurobipy import Model, GRB

# Creación del modelo
m = Model("OptimizacionCosechaLotes")

# Índices
S = [...]  # Conjunto de lotes comprados con spot
F = [...]  # Conjunto de lotes comprados con forward
L = [...]  # Conjunto de todos los lotes
T = [...]  # Periodos
C = [...]  # Cepas

# Parámetros
r_l = {...}  # Rendimiento del lote l
d_l = {...}  # Día óptimo de cosecha del lote l
d_c = {...}  # Cantidad de cepa c requerida
u_c = {...}  # Umbral de industrialización de cepa c
h_lc = {...} # 1 si el lote l es de cepa c
xi = {...}   # Debes definir xi para cada t
xi_hat = {...} # Debes definir xi_hat para cada t
a, b, c = ... , ... , ...  # Coeficientes de la función cuadrática

# Variables de Decisión
x_lt = m.addVars(L, T, vtype=GRB.BINARY, name="x")
xd_lt = m.addVars(L, T, vtype=GRB.BINARY, name="xd")
y_lt = m.addVars(L, T, vtype=GRB.BINARY, name="y")
z_l = m.addVars(L, vtype=GRB.BINARY, name="z")
dc_l = m.addVars(L, vtype=GRB.CONTINUOUS, name="dc")
w_ct = m.addVars(C, T, vtype=GRB.CONTINUOUS, name="w")
v_l = m.addVars(L, vtype=GRB.BINARY, name="v")
q_lt = m.addVars(L, T, vtype=GRB.CONTINUOUS, name="q")
q_prime_lt = m.addVars(L, T, vtype=GRB.CONTINUOUS, name="q_prime")

# Función Objetivo
m.setObjective(sum(q_lt[l, t] for l in L for t in T), GRB.MAXIMIZE)

# Restricciones
for l in S:
    m.addConstr(d_l[l] - dc_l[l] == 2, name=f"restr1_{l}")

for l in F:
    m.addConstr(d_l[l] - dc_l[l] >= 5, name=f"restr2_{l}")

for l in L:
    m.addConstr(sum(x_lt[l, t] + xd_lt[l, t] for t in T) == 1, name=f"restr3_{l}")

m.addConstr(sum(y_lt[l, t] for l in L for t in T) == 290, name="restr4")

for c in C:
    for t in T:
        m.addConstr(sum(y_lt[l, t] * r_l[l] * h_lc[l, c] * z_l[l] for l in L) == w_ct[c, t], name=f"restr5_{c}_{t}")

for c in C:
    m.addConstr(sum(x_lt[l, t] * h_lc[l, c] for l in L for t in T) >= d_c[c], name=f"restr6_{c}")

for l in L:
    m.addConstr((u_c[c] * h_lc[l, c] - q_lt[l, dc_l[l]]) * z_l[l] >= 0, name=f"restr7_{l}")

M = 1000  # Valor grande para la restricción
for l in L:
    m.addConstr(v_l[l] * M >= z_l[l], name=f"restr8_{l}")

for c in C:
    for t in T:
        m.addConstr(sum(y_lt[l, t] * r_l[l] * h_lc[l, c] * v_l[l] for l in L) == xd_lt[l, t], name=f"restr9_{c}_{t}")

# Restricciones de linearización para q_lt
for l in L:
    for t in T:
        m.addConstr(q_prime_lt[l, t] <= (a*t**2 + b*t + c) * (1 - xi[t]) * (1 - xi[t-1]) * (1 - xi[t-2]) * (1 - sum(xi_hat[theta] for theta in range(1, t-2))) * (1 - sum(xi_hat[theta] for theta in range(1, t))), name=f"restr10_{l}_{t}")
        m.addConstr(q_prime_lt[l, t] <= 1, name=f"restr11_{l}_{t}")
        m.addConstr(q_lt[l, t] >= q_prime_lt[l, t], name=f"restr12_{l}_{t}")
        m.addConstr(q_lt[l, t] >= 0, name=f"restr13_{l}_{t}")

# Resolver el modelo
m.optimize()

# Imprimir solución (esto es opcional)
if m.status == GRB.OPTIMAL:
    for l in L:
        for t in T:
            print(f"x_{l}_{t}:", x_lt[l, t].x)
            print(f"xd_{l}_{t}:", xd_lt[l, t].x)
            print(f"y_{l}_{t}:", y_lt[l, t].x)

