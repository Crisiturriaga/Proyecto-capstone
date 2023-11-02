from gurobipy import Model, GRB, quicksum

# Creación del modelo
m = Model("OptimizacionFermentacion")

# Índices
# Índices
P = ['Planta1', 'Planta2', 'Planta3']  # Plantas disponibles
Tramos = ['Tramo1', 'Tramo2', 'Tramo3']  # Tramos disponibles en cada planta
E = [(p, tramo, f'Tanque{tanque}') for p in P for tramo in Tramos for tanque in range(1, 25)]  # Tanques disponibles en cada tramo de cada planta
T = list(range(1, 161))  # Días a optimizar, del día 1 al día 160
J = [f'Lote{i}' for i in range(1, 291)]  # Lotes aptos para la industrialización, del Lote1 al Lote290

# Cada planta puede contratar 2 tramos adicionales
Tramos_adicionales = ['TramoAd1', 'TramoAd2']

# Cada tramo tiene 24 tanques
Tanques_por_tramo = 24
E_ad = [(planta, tramo, f'Tanque{tanque}') for planta in P for tramo in Tramos_adicionales for tanque in range(1, Tanques_por_tramo + 1)]
C = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']  # Ejemplo de cepas

# Parámetros (estos son ejemplos y deben ser reemplazados por tus datos reales)
u_jt = {(j, t): 10 for j in J for t in T}  # Cantidad de uva de lote j a recepcionar en día t
h_jc = {(j, c): 1 if c in j else 0 for j in J for c in C}  # 1 si el lote j es de cepa c
C_ep = {(e): 100 for e in E}  # Capacidad máxima de tanque e en planta p
Cmin_ep = {(e): 50 for e in E}  # Capacidad mínima para que se active el tanque e en planta p
T_e = {e: 5 for e in E}  # Tiempo promedio de fermentación del tanque e
q_jt = {(j, t): 0.8 for j in J for t in T}  # Calidad de la uva de lote j por recepcionar en t
C1 = 100  # Costo por arrendar tanques adicionales durante la temporada
B = 0.7  # Umbral de calidad de uva que no requiere rectificar
C_trans = 2  # Costo de almacenamiento en transporte por día
C_rect = 50  # Costo de rectificación de un tanque
U_p = {p: 500 for p in P}  # Capacidad de almacenamiento en planta p (litros de vino)
R_t = {t: 0.01 for t in T}  # Pérdida de calidad de la uva por día de espera en camión en el día t
H_j = {j: 1000 for j in J}  # cantidad de uva en kg por lote j
D_j = {j: 1 for j in J}  # Día en que lote j está listo para recepcionarse
C_eadp = {(e_ad, p): 150 for e_ad in E_ad for p in P}  # Define la capacidad de los tanques adicionales que se pueden contratar en cada planta p
C_jt = {(j, t): 20 for j in J for t in T}  # costo de desechar un lote j en base a la calidad t

# Variables de Decisión
t_jt = m.addVars(J, T, vtype=GRB.BINARY, name="t")
s_jt = m.addVars(J, T, vtype=GRB.BINARY, name="s")
r_et = m.addVars(E, T, vtype=GRB.BINARY, name="r")
e_pt = m.addVars(P, T, vtype=GRB.BINARY, name="e")
y_et = m.addVars(E, T, vtype=GRB.BINARY, name="y")
y_et = m.addVars(E, T, vtype=GRB.BINARY, name="y")
v_jpet = m.addVars(J, P, E, T, vtype=GRB.CONTINUOUS, name="v")
b_pet = m.addVars(P, E, T, vtype=GRB.BINARY, name="b")
x_jpet = m.addVars(J, P, E, T, vtype=GRB.CONTINUOUS, name="x")
ql_pet = m.addVars(P, E, T, vtype=GRB.CONTINUOUS, name="ql")
Q_jt = m.addVars(J, T, vtype=GRB.CONTINUOUS, name="Q")
z_jpetc = m.addVars(J, P, E, T, C, vtype=GRB.BINARY, name="z")
w_jpet = m.addVars(J, P, E, T, vtype=GRB.BINARY, name="w")
f_ept = m.addVars(E, P, T, vtype=GRB.CONTINUOUS, name="f")
v_ept = m.addVars(E, P, T, vtype=GRB.BINARY, name="v")

# Función Objetivo
m.setObjective(
    quicksum(C_rect * r_et[e, t] for e in E for t in T) +
    quicksum(C1 * e_pt[p, t] for p in P for t in T) +
    quicksum(C_trans * t_jt[j, t] * H_j[j] for j in J for t in T) +
    quicksum(C_jt[j, t] * (1 - t_jt[j, t]) for j in J for t in T),
    GRB.MINIMIZE
)

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
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")



