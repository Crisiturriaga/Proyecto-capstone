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
            eliminar_tanques(tanques_utilizar)

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
