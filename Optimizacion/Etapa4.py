import sys
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from Etapa3 import lotes_finales_ordenados
import math

# Leer datos del archivo CSV
df = pd.read_csv('datos.csv')

print("ETAPA 4 NUEVO------------------------")

L = []  # Lista de los lotes que son cosechados por etapa 3
Dia = {}  # Dias en que se debe cosechar segun etapa 3
Vol = {}  # Volumen de cada lote
Cepa = {}  # Tipo de cepa del lote
Calidad = {}  # Calidad de cada lote en el dia que se cosecha
C1 = 0
C2 = 0
C3 = 0
C4 = 0
C5 = 0
C6 = 0
for i in range(len(lotes_finales_ordenados)):
    if lotes_finales_ordenados[i][19] == 1:
        lote_id = lotes_finales_ordenados[i][0]
        L.append(lote_id)
        Dia[lote_id] = lotes_finales_ordenados[i][20]
        Vol[lote_id] = lotes_finales_ordenados[i][3] * 1000 * 0.5  # Convertir toneladas a litros
        Cepa[lote_id] = lotes_finales_ordenados[i][2]
        lista_calidad = lotes_finales_ordenados[i][18]
        Calidad[lote_id] = lista_calidad[lotes_finales_ordenados[i][20]]
        if lotes_finales_ordenados[i][2] == "C1":
            C1 += Vol[lote_id]
        if lotes_finales_ordenados[i][2] == "C2":
            C2 += Vol[lote_id]
        if lotes_finales_ordenados[i][2] == "C3":
            C3 += Vol[lote_id]
        if lotes_finales_ordenados[i][2] == "C4":
            C4 += Vol[lote_id]
        if lotes_finales_ordenados[i][2] == "C5":
            C5 += Vol[lote_id]
        if lotes_finales_ordenados[i][2] == "C6":
            C6 += Vol[lote_id]
print(lotes_finales_ordenados)
print("GGGGGGGGGGGGG")
print([C1,C2,C3,C4,C5,C6])
print(Vol)
print(Dia)
print("DDDD")
# Definir el rango de días correctamente antes de definir las variables
Dur = 8  # Duración de la fermentación
ultimo_dia = df['Dia optimo cosecha estimado inicialmente'].max() + 20
D = range(df['Dia optimo cosecha estimado inicialmente'].min() - 20, ultimo_dia)
ultimo_dia = df['Dia optimo cosecha estimado inicialmente'].max() + 20
D = range(df['Dia optimo cosecha estimado inicialmente'].min() - 20, ultimo_dia)
G = ["C1", "C2", "C3", "C4", "C5", "C6"]  # Tipos de uva
T = range(216)  # Tanques disponibles

Cap = 25000  # Capacidad de cada tanque
Costo = 1600  # Costo promedio por cada 24 tanques utilizados

# Crear modelo
modelo = gp.Model('Asignacion_Uva')

# Crear variables para los días y lotes relevantes
w = {}
z = {}

for l in L:
    for d in D:
        for t in T:
            if Dia[l] <= d < Dia[l] + Dur:
                w[l, t, d] = modelo.addVar(vtype=GRB.BINARY, name=f'w_{l}{t}{d}')
                z[l, t, d] = modelo.addVar(vtype=GRB.CONTINUOUS, name=f'z_{l}{t}{d}')

# Función objetivo
# Maximiza el volumen total de uva asignada, penalizando el uso innecesario de tanques
modelo.setObjective(
    gp.quicksum(z[l, t, d] - w[l, t, d] * 100 for l in L for t in T for d in D if Dia[l] <= d < Dia[l] + Dur),
    sense=GRB.MAXIMIZE)

# Restricción de ocupación de tanques: asegura que cada lote l esté asignado al menos a un tanque en cada día d de su periodo de fermentación
modelo.addConstrs((gp.quicksum(w[l, t, d] for t in T) >= 1 for l in L for d in D if Dia[l] <= d < Dia[l] + Dur),
                  name='ocupacion_tanques')

# Restricción de uso de tanques: un tanque específico t solo puede estar ocupado por un tipo de uva en un día específico d
modelo.addConstrs((gp.quicksum(w[l, t, d] for l in L if Dia[l] <= d < Dia[l] + Dur) <= 1 for t in T for d in D),
                  name='uso_tanques')

# Restricciones de capacidad de los tanques:
# Capacidad máxima (100%): asegura que la cantidad de uva asignada no exceda la capacidad máxima del tanque
modelo.addConstrs((z[l, t, d] <= Cap * w[l, t, d] for l in L for t in T for d in D if Dia[l] <= d < Dia[l] + Dur),
                  name='capacidad_maxima_tanque')

