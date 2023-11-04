from gurobipy import *

# Crear un nuevo modelo
m = Model("optimizacion_vinos")

# Indices para cepas y mercados
cepas = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']
mercados = ['A', 'B', 'C', 'D']

# Litros disponibles por cepa
litros_disponibles = {
    'C1': 9176250,
    'C2': 8086875,
    'C3': 6240000,
    'C4': 6296250,
    'C5': 10897500,
    'C6': 7483125
}

# Composición de Blend 4
blend4_composition = {
    'C1': 0.12,
    'C2': 0.15,
    'C3': 0.08,
    'C4': 0.1,
    'C5': 0.1,
    'C6': 0.45
}

# Demanda mínima en botellas por mercado
demanda_minima = {
    'A': 9520000,
    'B': 12693333,
    'C': 11106667,
    'D': 9520000
}

# Variables de decisión: litros de cada cepa asignados a cada mercado
litros = m.addVars(mercados, cepas, name="litros")

# Variables de holgura para la demanda mínima
holgura_demanda = m.addVars(mercados, name="holgura_demanda")

# Función objetivo: maximizar la cantidad total de botellas menos las penalizaciones por no cumplir la demanda mínima
penalizacion = 1000  # Penalización por cada botella por debajo de la demanda mínima
m.setObjective(
    quicksum(litros[mercado, cepa]*0.75 for mercado in mercados for cepa in cepas) -
    quicksum(penalizacion * holgura_demanda[mercado] for mercado in mercados),
    GRB.MAXIMIZE
)

# Restricciones de disponibilidad de litros por cepa
for cepa in cepas:
    m.addConstr(quicksum(litros[mercado, cepa] for mercado in mercados) <= litros_disponibles[cepa], name=f"disponibilidad_{cepa}")

# Restricciones de demanda mínima con holgura
for mercado in mercados:
    m.addConstr(quicksum(litros[mercado, cepa]*0.75 for cepa in cepas) + holgura_demanda[mercado] >= demanda_minima[mercado], name=f"demanda_minima_{mercado}")

# Optimizar el modelo
m.optimize()

# Imprimir la solución
if m.status == GRB.OPTIMAL:
    for mercado in mercados:
        total_botellas = sum(litros[mercado, cepa].X*0.75 for cepa in cepas)
        print(f"Mercado {mercado} tiene {total_botellas} botellas")
