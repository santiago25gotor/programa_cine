import json
import os

# Suponemos que estas funciones están definidas en el mismo archivo o correctamente importadas
from pelicula import seleccionar_pelicula
from sala import buscar_sala_por_id, seleccionar_sala, pedir_cantidad_asientos, seleccionar_multiples_asientos
from descuento import mostrar_descuentos, aplicar_descuento

# ↓↓↓ Cargar datos desde JSON como diccionarios ↓↓↓
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


# ↓↓↓ Proceso principal de reserva ↓↓↓
def proceso_reserva(dbFilms):
    # 1. Seleccionar película
    pelicula_seleccionada = seleccionar_pelicula(dbFilms['peliculas'])
    if not pelicula_seleccionada:
        return

    # 2. Seleccionar sala
    sala_info = seleccionar_sala(pelicula_seleccionada, dbFilms['salas'])
    if not sala_info:
        return

    # 3. Buscar sala completa
    sala_completa = buscar_sala_por_id(dbFilms['salas'], sala_info['salaId'])
    if not sala_completa:
        print("❌ Error: No se encontró la sala.")
        return

    # 4. pedir asientos selecionados
    cantidad_asiento = pedir_cantidad_asientos(sala_completa)
    if cantidad_asiento is None:
        return

    seleccionar_multiples_asientos(sala_completa, cantidad_asiento)

    # 5. Aplicar descuento si se desea
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

    # 6. Mostrar resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE TU RESERVA".center(50))
    print("=" * 50)
    print(f"🎬 Película: {pelicula_seleccionada['titulo']}")
    print(f"🏢 Sala: {sala_completa['nombre']}")
    print(f"🕒 Horario: {sala_info['horario']}")
    #print(f"💺 Asiento: {asiento_codigo}")
    print(f"💰 Precio: ${precio_final:.2f}")
    print("=" * 50)

    confirmacion = input("\n¿Confirmar reserva? (s/n): ").strip().lower()
    if confirmacion == 's':
        print("\n✅ ¡Reserva confirmada! Disfruta tu película 🎉")
    else:
        print("\n❌ Reserva cancelada.")

    input("\nPresiona ENTER para continuar...")


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
                print("Funcionalidad de tickets no implementada aún.")
                continue

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
