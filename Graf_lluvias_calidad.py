import matplotlib.pyplot as plt

# Definir las penalizaciones
penalizaciones_c1_c3_c5 = [0.03, 0.02, 0.01, 0.005]
penalizaciones_c2 = [0.025, 0.012, 0.004, 0.002]
penalizaciones_c4 = [0.025, 0.012, 0.01, 0.002]
penalizaciones_c6 = [0.025, 0.012, 0.004, 0.002]

# Crear una lista de porcentajes de lluvia de 0 a 1 (puedes ajustar el rango según tus necesidades)
porcentaje_lluvia = [i/100 for i in range(101)]  # 0% a 100%

# Calcular la calidad para cada porcentaje de lluvia usando la fórmula dada
calidad = [(1 - penalizaciones_c1_c3_c5[0] * p) *
           (1 - penalizaciones_c1_c3_c5[1] * p) *
           (1 - penalizaciones_c1_c3_c5[2] * p) *
           (1 - penalizaciones_c1_c3_c5[3] * p) * 
           (1 - penalizaciones_c1_c3_c5[3] * p) *
           (1 - penalizaciones_c1_c3_c5[3] * p) *
           (1 - penalizaciones_c1_c3_c5[3] * p) *
           (1 - penalizaciones_c1_c3_c5[3] * p)
             for p in porcentaje_lluvia]

calidad_c2 = [(1 - penalizaciones_c2[0] * p) *
           (1 - penalizaciones_c2[1] * p) *
           (1 - penalizaciones_c2[2] * p) *
           (1 - penalizaciones_c2[3] * p) * 
           (1 - penalizaciones_c2[3] * p) *
           (1 - penalizaciones_c2[3] * p) *
           (1 - penalizaciones_c2[3] * p) *
           (1 - penalizaciones_c2[3] * p)
             for p in porcentaje_lluvia]


calidad_c4 = [(1 - penalizaciones_c4[0] * p) *
           (1 - penalizaciones_c4[1] * p) *
           (1 - penalizaciones_c4[2] * p) *
           (1 - penalizaciones_c4[3] * p) * 
           (1 - penalizaciones_c4[3] * p) *
           (1 - penalizaciones_c4[3] * p) *
           (1 - penalizaciones_c4[3] * p) *
           (1 - penalizaciones_c4[3] * p)
             for p in porcentaje_lluvia]


calidad_c6 = [(1 - penalizaciones_c6[0] * p) *
           (1 - penalizaciones_c6[1] * p) *
           (1 - penalizaciones_c6[2] * p) *
           (1 - penalizaciones_c6[3] * p) * 
           (1 - penalizaciones_c6[3] * p) *
           (1 - penalizaciones_c6[3] * p) *
           (1 - penalizaciones_c6[3] * p) *
           (1 - penalizaciones_c6[3] * p)
             for p in porcentaje_lluvia]

# Crear el gráfico de porcentaje de lluvia vs. calidad
plt.figure(figsize=(10, 6))
plt.plot(porcentaje_lluvia, calidad, label='Calidad')
plt.xlabel('Porcentaje de Lluvia')
plt.ylabel('Ponderador de calidad')
plt.title('Porcentaje de Lluvia vs. Calidad cepa C1, C3 y C5')
plt.legend()
plt.grid(True)

plt.savefig('grafico_calidad_c1_c3_c5.png')


plt.close()

plt.figure(figsize=(10, 6))
plt.plot(porcentaje_lluvia, calidad_c2, label='Calidad')
plt.xlabel('Porcentaje de Lluvia')
plt.ylabel('Ponderador de calidad')
plt.title('Porcentaje de Lluvia vs. Calidad cepa C2')
plt.legend()
plt.grid(True)

plt.savefig('grafico_calidad_c2.png')

plt.close()

plt.figure(figsize=(10, 6))
plt.plot(porcentaje_lluvia, calidad_c4, label='Calidad')
plt.xlabel('Porcentaje de Lluvia')
plt.ylabel('Ponderador de calidad')
plt.title('Porcentaje de Lluvia vs. Calidad cepa C4')
plt.legend()
plt.grid(True)

plt.savefig('grafico_calidad_c4.png')

plt.close()

plt.figure(figsize=(10, 6))
plt.plot(porcentaje_lluvia, calidad_c6, label='Calidad')
plt.xlabel('Porcentaje de Lluvia')
plt.ylabel('Ponderador de calidad')
plt.title('Porcentaje de Lluvia vs. Calidad cepa C6')
plt.legend()
plt.grid(True)

plt.savefig('grafico_calidad_c6.png')

plt.close()