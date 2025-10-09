import json
import os

from pelicula import mostrar_peliculas
from sala import mostrar_salas
from reserva import mostrar_reservas
from ticket import mostrar_tickets
from descuento import mostrar_descuentos
from dataclasses import dataclass
from typing import List

@dataclass
class SalaHorario:
    salaId: int
    horario: str

@dataclass
class Pelicula:
    id: int
    titulo: str
    duracion: int
    genero: str
    salas: List[SalaHorario]

@dataclass
class Sala:
    id: int
    nombre: str
    asientos: List[List[int]]

@dataclass
class Reserva:
    id: str
    idUser: str
    timeStamp: str
    sala: int
    asiento: str
    pelicula: str
    formato: str

@dataclass
class PrecioEntrada:
    idEntrada: int
    precio: float

@dataclass
class Ticket:
    id: str
    idUser: str
    timeStamp: str
    precio: List[PrecioEntrada]
    pretioTotal: float
    descuento: str
    tipoDescuento: str
    formato: str

@dataclass
class Descuento:
    id: str
    name: str
    description: str
    descount: str

@dataclass
class CineData:
    peliculas: List[Pelicula]
    salas: List[Sala]
    reserva: List[Reserva]
    ticket: List[Ticket]
    descuentos: List[Descuento]


def cargar_datos():
    filename = "dbFilms.json" 
    if os.path.isfile(filename):
        print(f"El archivo '{filename}' fue encontrado.")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("Archivo cargado correctamente.")
        print(f"Cantidad de elementos en el JSON: {len(data)}")
        return data
    else:
        print(f"Error: El archivo '{filename}' NO fue encontrado.")
        return None


# Mostrar el menú
def mostrar_menu():
    print("\n--- Menú del Gestor de Cine ---")
    print("1. Buscar peliculas")
    print("2. Buscar mi ticket")
    print("3. Descuentos")
    print("4. Salir")


def main():
    data = cargar_datos()
    if data is None:
        print("No se pudo cargar el archivo JSON. Saliendo.")
        return

    dbFilms = CineData(**data)  # aquí ya debería funcionar si data es válido
    
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción (1-4): "))

            if opcion == 1:
                mostrar_peliculas(dbFilms.peliculas)
            elif opcion == 2:
               # quitar_producto() 
               continue
              
            elif opcion == 3:
             mostrar_descuentos(dbFilms.descuentos)
            elif opcion == 4:
                print("¡Gracias por usar el gestor de compras! Hasta pronto.")
                break 

            else:
                print("Opción no válida. Por favor, elige una opción entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Por favor, elige una opción numérica.")


'''
    mostrar_peliculas(dbFilms.peliculas)
    mostrar_salas(dbFilms.salas)
    mostrar_reservas(dbFilms.reserva)
    mostrar_tickets(dbFilms.ticket)
    mostrar_descuentos(dbFilms.descuentos)

'''

if __name__ == "__main__":
    main()
