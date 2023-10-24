from gurobipy import Model, GRB

# Creación del modelo
m = Model("OptimizacionReservaBarricas")

# Índices
C = [...]  # Conjunto de cepas
V = [...]  # Conjunto de tipos de vinos
M = [...]  # Conjunto de mercados
X = [...]  # Conjunto de recetas
B = [...]  # Conjunto de todas las barricas
T = [...]  # Periodo de tiempo en días a optimizar

# Parámetros
cf = ...  # Costo fermentación de 1 litro de vino
r_cxv = {...}  # Cantidad de cepa c requerida para hacer receta x del vino v
d_cxv = {...}  # Variable binaria 1 si cepa c requerida para hacer receta x del vino v, 0 eoc
L_cp = {...}  # Litros de vino de la cepa c que vienen del estanque e
D_tm = {...}  # Demanda en el mercado m para el vino de tipo t
P_vm = {...}  # Precio de venta del vino de tipo v en el mercado m

# Variables de Decisión
Y_vmt = m.addVars(V, M, T, vtype=GRB.BINARY, name="Y")
D_vxm = m.addVars(V, X, M, vtype=GRB.CONTINUOUS, name="D")
O_bt = m.addVars(B, T, vtype=GRB.BINARY, name="O")
X_cxt = m.addVars(C, X, T, vtype=GRB.CONTINUOUS, name="X")
A_vbt = m.addVars(V, B, T, vtype=GRB.BINARY, name="A")

# Función Objetivo
m.setObjective(
    sum(cf * D_vxm[v, x, m] + sum(d_cxv[c, x, v] * X_cxt[c, x, t] for c in C) for v in V for x in X for m in M for t in T) + 
    sum(P_vm[v, m] * A_vbt[v, b, t] for v in V for b in B for t in T for m in M), 
    GRB.MINIMIZE
)

# Restricciones
for v in V:
    for m in M:
        for t in T:
            for x in X:
                m.addConstr(D_vxm[v, x, m] <= D_tm[t, m] * Y_vmt[v, m, t], name=f"restr1_{v}_{m}_{t}_{x}")

for c in C:
    for x in X:
        for t in T:
            for b in B:
                m.addConstr(X_cxt[c, x, t] >= r_cxv[c, x, v] * O_bt[b, t], name=f"restr2_{c}_{x}_{t}_{b}")

for x in X:
    for c in C:
        m.addConstr(sum(D_vxm[v, x, m] for v in V for m in M) == sum(X_cxt[c, x, t] for t in T), name=f"restr3_{x}_{c}")

for x in X:
    for b in B:
        m.addConstr(sum(X_cxt[c, x, t] for c in C for t in T) >= 160 * O_bt[b, t], name=f"restr4_{x}_{b}")

for b in B:
    for t in T[1:]:
        m.addConstr(O_bt[b, t] >= O_bt[b, t-1], name=f"restr5_{b}_{t}")

for b in B:
    for t in T:
        m.addConstr(sum(O_bt[b, tp] for tp in T if tp <= t) >= 10 * A_vbt[v, b, t], name=f"restr6_{b}_{t}")

for b in B:
    m.addConstr(sum(O_bt[b, t] for t in T) <= 10, name=f"restr7_{b}")

# Resolver el modelo
m.optimize()

# Imprimir solución (esto es opcional)
if m.status == GRB.OPTIMAL:
    for v in V:
        for m in M:
            for t in T:
                print(f"Y_{v}_{m}_{t}:", Y_vmt[v, m, t].x)
