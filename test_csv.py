import pandas as pd

# Especifica la ruta de tu archivo CSV
file_path = 'data/test/MMLU-Pro_test_historia_del_peru.csv'

# Intenta leer el archivo CSV especificando la codificación 'latin1'
try:
    df = pd.read_csv(file_path, encoding='latin1')
    print(df.head())  # Muestra las primeras filas del DataFrame para verificar que se ha leído correctamente
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")

# Si df no está definido debido a un error de lectura, salir del script
if 'df' not in locals():
    print("Error: No se pudo leer el archivo CSV.")
    exit()

# Función para limpiar texto decodificándolo correctamente
def clean_text(text):
    try:
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text

# Aplicar la limpieza a todas las columnas de texto
for column in df.select_dtypes(include=['object']).columns:
    df[column] = df[column].apply(clean_text)

print(df.head())  # Verifica que los datos se han limpiado correctamente