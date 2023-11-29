import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from Etapa4 import info_lotes, litros_por_cepa, lista, lotes_fin, contador_tanques
# Datos de entrada
print("EEEEE")
print(info_lotes)
print(litros_por_cepa)
#info_lotes = [['L_1_C4', 100000.0, 132], ['L_2_C4', 258750.0, 139], ['L_3_C6', 225000.0, 88], ['L_4_C4', 75000.0, 128], ['L_6_C3', 75000.0, 109], ['L_7_C5', 275000.0, 118], ['L_8_C6', 221250.0, 79], ['L_9_C1', 150000.0, 139], ['L_11_C1', 275000.0, 109], ['L_12_C1', 206250.0, 137], ['L_14_C2', 249375.0, 124], ['L_15_C1', 50000.0, 140], ['L_17_C5', 268125.0, 124], ['L_18_C2', 123750.0, 106], ['L_19_C2', 225000.0, 91], ['L_20_C4', 100000.0, 91], ['L_21_C5', 213750.0, 84], ['L_22_C1', 210000.0, 73], ['L_23_C3', 125000.0, 98], ['L_25_C3', 75000.0, 129], ['L_28_C3', 191250.0, 96], ['L_30_C4', 50624.99999999999, 78], ['L_31_C1', 150000.0, 132], ['L_33_C6', 150000.0, 107], ['L_34_C2', 67500.0, 89], ['L_35_C5', 170625.0, 122], ['L_40_C1', 73125.0, 92], ['L_42_C4', 176250.0, 145], ['L_43_C1', 50000.0, 135], ['L_44_C2', 183750.0, 88], ['L_45_C4', 249375.0, 106], ['L_46_C4', 223125.0, 129], ['L_47_C2', 100000.0, 96], ['L_48_C1', 225000.0, 104], ['L_49_C5', 200000.0, 107], ['L_50_C5', 270000.0, 127], ['L_51_C1', 200000.0, 112], ['L_52_C2', 225000.0, 87], ['L_53_C6', 123750.0, 100], ['L_54_C2', 150000.0, 88], ['L_55_C2', 275000.0, 93], ['L_56_C2', 241875.0, 126], ['L_57_C5', 116250.0, 89], ['L_58_C4', 75000.0, 97], ['L_60_C4', 250000.0, 87], ['L_61_C1', 166875.0, 113], ['L_63_C3', 75000.0, 105], ['L_64_C2', 191250.0, 97], ['L_65_C3', 170625.0, 105], ['L_66_C3', 50000.0, 141], ['L_67_C3', 249375.0, 108], ['L_70_C5', 75000.0, 124], ['L_71_C5', 243750.0, 92], ['L_72_C1', 108750.0, 112], ['L_73_C2', 146250.0, 95], ['L_74_C2', 71250.0, 79], ['L_75_C2', 150000.0, 104], ['L_76_C2', 138750.0, 91], ['L_77_C2', 211875.0, 101], ['L_78_C5', 219375.0, 106], ['L_79_C5', 193125.0, 101], ['L_80_C5', 150000.0, 104], ['L_81_C5', 175000.0, 129], ['L_82_C2', 175000.0, 101], ['L_84_C1', 138750.0, 148], ['L_85_C4', 97500.0, 140], ['L_87_C3', 262500.0, 80], ['L_91_C3', 228750.0, 78], ['L_92_C5', 200000.0, 131], ['L_93_C1', 200000.0, 97], ['L_95_C5', 100000.0, 95], ['L_96_C5', 148125.0, 108], ['L_98_C4', 200000.0, 116], ['L_99_C2', 63750.0, 92], ['L_101_C2', 95625.0, 128], ['L_102_C5', 266250.0, 117], ['L_103_C2', 250000.0, 130], ['L_104_C4', 243750.0, 69], ['L_105_C2', 65625.0, 118], ['L_107_C1', 175000.0, 103], ['L_108_C4', 100000.0, 96], ['L_109_C4', 75000.0, 104], ['L_110_C3', 275000.0, 128], ['L_111_C3', 250000.0, 129], ['L_113_C1', 275000.0, 131], ['L_114_C3', 243750.0, 85], ['L_115_C3', 215625.0, 70], ['L_116_C3', 80625.0, 134], ['L_117_C1', 175000.0, 120], ['L_120_C3', 100000.0, 70], ['L_125_C4', 69375.0, 80], ['L_126_C5', 75000.0, 84], ['L_127_C5', 93750.0, 125], ['L_132_C2', 200000.0, 125], ['L_133_C2', 99375.0, 129], ['L_134_C4', 95625.0, 99], ['L_135_C4', 187500.0, 115], ['L_136_C3', 250000.0, 78], ['L_139_C6', 208125.0, 136], ['L_140_C3', 63750.0, 104], ['L_141_C5', 208125.0, 88], ['L_142_C5', 225000.0, 105], ['L_143_C2', 50000.0, 112], ['L_144_C4', 100000.0, 131], ['L_145_C2', 91875.0, 113], ['L_146_C5', 275000.0, 100], ['L_149_C5', 195000.0, 122], ['L_150_C6', 250000.0, 91], ['L_153_C5', 125000.0, 122], ['L_154_C3', 183750.0, 88], ['L_155_C4', 166875.0, 121], ['L_156_C4', 65625.0, 92], ['L_157_C2', 225000.0, 126], ['L_158_C4', 175000.0, 119], ['L_160_C1', 125000.0, 116], ['L_162_C5', 181875.0, 143], ['L_164_C5', 253125.0, 120], ['L_165_C4', 69375.0, 93], ['L_166_C4', 71250.0, 115], ['L_167_C4', 219375.0, 118], ['L_168_C2', 250000.0, 137], ['L_169_C2', 138750.0, 139], ['L_170_C5', 148125.0, 115], ['L_171_C3', 65625.0, 105], ['L_172_C1', 250000.0, 110], ['L_174_C2', 93750.0, 138], ['L_177_C3', 61875.0, 85], ['L_178_C6', 181875.0, 80], ['L_180_C2', 247500.0, 86], ['L_181_C4', 50000.0, 114], ['L_182_C2', 200000.0, 105], ['L_184_C1', 100000.0, 115], ['L_187_C2', 150000.0, 77], ['L_188_C2', 121875.0, 99], ['L_189_C4', 86250.0, 95], ['L_190_C5', 273750.0, 140], ['L_194_C4', 250000.0, 80], ['L_195_C5', 213750.0, 135], ['L_196_C2', 200000.0, 116], ['L_198_C3', 175000.0, 114], ['L_199_C5', 150000.0, 130], ['L_200_C5', 268125.0, 131], ['L_201_C1', 75000.0, 96], ['L_202_C3', 150000.0, 124], ['L_203_C3', 150000.0, 108], ['L_204_C2', 69375.0, 82], ['L_205_C2', 225000.0, 101], ['L_206_C3', 200000.0, 106], ['L_208_C2', 118125.0, 95], ['L_209_C5', 189375.0, 99], ['L_210_C4', 247500.0, 113], ['L_211_C5', 271875.0, 132], ['L_212_C5', 175000.0, 122], ['L_213_C4', 225000.0, 116], ['L_214_C1', 249375.0, 110], ['L_216_C2', 88125.0, 110], ['L_217_C3', 264375.0, 119], ['L_218_C4', 50000.0, 104], ['L_219_C4', 200000.0, 95], ['L_220_C4', 114375.0, 140], ['L_221_C6', 243750.0, 103], ['L_222_C6', 228750.0, 138], ['L_223_C2', 250000.0, 123], ['L_224_C2', 247500.0, 102], ['L_225_C4', 50000.0, 129], ['L_226_C2', 217500.0, 110], ['L_227_C3', 50000.0, 95], ['L_228_C2', 275000.0, 115], ['L_229_C2', 116250.0, 83], ['L_230_C5', 75000.0, 117], ['L_231_C3', 150000.0, 87], ['L_232_C5', 223125.0, 130], ['L_235_C2', 75000.0, 121], ['L_236_C4', 175000.0, 102], ['L_237_C3', 50000.0, 133], ['L_238_C5', 99375.0, 84], ['L_239_C5', 133125.0, 133], ['L_240_C3', 54375.0, 138], ['L_241_C4', 161250.0, 100], ['L_242_C4', 123750.0, 115], ['L_243_C1', 249375.0, 87], ['L_244_C5', 125000.0, 132], ['L_248_C1', 183750.0, 137], ['L_249_C4', 275000.0, 129], ['L_250_C3', 250000.0, 109], ['L_252_C6', 88125.0, 118], ['L_254_C3', 75000.0, 90], ['L_255_C5', 264375.0, 95], ['L_256_C1', 60000.0, 107], ['L_257_C3', 219375.0, 85], ['L_258_C2', 75000.0, 130], ['L_259_C2', 63750.0, 89], ['L_260_C3', 200000.0, 93], ['L_261_C5', 196875.0, 98], ['L_262_C2', 225000.0, 124], ['L_265_C6', 225000.0, 80], ['L_267_C3', 273750.0, 139], ['L_269_C3', 168750.0, 119], ['L_270_C4', 50000.0, 135], ['L_272_C1', 223125.0, 91], ['L_273_C6', 125000.0, 110], ['L_274_C1', 200000.0, 122], ['L_275_C4', 191250.0, 79], ['L_277_C3', 174375.0, 101], ['L_278_C5', 100000.0, 105], ['L_279_C4', 223125.0, 131], ['L_280_C2', 215625.0, 123], ['L_281_C1', 75000.0, 94], ['L_282_C6', 243750.0, 113], ['L_283_C4', 138750.0, 115], ['L_284_C3', 175000.0, 77], ['L_286_C2', 123750.0, 113], ['L_289_C5', 221250.0, 121]]
C1 = lista[0]
C2 = lista[1]
C3 = lista[2]
C4 = lista[3]
C5 = lista[4]
C6 = lista[5]
Blend1_1 = lista[6]
Blend1_2 = lista[7]
Blend2_1 = lista[8]
Blend2_2 = lista[9]
Blend2_3 = lista[10]
Blend3_1 = lista[11]
Blend4_1 = lista[12]
Blend4_2 = lista[13]
cepa_a_producir = {'C1': C1, 'C2': C2, 'C3': C3,'C4': C4, 'C5':C5, 'C6': C6}
blend_a_producir = {'Blend 1.1': Blend1_1, 'Blend 1.2': Blend1_2,'Blend 2.1': Blend2_1,'Blend 2.2': Blend2_2, 'Blend 2.3': Blend2_3, 'Blend 3.1': Blend3_1, 'Blend 4.1': Blend4_1, 'Blend 4.2': Blend4_2}
#para pasarlo a litros
cepa_a_producir = {k: v / 2 for k, v in cepa_a_producir.items()}
blend_a_producir = {k: v / 2 for k, v in blend_a_producir.items()}
# Crear un nuevo modelo3
modelo = gp.Model("optimizacion_vinos")

