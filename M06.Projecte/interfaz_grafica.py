# -*- coding: utf-8 -*-
"""
INSTRUCCIONES DE INSTALACIÓN:

Opción 1 - Instalar Build Tools (más completo):
1. Descargar: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Instalar "Desarrollo para el escritorio con C++"
3. pip install imgui[glfw]
4. pip install PyOpenGL

Opción 2 - Usar Pygame (MÁS FÁCIL para Windows):
pip install pygame
pip install imgui[pygame]
pip install PyOpenGL

Ejecutar: python main_imgui_pygame.py
"""

import pygame
import json
import os
from datetime import datetime

# Importar módulos del proyecto
import src 

# Inicializar Pygame
pygame.init()

# Configuración de ventana
ANCHO_VENTANA = 1800
ALTO_VENTANA = 1000
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Sistema de Reservas de Cine")

# Colores
COLOR_FONDO = (20, 20, 30)
COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (60, 60, 100)
COLOR_BOTON_HOVER = (80, 80, 140)
COLOR_DISPONIBLE = (50, 200, 50)
COLOR_OCUPADO = (200, 50, 50)
COLOR_SELECCIONADO = (50, 100, 220)
COLOR_TITULO = (100, 200, 255)


# ---------------------- FUNCIONES DE LA INTERFAZ ----------------------

def cargar_fuentes():
    fuentes_emoji = ['Segoe UI Emoji', 'Apple Color Emoji', 'Noto Color Emoji', 'Segoe UI Symbol', 'Arial Unicode MS']
    for fuente_nombre in fuentes_emoji:
        try:
            return (
                pygame.font.SysFont(fuente_nombre, 48),
                pygame.font.SysFont(fuente_nombre, 36),
                pygame.font.SysFont(fuente_nombre, 28),
            )
        except:
            continue
    return (pygame.font.Font(None, 48), pygame.font.Font(None, 36), pygame.font.Font(None, 28))

font_grande, font_mediana, font_pequena = cargar_fuentes()

# Variables globales
dbFilms = None
ventana_actual = 0
pelicula_seleccionada = None
sala_seleccionada = None
sala_completa = None
asientos_seleccionados = []
nombre_usuario = ""
descuento_aplicado = None
mensaje_sistema = ""
id_busqueda = ""
reserva_encontrada = None
scroll_offset = 0

cargar_datos = src.cargar_datos.cargar_datos

def resetear_seleccion():
    global pelicula_seleccionada, sala_seleccionada, sala_completa
    global asientos_seleccionados, descuento_aplicado, mensaje_sistema

    pelicula_seleccionada = None
    sala_seleccionada = None
    sala_completa = None
    asientos_seleccionados = []
    descuento_aplicado = None
    mensaje_sistema = ""

