import pandas as pd
from gurobipy import Model, GRB, quicksum
import gurobipy as gp
from gurobipy import GRB
from Etapa3 import lotes_finales_ordenados
import math



# Leer datos del archivo CSV
df = pd.read_csv('datos.csv')

print("ETAPA 4 NUEVO------------------------")
#El atributo lote[19] es una binaria que entrega un 1 si se cosecha el lote, cero si no se cosecha
#El atributo lote[20] entrega el dia en que se debe cosechar el lote, si no se cosecha, el valor del atributo es (-1)

L = []  # Lista de los lotes que son cosechados por etapa 3
Dia = {}  # dias en que se debe cosechar segun etapa 3
Vol = {}  # Volumen de cada lote, Cantidad de kg de cada lote
Cepa = {} #tipo de cepa del lote
Calidad = {}  # Calidad de cada lote en el dia que se cosecha
# Conjuntos
for i in range(0,len(lotes_finales_ordenados)):  # aqui se definen lo parametros
    if lotes_finales_ordenados[i][19] == 1:
        L.append(lotes_finales_ordenados[i][0])
        Dia[lotes_finales_ordenados[i][0]] = lotes_finales_ordenados[i][20]
        Vol[lotes_finales_ordenados[i][0]] = lotes_finales_ordenados[i][3]*1000*0.5
        Cepa[lotes_finales_ordenados[i][0]]= lotes_finales_ordenados[i][2]
        lista_calidad = lotes_finales_ordenados[i][18]
        Calidad[lotes_finales_ordenados[i][0]] = lista_calidad[lotes_finales_ordenados[i][20]] #calidad del dia de cosecha segun etapa 3


# Parámetros del problema
G = ["C1","C2","C3","C4","C5","C6"]  # Conjunto de tipos de uva
T = range(216)  # 216 tanques disponibles # Conjunto de tanques
D = range(df['Dia optimo cosecha estimado inicialmente'].min(),
          df['Dia optimo cosecha estimado inicialmente'].max() + 1)  # Horizonte de planificación, horizonte de periodo

# Parámetros
Cap = {t: 25000 for t in T}  # Capacidad de cada tanque t
Dur = 8  # Duración promedio de la fermentación
Costo = 1600  # Costo promedio por cada 24 tanques utilizados


# Crear modelo
modelo = gp.Model('Asignacion_Uva')

# Crear variables de decisión
x = modelo.addVars(G, T, D, vtype=GRB.BINARY, name='x')
y = modelo.addVars(T, D, vtype=GRB.BINARY, name='y')

# Función objetivo
modelo.setObjective(gp.quicksum(x[g, t, d] for g in G for t in T for d in D), sense=GRB.MAXIMIZE)

# Restricciones de asignación de uva,  asegura que cada tipo de uva g solo puede ser asignado a un tanque en un día específico d
modelo.addConstrs((x.sum(g, '*', d) <= 1 for g in G for d in D), name='asignacion_uva')

# Restricciones de ocupación de tanques  asegura que un tanque específico t solo puede estar ocupado por un tipo de uva en un día específico d.
modelo.addConstrs((x.sum('*', t, d) <= 1 for t in T for d in D), name='ocupacion_tanques')

# Restricciones de duración de fermentación, maximo 8 dias
modelo.addConstrs((gp.quicksum(x[g, t, d_prime] for d_prime in range(d, min(d + 8, len(D)))) <= 8 * y[t, d] for g in G for t in T for d in D), name='duracion_fermentacion')

# Capcacidad de cada tanque
modelo.addConstrs((gp.quicksum(Vol[l] * x[l, t, d] for l in L) <= Cap[t] * y[t, d] for t in T for d in D), name='capacidad_tanques')

# Restricciones de disponibilidad de uva (debes completar esta parte según tus necesidades)


# Optimizar el modelo
modelo.optimize()

# Imprimir resultado
if modelo.status == GRB.OPTIMAL:
    print('Valor objetivo:', modelo.objVal)
    print('Asignación de uva:')
    for g in G:
        for t in T:
            for d in D:
                if x[g, t, d].x > 0.5:
                    print(f'Tipo de uva {g} asignado al tanque {t} en el día {d}')
    print('Ocupación de tanques:')
    for t in T:
        for d in D:
            if y[t, d].x > 0.5:
                print(f'Tanque {t} ocupado en el día {d}')
else:
    print('El modelo no tiene solución óptima.')