# Convertir info_lotes en DataFrame
info_lotes_df = pd.DataFrame(info_lotes, columns=['Lote', 'Litros', 'Dia_salida'])
#litros_por_cepa = {'C1': 4619375.0, 'C2': 7853750.0, 'C3': 6072500.0, 'C4': 6105625.0, 'C5': 8044375.0, 'C6': 2514375.0}
cepa = ["C1", "C2", "C3", "C4", "C5", "C6"]
# Configuración de parámetros adicionales
mercados = ['A', 'B', 'C', 'D']
blends = ["Blend 1.1", "Blend 1.2","Blend 2.1", "Blend 2.2", "Blend 2.3", "Blend 3.1","Blend 4.1", "Blend 4.2"]
asignacion_cepa_mercado = {'C1': 'B', 'C2': 'C', 'C3': 'B', 'C4': 'D', 'C5': 'A', 'C6': 'D'}
asignacion_blend_mercado = {'Blend 1.1': 'D','Blend 1.2': 'D', 'Blend 2.1': 'B','Blend 2.2': 'B', 'Blend 2.3': 'B', 'Blend 3.1': 'B', 'Blend 4.1': 'C', 'Blend 4.2': 'C'}  # Ejemplo de asignación
# ESTA EN BOTELLAS
demanda_minima_botellas = {
    'A': 9520000,
    'B': 12693333,
    'C': 11106667,
    'D': 9520000
}