class Boton:
    def __init__(self, x, y, ancho, alto, texto, color=COLOR_BOTON):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color = color
        self.hover = False

    def dibujar(self, screen, font=None):
        if font is None:
            font = font_mediana

        color = COLOR_BOTON_HOVER if self.hover else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, COLOR_TEXTO, self.rect, 2, border_radius=10)

        texto_surface = font.render(self.texto, True, COLOR_TEXTO)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        screen.blit(texto_surface, texto_rect)

    def actualizar(self, pos_mouse):
        self.hover = self.rect.collidepoint(pos_mouse)

    def click(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

def dibujar_texto(texto, x, y, font=None, color=COLOR_TEXTO):
    if font is None:
        font = font_mediana

    texto_surface = font.render(texto, True, color)
    screen.blit(texto_surface, (x, y))
    return texto_surface.get_height()

def menu_principal(pos_mouse):
    global ventana_actual

    screen.fill(COLOR_FONDO)

    # Título
    dibujar_texto("🎬 Sistema de Cine", 550, 100, font_grande, COLOR_TITULO)
    dibujar_texto("Menú Principal", 650, 170, font_mediana)

    # Botones
    btn_peliculas = Boton(550, 260, 500, 80, "🎥 Buscar Películas y Reservar")
    btn_ticket = Boton(550, 360, 500, 80, "🎟️ Buscar Mi Ticket")
    btn_descuentos = Boton(550, 460, 500, 80, "💰 Ver Descuentos")
    btn_salir = Boton(550, 560, 500, 80, "❌ Salir")

    botones = [btn_peliculas, btn_ticket, btn_descuentos, btn_salir]

    for btn in botones:
        btn.actualizar(pos_mouse)
        btn.dibujar(screen)

    return botones

def ventana_peliculas_ui(pos_mouse, eventos):
    global ventana_actual, pelicula_seleccionada, sala_seleccionada
    global sala_completa, asientos_seleccionados, nombre_usuario
    global descuento_aplicado, mensaje_sistema, scroll_offset, dbFilms

    screen.fill(COLOR_FONDO)

    # Título
    dibujar_texto("🎬 Reserva de Entradas", 50, 20, font_grande, COLOR_TITULO)

    y_pos = 90
    botones = []

    # Paso 1: Selecciona una Película
    dibujar_texto("Paso 1: Selecciona una Película", 50, y_pos, font_mediana)
    y_pos += 50

    for peli in dbFilms['peliculas']:
        texto = f"{peli['titulo']} ({peli['genero']}, {peli['duracion']} min)"
        btn = Boton(50, y_pos, 600, 55, texto)
        btn.actualizar(pos_mouse)
        btn.dibujar(screen, font_pequena)
        botones.append(('pelicula', btn, peli))
        y_pos += 65

    # Paso 2: Seleccionar sala
    if pelicula_seleccionada:
        y_pos += 20
        dibujar_texto(f"✅ Película: {pelicula_seleccionada['titulo']}", 50, y_pos, font_pequena)
        y_pos += 50
        dibujar_texto("Paso 2: Selecciona Sala y Horario", 50, y_pos, font_mediana)
        y_pos += 50

        for sala_info in pelicula_seleccionada['salas']:
            sala_temp = src.sala.buscar_sala_por_id(dbFilms['salas'], sala_info['salaId'])
            
            #24/10/2025 - Verificar disponibilidad de la función específica (película + sala + horario)
            asientos_libres = src.sala.contar_asientos_disponibles_funcion(
                dbFilms, pelicula_seleccionada['id'], sala_info['salaId'], sala_info['horario']
            )
            disponible = src.sala.sala_tiene_asientos_disponibles_funcion(
                dbFilms, pelicula_seleccionada['id'], sala_info['salaId'], sala_info['horario']
            )

            texto = f"Sala {sala_info['salaId']} - {sala_info['horario']} - ${sala_info['precio']} ({asientos_libres} libres)"
            if disponible:
                btn = Boton(50, y_pos, 650, 55, texto + " ✅")
                btn.actualizar(pos_mouse)
                btn.dibujar(screen, font_pequena)
                # Pasar como tupla (sala_info, sala_temp)
                botones.append(('sala', btn, (sala_info, sala_temp)))
            else:
                btn = Boton(50, y_pos, 650, 55, texto + " ❌ COMPLETA", COLOR_OCUPADO)
                btn.dibujar(screen, font_pequena)

            y_pos += 65

    # Paso 3: Seleccionar asientos
    if sala_completa and sala_seleccionada:
        y_pos = 90
        x_asientos = 800

        dibujar_texto("Paso 3: Selecciona tus Asientos", x_asientos, y_pos, font_mediana)
        y_pos += 50
        dibujar_texto("─────── PANTALLA 🎬 ───────", x_asientos, y_pos, font_pequena)
        y_pos += 60

        filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        #24/10/2025 - Obtener asientos de la función específica
        asientos_funcion = src.sala.obtener_asientos_funcion(
            dbFilms, pelicula_seleccionada['id'], sala_seleccionada['salaId'], sala_seleccionada['horario']
        )

        if asientos_funcion:
            for idx_fila, fila in enumerate(asientos_funcion):
                letra_fila = filas[idx_fila] if idx_fila < len(filas) else str(idx_fila)
                dibujar_texto(letra_fila, x_asientos - 40, y_pos + 5, font_pequena)

                for idx_col, asiento in enumerate(fila):
                    asiento_pos = (idx_fila, idx_col)
                    x_btn = x_asientos + (idx_col * 70)

                    # Color según estado
                    if asiento_pos in asientos_seleccionados:
                        color = COLOR_SELECCIONADO
                    elif asiento == 0:
                        color = COLOR_DISPONIBLE
                    else:
                        color = COLOR_OCUPADO

                    btn = Boton(x_btn, y_pos, 60, 45, str(idx_col + 1), color)
                    btn.actualizar(pos_mouse)
                    btn.dibujar(screen, font_pequena)

                    if asiento == 0:
                        botones.append(('asiento', btn, asiento_pos))

                y_pos += 55

        y_pos += 30
        dibujar_texto("🟩 Disponible | 🟦 Seleccionado | 🟥 Ocupado", x_asientos, y_pos, font_pequena)
        y_pos += 40

        #24/10/2025 - Usar asientos de la función específica para calcular el mejor asiento
        if asientos_funcion:
            resultado = src.sala.asiento_mas_centrado(asientos_funcion)
            if resultado:
                f, c = resultado
                dibujar_texto(f"🎯 Recomendado: {src.sala.codigo_asiento(f, c)}", x_asientos, y_pos, font_pequena)

        y_pos += 50
        dibujar_texto(f"Asientos seleccionados: {len(asientos_seleccionados)}", x_asientos, y_pos, font_pequena)

        # Paso 4: Confirmar
        if len(asientos_seleccionados) > 0:
            y_pos += 70
            dibujar_texto("Paso 4: Confirmar Reserva", x_asientos, y_pos, font_mediana)
            y_pos += 50

            # Input de nombre
            dibujar_texto(f"Nombre: {nombre_usuario}_", x_asientos, y_pos, font_pequena)
            y_pos += 50

            # Descuentos
            dibujar_texto("Descuentos:", x_asientos, y_pos, font_pequena)
            y_pos += 40

            for desc in dbFilms['descuentos']:
                btn = Boton(x_asientos, y_pos, 280, 40, f"{desc['name']} ({desc['descount']}%)", COLOR_DISPONIBLE)
                btn.actualizar(pos_mouse)
                btn.dibujar(screen, font_pequena)
                botones.append(('descuento', btn, desc))
                y_pos += 50

            if descuento_aplicado:
                dibujar_texto(f"✅ Desc: {descuento_aplicado['name']}", x_asientos, y_pos, font_pequena)
                y_pos += 40

            # Precios
            precio_unitario = sala_seleccionada['precio']
            if descuento_aplicado:
                precio_unitario = precio_unitario * (1 - float(descuento_aplicado['descount']) / 100)
            precio_total = precio_unitario * len(asientos_seleccionados)

            dibujar_texto(f"💰 Precio/persona: ${precio_unitario:.2f}", x_asientos, y_pos, font_pequena)
            y_pos += 35
            dibujar_texto(f"💸 TOTAL: ${precio_total:.2f}", x_asientos, y_pos, font_pequena, COLOR_TITULO)
            y_pos += 70

    # Mensaje del sistema (si existe)
    if mensaje_sistema:
        dibujar_texto(mensaje_sistema, 50, ALTO_VENTANA - 140, font_pequena, COLOR_TITULO)

    # Botones en la parte inferior - LADO A LADO
    btn_volver = Boton(50, ALTO_VENTANA - 90, 400, 65, "🔄 Volver al Menú")
    btn_volver.actualizar(pos_mouse)
    btn_volver.dibujar(screen)
    botones.append(('volver', btn_volver, None))

    # Botón confirmar solo si hay asientos seleccionados
    if len(asientos_seleccionados) > 0 and nombre_usuario.strip():
        btn_confirmar = Boton(480, ALTO_VENTANA - 90, 450, 65, "✅ CONFIRMAR RESERVA", COLOR_DISPONIBLE)
        btn_confirmar.actualizar(pos_mouse)
        btn_confirmar.dibujar(screen)
        botones.append(('confirmar', btn_confirmar, None))

    # Manejar eventos de teclado para nombre
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                nombre_usuario = nombre_usuario[:-1]
            elif evento.key == pygame.K_RETURN:
                pass
            elif len(nombre_usuario) < 30 and evento.unicode.isprintable():
                nombre_usuario += evento.unicode

    return botones

def ventana_buscar_ticket_ui(pos_mouse, eventos):
    global ventana_actual, id_busqueda, reserva_encontrada, dbFilms

    screen.fill(COLOR_FONDO)

    dibujar_texto("🎟️ Buscar Mi Ticket", 550, 80, font_grande, COLOR_TITULO)

    y_pos = 200
    dibujar_texto("ID de Reserva:", 550, y_pos, font_mediana)
    y_pos += 60
    dibujar_texto(f"{id_busqueda}_", 550, y_pos, font_mediana, COLOR_TITULO)

    # Eventos de teclado
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                id_busqueda = id_busqueda[:-1]
            elif evento.key == pygame.K_RETURN:
                if 'reserva' in dbFilms and id_busqueda.strip():
                    dbFilms = cargar_datos()
                    reserva_encontrada = src.reserva.buscar_reserva_por_id(dbFilms['reserva'], id_busqueda.strip())
            elif len(id_busqueda) < 10 and evento.unicode.isalnum():
                id_busqueda += evento.unicode.upper()

    y_pos += 80
    btn_buscar = Boton(550, y_pos, 250, 60, "🔎 Buscar")
    btn_buscar.actualizar(pos_mouse)
    btn_buscar.dibujar(screen)

    botones = [('buscar', btn_buscar, None)]

    # Mostrar resultado
    if reserva_encontrada is not None and isinstance(reserva_encontrada, dict):
        y_pos += 120
        dibujar_texto("✅ RESERVA ENCONTRADA", 550, y_pos, font_mediana, COLOR_DISPONIBLE)
        y_pos += 60

        dibujar_texto(f"🆔 ID: {reserva_encontrada.get('id', 'N/A')}", 550, y_pos, font_pequena)
        y_pos += 40
        dibujar_texto(f"👤 Usuario: {reserva_encontrada.get('idUser', 'N/A')}", 550, y_pos, font_pequena)
        y_pos += 40
        dibujar_texto(f"🎬 Película: {reserva_encontrada.get('pelicula', 'N/A')}", 550, y_pos, font_pequena)
        y_pos += 40
        dibujar_texto(f"🏢 Sala: {reserva_encontrada.get('sala', 'N/A')}", 550, y_pos, font_pequena)
        y_pos += 40
        dibujar_texto(f"💺 Asientos: {reserva_encontrada.get('asiento', 'N/A')}", 550, y_pos, font_pequena)
    elif reserva_encontrada is None and id_busqueda.strip() != "":
        y_pos += 120
        dibujar_texto("❌ No se encontró la reserva", 550, y_pos, font_pequena, COLOR_OCUPADO)
        dibujar_texto("Verifica el ID o intenta de nuevo", 550, y_pos + 50, font_pequena)

    btn_volver = Boton(550, ALTO_VENTANA - 120, 350, 60, "🔄 Volver")
    btn_volver.actualizar(pos_mouse)
    btn_volver.dibujar(screen)
    botones.append(('volver', btn_volver, None))

    return botones

def ventana_descuentos_ui(pos_mouse):


    global ventana_actual

    screen.fill(COLOR_FONDO)

    dibujar_texto("💰 Descuentos Disponibles", 500, 80, font_grande, COLOR_TITULO)

    y_pos = 200
    for desc in dbFilms['descuentos']:
        dibujar_texto(f"🎊 {desc['name']}: {desc['descount']}%", 500, y_pos, font_mediana)
        y_pos += 50
        dibujar_texto(f"   {desc['description']}", 500, y_pos, font_pequena)
        y_pos += 80

    btn_volver = Boton(550, ALTO_VENTANA - 120, 350, 60, "🔄 Volver")
    btn_volver.actualizar(pos_mouse)
    btn_volver.dibujar(screen)

    return [('volver', btn_volver, None)]


# ---------------------- FUNCIÓN PRINCIPAL DE LA UI ----------------------

def iniciar_interfaz():
    """Inicia la interfaz Pygame del sistema de cine."""
    global dbFilms, ventana_actual, pelicula_seleccionada, sala_seleccionada
    global sala_completa, asientos_seleccionados, nombre_usuario
    global descuento_aplicado, mensaje_sistema, id_busqueda, reserva_encontrada

    dbFilms = cargar_datos()
    if dbFilms is None:
        print("No se pudo cargar el archivo JSON. Saliendo.")
        return

    clock = pygame.time.Clock()
    running = True

    while running:
        pos_mouse = pygame.mouse.get_pos()
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ventana_actual == 0:
                    botones = menu_principal(pos_mouse)
                    if botones[0].click(pos_mouse):
                        ventana_actual = 1
                        resetear_seleccion()
                    elif botones[1].click(pos_mouse):
                        ventana_actual = 2
                        id_busqueda = ""
                        reserva_encontrada = None
                    elif botones[2].click(pos_mouse):
                        ventana_actual = 3
                    elif botones[3].click(pos_mouse):
                        running = False

                elif ventana_actual == 1:
                    botones = ventana_peliculas_ui(pos_mouse, [])
                    for item in botones:
                        if len(item) < 2:
                            continue

                        tipo = item[0]
                        btn = item[1]

                        if btn.click(pos_mouse):
                            if tipo == 'pelicula':
                                pelicula_seleccionada = item[2]
                                sala_seleccionada = None
                                sala_completa = None
                                asientos_seleccionados = []
                                mensaje_sistema = ""
                            elif tipo == 'sala':
                                # Desempaquetar la tupla correctamente
                                datos_sala = item[2]
                                sala_seleccionada = datos_sala[0]  # sala_info
                                sala_completa = datos_sala[1]      # sala_temp
                                asientos_seleccionados = []
                                mensaje_sistema = ""
                                print(f"✅ Sala seleccionada: {sala_seleccionada['salaId']} - Horario: {sala_seleccionada['horario']}")
                            elif tipo == 'asiento':
                                asiento_pos = item[2]
                                if asiento_pos in asientos_seleccionados:
                                    asientos_seleccionados.remove(asiento_pos)
                                else:
                                    asientos_seleccionados.append(asiento_pos)
                            elif tipo == 'descuento':
                                descuento_aplicado = item[2]
                            elif tipo == 'confirmar':
                                if not nombre_usuario.strip():
                                    mensaje_sistema = "❌ Por favor, ingresa tu nombre"
                                elif len(asientos_seleccionados) == 0:
                                    mensaje_sistema = "❌ Selecciona al menos un asiento"
                                else:
                                    try:
                                        codigos_asientos = src.sala.asientos_a_codigo(asientos_seleccionados)

                                        #24/10/2025 - Marcar asientos en la función específica
                                        if src.sala.marcar_asientos_ocupados_funcion(
                                            dbFilms, pelicula_seleccionada['id'], 
                                            sala_seleccionada['salaId'], 
                                            sala_seleccionada['horario'], 
                                            asientos_seleccionados
                                        ):
                                            reserva = src.reserva.crear_reserva(
                                                idUser=nombre_usuario,
                                                sala=sala_seleccionada['salaId'],
                                                asientos=codigos_asientos,
                                                pelicula=pelicula_seleccionada['titulo'],
                                            )

                                            precio_unitario = sala_seleccionada['precio']
                                            if descuento_aplicado:
                                                precio_unitario = precio_unitario * (1 - float(descuento_aplicado['descount']) / 100)

                                            ticket = src.ticket.crear_ticket(
                                                idUser=nombre_usuario,
                                                pelicula=pelicula_seleccionada['titulo'],
                                                sala=sala_seleccionada['salaId'],
                                                asientos=codigos_asientos,
                                                horario=sala_seleccionada['horario'],
                                                precio_unitario=precio_unitario,
                                                cantidad_asientos=len(asientos_seleccionados),
                                                descuento=descuento_aplicado
                                            )

                                            #24/10/2025 - Guardar con el sistema de funciones
                                            src.sala.guardar_funciones_json(dbFilms)
                                            src.reserva.guardar_reserva_json(reserva, dbFilms)
                                            src.ticket.guardar_ticket_json(ticket, dbFilms)
                                            src.ticket.guardar_ticket_csv(ticket)
                                            
                                            src.generar_ticket.generar_ticket(reserva, descuento_aplicado) #24/10/2025 generamos ticket

                                            # Recargar datos
                                            dbFilms = cargar_datos()

                                            mensaje_sistema = f"✅ ¡RESERVA CONFIRMADA! ID: {reserva['id']}"
                                            print(f"✅ Reserva creada con éxito: {reserva['id']}")

                                            # Resetear
                                            nombre_usuario = ""
                                            pelicula_seleccionada = None
                                            sala_seleccionada = None
                                            sala_completa = None
                                            asientos_seleccionados = []
                                            descuento_aplicado = None
                                        else:
                                            mensaje_sistema = "❌ Error al marcar asientos"
                                    except Exception as e:
                                        mensaje_sistema = f"❌ Error: {str(e)}"
                                        print(f"❌ Error: {e}")
                            elif tipo == 'volver':
                                ventana_actual = 0
                                resetear_seleccion()

                elif ventana_actual == 2:
                    botones = ventana_buscar_ticket_ui(pos_mouse, [])
                    for item in botones:
                        if len(item) < 2:
                            continue

                        tipo = item[0]
                        btn = item[1]

                        if btn.click(pos_mouse):
                            if tipo == 'buscar':
                                if 'reserva' in dbFilms and id_busqueda.strip():
                                    dbFilms = cargar_datos()
                                    reserva_encontrada = src.reserva.buscar_reserva_por_id(dbFilms['reserva'], id_busqueda.strip())
                            elif tipo == 'volver':
                                ventana_actual = 0
                                id_busqueda = ""
                                reserva_encontrada = None

                elif ventana_actual == 3:
                    botones = ventana_descuentos_ui(pos_mouse)
                    if len(botones) > 0 and len(botones[0]) >= 2:
                        if botones[0][1].click(pos_mouse):
                            ventana_actual = 0

        # Renderizar ventana actual
        if ventana_actual == 0:
            menu_principal(pos_mouse)
        elif ventana_actual == 1:
            ventana_peliculas_ui(pos_mouse, eventos)
        elif ventana_actual == 2:
            ventana_buscar_ticket_ui(pos_mouse, eventos)
        elif ventana_actual == 3:
            ventana_descuentos_ui(pos_mouse)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    iniciar_interfaz()
