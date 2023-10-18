import gurobipy as gp

# Conjuntos
L = range(1, num_lotes + 1)
T = range(1, num_periodos + 1)

# Crear el modelo
model = gp.Model()

# Variables de decisión
x_spot = model.addVars(L, vtype=gp.GRB.BINARY, name="x_spot")  # Variable binaria: 1 si el lote l se compra con contrato spot, 0 en otro caso
x_forward = model.addVars(L, vtype=gp.GRB.BINARY, name="x_forward")  # Variable binaria: 1 si el lote l se compra con contrato forward, 0 en otro caso
forward_quantity = model.addVars(L, T, name="forward_quantity")  # Cantidad de lote l en el período t con contrato forward

# Función objetivo
model.setObjective(gp.quicksum(cl * (x_spot[l] * qlt + x_forward[l] * 0.8 * rl) for l in L), sense=gp.GRB.MINIMIZE)

# Restricciones
model.addConstrs((x_spot[l] + x_forward[l] == 1 for l in L), name="contrato_selector")

# Resolver el modelo
model.optimize()