# Capacidad mínima (30%): asegura que la cantidad de uva asignada sea al menos el 30% de la capacidad del tanque si está en uso
modelo.addConstrs((z[l, t, d] >= Cap * 0.3 * w[l, t, d] for l in L for t in T for d in D if Dia[l] <= d < Dia[l] + Dur),
                  name='capacidad_minima_tanque')

# Restricciones para garantizar que la suma de la uva asignada en todos los tanques y días no exceda el volumen total del lote
modelo.addConstrs(
    (gp.quicksum(z[l, t, d] for t in T for d in D if Dia[l] <= d < Dia[l] + Dur) <= Dur * Vol[l] for l in L),
    name='suma_volumen_total_lote')
modelo.addConstrs((gp.quicksum(z[l, t, d] for t in T) <= Vol[l] for l in L for d in D if Dia[l] <= d < Dia[l] + Dur),
                  name='suma_volumen_diario_lote')

# Restricción de continuidad de tanques
for l in L:
    for t in T:
        for d in range(Dia[l], Dia[l] + Dur - 1):
            if (d + 1) in D and (l, t, d) in w and (l, t, d + 1) in w:  # Asegurarse de que existen ambas combinaciones
                modelo.addConstr(w[l, t, d] == w[l, t, d + 1], f'continuidad_lote_tanque_{l}{t}{d}')

# Parámetros de optimización
mip_Gap = 0.2
modelo.setParam("MIPGap", mip_Gap)
time_limit_seconds = 3600
modelo.setParam("TimeLimit", time_limit_seconds)

# Optimizar el modelo
modelo.optimize()

# Lista para almacenar la información de los lotes
info_lotes = []

# Verificar si se encontró una solución óptima
if modelo.status == GRB.OPTIMAL:
    print("Solución óptima encontrada.")
    print('Asignación de uva y ocupación de tanques:')

    # Diccionario para acumular los litros asignados a cada lote por día
    litros_por_lote = {}

    for l in L:
        for d in D:
            for t in T:
                if Dia[l] <= d < Dia[l] + Dur:
                    if w[l, t, d].x > 0.5:
                        cantidad_asignada = z[l, t, d].x
                        print(f'Lote {l} en el día {d} asignado al tanque {t} con {cantidad_asignada} litros')

                        # Acumular los litros asignados a cada lote
                        if l not in litros_por_lote:
                            litros_por_lote[l] = 0
                        litros_por_lote[l] += cantidad_asignada/8

    # Agregar la información de cada lote a la lista
    for l in litros_por_lote:
        dia_salida = Dia[l] + Dur - 1
        info_lotes.append([l, litros_por_lote[l], dia_salida])

    # Imprimir la información de los lotes
    print("Información de los lotes:")
    for info in info_lotes:
        print(f"Lote: {info[0]}, Litros: {info[1]}, Día de salida: {info[2]}")

    # Cálculo de litros fermentados por cepa
    litros_por_cepa = {
        g: sum(z[l, t, d].x/8 for l in L for t in T for d in D if (Dia[l] <= d < Dia[l] + Dur) if Cepa[l] == g) for g in
        G}


else:
    print("No se encontró una solución óptima.")

# imprimimos el output para etapa 5

print(info_lotes)

# creamos un archivo es output para etapa 4
# Escribir output en un archivo de texto
with open('output_etapa4.txt', 'w') as file:
    file.write("Solución óptima encontrada.\n")
    file.write('Asignación de uva y ocupación de tanques:\n')

    for l in L:
        for d in D:
            for t in T:
                if Dia[l] <= d < Dia[l] + Dur:
                    if w[l, t, d].x > 0.5:
                        cantidad_asignada = z[l, t, d].x
                        file.write(f'Lote {l} en el día {d} asignado al tanque {t} con {cantidad_asignada} litros\n')

    file.write("\nInformación de los lotes:\n")
    for info in info_lotes:
        file.write(f"Lote: {info[0]}, Litros: {info[1]}, Día de salida: {info[2]}\n")

    # Cálculo de litros fermentados por cepa
    litros_por_cepa = {
        g: sum(z[l, t, d].x/8 for l in L for t in T for d in D if (Dia[l] <= d < Dia[l] + Dur) if Cepa[l] == g) for g in
        G}

    file.write("\nLitros fermentados por cepa:\n")
    for g in litros_por_cepa:
        file.write(
            f"{g}: {litros_por_cepa[g]} litros\n")  # Lo dividi mas arriba

    # Imprimir la lista para etapa 5
    file.write("\nOutput para Etapa 5:\n")
    file.write(str(info_lotes))