# Datos de composición de blends y asignación a mercados
data_blends = [
    ("Blend 1.1", 0.1, 0.2, 0.0, 0.3, 0.0, 0.4),
    ("Blend 1.2", 0.0, 0.4, 0.2, 0.2, 0.0, 0.2),
    ("Blend 2.1", 0.3, 0.2, 0.1, 0.2, 0.0, 0.2),
    ("Blend 2.2", 0.0, 0.2, 0.2, 0.2, 0.2, 0.2),
    ("Blend 2.3", 0.2, 0.0, 0.2, 0.2, 0.0, 0.4),
    ("Blend 3.1", 0.5, 0.0, 0.2, 0.0, 0.1, 0.2),
    ("Blend 4.1", 0.15, 0.15, 0.15, 0.15, 0.1, 0.3),
    ("Blend 4.2", 0.12, 0.15, 0.08, 0.1, 0.1, 0.45),
    ("C1", 1, 0.0, 0.0, 0.0, 0.0, 0.0),
    ("C2", 0.0, 1, 0.0, 0.0, 0.0, 0.0),
    ("C3", 0.0, 0.0, 1, 0.0, 0.0, 0.0),
    ("C4", 0.0, 0.0, 0.0, 1, 0.0, 0.0),
    ("C5", 0.0, 0.0, 0.0, 0.0, 1, 0.0),
    ("C6", 0.0, 0.0, 0.0, 0.0, 0.0, 1)
]
blend_df = pd.DataFrame(data_blends, columns=['Blend', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6'])
porcentaje_demanda = 1
# Crear el modelo
modelo = gp.Model("optimizacion_vinos")

# Variables en LITROS
x = modelo.addVars(blend_a_producir.keys(), range(int(info_lotes_df['Dia_salida'].min()), int(info_lotes_df['Dia_salida'].max() + 1)), name="x")
y = modelo.addVars(litros_por_cepa.keys(), range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1), name="y")

# Función objetivo: Maximizar la producción total de botellas
objetivo = gp.quicksum(
    x[blend, dia] / 0.75 for blend in blends for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)
) + gp.quicksum(
    y[cepa, dia] / 0.75 for cepa in litros_por_cepa.keys() for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)
)
modelo.setObjective(objetivo, GRB.MAXIMIZE)
# Restricciones
# Restricción de cantidad disponible ajustada para trabajar con botellas
for cepa in litros_por_cepa.keys():
    for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1):
        litros_disponibles_dia_botellas = sum(registro[1]  for registro in info_lotes if registro[0].endswith(cepa) and dia + 10 >= registro[2] >= dia)
        modelo.addConstr(
            gp.quicksum(x[blend, dia] * blend_df.loc[blend_df['Blend'] == blend, cepa].item() for blend in blends) + y[cepa, dia] <= litros_disponibles_dia_botellas,
            name=f"restr_cantidad_{cepa}_{dia}"
        )

