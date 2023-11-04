from gurobipy import Model, GRB, quicksum
import pandas as pd

# Cargar datos
df = pd.read_csv('datos.csv')

# Crear el modelo
m = Model("fermentacion_simplificada")

# Extraer los lotes y las cepas
Cepas = df['Tipo Uva'].unique().tolist()
J = df['Lote COD'].tolist()
H = df.set_index('Lote COD')['tn/Lote'].to_dict()

# Variables de decisión
# x[j] será la cantidad de litros que se deciden fermentar del lote j
x = m.addVars(J, vtype=GRB.CONTINUOUS, name="x")

# Función objetivo: Maximizar la cantidad de litros fermentados
m.setObjective(quicksum(x[j] for j in J), GRB.MAXIMIZE)

# Restricciones
# Asegurar que no se fermenten más litros de los disponibles por lote
for j in J:
    m.addConstr(x[j] <= H[j] * 1000 * 0.5, "MaxLitrosPorLote")

# Optimizar el modelo
m.optimize()

# Calcular los litros fermentados por cepa
litros_por_cepa = {c: 0 for c in Cepas}
for j in J:
    cepa = df.set_index('Lote COD').loc[j, 'Tipo Uva']
    litros = x[j].X  # Cantidad de litros fermentados del lote j
    litros_por_cepa[cepa] += litros

# Imprimir los resultados
print("Litros fermentados por cepa:")
for cepa, litros in litros_por_cepa.items():
    print(f"Cepa {cepa}: {litros} litros")
