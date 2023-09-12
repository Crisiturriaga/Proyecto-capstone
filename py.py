uso_plantas = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
litros_vino = 218274972
tanques_utilizar = 8

def uso_tanques(tanques_utilizar):
    stop = False
    while tanques_utilizar == 0 or stop == True:
        if uso_plantas[1][0] < 24:
            uso_plantas[1][0] += 1
            tanques_utilizar -= 1
        elif uso_plantas[0][0] < 24:
            uso_plantas[0][0] += 1
            tanques_utilizar -= 1
        elif uso_plantas[1][1] < 24:
            uso_plantas[1][1] += 1
            tanques_utilizar -= 1
        elif uso_plantas[1][2] < 24:
            uso_plantas[1][2] += 1
            tanques_utilizar -= 1
        elif uso_plantas[2][0] < 24:
            uso_plantas[2][0] += 1
            tanques_utilizar -= 1
        elif uso_plantas[0][1] < 24:
            uso_plantas[0][1] += 1
            tanques_utilizar -= 1
        elif uso_plantas[0][2] < 24:
            uso_plantas[0][2] += 1
            tanques_utilizar -= 1
        elif uso_plantas[2][1] < 24:
            uso_plantas[2][1] += 1
            tanques_utilizar -= 1
        elif uso_plantas[2][2] < 24:
            uso_plantas[2][2] += 1
            tanques_utilizar -= 1
        else:
            stop == True
            return tanques_utilizar

def sacar_tanques(lista, t):
    indices_a_eliminar = []

    for i, iteracion in enumerate(lista):
        if t == iteracion[1]:
            indices_a_eliminar.append(i)
            tanques_utilizar = iteracion[0]
            #eliminar_tanques(tanques_utilizar)

    # Eliminar sublistas en orden inverso para evitar problemas con los índices
    for index in reversed(indices_a_eliminar):
        lista.pop(index)

    return lista

# Ejemplo de uso
mi_lista = [[1, 10], [2, 11], [3, 10], [4, 12]]
t_valor = 10
mi_lista_resultante = sacar_tanques(mi_lista, t_valor)
print("Lista resultante después de eliminar elementos:", mi_lista_resultante)

def conversion_lt_tanque(litros_vino):
    tanques = 0
    while litros_vino >= 25000:
        litros_vino -= 25000
        tanques += 1
    return litros_vino, tanques



def uso_de_tanques():
    # revisa el estado de los tanques y devuelve el tanque que se puede utilizar
    if uso_plantas[1][0] < 24:
        return 1
    elif uso_plantas[0][0] < 24:
        return 2
    elif uso_plantas[1][1] < 24:
        return 3
    elif uso_plantas[1][2] < 24:
        return 4
    elif uso_plantas[2][0] < 24:
        return 5
    elif uso_plantas[0][1] < 24:
        return 6
    elif uso_plantas[0][2] < 24:
        return 7
    elif uso_plantas[2][1] < 24:
        return 8
    elif uso_plantas[2][2] < 24:
        return 9
    else:
        return 0

def utilizar_tanques(disponibilidad, litros_vino):
    # utilliza los tanques y llena a medida que llegan los lotes en orden de menor precio
    while litros_vino > 0:
        if disponibilidad == 1:
            uso_plantas[1][0] += 1
        elif disponibilidad == 2:
            uso_plantas[0][0] += 1
        elif disponibilidad == 3:
            uso_plantas[1][1] += 1
        elif disponibilidad == 4:
            uso_plantas[1][2] += 1
        elif disponibilidad == 5:
            uso_plantas[2][0] += 1
        elif disponibilidad == 6:
            uso_plantas[0][1] += 1
        elif disponibilidad == 7:
            uso_plantas[0][2] += 1
        elif disponibilidad == 8:
            uso_plantas[2][1] += 1
        elif disponibilidad == 9:
            uso_plantas[2][2] += 1
        elif disponibilidad == 0:
            # mantener en espera hasta que se desocupe un tanque
            pass
import numpy as np
import matplotlib.pyplot as plt

# Given points
t_minus_7 = -7
t_plus_7 = 7
q_t_minus_7 = 0.93
q_t_plus_7 = 0.94

# Vertex point
t_vertex = 0
q_vertex = 1

# Set up the equations to solve for coefficients a, b, and c
A = np.array([
    [t_minus_7**2, t_minus_7, 1],
    [t_vertex**2, t_vertex, 1],
    [t_plus_7**2, t_plus_7, 1]
])

b = np.array([q_t_minus_7, q_vertex, q_t_plus_7])

# Solve the equations
coefficients = np.linalg.solve(A, b)
a, b, c = coefficients

# Quality function
def quality_function(t):
    return max(min(a * t**2 + b * t + c, 1), 0)

# Datos de las distribuciones normales
calidades = [[0.85, 0.95],[0.92, 0.93],[0.91, 0.87],[0.95, 0.95],[0.85, 0.85],[0.93, 0.94]]

# Generate data for plotting
t_values = np.linspace(-10, 10, 400)
q_values = [quality_function(t) for t in t_values]

# Plot the function and the normal distributions
plt.plot(t_values, q_values, label='Distribución normal')
plt.scatter([t_minus_7, t_plus_7], [q_t_minus_7, q_t_plus_7], color='red', label='Puntos extremos')

for cal in calidades:
    mean = (cal[0] + cal[1]) / 2
    std = (cal[1] - cal[0]) / 6  # Just an example std, you can adjust this
    t_norm = np.linspace(cal[0] - 0.1, cal[1] + 0.1, 400)
    q_norm = np.exp(-0.5 * ((t_norm - mean) / std)**2)
    plt.plot(t_norm, q_norm, label=f'Normal({mean:.2f}, {std:.2f})')

plt.xlabel('t=Días')
plt.ylabel('q[t]=Calidad del día de cosecha t')
plt.title('Función de calidad C6')
plt.legend()
plt.grid()
plt.show()
