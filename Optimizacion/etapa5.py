import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from Etapa4 import info_lotes, litros_por_cepa
# Datos de entrada
#info_lotes = [['L_1_C4', 100000.0, 130], ['L_2_C4', 250000.0, 129], ['L_3_C6', 225000.0, 87], ['L_4_C4', 84375.00000000001, 138], ['L_6_C3', 75000.0, 102], ['L_7_C5', 275000.0, 113], ['L_8_C6', 221250.0, 88], ['L_9_C1', 150000.0, 130], ['L_10_C5', 50000.0, 91], ['L_11_C1', 275000.0, 109], ['L_12_C1', 200000.0, 141], ['L_14_C2', 249375.0, 126], ['L_15_C1', 50000.0, 140], ['L_17_C5', 250000.0, 119], ['L_18_C2', 100000.0, 103], ['L_19_C2', 225000.0, 95], ['L_20_C4', 100000.0, 90], ['L_21_C5', 213750.0, 90], ['L_22_C1', 210000.0, 73], ['L_23_C3', 125000.0, 105], ['L_25_C3', 84375.0, 132], ['L_28_C3', 191250.0, 93], ['L_29_C1', 142500.0, 86], ['L_30_C4', 50000.0, 89], ['L_31_C1', 150000.0, 121], ['L_33_C6', 150000.0, 113], ['L_34_C2', 67500.0, 89], ['L_35_C5', 170625.0, 124], ['L_37_C6', 150000.0, 104], ['L_38_C1', 91875.0, 107], ['L_39_C6', 75000.0, 90], ['L_40_C1', 73125.0, 100], ['L_42_C4', 176250.0, 144], ['L_43_C1', 50000.0, 123], ['L_44_C2', 183750.0, 76], ['L_45_C4', 249375.0, 103], ['L_46_C4', 223125.0, 140], ['L_47_C2', 112500.0, 90], ['L_48_C1', 50000.0, 117], ['L_49_C5', 200000.0, 112], ['L_50_C5', 250000.0, 120], ['L_51_C1', 200000.0, 104], ['L_52_C2', 225000.0, 96], ['L_53_C6', 123750.0, 96], ['L_54_C2', 153750.0, 77], ['L_55_C2', 275000.0, 89], ['L_56_C2', 225000.0, 123], ['L_57_C5', 100000.0, 93], ['L_58_C4', 75000.0, 94], ['L_60_C4', 250000.0, 78], ['L_61_C1', 150000.0, 112], ['L_62_C1', 114375.0, 131], ['L_63_C3', 75000.0, 110], ['L_64_C2', 191250.0, 95], ['L_65_C3', 170625.0, 101], ['L_66_C3', 50000.0, 140], ['L_67_C3', 249375.0, 107], ['L_70_C5', 75000.0, 116], ['L_71_C5', 150000.0, 102], ['L_72_C1', 100000.0, 102], ['L_73_C2', 146250.0, 97], ['L_74_C2', 71250.0, 86], ['L_75_C2', 150000.0, 104], ['L_76_C2', 125000.0, 87], ['L_77_C2', 200000.0, 101], ['L_78_C5', 200000.0, 99], ['L_79_C5', 193125.0, 96], ['L_80_C5', 125000.0, 118], ['L_81_C5', 185625.0, 131], ['L_82_C2', 100000.0, 109], ['L_84_C1', 125000.0, 132], ['L_85_C4', 97500.0, 142], ['L_87_C3', 262500.0, 77], ['L_88_C1', 175000.0, 99], ['L_90_C6', 50000.0, 134], ['L_91_C3', 228750.00000000015, 79], ['L_92_C5', 208125.0, 137], ['L_93_C1', 75000.0, 109], ['L_95_C5', 106875.0, 95], ['L_96_C5', 125000.0, 103], ['L_98_C4', 200000.0, 114], ['L_99_C2', 63750.0, 85], ['L_101_C2', 95625.0, 134], ['L_102_C5', 250000.0, 110], ['L_103_C2', 271875.0, 124], ['L_104_C4', 243750.0, 90], ['L_105_C2', 65625.0, 121], ['L_106_C1', 200000.0, 92], ['L_107_C1', 183750.0, 104], ['L_108_C4', 100000.0, 91], ['L_109_C4', 82500.0, 93], ['L_110_C3', 275000.0, 140], ['L_111_C3', 250000.0, 127], ['L_113_C1', 279375.0, 139], ['L_114_C3', 243750.0, 89], ['L_115_C3', 215625.0, 77], ['L_116_C3', 80625.0, 138], ['L_117_C1', 189375.0, 122], ['L_120_C3', 108750.0, 84], ['L_122_C6', 50000.0, 120], ['L_125_C4', 69375.0, 76], ['L_126_C5', 93750.0, 85], ['L_127_C5', 75000.0, 123], ['L_128_C1', 146250.0, 109], ['L_129_C1', 75000.0, 119], ['L_130_C3', 71250.0, 90], ['L_132_C2', 221250.0, 111], ['L_133_C2', 99375.0, 132], ['L_134_C4', 75000.0, 103], ['L_135_C4', 187500.0, 112], ['L_136_C3', 251249.99999999997, 71], ['L_139_C6', 208125.0, 137], ['L_140_C3', 50000.0, 109], ['L_141_C5', 200000.0, 100], ['L_142_C5', 225000.0, 101], ['L_143_C2', 63750.0, 112], ['L_144_C4', 100000.0, 130], ['L_145_C2', 75000.0, 112], ['L_146_C5', 275625.0, 86], ['L_147_C1', 138750.0, 131], ['L_149_C5', 195000.0, 120], ['L_150_C6', 75000.0, 98], ['L_152_C5', 175000.0, 87], ['L_153_C5', 125000.0, 127], ['L_154_C3', 183750.0, 73], ['L_155_C4', 100000.0, 117], ['L_156_C4', 65625.0, 92], ['L_157_C2', 225000.0, 124], ['L_158_C4', 175000.0, 116], ['L_159_C5', 90000.0, 131], ['L_160_C1', 125000.0, 122], ['L_162_C5', 181875.0, 141], ['L_163_C1', 48750.0, 105], ['L_164_C5', 250000.0, 110], ['L_165_C4', 69375.0, 86], ['L_166_C4', 71250.0, 116], ['L_167_C4', 219375.00000000015, 115], ['L_168_C2', 250000.0, 128], ['L_169_C2', 125000.0, 120], ['L_170_C5', 148125.0, 120], ['L_171_C3', 65625.0, 112], ['L_172_C1', 250000.0, 104], ['L_173_C1', 100000.0, 101], ['L_174_C2', 93750.0, 133], ['L_177_C3', 61875.0, 71], ['L_178_C6', 181875.0, 79], ['L_179_C4', 71250.0, 132], ['L_180_C2', 247500.0, 83], ['L_181_C4', 50000.0, 115], ['L_182_C2', 200000.0, 103], ['L_184_C1', 100000.0, 111], ['L_187_C2', 159375.0, 85], ['L_188_C2', 121875.0, 92], ['L_189_C4', 86250.0, 88], ['L_190_C5', 273750.0, 133], ['L_192_C1', 75000.0, 90], ['L_194_C4', 250000.0, 80], ['L_195_C5', 213750.0, 141], ['L_196_C2', 200000.0, 127], ['L_198_C3', 189375.00000000023, 106], ['L_199_C5', 150000.0, 129], ['L_200_C5', 268125.0, 130], ['L_201_C1', 75000.0, 80], ['L_202_C3', 150000.0, 118], ['L_203_C3', 150000.0, 106], ['L_204_C2', 69375.0, 87], ['L_205_C2', 234375.0, 98], ['L_206_C3', 200000.0, 108], ['L_208_C2', 118125.0, 93], ['L_209_C5', 50000.0, 102], ['L_210_C4', 247500.0, 121], ['L_211_C5', 271875.0, 138], ['L_212_C5', 175000.0, 130], ['L_213_C4', 225000.0, 111], ['L_214_C1', 249375.0, 120], ['L_216_C2', 88125.0, 107], ['L_217_C3', 264375.0, 131], ['L_218_C4', 50000.0, 109], ['L_219_C4', 200000.0, 94], ['L_220_C4', 114375.0, 130], ['L_221_C6', 225000.0, 101], ['L_222_C6', 228750.0, 139], ['L_223_C2', 250000.0, 129], ['L_224_C2', 247500.0, 97], ['L_225_C4', 50625.0, 148], ['L_226_C2', 217500.0, 112], ['L_227_C3', 50000.0, 94], ['L_228_C2', 275000.0, 119], ['L_229_C2', 100000.0, 89], ['L_231_C3', 150000.0, 74], ['L_232_C5', 223125.0, 120], ['L_234_C1', 213750.0, 94], ['L_235_C2', 84375.0, 122], ['L_236_C4', 175000.0, 102], ['L_237_C3', 58125.0, 135], ['L_238_C5', 99375.0, 85], ['L_239_C5', 125000.0, 121], ['L_240_C3', 50000.0, 144], ['L_241_C4', 161250.00000000012, 105], ['L_242_C4', 100000.0, 114], ['L_243_C1', 249375.0, 96], ['L_244_C5', 125625.0, 140], ['L_246_C1', 275000.0, 131], ['L_248_C1', 175000.0, 134], ['L_249_C4', 275000.0, 129], ['L_250_C3', 250000.0, 116], ['L_252_C6', 75000.0, 121], ['L_254_C3', 75000.0, 100], ['L_255_C5', 150000.0, 97], ['L_257_C3', 219375.0, 80], ['L_258_C2', 75000.0, 122], ['L_259_C2', 63750.0, 79], ['L_260_C3', 200000.0, 97], ['L_261_C5', 196875.0, 82], ['L_262_C2', 225000.0, 123], ['L_264_C1', 250000.0, 120], ['L_265_C6', 225000.0, 98], ['L_267_C3', 273750.0, 136], ['L_268_C1', 172500.0, 94], ['L_269_C3', 150000.0, 109], ['L_270_C4', 50000.0, 127], ['L_271_C2', 75000.0, 102], ['L_272_C1', 223125.0, 80], ['L_273_C6', 125000.0, 112], ['L_274_C1', 200000.0, 131], ['L_275_C4', 191250.0, 83], ['L_276_C1', 150000.0, 118], ['L_277_C3', 174375.0, 109], ['L_278_C5', 75000.0, 123], ['L_279_C4', 223125.0, 143], ['L_280_C2', 200000.0, 114], ['L_281_C1', 75000.0, 90], ['L_282_C6', 225000.0, 114], ['L_283_C4', 125000.0, 111], ['L_284_C3', 180000.0, 78], ['L_286_C2', 123750.0, 104], ['L_289_C5', 221250.0, 119]]
#litros_por_cepa = {'C1': 6601250.0, 'C2': 7826250.0, 'C3': 6153750.0, 'C4': 6060000.0, 'C5': 7781250.0, 'C6': 2613750.0}
print(litros_por_cepa)
# Crear un nuevo modelo
modelo = gp.Model("optimizacion_vinos")

