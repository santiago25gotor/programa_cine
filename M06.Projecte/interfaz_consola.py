# interfaz_consola.py
import src


dbFilmsRuta = src.cargar_datos.leer_ruta()
ticketsRuta = src.cargar_datos.leer_ruta_ticket()
class GestorCineConsola:
    def __init__(self):
        self.data = None
        self.gestor = None

    def cargar_datos(self):
        self.data = src.cargar_datos.cargar_datos()
        if self.data is None:
            print("❌ No se pudo cargar el archivo JSON. Saliendo.")
            return False
        self.gestor = GestorCine(self.data, dbFilmsRuta)
        return True

    def mostrar_menu(self):
        print("\n" + "─" * 40)
        print("🎬 GESTOR DE CINE - MENÚ PRINCIPAL".center(40))
        print("─" * 40)
        print("1. 🎥 Reservar entradas")
        print("2. 🔍 Buscar mi ticket")
        print("3. 🎟️  Ver descuentos disponibles")
        print("4. 🚪 Salir")
        print("─" * 40)

    def iniciar(self):
        if not self.cargar_datos():
            return

        while True:
            self.mostrar_menu()
            try:
                opcion = int(input("Elige una opción (1-4): ").strip())

                if opcion == 1:
                    self.gestor.proceso_reserva()
                elif opcion == 2:
                    src.reserva.proceso_buscar_reserva(self.data)
                elif opcion == 3:
                    src.descuento.mostrar_descuentos(self.data['descuentos'])
                elif opcion == 4:
                    print("\n¡Gracias por usar el gestor de cine! 🍿 Hasta pronto.\n")
                    break
                else:
                    print("⚠️ Opción no válida. Elige entre 1 y 4.")
            except ValueError:
                print("⚠️ Entrada inválida. Por favor, ingresa un número.")
            except KeyboardInterrupt:
                print("\n\n👋 Saliendo... ¡Hasta luego!")
                break


class GestorCine:
    def __init__(self, dbFilms, dbFilmsRuta):
        self.dbFilms = dbFilms
        self.dbFilmsRuta = dbFilmsRuta  
    def proceso_reserva(self):
        # 1. Seleccionar película
        pelicula_seleccionada = src.pelicula.seleccionar_pelicula(self.dbFilms['peliculas'])
        if not pelicula_seleccionada:
            return

        # 2. Seleccionar sala
        sala_info = src.sala.seleccionar_sala(pelicula_seleccionada, self.dbFilms['salas'], self.dbFilms)
        if not sala_info:
            return

        # 3. Buscar sala completa
        sala_completa = src.sala.buscar_sala_por_id(self.dbFilms['salas'], sala_info['salaId'])
        if not sala_completa:
            print("❌ Error: No se encontró la sala.")
            return

        # 4. Pedir cantidad de asientos
        cantidad_asientos = src.sala.pedir_cantidad_asientos_funcion(
            self.dbFilms, pelicula_seleccionada['id'], sala_info['salaId'], sala_info['horario']
        )
        if cantidad_asientos is None:
            return

        # 5. Seleccionar asientos
        asientos_seleccionados = src.sala.seleccionar_multiples_asientos_funcion(
            self.dbFilms, pelicula_seleccionada['id'], sala_completa, sala_info['horario'], cantidad_asientos
        )
        if not asientos_seleccionados:
            return

        codigos_asientos = src.sala.asientos_a_codigo(asientos_seleccionados)

        # 6. Aplicar descuento
        aplicar = input("\n¿Deseas aplicar un descuento? (s/n): ").strip().lower()
        if aplicar == 's':
            descuento_aplicado, precio_final = src.descuento.aplicar_descuento(self.dbFilms['descuentos'], sala_info['precio'])
            if descuento_aplicado:
                print(f"\n✅ Descuento aplicado: '{descuento_aplicado['name']}' ({descuento_aplicado['descount']}%)")
                print("💡 Recuerda llevar tu comprobante.")
            else:
                print("\n⚠️ No se aplicó descuento.")
        else:
            precio_final = sala_info['precio']
            descuento_aplicado = None

        precio_total = precio_final * cantidad_asientos

        # 7. Resumen
        print("\n" + "=" * 50)
        print("📋 RESUMEN DE TU RESERVA".center(50))
        print("=" * 50)
        print(f"🎬 Película: {pelicula_seleccionada['titulo']}")
        print(f"🏢 Sala: {sala_completa['nombre']}")
        print(f"🕒 Horario: {sala_info['horario']}")
        print("-" * 60)
        print(f"👥 Personas:        {cantidad_asientos}")
        print("-" * 60)
        print(f"💰 Precio/persona:  ${precio_final}")
        print(f"💵 TOTAL A PAGAR:   ${precio_total:.2f}")
        print("=" * 50)

        confirmacion = input("\n¿Confirmar reserva? (s/n): ").strip().lower()
        if confirmacion != 's':
            print("\n❌ Reserva cancelada.")
            input("\nPresiona ENTER para continuar...")
            return

        nombre_usuario = input("\n👤 Ingresa tu nombre: ").strip() or "Usuario"

        # Marcar asientos
        if not src.sala.marcar_asientos_ocupados_funcion(
            self.dbFilms, pelicula_seleccionada['id'], sala_info['salaId'],
            sala_info['horario'], asientos_seleccionados
        ):
            print("\n❌ Error al reservar asientos.")
            return

        # Crear reserva y ticket
        reserva = src.reserva.crear_reserva(
            idUser=nombre_usuario,
            sala=sala_info['salaId'],
            asientos=codigos_asientos,
            pelicula=pelicula_seleccionada['titulo'],
        )

        ticket = src.ticket.crear_ticket(
            idUser=nombre_usuario,
            pelicula=pelicula_seleccionada['titulo'],
            sala=sala_info['salaId'],
            asientos=codigos_asientos,
            horario=sala_info['horario'],
            precio_unitario=precio_final,
            cantidad_asientos=cantidad_asientos,
            descuento=descuento_aplicado
        )

        # Guardar todo
        src.sala.guardar_funciones_json(self.dbFilms, dbFilmsRuta)
        src.reserva.guardar_reserva_json(reserva, self.dbFilms, dbFilmsRuta)
        src.ticket.guardar_ticket_json(ticket, self.dbFilms, dbFilmsRuta)
        src.ticket.guardar_ticket_csv(ticket, ticketsRuta)

        # Confirmación final
        print("\n" + "="*60)
        print("✅ ¡RESERVA CONFIRMADA!".center(60))
        print("="*60)
        print(f"🆔 ID RESERVA: {reserva['id']}")
        print(f"👤 Usuario: {nombre_usuario}")
        print(f"🎬 Película: {reserva['pelicula']}")
        print(f"💺 Asientos: {', '.join(codigos_asientos)}")
        print(f"🕒 Horario: {sala_info['horario']}")
        print("-"*60)
        print("⚠️ GUARDA ESTE ID PARA BUSCAR TU TICKET")
        print("="*60)

        src.generar_ticket.generar_ticket(reserva, descuento_aplicado, ticketsRuta)
        print("\n")
        src.ticket.mostrar_ticket(ticket)
        print("\n¡Disfruta tu película! 🍿🎉")
        print("="*60)

        input("\nPresiona ENTER para volver al menú...")