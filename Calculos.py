
litros = [8550000, 7425000, 5850000, 5775000, 10125000, 6950000]

ml_C1 = 8550000 * 1000
ml_C2 = 7425000*1000
ml_C3 = 5850000*1000
ml_C4 = 5775000*1000
ml_C5 = 10125000*1000
ml_C6 = 6950000*1000

cantidad_blend_4 = 0
0.15, 0.15, 0.15, 0.15, 0.1, 0.3

botellas_mercado_C = 11106667
ml_mercado_C = botellas_mercado_C*750

ml_c1_b4 = ml_mercado_C*0.15
ml_c2_b4 = ml_mercado_C*0.15
ml_c3_b4 = ml_mercado_C*0.15
ml_c4_b4 = ml_mercado_C*0.15
ml_c5_b4 = ml_mercado_C*0.1
ml_c6_b4 = ml_mercado_C*0.3

ml_C1 -= ml_c1_b4
ml_C2 -= ml_c2_b4
ml_C3 -= ml_c3_b4
ml_C4 -= ml_c4_b4
ml_C5 -= ml_c5_b4
ml_C6 -= ml_c6_b4

lista = [ml_C1,ml_C2,ml_C3,ml_C4,ml_C5,ml_C6]
lista_final = []
for a in lista:
    b = a/750
    lista_final.append(b)

print (lista_final)
mercado_a = lista_final[4]
mercado_b = lista_final[0]+lista_final[2]
mercado_c = botellas_mercado_C + lista_final[1]
mercado_d = lista_final[3]+lista_final[5]

print (mercado_a)
print (mercado_b)
print (mercado_c)
print (mercado_d)

    






#for a in litros:
    #o = a/0.75
    #print(o)


