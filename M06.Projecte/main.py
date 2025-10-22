import json
import os

from pelicula import mostrar_peliculas, seleccionar_pelicula
from sala import (mostrar_salas, buscar_sala_por_id, seleccionar_sala, 
                  pedir_cantidad_asientos, seleccionar_multiples_asientos,
                  marcar_asientos_ocupados, asientos_a_codigo, guardar_salas_json)
from reserva import mostrar_reservas, crear_reserva, guardar_reserva_json, proceso_buscar_reserva
from ticket import mostrar_tickets, crear_ticket, guardar_ticket_json, guardar_ticket_csv, mostrar_ticket
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


# 22/10/2025 - CORREGIDO: Ahora muestra el ID de reserva claramente
def proceso_reserva(dbFilms):
   
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
        # 22/10/2025 - Pedir nombre del usuario
        nombre_usuario = input("\n👤 Por favor, ingresa tu nombre: ").strip()
        if not nombre_usuario:
            nombre_usuario = "Usuario"
        
        if marcar_asientos_ocupados(sala_completa, asientos_seleccionados):
            
            # 22/10/2025 - CREAR Y GUARDAR LA RESERVA
            reserva = crear_reserva(
                idUser=nombre_usuario,
                sala=sala_info['salaId'],
                asientos=codigos_asientos,
                pelicula=pelicula_seleccionada['titulo'],
                formato="4K"
            )
            
            # 22/10/2025 - CREAR Y GUARDAR EL TICKET
            ticket = crear_ticket(
                idUser=nombre_usuario,
                pelicula=pelicula_seleccionada['titulo'],
                sala=sala_info['salaId'],
                asientos=codigos_asientos,
                horario=sala_info['horario'],
                precio_unitario=precio_unitario,
                cantidad_asientos=cantidad_asientos,
                descuento=None  # Sin descuento por ahora
            )
            
            # 22/10/2025 - Guardar todo en el JSON
            guardar_salas_json(dbFilms['salas'])
            guardar_reserva_json(reserva, dbFilms)
            guardar_ticket_json(ticket, dbFilms)
            guardar_ticket_csv(ticket)
            
            # 22/10/2025 - MOSTRAR CONFIRMACIÓN CON ID DE RESERVA
            print("\n" + "="*60)
            print("✅ ¡RESERVA CONFIRMADA!".center(60))
            print("="*60)
            print()
            print("🎉 Tu reserva ha sido procesada exitosamente")
            print()
            print("📋 INFORMACIÓN IMPORTANTE:")
            print("-"*60)
            print(f"🆔 ID DE RESERVA:  {reserva['id']}")
            print(f"👤 Usuario:        {reserva['idUser']}")
            print(f"🎬 Película:       {reserva['pelicula']}")
            print(f"🏢 Sala:           {reserva['sala']}")
            print(f"🕒 Horario:        {sala_info['horario']}")
            print(f"💺 Asientos:       {reserva['asiento']}")
            print("-"*60)
            print()
            print("⚠️  GUARDA ESTE ID DE RESERVA: " + reserva['id'])
            print("   Lo necesitarás para buscar tu reserva")
            print()
            print("="*60)
            
            # Mostrar el ticket completo
            print("\n")
            mostrar_ticket(ticket)
            
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
    print("2. 🔍 Buscar mi reserva")
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
                # 22/10/2025 - Búsqueda de reservas por ID
                proceso_buscar_reserva(data)
              
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