from gurobipy import Model, GRB

# Creación del modelo
m = Model("OptimizacionFermentacion")

# Índices
P = [...]  # Conjunto de las plantas disponibles
E = [...]  # Conjunto de tanques disponibles en cada planta
T = [...]  # Conjunto de los días a optimizar
J = [...]  # Conjunto de lotes aptos para la industrizlización
E_ad = [...]  # Conjunto de tanques adicionales que se pueden contratar
C = [...]  # Cepas

# Parámetros
u_jt = {...}  # Cantidad de uva de lote j a recepcionar en día t
h_jc = {...}  # 1 si el lote j es de cepa c
C_ep = {...}  # Capacidad máxima de tanque e en planta p
Cmin_ep = {...}  # Capacidad mínima para que se active el tanque e en planta p
T_e = {...}  # Tiempo promedio de fermentación del tanque e
q_jt = {...}  # Calidad de la uva de lote j por recepcionar en t
C1 = ...  # Costo por arrendar tanques adicionales durante la temporada
B = ...  # Umbral de calidad de uva que no requiere rectificar
C_trans = ...  # Costo de almacenamiento en transporte por día
C_rect = ...  # Costo de rectificación de un tanque
U_p = {...}  # Capacidad de almacenamiento en planta p (litros de vino)
R_t = {...}  # Pérdida de calidad de la uva por día de espera en camión en el día t
H_j = {...}  # cantidad de uva en kg por lote j
D_j = {...}  # Día en que lote j está listo para recepcionarse
C_eadp = {...}  # Define la capacidad de los tanques adicionales que se pueden contratar en cada planta p
C_jt = {...}  # costo de desechar un lote j en base a la calidad t

# Variables de Decisión
t_jt = m.addVars(J, T, vtype=GRB.BINARY, name="t")
s_jt = m.addVars(J, T, vtype=GRB.BINARY, name="s")
r_et = m.addVars(E, T, vtype=GRB.BINARY, name="r")
e_pt = m.addVars(P, T, vtype=GRB.BINARY, name="e")
y_et = m.addVars(E, T, vtype=GRB.BINARY, name="y")
v_jpet = m.addVars(J, P, E, T, vtype=GRB.CONTINUOUS, name="v")
d_jt = m.addVars(J, T, vtype=GRB.CONTINUOUS, name="d")
b_pet = m.addVars(P, E, T, vtype=GRB.BINARY, name="b")
x_jpet = m.addVars(J, P, E, T, vtype=GRB.CONTINUOUS, name="x")
ql_pet = m.addVars(P, E, T, vtype=GRB.CONTINUOUS, name="ql")
Q_jt = m.addVars(J, T, vtype=GRB.CONTINUOUS, name="Q")
z_jpetc = m.addVars(J, P, E, T, C, vtype=GRB.BINARY, name="z")

# Función Objetivo
m.setObjective(sum(C_rect * r_et[e, t] for e in E for t in T) + sum(C1 * e_pt[p, t] for p in P for t in T) + sum(C_trans * t_jt[j, t] * H_j[j] for j in J for t in T) + sum(C_jt[j, t] * (1 - t_jt[j, t]) for j in J for t in T), GRB.MINIMIZE)

# Restricciones
for j in J:
    for t in T:
        m.addConstr(Q_jt[j, t] == q_jt[j, t] - (d_jt[j, t] - D_j[j]) * R_t[t], name=f"restr1_{j}_{t}")

for j in J:
    for t in T:
        m.addConstr(t_jt[j, t] + s_jt[j, t] <= 1, name=f"restr2_{j}_{t}")

for p in P:
    for j in J:
        for t in T:
            m.addConstr(sum(x_jpet[j, p, e, t] for e in E) * s_jt[j, t] == u_jt[j, t], name=f"restr3_{p}_{j}_{t}")

for j in J:
    for t in T:
        m.addConstr(0.5 * sum(x_jpet[j, p, e, t] for p in P for e in E) == sum(v_jpet[j, p, e, t] for p in P for e in E), name=f"restr4_{j}_{t}")

for c in C:
    for p in P:
        for e in E:
            for t in T:
                m.addConstr(z_jpetc[j, p, e, t, c] == 1, name=f"restr5_{c}_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(sum(v_jpet[j, p, e, t] for j in J) <= C_ep[e, p] * y_et[e, t], name=f"restr6_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(sum(v_jpet[j, p, e, t] for j in J) >= Cmin_ep[e, p] * y_et[e, t], name=f"restr7_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(y_et[e, t] <= sum(v_jpet[j, p, e, t] for j in J), name=f"restr8_{p}_{e}_{t}")

for p in P:
    for j in J:
        for t in T:
            m.addConstr(sum(v_jpet[j, p, e, t] for e in E) <= U_p[p], name=f"restr9_{p}_{j}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(ql_pet[p, e, t] == sum(x_jpet[j, p, e, t] * Q_jt[j, t] for j in J) / sum(x_jpet[j, p, e, t] for j in J), name=f"restr10_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(ql_pet[p, e, t] <= B + (1 - r_et[e, t]), name=f"restr11_{p}_{e}_{t}")

for p in P:
    for t in T:
        m.addConstr(sum(C_ep[e, p] * y_et[e, t] for e in E) + sum(C_eadp[e_ad, p] * e_pt[p, t] for e_ad in E_ad) >= sum(v_jpet[j, p, e, t] for j in J for e in E), name=f"restr12_{p}_{t}")

# Resolver el modelo
m.optimize()

# Imprimir solución (esto es opcional)
if m.status == GRB.OPTIMAL:
    for j in J:
        for t in T:
            print(f"t_{j}_{t}:", t_jt[j, t].x)
            print(f"s_{j}_{t}:", s_jt[j, t].x)
