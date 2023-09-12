data = [
    ("Blend 1", 1, 0.1, 0.2, 0.0, 0.3, 0.0, 0.4),
    ("Blend 1", 2, 0.0, 0.4, 0.2, 0.2, 0.2, 0.0),
    ("Blend 2", 1, 0.3, 0.2, 0.1, 0.2, 0.0, 0.2),
    ("Blend 2", 2, 0.0, 0.2, 0.2, 0.2, 0.2, 0.2),
    ("Blend 2", 3, 0.2, 0.0, 0.2, 0.0, 0.2, 0.4),
    ("Blend 3", 1, 0.5, 0.0, 0.2, 0.0, 0.1, 0.2),
    ("Blend 4", 1, 0.15, 0.15, 0.15, 0.15, 0.1, 0.3),
    ("Blend 4", 2, 0.12, 0.15, 0.08, 0.1, 0.1, 0.45),
    ("C1", 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0),
    ("C2", 1, 0.0, 1, 0.0, 0.0, 0.0, 0.0),
    ("C3", 1, 0.0, 0.0, 1, 0.0, 0.0, 0.0),
    ("C4", 1, 0.0, 0.0, 0.0, 1, 0.0, 0.0),
    ("C5", 1, 0.0, 0.0, 0.0, 0.0, 1, 0.0),
    ("C6", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 1)
]

data = [
    ("Blend 4", 1, 0.15, 0.15, 0.15, 0.15, 0.1, 0.3),
    ("Blend 4", 2, 0.12, 0.15, 0.08, 0.1, 0.1, 0.45),
    ("C1", 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0),
    ("C2", 1, 0.0, 1, 0.0, 0.0, 0.0, 0.0),
    ("C3", 1, 0.0, 0.0, 1, 0.0, 0.0, 0.0),
    ("C4", 1, 0.0, 0.0, 0.0, 1, 0.0, 0.0),
    ("C5", 1, 0.0, 0.0, 0.0, 0.0, 1, 0.0),
    ("C6", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 1)
]

recipe_dict = {}

for row in data:
    blend = row[0]
    receta = row[1]
    c_values = row[2:]
    if blend not in recipe_dict:
        recipe_dict[blend] = {}
    recipe_dict[blend][receta] = c_values

litros_por_cepa = [8550000, 7425000, 5850000, 5775000, 10125000, 6950000]

botellas_llenas = {key: 0 for key in recipe_dict.keys()}
sobrante_por_cepa = {key: 0 for key in recipe_dict.keys()}

for blend, recetas in recipe_dict.items():
    for receta, c_values in recetas.items():
        botellas = float('inf')
        for i, cepa in enumerate(["C1", "C2", "C3", "C4", "C5", "C6"]):
            if c_values[i] != 0:
                botellas = min(botellas, litros_por_cepa[i] / c_values[i])

        if botellas != float('inf'):
            for i, cepa in enumerate(["C1", "C2", "C3", "C4", "C5", "C6"]):
                litros_usados = botellas * c_values[i]
                litros_por_cepa[i] -= litros_usados
            botellas_llenas[blend] += botellas
            print(f"Llenando {int(botellas)} botellas de '{blend}' con receta '{receta}'")
        else:
            sobrante_por_cepa[blend] = "No hay suficiente capacidad para esta receta"

print("\nSobrante o falta de capacidad por blend:")
for key, value in sobrante_por_cepa.items():
    print(f"{key}: {value}")