import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# Cargar los datos desde el archivo CSV
data = pd.read_csv("datos.csv")

# Crear diccionarios para cada columna
lote_cod_dict = dict(zip(data["Lote Numero"], data["Lote COD"]))
lote_numero_dict = dict(zip(data["Lote COD"], data["Lote Numero"]))
tipo_uva_dict = dict(zip(data["Lote Numero"], data["Tipo Uva"]))
tn_lote_dict = dict(zip(data["Lote Numero"], data["tn/Lote"]))
dia_optimo_dict = dict(zip(data["Lote Numero"], data["Dia optimo cosecha estimado inicialmente"]))
prob_lluvia_seca_dict = dict(zip(data["Lote Numero"], data["Prob de lluvia (seca a lluvia)"]))
prob_lluvia_lluvia_dict = dict(zip(data["Lote Numero"], data["Prob de lluvia (lluvia a lluvia)"]))
usd_compra_futuro_dict = dict(zip(data["Lote Numero"], data["usd Compra Futuro/ kg uva"]))

# Ejemplo de cómo acceder a la información utilizando los diccionarios
#lote_cod = lote_cod_dict[1]
#tipo_uva = tipo_uva_dict[1]
#tn_lote = tn_lote_dict[1]
# etc. De esta forma hace que se lean todos los lotes del 1 al 290 para cada columna del excel

# Crear el modelo
model = gp.Model("Planificacion_Vinicola")

# Definir las variables

# ...

# Definir la función objetivo

# ...

# Restricciones y otras partes del modelo

# ...

# Resolver el modelo
model.optimize()

# Mostrar resultados
if model.status == GRB.OPTIMAL:
    for v in model.getVars():
        if v.x > 0:
            print(f"{v.varName}: {v.x}")
    print(f"Utilidad total: {model.objVal}")
else:
    print("El modelo no encontró una solución óptima.")
