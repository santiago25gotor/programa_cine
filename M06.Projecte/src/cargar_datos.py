import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

filename = BASE_DIR / ".." / "data" / "dbFilms.json"
dirResultName = BASE_DIR / ".." / "results" / "tickets.csv"

# O si está en la misma carpeta:
# filename = BASE_DIR / "dbFilms.json"

# ↓↓↓ Cargar datos desde JSON como diccionarios ↓↓↓
def cargar_datos():
    if os.path.isfile(filename):
        print(f"El archivo '{filename}' fue encontrado.")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Archivo cargado correctamente.")
        print(f"Cantidad de elementos en el JSON: {len(data)}")
        
        #24/10/25 - Inicializar estructura de funciones si no existe
        if 'funciones' not in data:
            data['funciones'] = {}
            print("✅ Sistema de funciones independientes inicializado")
        
        return data
    else:
        print(f"Error: El archivo '{filename}' NO fue encontrado.")
        return None
    
def leer_ruta():
     if os.path.isfile(filename):
        return filename
     else:
         return 0
     
def leer_ruta_ticket():
     if os.path.isfile(dirResultName):
        return dirResultName
     else:
         return 0