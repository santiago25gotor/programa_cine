import json
import os

from pelicula import seleccionar_pelicula
#24/10/25 - Importar nuevas funciones para sistema de funciones independientes
from sala import (buscar_sala_por_id, seleccionar_sala, 
                  pedir_cantidad_asientos_funcion, seleccionar_multiples_asientos_funcion,
                  marcar_asientos_ocupados_funcion, asientos_a_codigo, guardar_funciones_json)
from reserva import crear_reserva, guardar_reserva_json, proceso_buscar_reserva
from ticket import crear_ticket, guardar_ticket_json, guardar_ticket_csv, mostrar_ticket
from descuento import mostrar_descuentos, aplicar_descuento
from generar_ticket import generar_ticket # 24/10/2025 

# ↓↓↓ Cargar datos desde JSON como diccionarios ↓↓↓
def cargar_datos():
    filename = "dbFilms.json" 
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


# ↓↓↓ Proceso principal de reserva ↓↓↓
def proceso_reserva(dbFilms):
    # 1. Seleccionar película
    pelicula_seleccionada = seleccionar_pelicula(dbFilms['peliculas'])
    if not pelicula_seleccionada:
        return

    #24/10/25 - 2. Seleccionar sala (ahora recibe dbFilms para verificar disponibilidad por función)
    sala_info = seleccionar_sala(pelicula_seleccionada, dbFilms['salas'], dbFilms)
    if not sala_info:
        return

    # 3. Buscar sala completa (plantilla base)
    sala_completa = buscar_sala_por_id(dbFilms['salas'], sala_info['salaId'])
    if not sala_completa:
        print("❌ Error: No se encontró la sala.")
        return

    #24/10/25 - 4. Pedir asientos para la función específica
    cantidad_asientos = pedir_cantidad_asientos_funcion(
        dbFilms, pelicula_seleccionada['id'], sala_info['salaId'], sala_info['horario']
    )
    if cantidad_asientos is None:
        return

    #24/10/25 - 5. Seleccionar asientos de la función específica
    asientos_seleccionados = seleccionar_multiples_asientos_funcion(
        dbFilms, pelicula_seleccionada['id'], sala_completa, sala_info['horario'], cantidad_asientos
    )
    if not asientos_seleccionados:
        return
    
    # Convertir asientos a códigos legibles (A1, A2, B3, etc.)
    codigos_asientos = asientos_a_codigo(asientos_seleccionados)
    

    # 6. Aplicar descuento si se desea
    aplicar = input("\n¿Deseas aplicar un descuento? (s/n): ").strip().lower()
    if aplicar == 's':
        descuento_aplicado, precio_final = aplicar_descuento(dbFilms['descuentos'], sala_info['precio'])
        if descuento_aplicado:
            print(f"\n✅ Se aplicó el descuento '{descuento_aplicado['name']}' ({descuento_aplicado['descount']}%).")
            print("💡 Recuerda presentar tu comprobante del descuento al ingresar a la sala.")
        else:
            print("\n⚠️ No se aplicó ningún descuento.")
    else:
        precio_final = sala_info['precio']
        descuento_aplicado = None

    # Calcular precio total
    precio_total = precio_final * cantidad_asientos

    # 7. Mostrar resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE TU RESERVA".center(50))
    print("=" * 50)
    print(f"🎬 Película: {pelicula_seleccionada['titulo']}")
    print(f"🏢 Sala: {sala_completa['nombre']}")
    print(f"🕒 Horario: {sala_info['horario']}")
    print("-"*60)
    print(f"👥 Personas:        {cantidad_asientos}")
    print("-"*60)
    print(f"💰 Precio/persona:  ${precio_final}")
    print(f"💵 TOTAL A PAGAR:   ${precio_total:.2f}")
    print("=" * 50)

    confirmacion = input("\n¿Confirmar reserva? (s/n): ").strip().lower()
    if confirmacion == 's':
        # Pedir nombre del usuario
        nombre_usuario = input("\n👤 Por favor, ingresa tu nombre: ").strip()
        if not nombre_usuario:
            nombre_usuario = "Usuario"
        
        #24/10/25 - Marcar asientos en la función específica
        if marcar_asientos_ocupados_funcion(
            dbFilms, pelicula_seleccionada['id'], sala_info['salaId'], 
            sala_info['horario'], asientos_seleccionados
        ):
            
            # CREAR Y GUARDAR LA RESERVA
            reserva = crear_reserva(
                idUser=nombre_usuario,
                sala=sala_info['salaId'],
                asientos=codigos_asientos,
                pelicula=pelicula_seleccionada['titulo'],
            )
            
            # CREAR Y GUARDAR EL TICKET
            ticket = crear_ticket(
                idUser = nombre_usuario,
                pelicula = pelicula_seleccionada['titulo'],
                sala = sala_info['salaId'],
                asientos = codigos_asientos,
                horario = sala_info['horario'],
                precio_unitario = precio_final,
                cantidad_asientos = cantidad_asientos,
                descuento = descuento_aplicado
            )
            
            #24/10/25 - Guardar todo en el JSON (incluyendo funciones)
            guardar_funciones_json(dbFilms)
            guardar_reserva_json(reserva, dbFilms)
            guardar_ticket_json(ticket, dbFilms)
            guardar_ticket_csv(ticket)
            
            # MOSTRAR CONFIRMACIÓN CON ID DE RESERVA
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
            
            generar_ticket(reserva, descuento_aplicado)
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


# ↓↓↓ Menú principal ↓↓↓
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

    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción (1-4): "))

            if opcion == 1:
                proceso_reserva(data)

            elif opcion == 2:
                # Búsqueda de reservas por ID
                proceso_buscar_reserva(data)

            elif opcion == 3:
                mostrar_descuentos(data['descuentos'])

            elif opcion == 4:
                print("¡Gracias por usar el gestor de compras! Hasta pronto.")
                break

            else:
                print("Opción no válida. Por favor, elige una opción entre 1 y 4.")
        except ValueError:
            print("Entrada inválida. Por favor, elige una opción numérica.")


if __name__ == "__main__":
    main()