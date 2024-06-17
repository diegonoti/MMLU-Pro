import json
import pandas as pd
import random

# Cargar los archivos JSON
with open('data/test/preguntas_historia_del _Peru_10_opciones.json', 'r', encoding='utf-8') as f:
    preguntas_original = json.load(f)

with open('data/test/preguntas_historia_del_peru_10_opciones_actualizado.json', 'r', encoding='utf-8') as f:
    preguntas_actualizadas = json.load(f)

# Unir las preguntas de ambos archivos
todas_preguntas = preguntas_original + preguntas_actualizadas

# Definir la cantidad deseada de preguntas para test y validation
cantidad_test = 83
cantidad_validation = 5

# Asegurarse de que la cantidad total de preguntas coincida con la suma deseada
if len(todas_preguntas) != (cantidad_test + cantidad_validation):
    raise ValueError("La cantidad total de preguntas no coincide con la suma de las cantidades deseadas para test y validation.")

# Barajar las preguntas para una distribución aleatoria
random.shuffle(todas_preguntas)

# Dividir las preguntas en test y validation según la cantidad definida
preguntas_test = todas_preguntas[:cantidad_test]
preguntas_validation = todas_preguntas[cantidad_test:cantidad_test + cantidad_validation]

# Crear DataFrames para test y validation
def crear_dataframe(preguntas):
    data = {
        "question": [p["question"] for p in preguntas],
        "options": ["; ".join(p["options"]) for p in preguntas],
        "answer": [p["answer"] for p in preguntas]
    }
    return pd.DataFrame(data)

df_test = crear_dataframe(preguntas_test)
df_validation = crear_dataframe(preguntas_validation)

# Guardar los DataFrames en archivos CSV
df_test.to_csv('MMLU-Pro_test_historia_del_peru_utf8.csv', index=False, encoding='utf-8')
df_validation.to_csv('MMLU-Pro_validation_historia_del_peru_utf8.csv', index=False, encoding='utf-8')

print(f"Test questions: {df_test.shape[0]}, Validation questions: {df_validation.shape[0]}")
