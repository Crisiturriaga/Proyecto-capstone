import pandas as pd


Informacion = 'info-vinos_2023_v2.xlsx'

#Definiendo los indices de las hojas en excel
hoja_lotes = 1
indice_hoja_3 = 2
nu_por_uva = 3
umbral_industrializacion = 4
receta_vinos = 5
info_mercados = 6
info_tramos_fermentación = 7

#Hacemos la lectura de los datos
Datos_lotes = pd.read_excel(Informacion,sheet_name=hoja_lotes)

Datos_nu = pd.read_excel(Informacion, sheet_name = nu_por_uva)
Datos_umbral = pd.read_excel(Informacion, sheet_name = umbral_industrializacion)
Datos_recetas = pd.read_excel(Informacion, sheet_name = receta_vinos)
Datos_mercados = pd.read_excel(Informacion, sheet_name = info_mercados)
Datos_fermentacion = pd.read_excel(Informacion, sheet_name = info_tramos_fermentación)




print(Datos_lotes)