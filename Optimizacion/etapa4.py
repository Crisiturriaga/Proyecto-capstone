from gurobipy import Model, GRB, quicksum
import random
import pandas as pd
import numpy as np

# Read the CSV file
df = pd.read_csv('datos.csv')

# Convert tons to liters (assuming 1 ton = 1000 kg and 1 kg of grapes produces 0.5 liters of wine)
df['Litros_Uva'] = df['tn/Lote'] * 1000 * 0.5
df['Lote COD'] = df['Lote COD'].astype(str)
nombre_lote = df['Lote COD'].tolist()

# Create a list with the total liters of grape juice per batch
litros_totales_uva = df['Litros_Uva'].tolist()

# Print the list to verify



# Creación del modelo
m = Model("OptimizacionFermentacion")

# Índices
# Índices
P = ['Planta1', 'Planta2', 'Planta3']  # Plantas disponibles
Tramos = ['Tramo1', 'Tramo2', 'Tramo3']  # Tramos disponibles en cada planta
E = [(p, tramo, f'Tanque{tanque}') for p in P for tramo in Tramos for tanque in range(1, 25)]  # Tanques disponibles en cada tramo de cada planta
T = list(range(1, 161))  # Días a optimizar, del día 1 al día 160
J = [f'Lote{i}' for i in range(1, 291)]  # Lotes aptos para la industrialización, del Lote1 al Lote290

# Cada planta puede contratar 2 tramos adicionales
Tramos_adicionales = ['TramoAd1', 'TramoAd2']

# Cada tramo tiene 24 tanques
Tanques_por_tramo = 24
E_ad = [(planta, tramo, f'Tanque{tanque}') for planta in P for tramo in Tramos_adicionales for tanque in range(1, Tanques_por_tramo + 1)]
C = ['C1', 'C2', 'C3', 'C4', 'C5', 'C6']  # Ejemplo de cepas

# Parámetros (estos son ejemplos y deben ser reemplazados por tus datos reales)
u_jt = litros_totales_uva  # Cantidad de uva de lote j a recepcionar en día t
# Suponiendo que J es una lista de nombres de lotes y C es una lista de cepas
J = nombre_lote  # Ejemplo de nombres de lotes

# Crear el diccionario h_jc
h_jc = {(j, c): 1 if c in j else 0 for j in J for c in C}
capacidad_maxima = 25000  # Capacidad máxima en litros
capacidad_minima = capacidad_maxima * 0.3  # 30% de la capacidad máxima
C_ep = {(p, tramo, e): capacidad_maxima for p in P for tramo in Tramos for e in E}
Cmin_ep = {(p, tramo, e): capacidad_minima for p in P for tramo in Tramos for e in E}

random.seed(0)  # Establece la semilla del generador de números aleatorios
T_e = {e: random.uniform(7, 9) for e in E}

random.seed(0)  # Establece la semilla del generador de números aleatorios
q_jt = {(j, t): random.uniform(0.8, 1) for j in J for t in T}

# Costos por tramo y planta en USD/m3/temporada
costos_tramo = {
    'Planta1': [1600, 1840, 1840],
    'Planta2': [1500, 1725, 1725],
    'Planta3': [1800, 2070, 2070]
}

# Capacidad de cada tanque en m3
capacidad_tanque_m3 = 25  # 25,000 litros son 25 m3

# Calculamos el costo por tanque para cada tramo y planta
C1_por_planta_tramo = {
    planta: [costo * capacidad_tanque_m3 for costo in costos]
    for planta, costos in costos_tramo.items()
}

# Ejemplo de cómo acceder al costo por tanque para el Tramo 1 de la Planta 1
costo_tanque_planta1_tramo1 = C1_por_planta_tramo['Planta1'][0]

# Si necesitas un costo general por tanque adicional, podrías tomar un promedio
C1 = (
    costo_tanque_planta1_tramo1 + C1_por_planta_tramo['Planta2'][0] + C1_por_planta_tramo['Planta3'][0]
) / 3


# Umbrales de calidad por tipo de uva
umbrales_calidad = {
    'C1': 0.8,
    'C2': 0.75,
    'C3': 0.8,
    'C4': 0.7,
    'C5': 0.8,
    'C6': 0.7
}

