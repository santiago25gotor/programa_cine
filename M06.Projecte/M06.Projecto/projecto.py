import json
import os

archivo_path = 'dbFilms.json'

# Verificar si el archivo existe
if os.path.exists(archivo_path):
    print(f"El archivo '{archivo_path}' fue encontrado.")
    # Intentar abrir y cargar el JSON
    try:
        with open(archivo_path, 'r', encoding='utf-8') as archivo:
            data = json.load(archivo)
        print("Archivo cargado correctamente.")
        # Podés imprimir algo para chequear el contenido
        print(f"Cantidad de elementos en el JSON: {len(data)}")
    except json.JSONDecodeError:
        print("Error: El archivo no es un JSON válido.")
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
else:
    print(f"Error: El archivo '{archivo_path}' NO fue encontrado.")



# Recorrer el contenido
##for persona in datos:
  ##  print(f"Nombre: {persona['nombre']}, Edad: {persona['edad']}")

# Mostrar el menú
def mostrar_menu():
    print("\n--- Menú del Gestor de Cine ---")
    print("1. Buscar peliculas")
    print("2. Buscar mi ticket")
    print("3. Descuentos")
    print("4. Salir")


def buscar_pelicula():
# Recorrer e imprimir títulos y horarios
    for pelicula in data["peliculas"]:
     print(f"Título: {pelicula['titulo']}")
     print("Horarios:")
     for sala in pelicula["salas"]:
        print(f"  Sala {sala['salaId']}: {sala['horario']}")
        print("-" * 30)

def buscar_descuentos():

    for descuento in data["descuentos"]:
        print(f"Nombre: {descuento['name']}")
        print(f"Descripcion:  {descuento['description']}")
        print(f"Descuento:  {descuento['descount']}")


while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción (1-4): "))

            if opcion == 1:
              buscar_pelicula()  
            elif opcion == 2:
               # quitar_producto() 
               continue
              
            elif opcion == 3:
                buscar_descuentos()
            elif opcion == 4:
                print("¡Gracias por usar el gestor de compras! Hasta pronto.")
                break 

            else:
                print("Opción no válida. Por favor, elige una opción entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Por favor, elige una opción numérica.")

