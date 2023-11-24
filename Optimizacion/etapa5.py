import pandas as pd
import gurobipy as gp
from gurobipy import GRB

#from Etapa4 import info_lotes, litros_por_cepa

# Datos proporcionados
info_lotes = [['L_1_C4', 108750.0, 121], ['L_2_C4', 250000.0, 128], ['L_4_C4', 84375.0, 121], ['L_6_C3', 75000.0, 93], ['L_7_C5', 275000.0, 108], ['L_9_C1', 25000.0, 125], ['L_10_C5', 50000.0, 101], ['L_12_C1', 206250.0, 138], ['L_14_C2', 249375.0, 130], ['L_15_C1', 50000.0, 141], ['L_17_C5', 67031.2454687501, 155], ['L_18_C2', 123750.0, 108], ['L_19_C2', 225000.0, 83], ['L_20_C4', 112500.0, 78], ['L_21_C5', 213750.0, 76], ['L_22_C1', 210000.0, 82], ['L_23_C3', 131250.0, 108], ['L_24_C5', 45468.75, 155], ['L_25_C3', 75000.0, 122], ['L_28_C3', 175000.0, 107], ['L_30_C4', 50000.0, 87], ['L_31_C1', 150000.0, 127], ['L_34_C2', 67500.0, 87], ['L_35_C5', 170625.0, 127], ['L_42_C4', 175000.0, 133], ['L_43_C1', 50000.0, 133], ['L_44_C2', 183750.0, 86], ['L_45_C4', 249375.0, 104], ['L_46_C4', 223125.0, 146], ['L_47_C2', 112500.0, 101], ['L_48_C1', 225000.0, 114], ['L_50_C5', 270000.0, 92], ['L_51_C1', 200000.0, 103], ['L_52_C2', 225000.0, 93], ['L_53_C6', 123750.0, 94], ['L_54_C2', 150000.0, 83], ['L_55_C2', 279375.0, 79], ['L_56_C2', 241875.0, 116], ['L_57_C5', 116250.0, 77], ['L_58_C4', 75000.0, 88], ['L_60_C4', 250000.0, 79], ['L_61_C1', 166875.0, 107], ['L_63_C3', 75000.0, 97], ['L_64_C2', 191250.0, 105], ['L_65_C3', 170625.0, 96], ['L_66_C3', 25000.0, 125], ['L_67_C3', 249375.0, 99], ['L_70_C5', 75000.0, 117], ['L_71_C5', 243750.0, 99], ['L_72_C1', 108750.0, 107], ['L_73_C2', 146250.0, 91], ['L_74_C2', 71250.0, 88], ['L_75_C2', 150000.0, 94], ['L_76_C2', 138750.0, 91], ['L_77_C2', 200000.0, 103], ['L_80_C5', 150000.0, 115], ['L_81_C5', 75000.0, 122], ['L_82_C2', 175000.0, 105], ['L_85_C4', 97500.0, 137], ['L_87_C3', 262500.0, 78], ['L_88_C1', 175000.0, 122], ['L_91_C3', 228750.00000000006, 90], ['L_95_C5', 106875.0, 84], ['L_96_C5', 148125.0, 108], ['L_98_C4', 175000.0, 123], ['L_99_C2', 63750.0, 93], ['L_101_C2', 95625.0, 130], ['L_102_C5', 266250.0, 113], ['L_103_C2', 175000.0, 129], ['L_104_C4', 243750.0, 74], ['L_105_C2', 65625.0, 111], ['L_107_C1', 175000.0, 106], ['L_108_C4', 100000.0, 93], ['L_109_C4', 75000.0, 104], ['L_110_C3', 275000.0, 132], ['L_111_C3', 250000.0, 113], ['L_114_C3', 243750.0, 86], ['L_115_C3', 200000.0, 123], ['L_116_C3', 75000.0, 128], ['L_120_C3', 100000.0, 74], ['L_122_C6', 50000.0, 107], ['L_123_C1', 144375.0, 67], ['L_125_C4', 69375.0, 82], ['L_126_C5', 93750.0, 81], ['L_127_C5', 93750.0, 114], ['L_128_C1', 146250.0, 100], ['L_130_C3', 71250.0, 86], ['L_132_C2', 200000.0, 126], ['L_133_C2', 99375.0, 133], ['L_134_C4', 95625.0, 92], ['L_135_C4', 175000.0, 125], ['L_136_C3', 251249.99999999997, 76], ['L_140_C3', 50000.0, 105], ['L_141_C5', 208125.0, 94], ['L_142_C5', 240000.0, 100], ['L_143_C2', 50000.0, 122], ['L_144_C4', 105000.0, 138], ['L_145_C2', 91875.0, 114], ['L_146_C5', 275000.0, 102], ['L_149_C5', 195000.0, 119], ['L_150_C6', 256875.0, 87], ['L_153_C5', 127500.0, 118], ['L_154_C3', 175000.0, 85], ['L_155_C4', 150000.0, 127], ['L_156_C4', 65625.0, 101], ['L_157_C2', 225000.0, 119], ['L_158_C4', 175000.0, 123], ['L_160_C1', 25000.0, 122], ['L_162_C5', 175000.0, 123], ['L_164_C5', 253125.0, 120], ['L_165_C4', 69375.0, 86], ['L_166_C4', 71250.0, 100], ['L_167_C4', 219375.0, 107], ['L_168_C2', 258750.0, 137], ['L_169_C2', 138750.0, 131], ['L_170_C5', 148125.0, 116], ['L_171_C3', 65625.0, 108], ['L_174_C2', 75000.0, 127], ['L_177_C3', 61875.0, 87], ['L_179_C4', 71250.0, 126], ['L_180_C2', 247500.0, 91], ['L_181_C4', 58124.99999999996, 119], ['L_182_C2', 200000.0, 117], ['L_184_C1', 100000.0, 107], ['L_187_C2', 159375.0, 69], ['L_188_C2', 121875.0, 91], ['L_189_C4', 86250.0, 104], ['L_190_C5', 273750.0, 142], ['L_194_C4', 251249.99999999997, 77], ['L_195_C5', 213750.0, 133], ['L_196_C2', 200000.0, 126], ['L_198_C3', 175000.0, 109], ['L_199_C5', 100000.0, 106], ['L_200_C5', 50000.0, 127], ['L_201_C1', 75000.0, 88], ['L_202_C3', 25000.0, 123], ['L_203_C3', 150000.0, 106], ['L_204_C2', 69375.0, 82], ['L_205_C2', 225000.0, 100], ['L_206_C3', 200000.0, 99], ['L_208_C2', 118125.0, 97], ['L_210_C4', 25000.0, 125], ['L_212_C5', 175000.0, 125], ['L_213_C4', 225000.0, 122], ['L_214_C1', 249375.0, 110], ['L_216_C2', 88125.0, 97], ['L_217_C3', 250000.0, 128], ['L_218_C4', 50000.0, 109], ['L_219_C4', 200000.0, 100], ['L_220_C4', 114375.0, 142], ['L_222_C6', 228750.0, 140], ['L_223_C2', 250000.0, 125], ['L_224_C2', 247500.0, 104], ['L_225_C4', 50000.0, 129], ['L_226_C2', 200000.0, 100], ['L_227_C3', 50000.0, 88], ['L_228_C2', 275000.0, 126], ['L_229_C2', 116250.0, 81], ['L_230_C5', 88125.0, 116], ['L_231_C3', 150000.0, 72], ['L_232_C5', 223125.0, 132], ['L_235_C2', 84375.0, 111], ['L_236_C4', 175000.0, 107], ['L_237_C3', 58125.0, 135], ['L_238_C5', 99375.0, 71], ['L_240_C3', 50000.0, 130], ['L_241_C4', 150000.0, 110], ['L_242_C4', 123750.0, 119], ['L_244_C5', 125000.0, 129], ['L_249_C4', 275000.0, 135], ['L_250_C3', 250000.0, 102], ['L_252_C6', 75000.0, 110], ['L_254_C3', 82500.0, 91], ['L_255_C5', 264375.0, 95], ['L_256_C1', 50000.0, 101], ['L_257_C3', 219375.0, 93], ['L_258_C2', 75000.0, 122], ['L_259_C2', 63750.0, 85], ['L_260_C3', 204375.0, 88], ['L_261_C5', 196875.0, 94], ['L_262_C2', 225000.0, 122], ['L_267_C3', 250000.0, 128], ['L_269_C3', 168750.0, 106], ['L_270_C4', 50625.0, 137], ['L_271_C2', 91875.0, 99], ['L_272_C1', 223125.0, 93], ['L_274_C1', 200000.0, 124], ['L_275_C4', 191250.0, 77], ['L_277_C3', 125000.0, 103], ['L_278_C5', 100000.0, 104], ['L_279_C4', 223125.0, 145], ['L_280_C2', 200000.0, 125], ['L_281_C1', 80625.0, 79], ['L_282_C6', 243750.0, 109], ['L_283_C4', 125000.0, 124], ['L_284_C3', 180000.0, 136], ['L_286_C2', 123750.0, 105], ['L_289_C5', 221250.0, 120]]
litros_por_cepa = {'C1': 3035625.0, 'C2': 7851250.0, 'C3': 5874375.0, 'C4': 5910000.0, 'C5': 6213125.0, 'C6': 978125.0}


