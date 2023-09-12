import sqlite3
import csv

# NO CORRER ESTE ARCHIVO DE NUEVO, A MENOS QUE NO EXISTA VINOS.DB

# Crear una conexión a la base de datos (o crearla si no existe)
conn = sqlite3.connect('vinos.db')
c = conn.cursor()

# Crear la tabla 'lotes' en la base de datos
c.execute('''CREATE TABLE IF NOT EXISTS lotes
             (id INTEGER PRIMARY KEY,
              lote_cod TEXT,
              lote_numero INTEGER,
              tipo_uva TEXT,
              tn_lote REAL,
              dia_optimo INTEGER,
              prob_lluvia_seca REAL,
              prob_lluvia_lluvia REAL,
              usd_compra_futuro REAL)''')

# Cargar datos desde el archivo CSV
with open('datos.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Saltar la primera fila de encabezados
    for row in csv_reader:
        lote_cod, lote_numero, tipo_uva, tn_lote, dia_optimo, prob_lluvia_seca, prob_lluvia_lluvia, usd_compra_futuro = row
        c.execute('INSERT INTO lotes (lote_cod, lote_numero, tipo_uva, tn_lote, dia_optimo, prob_lluvia_seca, prob_lluvia_lluvia, usd_compra_futuro) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (lote_cod, int(lote_numero), tipo_uva, float(tn_lote), int(dia_optimo), float(prob_lluvia_seca), float(prob_lluvia_lluvia), float(usd_compra_futuro)))

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión a la base de datos
conn.close()
