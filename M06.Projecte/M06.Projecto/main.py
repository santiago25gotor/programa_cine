import json
import os

from pelicula import mostrar_peliculas, seleccionar_pelicula
from sala import (mostrar_salas, buscar_sala_por_id, seleccionar_sala, 
                  seleccionar_asiento, marcar_asiento_ocupado)
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
    """Carga los datos del archivo JSON"""
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


def guardar_datos(data):
    """Guarda los datos actualizados en el archivo JSON"""
    filename = "dbFilms.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("✅ Datos guardados correctamente en el archivo.")
        return True
    except Exception as e:
        print(f"❌ Error al guardar los datos: {e}")
        return False


def convertir_dbfilms_a_dict(dbFilms):
    """Convierte el objeto CineData de vuelta a diccionario para guardar en JSON"""
    return {
        "peliculas": dbFilms.peliculas,
        "salas": dbFilms.salas,
        "reserva": dbFilms.reserva,
        "ticket": dbFilms.ticket,
        "descuentos": dbFilms.descuentos
    }


def proceso_reserva(dbFilms):
    """
    Proceso completo de reserva: película -> sala -> asiento
    Ahora guarda el asiento como ocupado en el archivo JSON
    """
    # 1. Seleccionar película
    pelicula_seleccionada = seleccionar_pelicula(dbFilms.peliculas)
    if not pelicula_seleccionada:
        return
    
    # 2. Seleccionar sala (ahora verifica disponibilidad)
    sala_info = seleccionar_sala(pelicula_seleccionada, dbFilms.salas)
    if not sala_info:
        return
    
    # 3. Buscar la sala completa con los asientos
    sala_completa = buscar_sala_por_id(dbFilms.salas, sala_info['salaId'])
    if not sala_completa:
        print("❌ Error: No se encontró la sala.")
        return
    
    # 4. Seleccionar asiento
    asiento_seleccionado = seleccionar_asiento(sala_completa)
    if not asiento_seleccionado:
        return
    
    fila, columna = asiento_seleccionado
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    asiento_codigo = f"{filas[fila]}{columna + 1}"
    
    # Resumen de la reserva
    print("\n" + "="*50)
    print("📋 RESUMEN DE TU RESERVA".center(50))
    print("="*50)
    print(f"🎬 Película: {pelicula_seleccionada['titulo']}")
    print(f"🏢 Sala: {sala_completa['nombre']}")
    print(f"🕒 Horario: {sala_info['horario']}")
    print(f"💺 Asiento: {asiento_codigo}")
    print(f"💰 Precio: ${sala_info['precio']}")
    print("="*50)
    
    confirmacion = input("\n¿Confirmar reserva? (s/n): ").strip().lower()
    if confirmacion == 's':
        # Marcar el asiento como ocupado
        if marcar_asiento_ocupado(sala_completa, fila, columna):
            print("\n✅ ¡Reserva confirmada! Disfruta tu película 🎉")
            
            # Guardar los cambios en el archivo JSON
            data_actualizada = convertir_dbfilms_a_dict(dbFilms)
            if guardar_datos(data_actualizada):
                print("💾 El asiento ha sido reservado y guardado en el sistema.")
            else:
                print("⚠️ La reserva se realizó pero hubo un problema al guardar.")
        else:
            print("\n❌ Error al marcar el asiento como ocupado.")
    else:
        print("\n❌ Reserva cancelada.")
    
    input("\nPresiona ENTER para continuar...")


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n--- Menú del Gestor de Cine ---")
    print("1. Buscar películas")
    print("2. Buscar mi ticket")
    print("3. Descuentos")
    print("4. Salir")


def main():
    data = cargar_datos()
    if data is None:
        print("No se pudo cargar el archivo JSON. Saliendo.")
        return

    dbFilms = CineData(**data)
    
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción (1-4): "))

            if opcion == 1:
                proceso_reserva(dbFilms)
                
            elif opcion == 2:
                # Aquí puedes implementar la búsqueda de tickets
                mostrar_tickets(dbFilms.ticket)
                input("\nPresiona ENTER para continuar...")
              
            elif opcion == 3:
                mostrar_descuentos(dbFilms.descuentos)
                input("\nPresiona ENTER para continuar...")
                
            elif opcion == 4:
                print("¡Gracias por usar el gestor de cine! Hasta pronto.")
                break 

            else:
                print("Opción no válida. Por favor, elige una opción entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Por favor, elige una opción numérica.")


if __name__ == "__main__":
    main()