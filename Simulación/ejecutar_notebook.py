import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

# Ruta relativa del notebook
notebook_path = 'Simulacion_proyecto.ipynb'
directory_path = os.path.dirname(os.path.abspath(notebook_path))

# Carga el notebook
with open(notebook_path) as f:
    nb = nbformat.read(f, as_version=4)

# Configura el preprocesador para ejecutar el notebook
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

costos_totales_list = []
ingresos_totales_list = []
utilidad_list = []

# Ejecuta el notebook 100 veces
for _ in range(100):
    # Ejecuta el notebook
    ep.preprocess(nb, {'metadata': {'path': directory_path}})
    
    # Recopila los resultados de las variables de interés
    for cell in nb.cells:
        if cell.cell_type == 'code':
            for output in cell.outputs:
                if 'Costos_totales' in output['text']:
                    costos_totales_list.append(float(output['text'].split()[0]))
                if 'ingreso_total' in output['text']:
                    ingresos_totales_list.append(float(output['text'].split()[0]))
                if 'utilidad' in output['text']:
                    utilidad_list.append(float(output['text'].split()[0]))

# Calcula los promedios
promedio_costos = sum(costos_totales_list) / len(costos_totales_list)
promedio_ingresos = sum(ingresos_totales_list) / len(ingresos_totales_list)
promedio_utilidad = sum(utilidad_list) / len(utilidad_list)

print(f"Promedio Costos Totales: {promedio_costos}")
print(f"Promedio Ingresos Totales: {promedio_ingresos}")
print(f"Promedio Utilidad: {promedio_utilidad}")
