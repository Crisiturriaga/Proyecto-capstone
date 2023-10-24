from gurobipy import Model, GRB

# Leer base de datos y crear una lista de listas con la data
import pandas as pd
df = pd.read_csv('datos.csv')
lista_de_listas = df.values.tolist()
print(lista_de_listas)

# Creación del modelo
m = Model("OptimizacionUvas")

# Índices
M = [...]  # Debes definir los elementos del conjunto de mercados
C = [...]  # Debes definir los elementos del conjunto de cepas
B = [...]  # Debes definir los elementos del conjunto de blends
I = [...]  # Debes definir los elementos del conjunto de recetas por blend

# Parámetros
d_mc = {...}  # Debes definir los valores para cada m y c
d_mb = {...}  # Debes definir los valores para cada m y b
c_c = {...}   # Debes definir los valores para cada c
r_cib = {...} # Debes definir los valores para cada c, i y b

# Variables de Decisión
x_ib = m.addVars(I, B, vtype=GRB.BINARY, name="x")
y_cb = m.addVars(C, B, vtype=GRB.CONTINUOUS, name="y")
z_c = m.addVars(C, vtype=GRB.CONTINUOUS, name="z")
v_cib = m.addVars(C, I, B, vtype=GRB.CONTINUOUS, name="v")

# Función Objetivo
m.setObjective(sum(c_c[c] * (z_c[c] + sum(y_cb[c, b] for b in B)) for c in C), GRB.MINIMIZE)

# Restricciones
for c in C:
    m.addConstr(z_c[c] >= sum(d_mc[m, c] for m in M), name=f"restr1_{c}")

for b in B:
    m.addConstr(sum(y_cb[c, b] for c in C) >= sum(d_mb[m, b] for m in M), name=f"restr2_{b}")

for i in I:
    for b in B:
        m.addConstr(sum(r_cib[c, i, b] * x_ib[i, b] for c in C) == sum(v_cib[c, i, b] for c in C), name=f"restr3_{i}_{b}")

for c in C:
    for b in B:
        m.addConstr(sum(v_cib[c, i, b] for i in I) == y_cb[c, b], name=f"restr4_{c}_{b}")

# Resolver el modelo
m.optimize()

# Imprimir solución (esto es opcional)
if m.status == GRB.OPTIMAL:
    for c in C:
        print(f"z_{c}:", z_c[c].x)
    for c in C:
        for b in B:
            print(f"y_{c}_{b}:", y_cb[c, b].x)
    for i in I:
        for b in B:
            print(f"x_{i}_{b}:", x_ib[i, b].x)
    for c in C:
        for i in I:
            for b in B:
                print(f"v_{c}_{i}_{b}:", v_cib[c, i, b].x)
