from gurobipy import Model, GRB, quicksum

# Creación del modelo
m = Model("OptimizacionUvas")
print("ETAPA 1 ------------------")
# Índices
M = ['A', 'B', 'C', 'D']
Productos = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'Blend 1.1', 'Blend 1.2', 'Blend 2.1', 'Blend 2.2', 'Blend 2.3', 'Blend 3.1', 'Blend 4.1', 'Blend 4.2']
Blends = ['Blend 1.1', 'Blend 1.2', 'Blend 2.1', 'Blend 2.2', 'Blend 2.3', 'Blend 3.1', 'Blend 4.1', 'Blend 4.2']

# Parámetros

d_m = {
    'A': 9520000*(3/4)*2,
    'B': 12693333*(3/4)*2,
    'C': 11106667*(3/4)*2,
    'D': 9520000*(3/4)*2
} # se multiplico la demanda de cada mercado por 3/4 para pasarlo de botellas a litros y luego por 2 para obtener los kilos que se necesitan

Datos_finales = []
prop = {
    ('C1', 'Blend 1.1'): 0.1,
    ('C2', 'Blend 1.1'): 0.2,
    ('C3', 'Blend 1.1'): 0,
    ('C4', 'Blend 1.1'): 0.3,
    ('C5', 'Blend 1.1'): 0,
    ('C6', 'Blend 1.1'): 0.4,
    ('C1', 'Blend 1.2'): 0,
    ('C2', 'Blend 1.2'): 0.4,
    ('C3', 'Blend 1.2'): 0.2,
    ('C4', 'Blend 1.2'): 0.2,
    ('C5', 'Blend 1.2'): 0,
    ('C6', 'Blend 1.2'): 0.2,
    ('C1', 'Blend 2.1'): 0.3,
    ('C2', 'Blend 2.1'): 0.2,
    ('C3', 'Blend 2.1'): 0.1,
    ('C4', 'Blend 2.1'): 0.2,
    ('C5', 'Blend 2.1'): 0,
    ('C6', 'Blend 2.1'): 0.2,
    ('C1', 'Blend 2.2'): 0,
    ('C2', 'Blend 2.2'): 0.2,
    ('C3', 'Blend 2.2'): 0.2,
    ('C4', 'Blend 2.2'): 0.2,
    ('C5', 'Blend 2.2'): 0.2,
    ('C6', 'Blend 2.2'): 0,
    ('C1', 'Blend 2.3'): 0.2,
    ('C2', 'Blend 2.3'): 0,
    ('C3', 'Blend 2.3'): 0.2,
    ('C4', 'Blend 2.3'): 0.2,
    ('C5', 'Blend 2.3'): 0,
    ('C6', 'Blend 2.3'): 0.4,
    ('C1', 'Blend 3.1'): 0.5,
    ('C2', 'Blend 3.1'): 0,
    ('C3', 'Blend 3.1'): 0.2,
    ('C4', 'Blend 3.1'): 0,
    ('C5', 'Blend 3.1'): 0.1,
    ('C6', 'Blend 3.1'): 0.2,
    ('C1', 'Blend 4.1'): 0.15,
    ('C2', 'Blend 4.1'): 0.15,
    ('C3', 'Blend 4.1'): 0.15,
    ('C4', 'Blend 4.1'): 0.15,
    ('C5', 'Blend 4.1'): 0.1,
    ('C6', 'Blend 4.1'): 0.3,
    ('C1', 'Blend 4.2'): 0.12,
    ('C2', 'Blend 4.2'): 0.15,
    ('C3', 'Blend 4.2'): 0.08,
    ('C4', 'Blend 4.2'): 0.1,
    ('C5', 'Blend 4.2'): 0.1,
    ('C6', 'Blend 4.2'): 0.45,
    ('C1', 'C1'): 1,
    ('C2', 'C1'): 0,
    ('C3', 'C1'): 0,
    ('C4', 'C1'): 0,
    ('C5', 'C1'): 0,
    ('C6', 'C1'): 0,
    ('C1', 'C2'): 0,
    ('C2', 'C2'): 1,
    ('C3', 'C2'): 0,
    ('C4', 'C2'): 0,
    ('C5', 'C2'): 0,
    ('C6', 'C2'): 0,
    ('C1', 'C3'): 0,
    ('C2', 'C3'): 0,
    ('C3', 'C3'): 1,
    ('C4', 'C3'): 0,
    ('C5', 'C3'): 0,
    ('C6', 'C3'): 0,
    ('C1', 'C4'): 0,
    ('C2', 'C4'): 0,
    ('C3', 'C4'): 0,
    ('C4', 'C4'): 1,
    ('C5', 'C4'): 0,
    ('C6', 'C4'): 0,
    ('C1', 'C5'): 0,
    ('C2', 'C5'): 0,
    ('C3', 'C5'): 0,
    ('C4', 'C5'): 0,
    ('C5', 'C5'): 1,
    ('C6', 'C5'): 0,
    ('C1', 'C6'): 0,
    ('C2', 'C6'): 0,
    ('C3', 'C6'): 0,
    ('C4', 'C6'): 0,
    ('C5', 'C6'): 0,
    ('C6', 'C6'): 1,
}
m_b = {
    'C1': 'B',
    'C2': 'C',
    'C3': 'B',
    'C4': 'D',
    'C5': 'A',
    'C6': 'D',
    'Blend 1.1': 'D',
    'Blend 1.2': 'D',
    'Blend 2.1': 'B',
    'Blend 2.2': 'B',
    'Blend 2.3': 'B',
    'Blend 3.1': 'B',
    'Blend 4.1': 'C',
    'Blend 4.2': 'C'
}
max_cepa = {
    'C1': 18352500,
    'C2': 16173750,
    'C3':  12480000,
    'C4': 12592500,
    'C5': 21795000,
    'C6': 14966250
}



