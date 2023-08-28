import pandas as pd


Informacion = 'info-vinos_2023_v2.xlsx'
indice_hoja_2 = 1
Datos_lotes = pd.read_excel(Informacion,sheet_name=indice_hoja_2)



print(Datos_lotes)