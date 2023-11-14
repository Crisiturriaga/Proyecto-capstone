from gurobipy import Model, GRB
from Etapa1 import Requerimientos,prop
from Etapa2 import lotes_finales_ordenados, lote_info
import numpy as np

# Creación del modelo
m = Model("OptimizacionCosechaLotes")

# Índices
S = []  # Conjunto de lotes comprados con spot
F = [] # Conjunto de lotes comprados con forward
for i in lotes_finales_ordenados:
    if i[15] == 1:
        S.append(i[0])
    elif i[16] == 1:
        F.append(i[0])
print("S",S)
print("F",F)

L = [
    'L_1_C4', 'L_2_C4', 'L_3_C6', 'L_4_C4', 'L_5_C6', 'L_6_C3', 'L_7_C5', 'L_8_C6', 'L_9_C1', 'L_10_C5',
    'L_11_C1', 'L_12_C1', 'L_13_C5', 'L_14_C2', 'L_15_C1', 'L_16_C6', 'L_17_C5', 'L_18_C2', 'L_19_C2', 'L_20_C4',
    'L_21_C5', 'L_22_C1', 'L_23_C3', 'L_24_C5', 'L_25_C3', 'L_26_C6', 'L_27_C6', 'L_28_C3', 'L_29_C1', 'L_30_C4',
    'L_31_C1', 'L_32_C6', 'L_33_C6', 'L_34_C2', 'L_35_C5', 'L_36_C6', 'L_37_C6', 'L_38_C1', 'L_39_C6', 'L_40_C1',
    'L_41_C1', 'L_42_C4', 'L_43_C1', 'L_44_C2', 'L_45_C4', 'L_46_C4', 'L_47_C2', 'L_48_C1', 'L_49_C5', 'L_50_C5',
    'L_51_C1', 'L_52_C2', 'L_53_C6', 'L_54_C2', 'L_55_C2', 'L_56_C2', 'L_57_C5', 'L_58_C4', 'L_59_C5', 'L_60_C4',
    'L_61_C1', 'L_62_C1', 'L_63_C3', 'L_64_C2', 'L_65_C3', 'L_66_C3', 'L_67_C3', 'L_68_C1', 'L_69_C1', 'L_70_C5',
    'L_71_C5', 'L_72_C1', 'L_73_C2', 'L_74_C2', 'L_75_C2', 'L_76_C2', 'L_77_C2', 'L_78_C5', 'L_79_C5', 'L_80_C5',
    'L_81_C5', 'L_82_C2', 'L_83_C5', 'L_84_C1', 'L_85_C4', 'L_86_C5', 'L_87_C3', 'L_88_C1', 'L_89_C6', 'L_90_C6',
    'L_91_C3', 'L_92_C5', 'L_93_C1', 'L_94_C6', 'L_95_C5', 'L_96_C5', 'L_97_C6', 'L_98_C4', 'L_99_C2', 'L_100_C6',
    'L_101_C2', 'L_102_C5', 'L_103_C2', 'L_104_C4', 'L_105_C2', 'L_106_C1', 'L_107_C1', 'L_108_C4', 'L_109_C4',
    'L_110_C3', 'L_111_C3', 'L_112_C1', 'L_113_C1', 'L_114_C3', 'L_115_C3', 'L_116_C3', 'L_117_C1', 'L_118_C6',
    'L_119_C6', 'L_120_C3', 'L_121_C5', 'L_122_C6', 'L_123_C1', 'L_124_C6', 'L_125_C4', 'L_126_C5', 'L_127_C5',
    'L_128_C1', 'L_129_C1', 'L_130_C3', 'L_131_C6', 'L_132_C2', 'L_133_C2', 'L_134_C4', 'L_135_C4', 'L_136_C3',
    'L_137_C1', 'L_138_C1', 'L_139_C6', 'L_140_C3', 'L_141_C5', 'L_142_C5', 'L_143_C2', 'L_144_C4', 'L_145_C2',
    'L_146_C5', 'L_147_C1', 'L_148_C6', 'L_149_C5', 'L_150_C6', 'L_151_C6', 'L_152_C5', 'L_153_C5', 'L_154_C3',
    'L_155_C4', 'L_156_C4', 'L_157_C2', 'L_158_C4', 'L_159_C5', 'L_160_C1', 'L_161_C6', 'L_162_C5', 'L_163_C1',
    'L_164_C5', 'L_165_C4', 'L_166_C4', 'L_167_C4', 'L_168_C2', 'L_169_C2', 'L_170_C5', 'L_171_C3', 'L_172_C1',
    'L_173_C1', 'L_174_C2', 'L_175_C1', 'L_176_C1', 'L_177_C3', 'L_178_C6', 'L_179_C4', 'L_180_C2', 'L_181_C4',
    'L_182_C2', 'L_183_C5', 'L_184_C1', 'L_185_C6', 'L_186_C5', 'L_187_C2', 'L_188_C2', 'L_189_C4', 'L_190_C5',
    'L_191_C1', 'L_192_C1', 'L_193_C6', 'L_194_C4', 'L_195_C5', 'L_196_C2', 'L_197_C1', 'L_198_C3', 'L_199_C5',
    'L_200_C5', 'L_201_C1', 'L_202_C3', 'L_203_C3', 'L_204_C2', 'L_205_C2', 'L_206_C3', 'L_207_C5', 'L_208_C2',
    'L_209_C5', 'L_210_C4', 'L_211_C5', 'L_212_C5', 'L_213_C4', 'L_214_C1', 'L_215_C6', 'L_216_C2', 'L_217_C3',
    'L_218_C4', 'L_219_C4', 'L_220_C4', 'L_221_C6', 'L_222_C6', 'L_223_C2', 'L_224_C2', 'L_225_C4', 'L_226_C2',
    'L_227_C3', 'L_228_C2', 'L_229_C2', 'L_230_C5', 'L_231_C3', 'L_232_C5', 'L_233_C5', 'L_234_C1', 'L_235_C2',
    'L_236_C4', 'L_237_C3', 'L_238_C5', 'L_239_C5', 'L_240_C3', 'L_241_C4', 'L_242_C4', 'L_243_C1', 'L_244_C5',
    'L_245_C5', 'L_246_C1', 'L_247_C6', 'L_248_C1', 'L_249_C4', 'L_250_C3', 'L_251_C6', 'L_252_C6', 'L_253_C6',
    'L_254_C3', 'L_255_C5', 'L_256_C1', 'L_257_C3', 'L_258_C2', 'L_259_C2', 'L_260_C3', 'L_261_C5', 'L_262_C2',
    'L_263_C6', 'L_264_C1', 'L_265_C6', 'L_266_C6', 'L_267_C3', 'L_268_C1', 'L_269_C3', 'L_270_C4', 'L_271_C2',
    'L_272_C1', 'L_273_C6', 'L_274_C1', 'L_275_C4', 'L_276_C1', 'L_277_C3', 'L_278_C5', 'L_279_C4', 'L_280_C2',
    'L_281_C1', 'L_282_C6', 'L_283_C4', 'L_284_C3', 'L_285_C6', 'L_286_C2', 'L_287_C5', 'L_288_C6', 'L_289_C5',
    'L_290_C6'
]
T = list(range(1, 151)) # Periodos
Cepas = ["C1", "C2", "C3", "C4", "C5", "C6"]

