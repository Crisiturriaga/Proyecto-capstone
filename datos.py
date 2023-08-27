import pandas as pd

# Cargar el archivo CSV
df = pd.read_csv("datos.csv")

# Lista de tipos de uva
tipos_de_uva = ["C1", "C2", "C3", "C4", "C5", "C6"]

# Crear un DataFrame para almacenar los promedios por tipo de uva
promedios_data = []

# Calcular promedios y agregarlos a la lista
for tipo in tipos_de_uva:
    filtro = df[df["Tipo Uva"] == tipo]
    
    # Seleccionar solo las columnas numéricas para el cálculo del promedio
    columnas_numericas = filtro.select_dtypes(include=[int, float])
    
    # Calcular promedio y agregar el tipo de uva
    promedios = columnas_numericas.mean()
    promedios["Tipo Uva"] = tipo
    
    # Agregar los promedios a la lista
    promedios_data.append(promedios)

# Crear un DataFrame a partir de la lista de promedios
promedios_df = pd.DataFrame(promedios_data)

# Eliminar la columna "Lote Numero" del DataFrame de promedios
promedios_df = promedios_df.drop(columns=["Lote Numero"])

# Reorganizar las columnas para que "Tipo Uva" sea la primera
column_order = ["Tipo Uva"] + [col for col in promedios_df.columns if col != "Tipo Uva"]
promedios_df = promedios_df[column_order]

# Guardar el DataFrame con los promedios en un nuevo archivo CSV
promedios_df.to_csv("promedios_tipo_uva.csv", index=False)

# Crear archivos CSV individuales para cada tipo de uva
for tipo in tipos_de_uva:
    uva_df = df[df["Tipo Uva"] == tipo]
    uva_df.to_csv(f"uva_tipo_{tipo}.csv", index=False)