# Restricción para garantizar que la producción de cada cepa sea al menos el valor mínimo
for cepa, minimo in cepa_a_producir.items():
    modelo.addConstr(
        gp.quicksum(y[cepa, dia] for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)) >= minimo,
        name=f"restr_minimo_{cepa}"
    )

# Restricción para garantizar que la producción de cada blend sea al menos el valor mínimo
for blend, minimo in blend_a_producir.items():
    modelo.addConstr(
        gp.quicksum(x[blend, dia]  for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)) >= minimo,
        name=f"restr_minimo_{blend}"
    )
# Restricción de satisfacer al menos el 80% de la demanda mínima para cada mercado
for mercado, demanda in demanda_minima_botellas.items():
    modelo.addConstr(
        gp.quicksum(x[blend, dia]/0.75 for blend in blends if asignacion_blend_mercado.get(blend, 'Ninguno') == mercado for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)) +
        gp.quicksum(y[cepa, dia]/0.75 for cepa in litros_por_cepa.keys() if asignacion_cepa_mercado.get(cepa, 'Ninguno') == mercado for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1))
        >= demanda * porcentaje_demanda,
        name=f"demanda_min_{mercado}"
    )
# Añadir una restricción para asegurar que la producción total de botellas no exceda la capacidad total de botellas
#aqui se pasa a botellas lo

# Asegurar que la cantidad utilizada en blends más la cantidad producida no sea mayor a la capacidad total por cepa
for cepa in litros_por_cepa.keys():
    modelo.addConstr(
        gp.quicksum(x[blend, dia] * blend_df.loc[blend_df['Blend'] == blend, cepa].item() for blend in blends for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)) +
        gp.quicksum(y[cepa, dia] for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1))
        <= litros_por_cepa[cepa],
        name=f"capacidad_total_blend_{cepa}"
    )
# Optimización
modelo.optimize()


botellas_finales = []