# Si necesitas un umbral general para la rectificación, podrías tomar el mínimo
B = min(umbrales_calidad.values())


# Leer el archivo CSV
df = pd.read_csv('datos.csv')

# Convertir toneladas a kilogramos y calcular el costo de almacenamiento y rectificación
df['Precio por kg'] = df['usd Compra Futuro/ kg uva']  # Asumiendo que esta columna ya está en precio por kg
df['Costo Almacenamiento Transporte'] = 0.02 * (df['Precio por kg']*(df['tn/Lote']*1000))  # 2% del precio por kg para el costo de transporte
df['Costo Rectificación'] = df['Costo Almacenamiento Transporte'] # 2% del precio por kg para el costo de rectificación

# Calcular el precio promedio por cepa
precios_por_cepa = df.groupby('Tipo Uva')['Precio por kg'].mean().to_dict()

# Asignar los costos a las variables C_trans y C_rect
C_trans = {cepa: 0.02 * precio for cepa, precio in precios_por_cepa.items()}
C_rect = {cepa: 0.02 * precio for cepa, precio in precios_por_cepa.items()}


# Conversión de toneladas a kilogramos para obtener la cantidad de uva en kg por lote
df['kg por lote'] = df['tn/Lote'] * 1000

# Genera un valor aleatorio de la distribución uniforme entre 7 y 9 días para cada lote
df['dias_fermentacion'] = np.random.uniform(7, 9, size=len(df))

# Suma el valor de la distribución uniforme al día estimado de cosecha
df['Dia listo para recepcion'] = df['Dia optimo cosecha estimado inicialmente'] + df['dias_fermentacion']

# Crea el diccionario para D_j
D_j = df.set_index('Lote Numero')['Dia listo para recepcion'].to_dict()

# Cantidad de uva en kg por lote j
H_j = df.set_index('Lote Numero')['kg por lote'].to_dict()

# Capacidad de almacenamiento en cada planta (litros de vino)
U_p = {p: 24 * 25000 for p in P}

# Pérdida de calidad de la uva por día de espera en camión en el día t
R_t = {t: 0.05 for t in T}

C_eadp = {(p, e_ad): capacidad_maxima for p in P for e_ad in E_ad}
Cmin_eadp = {(p, e_ad): capacidad_minima for p in P for e_ad in E_ad}
# Variables de Decisión
t_jt = m.addVars(J, T, vtype=GRB.BINARY, name="t")
s_jt = m.addVars(J, T, vtype=GRB.BINARY, name="s")
r_et = m.addVars(E, T, vtype=GRB.BINARY, name="r")
e_pt = m.addVars(P, T, vtype=GRB.BINARY, name="e")
y_et = m.addVars(E, T, vtype=GRB.BINARY, name="y")
y_et = m.addVars(E, T, vtype=GRB.BINARY, name="y")
v_jpet = m.addVars(J, P, E, T, vtype=GRB.CONTINUOUS, name="v")
b_pet = m.addVars(P, E, T, vtype=GRB.BINARY, name="b")
x_jpet = m.addVars(J, P, E, T, vtype=GRB.CONTINUOUS, name="x")
ql_pet = m.addVars(P, E, T, vtype=GRB.CONTINUOUS, name="ql")
Q_jt = m.addVars(J, T, vtype=GRB.CONTINUOUS, name="Q")
z_jpetc = m.addVars(J, P, E, T, C, vtype=GRB.BINARY, name="z")
w_jpet = m.addVars(J, P, E, T, vtype=GRB.BINARY, name="w")
f_ept = m.addVars(E, P, T, vtype=GRB.CONTINUOUS, name="f")
v_ept = m.addVars(E, P, T, vtype=GRB.BINARY, name="v")

# Función Objetivo
m.setObjective(
    quicksum(C_rect * r_et[e, t] for e in E for t in T) +
    quicksum(C1 * e_pt[p, t] for p in P for t in T) +
    quicksum(C_trans * t_jt[j, t] * H_j[j] for j in J for t in T) +
    quicksum(C_jt[j, t] * (1 - t_jt[j, t]) for j in J for t in T),
    GRB.MINIMIZE
)