calidades = {'C1': [0.85, 0.95], 'C2': [0.92, 0.93], 'C3': [0.91, 0.87], 'C4': [0.95, 0.95], 'C5': [0.85, 0.85],
             'C6': [0.93, 0.94]}

Dl = [6674412, 16173750, 12480000, 12592500, 14337206, 2002133]



# Parámetros
r = {} #riesgo por lote
requerimientos = {} #requerimientos por cepa
kg = {} #kilogramos por lote
d_optimo = {} #dia optimo por lote
lote_cepa = {} #cepa de cada lote
umbral = {} #umbral de cada lote
umbrales = {
    "C1": 0.8,
    "C2": 0.75,
    "C3": 0.8,
    "C4": 0.7,
    "C5": 0.8,
    "C6": 0.7
} #definido solo para asignar umbral por lote

for l, lote_info in enumerate(lotes_finales_ordenados, start=1):
    kg[l] = lote_info[3]*1000 #Kilogramos de uva por lote
    d_optimo = lote_info[4] #dia optimo de cosecha por lote
    r[l] = lote_info[9] #riesgo por lote
    #c[l] = lote_info[7] #costo por kg
    #q_expec[l] = lote_info[14]
    lote_cepa[l] = lote_info[2] #cepa de cada lote
    umbral[l] = umbrales[lote_info[2]] #umbral industrializacion de cada lote

indice = 0
for cepa in Cepas:
    requerimientos[cepa] = Requerimientos[indice]
    indice += 1



q_lt = {} # Calidad del lote l en el periodo t
M = 1 #parametro grande considernado

#Actualizar los dias optimos de cada lote incluyendo variabilidad

def dia_estimado():
    optimal_day = np.random.normal(0, 2)
    return int(round(optimal_day))

for clave, valor in d_l.items():
    d_l[clave] = valor + dia_estimado()