# Ver resultados
if modelo.Status == GRB.OPTIMAL:
    print("Producción total por Cepa y Blend:")

    # Imprimir la producción por Cepa
    for cepa in litros_por_cepa.keys():
        total_cepa = sum((y[cepa, dia].X / 0.75 for dia in
                          range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)))
        print(f"Cepa {cepa}: {total_cepa:.2f} botellas")
        

    # Imprimir la producción por Blend
    for blend in blends:
        total_blend = sum((x[blend, dia].X / 0.75 for dia in
                           range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)))
        print(f"{blend}: {total_blend:.2f} botellas")
    print("Producción total de botellas:")
    for mercado in mercados:
        total_botellas = sum(
            (x[blend, dia].X / 0.75 for blend in blends if asignacion_blend_mercado.get(blend, 'Ninguno') == mercado for
             dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1))) + \
                         sum((y[cepa, dia].X / 0.75 for cepa in litros_por_cepa.keys() if
                              asignacion_cepa_mercado.get(cepa, 'Ninguno') == mercado for dia in
                              range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)))
        print(total_botellas)
        botellas_finales.append(total_botellas)
        print(f"Mercado {mercado}: {total_botellas:.2f} botellas")

else:
    print("No se encontró una solución óptima.")


ultimos_lotes = []
for lote_1 in lotes_fin:
    for lote_2 in info_lotes:
        if lote_2[0] == lote_1[0]:
            ultimos_lotes.append(lote_1)


for lote in ultimos_lotes:
    lote.pop(18)

# Crear un DataFrame de pandas a partir de la lista de listas
df = pd.DataFrame(ultimos_lotes)

# Guardar el DataFrame en un archivo Excel
df.to_excel("archivo_excel.xlsx", index=False)



#El atributo lote[0] Nombre lote
#El atributo lote[1] Numero lote
#El atributo lote[2] Tipo Uva
#El atributo lote[3] Ton lote
#El atributo lote[4] dia optimo
#El atributo lote[5] seca a lluvia
#El atributo lote[6] lluvia a lluvia
#El atributo lote[7] costo por kg
#El atributo lote[15] binaria spot
#El atributo lote[16] binaria fwd
#El atributo lote[--] Lista de calidad a lo largo de todos los dias
#El atributo lote[18] es una binaria que entrega un 1 si se cosecha el lote, cero si no se cosecha
#El atributo lote[19] entrega el dia en que se debe cosechar el lote, si no se cosecha, el valor del atributo es (-1)
#El atributo lote[20] calidad con la que se cosechó el lote
print (f"Esta la cantidad de botellas por mercado{botellas_finales}")

#calcular cantidad de lotes a comprar y fermentar
cantidad_lotes = len(ultimos_lotes)

#Calcular costos de comprar los lotes
#Calcular cuanto cuesta la compra de lotes (precio de los kilos del lote)
costo_compra_lotes = 0
costo_c1 = 0
costo_c2 = 0
costo_c3 = 0
costo_c4 = 0
costo_c5 = 0
costo_c6 = 0
kilos_c1 = 0
kilos_c2 = 0
kilos_c3 = 0
kilos_c4 = 0
kilos_c5 = 0
kilos_c6 = 0
for lote in ultimos_lotes:
    if lote[2] == "C1":
        costo_c1 += lote[3] * 1000 * lote[7] * (lote[15] * lote[20] + lote[16] * 0.8)

    if lote[2] == "C2":
        costo_c2 += lote[3] * 1000 * lote[7] * (lote[15] * lote[20] + lote[16] * 0.8)

    if lote[2] == "C3":
        costo_c3 += lote[3] * 1000 * lote[7] * (lote[15] * lote[20] + lote[16] * 0.8)

    if lote[2] == "C4":
        costo_c4 += lote[3] * 1000 * lote[7] * (lote[15] * lote[20] + lote[16] * 0.8)

    if lote[2] == "C5":
        costo_c5 += lote[3] * 1000 * lote[7] * (lote[15] * lote[20] + lote[16] * 0.8)
    
    if lote[2] == "C6":
        costo_c6 += lote[3] * 1000 * lote[7] * (lote[15] * lote[20] + lote[16] * 0.8)




costo_compra_lotes = costo_c1 + costo_c2 + costo_c3 + costo_c4 + costo_c5 + costo_c6