# Creación del modelo
m = Model("OptimizacionUvas")
print("ETAPA 1 ------------------")
# Índices
M = ['A', 'B', 'C', 'D']
Productos = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'Blend 1.1', 'Blend 1.2', 'Blend 2.1', 'Blend 2.2', 'Blend 2.3', 'Blend 3.1', 'Blend 4.1', 'Blend 4.2']
Blends = ['Blend 1.1', 'Blend 1.2', 'Blend 2.1', 'Blend 2.2', 'Blend 2.3', 'Blend 3.1', 'Blend 4.1', 'Blend 4.2']

# Parámetros

d_m = {
    'A': 9520000*(3/4)*2,
    'B': 12693333*(3/4)*2,
    'C': 11106667*(3/4)*2,
    'D': 9520000*(3/4)*2
} # se multiplico la demanda de cada mercado por 3/4 para pasarlo de botellas a litros y luego por 2 para obtener los kilos que se necesitan

Datos_finales = []
prop = {
    ('C1', 'Blend 1.1'): 0.1,
    ('C2', 'Blend 1.1'): 0.2,
    ('C3', 'Blend 1.1'): 0,
    ('C4', 'Blend 1.1'): 0.3,
    ('C5', 'Blend 1.1'): 0,
    ('C6', 'Blend 1.1'): 0.4,
    ('C1', 'Blend 1.2'): 0,
    ('C2', 'Blend 1.2'): 0.4,
    ('C3', 'Blend 1.2'): 0.2,
    ('C4', 'Blend 1.2'): 0.2,
    ('C5', 'Blend 1.2'): 0,
    ('C6', 'Blend 1.2'): 0.2,
    ('C1', 'Blend 2.1'): 0.3,
    ('C2', 'Blend 2.1'): 0.2,
    ('C3', 'Blend 2.1'): 0.1,
    ('C4', 'Blend 2.1'): 0.2,
    ('C5', 'Blend 2.1'): 0,
    ('C6', 'Blend 2.1'): 0.2,
    ('C1', 'Blend 2.2'): 0,
    ('C2', 'Blend 2.2'): 0.2,
    ('C3', 'Blend 2.2'): 0.2,
    ('C4', 'Blend 2.2'): 0.2,
    ('C5', 'Blend 2.2'): 0.2,
    ('C6', 'Blend 2.2'): 0.2,
    ('C1', 'Blend 2.3'): 0.2,
    ('C2', 'Blend 2.3'): 0,
    ('C3', 'Blend 2.3'): 0.2,
    ('C4', 'Blend 2.3'): 0.2,
    ('C5', 'Blend 2.3'): 0,
    ('C6', 'Blend 2.3'): 0.4,
    ('C1', 'Blend 3.1'): 0.5,
    ('C2', 'Blend 3.1'): 0,
    ('C3', 'Blend 3.1'): 0.2,
    ('C4', 'Blend 3.1'): 0,
    ('C5', 'Blend 3.1'): 0.1,
    ('C6', 'Blend 3.1'): 0.2,
    ('C1', 'Blend 4.1'): 0.15,
    ('C2', 'Blend 4.1'): 0.15,
    ('C3', 'Blend 4.1'): 0.15,
    ('C4', 'Blend 4.1'): 0.15,
    ('C5', 'Blend 4.1'): 0.1,
    ('C6', 'Blend 4.1'): 0.3,
    ('C1', 'Blend 4.2'): 0.12,
    ('C2', 'Blend 4.2'): 0.15,
    ('C3', 'Blend 4.2'): 0.08,
    ('C4', 'Blend 4.2'): 0.1,
    ('C5', 'Blend 4.2'): 0.1,
    ('C6', 'Blend 4.2'): 0.45,
    ('C1', 'C1'): 1,
    ('C2', 'C1'): 0,
    ('C3', 'C1'): 0,
    ('C4', 'C1'): 0,
    ('C5', 'C1'): 0,
    ('C6', 'C1'): 0,
    ('C1', 'C2'): 0,
    ('C2', 'C2'): 1,
    ('C3', 'C2'): 0,
    ('C4', 'C2'): 0,
    ('C5', 'C2'): 0,
    ('C6', 'C2'): 0,
    ('C1', 'C3'): 0,
    ('C2', 'C3'): 0,
    ('C3', 'C3'): 1,
    ('C4', 'C3'): 0,
    ('C5', 'C3'): 0,
    ('C6', 'C3'): 0,
    ('C1', 'C4'): 0,
    ('C2', 'C4'): 0,
    ('C3', 'C4'): 0,
    ('C4', 'C4'): 1,
    ('C5', 'C4'): 0,
    ('C6', 'C4'): 0,
    ('C1', 'C5'): 0,
    ('C2', 'C5'): 0,
    ('C3', 'C5'): 0,
    ('C4', 'C5'): 0,
    ('C5', 'C5'): 1,
    ('C6', 'C5'): 0,
    ('C1', 'C6'): 0,
    ('C2', 'C6'): 0,
    ('C3', 'C6'): 0,
    ('C4', 'C6'): 0,
    ('C5', 'C6'): 0,
    ('C6', 'C6'): 1,
}
m_b = {
    'C1': 'B',
    'C2': 'C',
    'C3': 'B',
    'C4': 'D',
    'C5': 'A',
    'C6': 'D',
    'Blend 1.1': 'D',
    'Blend 1.2': 'D',
    'Blend 2.1': 'B',
    'Blend 2.2': 'B',
    'Blend 2.3': 'B',
    'Blend 3.1': 'B',
    'Blend 4.1': 'C',
    'Blend 4.2': 'C'
}
max_cepa = {
    'C1': 18352500,
    'C2': 16173750,
    'C3':  12480000,
    'C4': 12592500,
    'C5': 21795000,
    'C6': 14966250
}