def obtener_coeficientes(tipo_uva):
    q_t_minus = calidades[tipo_uva][0]
    q_t_plus = calidades[tipo_uva][1]
    t_minus = -7
    t_plus = 7
    A = np.array([
        [t_minus ** 2, t_minus, 1],
        [0, 0, 1],
        [t_plus ** 2, t_plus, 1]])
    b = np.array([q_t_minus, 1, q_t_plus])
    coefficients = np.linalg.solve(A, b)
    a, b, c = coefficients
    return a, b, c


def funcion_cuadratica_calidad(tipo_uva, t,l):
    a, b, c = obtener_coeficientes(tipo_uva)
    x = a * t ** 2 + b * t + c
    calidad = max(min(x*lotes_finales_ordenados[l][12], 1),0)
    return calidad


for l in range(0,len(L)):
    tipo_uva = L[l][(len(L[l]) - 2):len(L[l])]
    tipo_uva_con_comillas = "'" + tipo_uva + "'"
    for t in T:
        if (d_l[L[l]] - 7) <= t <= (d_l[L[l]]) + 7:
            calidad_dia_final = funcion_cuadratica_calidad(tipo_uva, (t - (d_l[L[l]])), l)
            q_lt[L[l], t] = calidad_dia_final
        else:
            q_lt[L[l], t] = 0


# Variables de Decisión
x_lt = m.addVars(L, T, vtype=GRB.BINARY, name="x")
y_lt = m.addVars(L, T, vtype=GRB.BINARY, name="x")
xd_lt = m.addVars(L, T, vtype=GRB.BINARY, name="xd")
z_lt = m.addVars(L,T, vtype=GRB.BINARY, name="z")
dc_l = m.addVars(L, vtype=GRB.CONTINUOUS, name="dc")
w_ct = m.addVars(C, T, vtype=GRB.CONTINUOUS, name="w")

# Función Objetivo
m.setObjective(sum(q_lt[l, t]*x_lt[l, t] - M*riesgo_l[l]  for l in L for t in T), GRB.MAXIMIZE)

# Restricciones
for l in S:
    #Aviso de cosecha para los lotes de tipo forward (que aviso se emita dos dias antes)
    m.addConstr(d_l[l] - dc_l[l] == 2, name=f"restr1_{l}")

for l in F:
    #Aviso de cosecha para los lotes de tipo spot (aviso tiene que ser 5 dias antes)
    m.addConstr(d_l[l] - dc_l[l] >= 5, name=f"restr2_{l}")

for l in L:
    #Sumatoria a lo largo de los periodos que dice que un lote debe ser enviado a la planta o debe ser desechado
    m.addConstr(sum(x_lt[l, t] + xd_lt[l, t] for t in T) == 1, name=f"restr3_{l}")

for f in C:
    for t in T:
        m.addConstr(sum(z_lt[l, t] * r_cl[f,l] for c, l in r_cl if l in L and  c == f) == w_ct[f, t], name=f"restr5_{f}_{t}")

for f in C:
    m.addConstr(sum(z_lt[l, t] * r_cl[f,l]  for c, l in r_cl if l in L and  c == f for t in T) >= d_c[f], name=f"restr6_{f}")

# Agrega restricciones para calcular la calidad en función del día de cosecha --------
#----------------------------------

for l in L:
    for t in T:
        m.addConstr(0 <= (q_lt[l, t] - u_l[l])* z_lt[l,t])

# Suponiendo que 'm' es el modelo de Gurobi
for l in L:
    for t in T:
        m.addConstr(y_lt[l, t] <= x_lt[l, t], name=f"Restriction_y_x_{l}_{t}")

for l in L:
    m.addConstr(sum(z_lt[l,t] for t in T) <= 1, name=f"restr3_{l}")


# Suponiendo que 'm' es el modelo de Gurobi
for l in L:
    for t in T:
        m.addConstr(y_lt[l, t] >= z_lt[l,t], name=f"Restriction_y_z_{l}_{t}")

# Suponiendo que 'm' es el modelo de Gurobi
for l in L:
    for t in T:
        m.addConstr(y_lt[l, t] >= x_lt[l, t] + z_lt[l,t] - 1, name=f"Restriction_y_x_z_{l}_{t}")

# Resolver el modelo
m.optimize()

# Imprimir solución (esto es opcional)
if m.status == GRB.OPTIMAL:
    for l in L:
        for t in T:
            if x_lt[l, t].x == 1:
                Conjunto_final[f"x_{l}"] = t
                print(f"x_{l}_{t}:", x_lt[l, t].x, f"Cosechado el dia", t , f" Cantidad de kilo del lote, pta no alcanze a definirlo se podria sacar de forma manual desde r_cl")

print(Conjunto_final)