#Calcular costos/ingresos por botellas en mercados
Ingreso_mercado_A = 0
Ingreso_mercado_B = 0
Ingreso_mercado_C = 0
Ingreso_mercado_D = 0
Costo_mercado_A = 0
Costo_mercado_B = 0
Costo_mercado_C = 0
Costo_mercado_D = 0
costo_A = 2.875
costo_B = 2.375
costo_C = 1.825
costo_D = 1.545
# nose cual queri poner aca
#precio max es 6, precio min es 4 para A
p_A =6
#precio max es 4.5, precio min es 2.8 para B
p_B =4.5
#precio max es 3.5, precio min es 2.1 para C
p_C =3.5
#precio max es 2.2, precio min es 1.5 para D
p_D =2.2
for i in range(0,len(botellas_finales)):
    if i == 0:
        Ingreso_mercado_A += botellas_finales[i]*p_A
        Costo_mercado_A += botellas_finales[i] * costo_A
    elif i == 1:
        Ingreso_mercado_B += botellas_finales[i] * p_B
        Costo_mercado_B += botellas_finales[i] * costo_B

    elif i == 2:
        Ingreso_mercado_C += botellas_finales[i] * p_C
        Costo_mercado_C += botellas_finales[i] * costo_C

    elif i == 3:
        Ingreso_mercado_D += botellas_finales[i] * p_D
        Costo_mercado_D += botellas_finales[i] * costo_D


#Utilidades por mercado sin costos por compra de lote
Utilidad_A = Ingreso_mercado_A - Costo_mercado_A 

Utilidad_B = Ingreso_mercado_B - Costo_mercado_B

Utilidad_C = Ingreso_mercado_C - Costo_mercado_C

Utilidad_D = Ingreso_mercado_D - Costo_mercado_D

Ingreso_total_botellas = Ingreso_mercado_A + Ingreso_mercado_B + Ingreso_mercado_C + Ingreso_mercado_D
Costo_total_botellas = Costo_mercado_A + Costo_mercado_B + Costo_mercado_C + Costo_mercado_D

Utilidad_por_botellas = Ingreso_total_botellas - Costo_total_botellas


#Procesando tanques (todos los tanques se arriendan con anticipacion, ninguno sobre la marcha)
def tanq_planta(cantidad_tanques):
    if cantidad_tanques >= (24*3):
        return (24 * 3)
    else:
        return(cantidad_tanques)

Tanques_planta1 = tanq_planta(contador_tanques)
Tanques_planta2 = tanq_planta(contador_tanques - Tanques_planta1)
Tanques_planta3 = tanq_planta(contador_tanques - Tanques_planta1 - Tanques_planta2)

costo_planta1 = Tanques_planta1 * 1500 * 25
costo_planta2 = Tanques_planta2 * 1600 * 25
costo_planta3 = Tanques_planta3 * 1800 * 25

costo_plantas = costo_planta1 + costo_planta2 + costo_planta3


print(f"Utilidad por botellas mercado A: {Utilidad_A}")
print("...")
print(f"Utilidad por botellas mercado B: {Utilidad_B}")
print("...")
print(f"Utilidad por botellas mercado C: {Utilidad_C}")
print("...")
print(f"Utilidad por botellas mercado D: {Utilidad_D}")
print("...")
print(f"Ingresos por botellas: {Ingreso_total_botellas}")
print("...")
print(f"Costo por botellas: {Costo_total_botellas}")
print("...")
print(f"Utilidad solo por botellas: {Utilidad_por_botellas}")
print("...")
print(f"Costos de compra de lotes de C1: {costo_c1}")
print("...")
print(f"Costos de compra de lotes de C2: {costo_c2}")
print("...")
print(f"Costos de compra de lotes de C3: {costo_c3}")
print("...")
print(f"Costos de compra de lotes de C4: {costo_c4}")
print("...")
print(f"Costos de compra de lotes de C5: {costo_c5}")
print("...")
print(f"Costos de compra de lotes de C6: {costo_c6}")
print("...")
print(f"Este es el costo de comprar los lotes: {costo_compra_lotes}")
print("...")
print(f"Utilidades totales hasta el momento Uti. por botellas - costo compra lotes: {Utilidad_por_botellas - costo_compra_lotes}")
print("...")
print(f"La cantidad de lotes que se compran y se fermentan es: {cantidad_lotes}")
print("...")
print(f"Cantidad de tanques usados en planta 1: {Tanques_planta2}, su costo es {costo_planta2}")
print("...")
print(f"Cantidad de tanques usados en planta 2: {Tanques_planta1}, su costo es {costo_planta1}")
print("...")
print(f"Cantidad de tanques usados en planta 3: {Tanques_planta3}, su costo es {costo_planta3}")
print("...")
print(f"El costo total en tanques es: {costo_plantas}")
print("...")
print(f"Utilidades totales hasta el momento Uti. por botellas - costo compra lotes - costo arriendo plantas: {Utilidad_por_botellas - costo_compra_lotes - costo_plantas}")