# Crear un nuevo modelo
modelo = gp.Model("optimizacion_vinos")

# Convertir info_lotes en DataFrame
info_lotes_df = pd.DataFrame(info_lotes, columns=['Lote', 'Litros', 'Dia_salida'])

# Agrupar los litros por cepa
litros_disponibles = {}
for cepa in litros_por_cepa.keys():
    litros_disponibles[cepa] = litros_por_cepa[cepa]

# Datos de demanda del mercado (en botellas), convertidos a litros
demanda_minima_botellas = {
    'A': 9520000,
    'B': 12693333,
    'C': 11106667,
    'D': 9520000
}
demanda_minima_litros = {mercado: botellas * 0.75 for mercado, botellas in demanda_minima_botellas.items()}

# Datos de composición de blends y asignación a mercados
data = [
    ("Blend 1", 'D', 0.1, 0.2, 0.0, 0.3, 0.0, 0.4),
    ("Blend 2", 'B', 0.2, 0.0, 0.2, 0.2, 0.0, 0.4),
    ("Blend 3", 'B', 0.5, 0.0, 0.2, 0.0, 0.1, 0.2),
    ("Blend 4", 'C', 0.12, 0.15, 0.08, 0.1, 0.1, 0.45),
    ("C1", 'B', 1, 0.0, 0.0, 0.0, 0.0, 0.0),
    ("C2", 'C', 0.0, 1, 0.0, 0.0, 0.0, 0.0),
    ("C3", 'B', 0.0, 0.0, 1, 0.0, 0.0, 0.0),
    ("C4", 'D', 0.0, 0.0, 0.0, 1, 0.0, 0.0),
    ("C5", 'A', 0.0, 0.0, 0.0, 0.0, 1, 0.0),
    ("C6", 'D', 0.0, 0.0, 0.0, 0.0, 0.0, 1)
]
asignacion_cepa_mercado = {
    'C1': 'B', 'C2': 'C', 'C3': 'B', 'C4': 'D', 'C5': 'A', 'C6': 'D'
}
# Crear DataFrame de blends y cepas
blend_df = pd.DataFrame(data, columns=['Blend', 'Mercado', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6'])

# Crear variables para el modelo
x = modelo.addVars(blend_df['Blend'], name="x")  # Litros destinados a cada blend
y = modelo.addVars(litros_por_cepa.keys(), name="y")  # Litros de cepa pura vendidos directamente

# Función objetivo: Minimizar la diferencia entre la demanda y la oferta
modelo.setObjective(
    sum(
        (demanda_minima_litros[mercado] 
         - gp.quicksum(
             x[blend] * blend_df.at[i, cepa]
             for i, blend in enumerate(blend_df['Blend'])
             if blend_df.at[i, 'Mercado'] == mercado
             for cepa in litros_por_cepa.keys()
           ) 
         - gp.quicksum(
             y[cepa] 
             for cepa in litros_por_cepa.keys() 
             if asignacion_cepa_mercado[cepa] == mercado
           )
        )**2
    for mercado in demanda_minima_litros), GRB.MINIMIZE)

# Restricciones
# 1. No exceder la cantidad disponible de cada cepa
for cepa in litros_disponibles:
    modelo.addConstr(
        gp.quicksum(x[blend] * blend_df.at[j, cepa] for j, blend in enumerate(blend_df['Blend'])) + y[cepa] <= litros_disponibles[cepa], 
        name=f"restr_cantidad_{cepa}")

# 2. Satisfacer la demanda mínima de cada mercado (en litros), en lo posible
for mercado in demanda_minima_litros:
    modelo.addConstr(
        gp.quicksum(
            x[blend] * blend_df.at[i, cepa]
            for i, blend in enumerate(blend_df['Blend'])
            if blend_df.at[i, 'Mercado'] == mercado
            for cepa in litros_por_cepa.keys()
        ) +
        gp.quicksum(
            y[cepa]
            for cepa in litros_por_cepa.keys()
            if asignacion_cepa_mercado[cepa] == mercado
        ) >= demanda_minima_litros[mercado] * 0.8, 
        name=f"demanda_min_{mercado}")

# Optimizar
modelo.optimize()

# Resultados
if modelo.Status == GRB.OPTIMAL:
    # Cálculo de botellas producidas para cada mercado
    botellas_producidas = {mercado: 0 for mercado in demanda_minima_litros}
    for mercado in botellas_producidas:
        botellas_producidas[mercado] = (
            sum(x[blend].X * blend_df.at[i, cepa]
                for i, blend in enumerate(blend_df['Blend'])
                if blend_df.at[i, 'Mercado'] == mercado
                for cepa in litros_por_cepa.keys()) +
            sum(y[cepa].X for cepa in litros_por_cepa.keys() if asignacion_cepa_mercado[cepa] == mercado)
        ) / 0.75  # Convertir a botellas

    for mercado, botellas in botellas_producidas.items():
        print(f"Mercado {mercado}: {botellas} botellas")
else:
    print("No se encontró una solución óptima.")