import json
import os

from pelicula import mostrar_peliculas, seleccionar_pelicula
from sala import (mostrar_salas, buscar_sala_por_id, seleccionar_sala, 
                  pedir_cantidad_asientos, seleccionar_multiples_asientos,
                  marcar_asientos_ocupados, asientos_a_codigo)
from reserva import mostrar_reservas
from ticket import mostrar_tickets
from descuento import mostrar_descuentos
from dataclasses import dataclass
from descuento import aplicar_descuento
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

def proceso_reserva(dbFilms):
    """
    Proceso completo de reserva: película -> sala -> asiento
    """
    # 1. Seleccionar película
    pelicula_seleccionada = seleccionar_pelicula(dbFilms['peliculas'])
    if not pelicula_seleccionada:
        return
    
    # 2. Seleccionar sala (que ya incluye horario y precio)
    sala_info = seleccionar_sala(pelicula_seleccionada)
    if not sala_info:
        return
    
    # 3. Buscar la sala completa con los asientos
    sala_completa = buscar_sala_por_id(dbFilms['salas'], sala_info['salaId'])
    if not sala_completa:
        print("❌ Error: No se encontró la sala.")
        return
        
    # 4. Preguntar cuántas personas van al cine
    cantidad_asientos = pedir_cantidad_asientos(sala_completa)
    if not cantidad_asientos:
        return

    # 5. Seleccionar los asientos (uno por cada persona)
    asientos_seleccionados = seleccionar_multiples_asientos(sala_completa, cantidad_asientos)
    if not asientos_seleccionados:
        return

     # Convertir asientos a códigos legibles (A1, A2, B3, etc.)
    codigos_asientos = asientos_a_codigo(asientos_seleccionados)

    # Calcular precio total
    precio_unitario = sala_info['precio']
    precio_total = precio_unitario * cantidad_asientos

    # Mostrar resumen completo de la reserva
    print("\n" + "="*60)
    print("📋 RESUMEN DE TU RESERVA".center(60))
    print("="*60)
    print(f"🎬 Película:        {pelicula_seleccionada['titulo']}")
    print(f"🎭 Género:          {pelicula_seleccionada['genero']}")
    print(f"⏱️  Duración:        {pelicula_seleccionada['duracion']} minutos")
    print(f"🏢 Sala:            {sala_completa['nombre']}")
    print(f"🕒 Horario:         {sala_info['horario']}")
    print("-"*60)
    print(f"👥 Personas:        {cantidad_asientos}")
    print(f"💺 Asientos:        {', '.join(codigos_asientos)}")
    print("-"*60)
    print(f"💰 Precio/persona:  ${precio_unitario}")
    print(f"💵 TOTAL A PAGAR:   ${precio_total:.2f}")
    print("="*60)
    
    fila, columna = asiento_seleccionado
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    asiento_codigo = f"{filas[fila]}{columna + 1}"

# 5. Preguntar si desea aplicar un descuento
    aplicar = input("\n¿Deseas aplicar un descuento? (s/n): ").strip().lower()
    if aplicar == 's':
     descuento_aplicado, precio_final = aplicar_descuento(dbFilms.descuentos, sala_info['precio'])
     if descuento_aplicado:
         print(f"\n✅ Se aplicó el descuento '{descuento_aplicado['name']}' ({descuento_aplicado['descount']}%).")
         print("💡 Recuerda presentar tu comprobante del descuento al ingresar a la sala.")
     else:
         print("\n⚠️ No se aplicó ningún descuento.")
    else:
     precio_final = sala_info['precio']
     descuento_aplicado = None

    print("\n" + "="*50)
    print("📋 RESUMEN DE TU RESERVA".center(50))
    print("="*50)
    print(f"🎬 Película: {pelicula_seleccionada['titulo']}")
    print(f"🏢 Sala: {sala_completa['nombre']}")
    print(f"🕒 Horario: {sala_info['horario']}")
    print(f"💺 Asiento: {asiento_codigo}")
    print(f"💰 Precio: ${precio_final:.2f}")
    print("="*50)
    
    confirmacion = input("\n¿Confirmar reserva? (s/n): ").strip().lower()
    if confirmacion == 's':
        # Marcar todos los asientos como ocupados
        if marcar_asientos_ocupados(sala_completa, asientos_seleccionados):
            print("\n" + "="*60)
            print("✅ ¡RESERVA CONFIRMADA!".center(60))
            print("="*60)
            print(f"🎫 Tus asientos: {', '.join(codigos_asientos)}")
            print(f"💵 Total pagado: ${precio_total:.2f}")
            print(f"🎬 Película: {pelicula_seleccionada['titulo']}")
            print(f"🕒 Horario: {sala_info['horario']}")
            print("\n¡Disfruta tu película! 🍿🎉")
            print("="*60)
        else:
            print("\n❌ Error al confirmar la reserva. Intenta de nuevo.")
    input("\nPresiona ENTER para volver al menú principal...")

# Mostrar el menú
def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*60)
    print("🎬 SISTEMA DE RESERVAS DE CINE 🎬".center(60))
    print("="*60)
    print("1. 🎥 Reservar película")
    print("2. 🎫 Buscar mi ticket")
    print("3. 🎁 Ver descuentos disponibles")
    print("4. 🚪 Salir")
    print("="*60)


def main():
     """Función principal del programa"""
    data = cargar_datos()
    if data is None:
        print("No se pudo cargar el archivo JSON. Saliendo.")
        return

    dbFilms = CineData(**data)  # aquí ya debería funcionar si data es válido
    
    while True:
        mostrar_menu()
        try:
            opcion = int(input("\n➤ Elige una opción (1-4): "))

            if opcion == 1:
                proceso_reserva(dbFilms)
                
            elif opcion == 2:
               print("\n🚧 Función en desarrollo...")
                print("Pronto podrás buscar y ver tus tickets.")
                input("\nPresiona ENTER para continuar...")
               continue
              
            elif opcion == 3:
             mostrar_descuentos(dbFilms.descuentos)
             input("\nPresiona ENTER para continuar...")
            elif opcion == 4:
                print("\n" + "="*60)
                print("¡Gracias por usar el Sistema de Reservas!".center(60))
                print("¡Disfruta tu película! 🎬🍿".center(60))
                print("="*60)
                break 

            else:
                print("❌ Opción no válida. Por favor, elige entre 1 y 4.")
                input("\nPresiona ENTER para continuar...")
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

