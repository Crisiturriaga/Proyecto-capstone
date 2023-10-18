import gurobipy as gp
from gurobipy import GRB

# Creación del modelo
model = gp.Model("Optimización_de_Cosecha")

# Conjuntos
P = [1, 2, 3]  # Ejemplo de conjunto P
E = [1, 2, 3]  # Ejemplo de conjunto E
T = [1, 2, 3]  # Ejemplo de conjunto T
J = [1, 2, 3]  # Ejemplo de conjunto J
Ead = [1, 2]  # Ejemplo de conjunto Ead

# Parámetros
u = {}  # Cantidad de uva de lote j a recibir en día t
h = {}  # 1 si el lote j es de cepa c
Ce = {}  # Capacidad máxima de tanque e en planta p
Cmin = {}  # Capacidad mínima para que se active el tanque e en planta p
T = {}  # Tiempo promedio de fermentación del tanque e
qj = {}  # Calidad de la uva de lote j por recibir en t
C1 =  # Costo por arrendar tanques adicionales durante la temporada
Ctrans =  # Costo de almacenamiento en transporte por día
Crect =  # Costo de rectificación de un tanque
Up = {}  # Capacidad de almacenamiento en planta p
Rt = {}  # Pérdida de calidad de la uva por día de espera en camión en el día t
H = {}  # Cantidad de uva en kg por lote j
Dj = {}  # Día en que lote j está listo para ser recibido
Ce,p = {}  # Define la capacidad de los tanques adicionales que se pueden contratar en cada planta p
C = {}  # Costo de desechar un lote j en base a la calidad t
# Variables de decisión
t = {}  # Variable binaria, 1 si lote j se guarda en transporte para el día t
for j in J:
    for t in T:
        t[j, t] = model.addVar(vtype=GRB.BINARY, name=f't_{j}_{t}')

s = {}  # Variable binaria, 1 si lote j se recibe para el día t
for j in J:
    for t in T:
        s[j, t] = model.addVar(vtype=GRB.BINARY, name=f's_{j}_{t}')

r = {}  # Variable binaria si se rectifica el tanque e en el día t
for e in E:
    for t in T:
        r[e, t] = model.addVar(vtype=GRB.BINARY, name=f'r_{e}_{t}')

ept = {}  # Variable binaria si se contrata un tanque adicional en la planta p en el día t
for p in P:
    for t in T:
        ept[p, t] = model.addVar(vtype=GRB.BINARY, name=f'ept_{p}_{t}')

yep = {}  # Variable binaria si el tanque e está lleno o no en el día t
for e in E:
    for p in P:
        for t in T:
            yep[e, p, t] = model.addVar(vtype=GRB.BINARY, name=f'yep_{e}_{p}_{t}')

vjp = {}  # Cantidad de vino de lote j enviado a la planta p y al tanque e en día t
for j in J:
    for p in P:
        for e in E:
            for t in T:
                vjp[j, p, e, t] = model.addVar(lb=0.0, name=f'vjp_{j}_{p}_{e}_{t}')

djt = {}  # Día en que el lote j entra a tanque t
for j in J:
    for t in T:
        djt[j, t] = model.addVar(lb=0, vtype=GRB.INTEGER, name=f'djt_{j}_{t}')

bpet = {}  # Variable binaria que indica si el contenido de la planta p del tanque e se rectifica en el día t
for p in P:
    for e in E:
        for t in T:
            bpet[p, e, t] = model.addVar(vtype=GRB.BINARY, name=f'bpet_{p}_{e}_{t}')

xjp = {}  # Cantidad de uva del lote j enviada a la planta p en el tanque e en el día t
for j in J:
    for p in P:
        for e in E:
            for t in T:
                xjp[j, p, e, t] = model.addVar(lb=0.0, name=f'xjp_{j}_{p}_{e}_{t}')

qlep = {}  # Calidad en planta p en el tanque e en el día t
for p in P:
    for e in E:
        for t in T:
            qlep[p, e, t] = model.addVar(lb=0.0, ub=1.0, name=f'qlep_{p}_{e}_{t}')

Qjt = {}  # Calidad final del lote j al entrar a procesamiento en el día t
for j in J:
    for t in T:
        Qjt[j, t] = model.addVar(lb=0.0, ub=1.0, name=f'Qjt_{j}_{t}')

z = {}  # Variable binaria que indica si el lote j de la cepa c se almacena en el tanque e en la planta p en el día t
for j in J:
    for p in P:
        for e in E:
            for t in T:
                for c in C:
                    z[j, p, e, t, c] = model.addVar(vtype=GRB.BINARY, name=f'z_{j}_{p}_{e}_{t}_{c}')

jpetc = {}  # Resto de las variables
for j in J:
    for p in P:
        for e in E:
            for t in T:
                for c in C:
                    jpetc[j, p, e, t, c] = model.addVar(lb=0.0, name=f'jpetc_{j}_{p}_{e}_{t}_{c}')

# Resto del código...
# Restricciones adicionales
for j in J:
    for t in T:
        model.addConstr(Qjt[j, t] == qj[j, t] - (djt[j, t] - Dj) * Rt, name=f'restriccion1_{j}_{t}')

for j in J:
    for t in T:
        model.addConstr(t[j, t] + s[j, t] <= 1, name=f'restriccion2_{j}_{t}')

for p in P:
    for j in J:
        for t in T:
            for c in C:
                model.addConstr(sum(xjp[j, p, e, t] * z[j, p, e, t, c] for e in E) == u[j, t], name=f'restriccion3_{p}_{j}_{t}_{c}')

for j in J:
    for t in T:
        model.addConstr(0.5 * sum(xjp[j, p, e, t] for p in P for e in E) == sum(vjp[j, p, e, t] for p in P for e in E), name=f'restriccion4_{j}_{t}')

for p in P:
    for e in E:
        for t in T:
            for c in C:
                model.addConstr(sum(z[j, p, e, t, c] for j in J) == 1, name=f'restriccion5_{p}_{e}_{t}_{c}')

for p in P:
    for e in E:
        for t in T:
            model.addConstr(sum(vjp[j, p, e, t] for j in J) <= Ce[e, p] * yep[e, t], name=f'restriccion6_{p}_{e}_{t}')

for p in P:
    for e in E:
        for t in T:
            model.addConstr(sum(vjp[j, p, e, t] for j in J) >= Cmin[e, p] *

model.setObjective(
    gp.quicksum(Crect * r[e, t] for p in P for e in E for t in T) +
    gp.quicksum(C1 * ep[p, t] for p in P for t in T) +
    gp.quicksum(Ctrans * t[j, t] * H[j] for j in J for t in T) +
    gp.quicksum(Cj[t] * (1 - t[j, t]) for j in J for t in T),
    GRB.MINIMIZE
)