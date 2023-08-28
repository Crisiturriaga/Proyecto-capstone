import sqlite3

# Crear una conexión a la base de datos
conn = sqlite3.connect('vinos.db')
c = conn.cursor()

# Simulación de toma de decisiones y restricciones
def simular():
    c.execute('SELECT * FROM lotes')
    lotes = c.fetchall()
    
    for lote in lotes:
        lote_id = lote[0]
        lote_codigo = lote[1]
        lote_numero = lote[2]
        lote_tipo_uva = lote[3]
        lote_toneladas = lote[4]
        lote_dia_optimo = lote[5]
        lote_prob_seco_lluvia = lote[6]
        lote_prob_lluvia_lluvia = lote[7]
        lote_precio_usd = lote[8]

        
        

# Ejecutar la simulación
simular()

# Cerrar la conexión a la base de datos
conn.close()
