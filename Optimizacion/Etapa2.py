import gurobipy as gp

# Conjuntos
L = range(1, num_lotes + 1)
T = range(1, num_periodos + 1)

# Parámetros
q = {}  # Calidad del lote en cada periodo
c = {}  # Costo por kilo de uva de lote
r = {}  # Riesgo de comprar el lote con contrato forward


# Crear el modelo
model = gp.Model()

# Variables de decisión
x_spot = model.addVars(L, vtype=gp.GRB.BINARY, name="x_spot")  # Variable binaria: 1 si el lote l se compra con contrato spot, 0 en otro caso
x_forward = model.addVars(L, vtype=gp.GRB.BINARY, name="x_forward")  # Variable binaria: 1 si el lote l se compra con contrato forward, 0 en otro caso
forward_quantity = model.addVars(L, T, name="forward_quantity")  # Cantidad de lote l en el período t con contrato forward


# Función Objetivo
model.setObjective(quicksum(c[l] * (x_spot[l] * q[l, t] + x_forward[l] * 0.8 * r[l]) for l in L for t in T), GRB.MINIMIZE)
# Restricciones
for l in L:
    model.addConstr(x_spot[l] + x_forward[l] == 1, name=f'restriccion1_{l}')

# Resolver el modelo
model.optimize()
