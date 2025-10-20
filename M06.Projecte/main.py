import json
import os

from pelicula import mostrar_peliculas, seleccionar_pelicula
from sala import (mostrar_salas, buscar_sala_por_id, seleccionar_sala, 
                  pedir_cantidad_asientos, seleccionar_multiples_asientos,
                  marcar_asientos_ocupados, asientos_a_codigo)
from reserva import mostrar_reservas
from ticket import mostrar_tickets
from descuento import mostrar_descuentos


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
    Proceso completo de reserva: película -> sala -> cantidad personas -> asientos
    """
    # 1. Seleccionar película
    pelicula_seleccionada = seleccionar_pelicula(dbFilms['peliculas'])
    if not pelicula_seleccionada:
        return
    
    # 2. Seleccionar sala y horario
    sala_info = seleccionar_sala(pelicula_seleccionada, dbFilms['salas'])
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
    else:
        print("\n❌ Reserva cancelada. Los asientos no fueron reservados.")
    
    input("\nPresiona ENTER para volver al menú principal...")


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
    
    print("\n" + "="*60)
    print("¡Bienvenido al Sistema de Reservas de Cine! 🎬".center(60))
    print("="*60)
    input("\nPresiona ENTER para continuar...")
    
    while True:
        mostrar_menu()
        try:
            opcion = int(input("\n➤ Elige una opción (1-4): "))

            if opcion == 1:
                proceso_reserva(data)
                
            elif opcion == 2:
                print("\n🚧 Función en desarrollo...")
                print("Pronto podrás buscar y ver tus tickets.")
                input("\nPresiona ENTER para continuar...")
              
            elif opcion == 3:
                mostrar_descuentos(data['descuentos'])
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
            print("❌ Entrada inválida. Por favor, ingresa un número.")
            input("\nPresiona ENTER para continuar...")
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido. ¡Hasta pronto!")
            break


if __name__ == "__main__":
    main()