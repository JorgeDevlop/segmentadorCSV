import pandas as pd
from pathlib import Path
from slugify import slugify
from tqdm import tqdm

# Configuración inicial
file_path = Path('Spotify_Song_Attributes.csv')
output_dir = Path('generos')  # Carpeta base de salida

# Manejo de errores al leer el archivo
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: El archivo {file_path} no fue encontrado.")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: El archivo CSV está vacío.")
    exit(1)

# Validación de que exista la columna 'genre'
if 'genre' not in df.columns:
    raise ValueError("Error: La columna 'genre' no existe en el archivo CSV.")

# Limpieza de valores no válidos en la columna 'genre'
df['genre'] = df['genre'].fillna('unknown').astype(str)

# Advertencia si la columna está vacía
if df['genre'].nunique() == 1 and df['genre'].iloc[0] == 'unknown':
    print("Advertencia: Todos los valores en la columna 'genre' están vacíos.")
    exit(1)

# Crear directorios y guardar archivos
for genero, genero_df in tqdm(df.groupby('genre'), desc="Procesando géneros"):
    dir_path = output_dir / slugify(genero)
    dir_path.mkdir(parents=True, exist_ok=True)
    try:
        genero_df.to_csv(dir_path / f'Spotify_Song_Attributes_{slugify(genero)}.csv', index=False)
    except Exception as e:
        print(f"Error al guardar el archivo para el género {genero}: {e}")

print('Proceso terminado.')