utilidad = {
    'C1':(3.225 - 2.375),
    'C2':(2.45 - 1.825),
    'C3':(3.225 - 2.375) ,
    'C4':(1.675 - 1.545) ,
    'C5':(4.5 - 2.875),
    'C6':(1.675 - 1.545) ,
    'Blend 1.1':(1.675 - 1.545) ,
    'Blend 1.2':(1.675 - 1.545) ,
    'Blend 2.1':(3.225 - 2.375) ,
    'Blend 2.2':(3.225 - 2.375) ,
    'Blend 2.3':(3.225 - 2.375),
    'Blend 3.1':(3.225 - 2.375),
    'Blend 4.1':(2.45 - 1.825) ,
    'Blend 4.2':(2.45 - 1.825)
}

# Variables de decisión
x = {}
for p in Productos:
    x[p] = m.addVar(vtype=GRB.INTEGER, name=f"x_{p}")

# Restricciones de demanda, por 0.75 para que entregue la cantidad de litros que se tienen que producir
for mkt in M:
    m.addConstr(sum(x[p] * prop[cep, p] for cep, p in prop if p in Productos and m_b[p] == mkt) >= d_m[mkt])


# Restricción para el vino1
# Crear restricciones para cada vino
for vino, limite in max_cepa.items():
    blend_terms = [prop[(vino, blend)] * x[blend] for blend in Blends]
    m.addConstr(x[vino] + quicksum(blend_terms) <= limite*0.89, name=f"{vino}_Limit")




