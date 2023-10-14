
import matplotlib.pyplot as plt
import numpy as np

# Valores de los porcentajes
porcentajes = [6, 5, 4, 3, 2, 1, 0]

# Valores de las variables "con" en millones
valores_con = [x / 1000000 for x in [144928853.588, 144689136.087, 144117577.412, 144085999.863, 144035926.703, 143930722.575, 144008822.709]]

# Crear el gráfico
plt.plot(porcentajes, valores_con, marker='o', linestyle='-', color='b')
plt.title('Costos en funcion de porcentaje de compra spot')
plt.xlabel('Porcentaje de compra spot')
plt.ylabel('Costos (en millones)')
plt.grid(True)

plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}M'))

# Guardar el gráfico en un archivo (por ejemplo, en formato PNG)
plt.savefig('grafico_porcentajes_spot_costo')

# Mostrar el gráfico (opcional)
plt.show()