# Convertir info_lotes en DataFrame
info_lotes_df = pd.DataFrame(info_lotes, columns=['Lote', 'Litros', 'Dia_salida'])


# Configuración de parámetros adicionales
mercados = ['A', 'B', 'C', 'D']
blends = ["Blend 1", "Blend 2", "Blend 3", "Blend 4", "C1", "C2", "C3", "C4", "C5", "C6"]
asignacion_cepa_mercado = {'C1': 'B', 'C2': 'C', 'C3': 'B', 'C4': 'D', 'C5': 'A', 'C6': 'D'}
asignacion_blend_mercado = {'Blend 1': 'D', 'Blend 2': 'B', 'Blend 3': 'B', 'Blend 4': 'C'}  # Ejemplo de asignación
demanda_minima_litros = {
    'A': 9520000,
    'B': 12693333,
    'C': 11106667,
    'D': 9520000
}
litros_por_cepa_botellas = {cepa: litros / 0.75 for cepa, litros in litros_por_cepa.items()}


# Datos de composición de blends y asignación a mercados
data_blends = [
    ("Blend 1", 0.1, 0.2, 0.0, 0.3, 0.0, 0.4),
    ("Blend 2", 0.2, 0.0, 0.2, 0.2, 0.0, 0.4),
    ("Blend 3", 0.5, 0.0, 0.2, 0.0, 0.1, 0.2),
    ("Blend 4", 0.12, 0.15, 0.08, 0.1, 0.1, 0.45),
    ("C1", 'B', 1, 0.0, 0.0, 0.0, 0.0, 0.0),
    ("C2", 'C', 0.0, 1, 0.0, 0.0, 0.0, 0.0),
    ("C3", 'B', 0.0, 0.0, 1, 0.0, 0.0, 0.0),
    ("C4", 'D', 0.0, 0.0, 0.0, 1, 0.0, 0.0),
    ("C5", 'A', 0.0, 0.0, 0.0, 0.0, 1, 0.0),
    ("C6", 'D', 0.0, 0.0, 0.0, 0.0, 0.0, 1)
]
blend_df = pd.DataFrame(data_blends, columns=['Blend', 'Mercado', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6'])

porcentaje_demanda = 0.59
# Crear el modelo
modelo = gp.Model("optimizacion_vinos")

# Variables
x = modelo.addVars(blends, range(int(info_lotes_df['Dia_salida'].min()), int(info_lotes_df['Dia_salida'].max() + 1)), name="x")
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
        litros_disponibles_dia_botellas = sum(registro[1] / 0.75 for registro in info_lotes if registro[0].endswith(cepa) and registro[2] <= dia)
        modelo.addConstr(
            gp.quicksum(x[blend, dia] * blend_df.loc[blend_df['Blend'] == blend, cepa].item() for blend in blends) + y[cepa, dia] <= litros_disponibles_dia_botellas,
            name=f"restr_cantidad_{cepa}_{dia}"
        )
# Restricción de satisfacer al menos el 80% de la demanda mínima para cada mercado
for mercado, demanda in demanda_minima_litros.items():
    modelo.addConstr(
        gp.quicksum(x[blend, dia] for blend in blends if asignacion_blend_mercado.get(blend, 'Ninguno') == mercado for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)) + 
        gp.quicksum(y[cepa, dia] for cepa in litros_por_cepa.keys() if asignacion_cepa_mercado.get(cepa, 'Ninguno') == mercado for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1))
        >= demanda * porcentaje_demanda,
        name=f"demanda_min_{mercado}"
    )
# Añadir una restricción para asegurar que la producción total de botellas no exceda la capacidad total de litros
capacidad_total_litros = sum(litros_por_cepa.values()) * 0.75
modelo.addConstr(
    gp.quicksum(x[blend, dia] / 0.75 for blend in blends for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)) +
    gp.quicksum(y[cepa, dia] / 0.75 for cepa in litros_por_cepa.keys() for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1))
    <= capacidad_total_litros,
    name="capacidad_total"
)

# Optimización
modelo.optimize()

# Ver resultados
if modelo.Status == GRB.OPTIMAL:
    print("Producción total de botellas:")
    for mercado in mercados:
        total_botellas = sum((x[blend, dia].X / 0.75 for blend in blends if asignacion_blend_mercado.get(blend, 'Ninguno') == mercado for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1))) + \
                         sum((y[cepa, dia].X / 0.75 for cepa in litros_por_cepa.keys() if asignacion_cepa_mercado.get(cepa, 'Ninguno') == mercado for dia in range(info_lotes_df['Dia_salida'].min(), info_lotes_df['Dia_salida'].max() + 1)))
        print(f"Mercado {mercado}: {total_botellas:.2f} botellas")
else:
    print("No se encontró una solución óptima.")