# Función objetivo: Minimizar la cantidad de cepas utilizadas
m.setObjective(sum(x[p] * utilidad[p] for p in Productos), GRB.MAXIMIZE)

# Optimizar el modelo
m.optimize()
lista = []
# Imprimir resultados
if m.status == GRB.OPTIMAL:
    for p in Productos:
        Datos_finales.append(x[p].x)
        print(f"Cantidad de {p}: {x[p].x}")
        lista.append(x[p].x)
print(Datos_finales)
print("UUU")
C1 = Datos_finales[0] + Datos_finales[6]*0.1 + Datos_finales[8]*0.3 + Datos_finales[10]*0.2 + Datos_finales[11]*0.5 + Datos_finales[12]*0.15 + Datos_finales[13]*0.12
C2 = Datos_finales[1] + Datos_finales[6]*0.2 + Datos_finales[7]*0.4 + Datos_finales[8]*0.2 + Datos_finales[9]*0.2 + Datos_finales[12]*0.15 + Datos_finales[13]*0.15
C3 = Datos_finales[2] + Datos_finales[7]*0.2 + Datos_finales[8]*0.1 + Datos_finales[9]*0.2 + Datos_finales[10]*0.2 + Datos_finales[11]*0.2 + Datos_finales[12]*0.15 + Datos_finales[13]*0.08
C4 = Datos_finales[3] + Datos_finales[6]*0.3 + Datos_finales[7]*0.2 + Datos_finales[8]*0.2 + Datos_finales[9]*0.2 + Datos_finales[10]*0.2 + Datos_finales[12]*0.15 + Datos_finales[13]*0.1
C5 = Datos_finales[4] + Datos_finales[9]*0.2 + Datos_finales[11]*0.1 + Datos_finales[12]*0.1 + Datos_finales[13]*0.1
C6 = Datos_finales[5] + Datos_finales[6]*0.4 + Datos_finales[7]*0.2 + Datos_finales[8]*0.2 + Datos_finales[9]*0.2 + Datos_finales[10]*0.4 + Datos_finales[11]*0.2 + Datos_finales[12]*0.3 + Datos_finales[13]*0.45

print("AAA")
print(C1,C2,C3,C4,C5,C6)
C1 = C1 * 1.11
C2 = C2 * 1.11
C3 = C3 * 1.11
C4 = C4 * 1.11
C5 = C5 * 1.11
C6 = C6 * 1.11
Requerimientos = [C1,C2,C3,C4,C5,C6]
print(Requerimientos)