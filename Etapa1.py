import gurobipy as gp

# Conjuntos
M = [A,B,C,D]
C = [C1,C2,C3,C4,C5,C6]
B = [Blend1, Blend2, Blend3, Blend4]
I = range(1, num_recetas + 1)

# Crear el modelo
model = gp.Model()
# Variables de decisión
x = model.addVars(I, B, vtype=gp.GRB.BINARY, ame="x")  # Variable binaria para indicar si se hace la receta i del blend b
y = model.addVars(C, B, name="y")  # Cantidad de kilos de cepa c a comprar para el blend b
z = model.addVars(C, name="z")  # Cantidad de kilos de cepa c a comprar para varietal de cepa c
v = model.addVars(C, I, B, name="v")  # Cantidad de kilos de cepa c a comprar para hacer receta i del blend b

# Función objetivo
model.setObjective(gp.quicksum(cc * (z[c] + gp.quicksum(y[c, b] for b in B)) for c in C), sense=gp.GRB.MINIMIZE)

# Restricciones
# la primera restricción garantiza que la cantidad de uvas de cepa c para el vino varietal sea al menos igual a la demanda mínima en todos los mercados m
for c in C:
    model.addConstr(z[c] >= gp.quicksum(dm, c) for dm in demanda_minima_mercado)
#La segunda restricción asegura que la cantidad de uvas de cepa c compradas para el blend b sea al menos igual a la demanda mínima en todos los mercados m.
for b in B:
    model.addConstr(gp.quicksum(y[c, b] for c in C) >= gp.quicksum(dm, b) for dm in demanda_minima_blend)
#La tercera restricción garantiza que la cantidad de cepa c comprada para la receta i del blend b sea igual a la cantidad de cepa requerida para esa receta.
for i in I:
    for b in B:
        model.addConstr(gp.quicksum(rcib * x[i, b] for c in C) == gp.quicksum(vcib for c in C))
#La cuarta restricción asegura que la cantidad total de uvas de cepa c compradas para el blend b sea igual a la cantidad de uvas de cepa c compradas en total.
for c in C:
    for b in B:
        model.addConstr(gp.quicksum(vcbi for i in I) == y[c, b])

# Resolver el modelo
model.optimize()