# Restricciones
for j in J:
    for t in T:
        m.addConstr(Q_jt[j, t] == q_jt[j, t] - (d_jt[j, t] - D_j[j]) * R_t[t], name=f"restr1_{j}_{t}")

for j in J:
    for t in T:
        m.addConstr(t_jt[j, t] + s_jt[j, t] <= 1, name=f"restr2_{j}_{t}")

for p in P:
    for j in J:
        for t in T:
            m.addConstr(sum(x_jpet[j, p, e, t] for e in E) * s_jt[j, t] == u_jt[j, t], name=f"restr3_{p}_{j}_{t}")

for j in J:
    for t in T:
        m.addConstr(0.5 * sum(x_jpet[j, p, e, t] for p in P for e in E) == sum(v_jpet[j, p, e, t] for p in P for e in E), name=f"restr4_{j}_{t}")

for c in C:
    for p in P:
        for e in E:
            for t in T:
                m.addConstr(z_jpetc[j, p, e, t, c] == 1, name=f"restr5_{c}_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(sum(v_jpet[j, p, e, t] for j in J) <= C_ep[e, p] * y_et[e, t], name=f"restr6_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(sum(v_jpet[j, p, e, t] for j in J) >= Cmin_ep[e, p] * y_et[e, t], name=f"restr7_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(y_et[e, t] <= sum(v_jpet[j, p, e, t] for j in J), name=f"restr8_{p}_{e}_{t}")

for p in P:
    for j in J:
        for t in T:
            m.addConstr(sum(v_jpet[j, p, e, t] for e in E) <= U_p[p], name=f"restr9_{p}_{j}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(ql_pet[p, e, t] == sum(x_jpet[j, p, e, t] * Q_jt[j, t] for j in J) / sum(x_jpet[j, p, e, t] for j in J), name=f"restr10_{p}_{e}_{t}")

for p in P:
    for e in E:
        for t in T:
            m.addConstr(ql_pet[p, e, t] <= B + (1 - r_et[e, t]), name=f"restr11_{p}_{e}_{t}")

for p in P:
    for t in T:
        m.addConstr(sum(C_ep[e, p] * y_et[e, t] for e in E) + sum(C_eadp[e_ad, p] * e_pt[p, t] for e_ad in E_ad) >= sum(v_jpet[j, p, e, t] for j in J for e in E), name=f"restr12_{p}_{t}")


# Resolver el modelo
m.optimize()

# Resolver el modelo
m.optimize()

# Imprimir el estado del modelo
status = m.status
if status == GRB.OPTIMAL:
    print("Solución óptima encontrada.")
    # Imprimir las variables de decisión
    for v in m.getVars():
        print(f"{v.varName}: {v.x}")
elif status == GRB.INFEASIBLE:
    print("El modelo es inviable. No se puede encontrar una solución óptima.")
elif status == GRB.UNBOUNDED:
    print("El modelo es ilimitado. Las soluciones pueden mejorar indefinidamente.")
elif status == GRB.INF_OR_UNBD:
    print("El modelo es inviable o ilimitado.")
elif status == GRB.CUTOFF:
    print("No se encontraron soluciones que cumplan con el límite de corte establecido.")
elif status == GRB.ITERATION_LIMIT:
    print("Se alcanzó el límite de iteraciones antes de encontrar una solución óptima.")
elif status == GRB.NODE_LIMIT:
    print("Se alcanzó el límite de nodos antes de encontrar una solución óptima.")
elif status == GRB.TIME_LIMIT:
    print("Se alcanzó el límite de tiempo antes de encontrar una solución óptima.")
elif status == GRB.SOLUTION_LIMIT:
    print("Se alcanzó el límite de soluciones antes de encontrar una solución óptima.")
elif status == GRB.INTERRUPTED:
    print("La optimización fue interrumpida por el usuario.")
elif status == GRB.NUMERIC:
    print("Problemas numéricos encontrados durante la optimización.")
elif status == GRB.SUBOPTIMAL:
    print("Solución subóptima encontrada.")
else:
    print(f"Estado de optimización desconocido: {status}")
