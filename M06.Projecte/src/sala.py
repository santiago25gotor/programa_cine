from dataclasses import dataclass
from typing import List, Optional, Tuple
import json

@dataclass
class Sala:
    id: int
    nombre: str
    asientos: List[List[int]]


def buscar_sala_por_id(salas: List[dict], sala_id: int) -> Optional[dict]:
    for sala in salas:
        if sala['id'] == sala_id:
            return sala
    return None


#24/10/25 - Nueva función para obtener clave única de función
def obtener_clave_funcion(pelicula_id: int, sala_id: int, horario: str) -> str:
    """
    Genera una clave única para identificar una función específica.
    Cada combinación de película + sala + horario tiene su propia matriz de asientos.
    """
    return f"pelicula_{pelicula_id}_sala_{sala_id}_horario_{horario.replace(':', '')}"


#24/10/25 - Nueva función para obtener asientos de una función específica
def obtener_asientos_funcion(dbFilms: dict, pelicula_id: int, sala_id: int, horario: str) -> List[List[int]]:
    """
    Obtiene los asientos de una función específica.
    Si no existe, crea una nueva matriz basada en la plantilla de la sala.
    Si la sala no existe en dbFilms['salas'], la crea automáticamente.
    """
    clave = obtener_clave_funcion(pelicula_id, sala_id, horario)
    
    # Inicializar estructura si no existe
    if 'funciones' not in dbFilms:
        dbFilms['funciones'] = {}
    
    # Si la función no existe, crear una nueva matriz desde la plantilla
    if clave not in dbFilms['funciones']:
        sala_plantilla = buscar_sala_por_id(dbFilms['salas'], sala_id)
        
        # Si la sala no existe en la lista de salas, crearla
        if not sala_plantilla:
            nueva_sala = {
                "id": sala_id,
                "nombre": f"Sala {sala_id}",
                "asientos": [
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                ]
            }
            dbFilms['salas'].append(nueva_sala)
            sala_plantilla = nueva_sala
            print(f"✅ Sala {sala_id} creada automáticamente")
        
        if sala_plantilla and 'asientos' in sala_plantilla:
            # Crear copia profunda de la matriz de asientos
            import copy
            dbFilms['funciones'][clave] = copy.deepcopy(sala_plantilla['asientos'])
        else:
            # Crear matriz por defecto si no hay plantilla
            dbFilms['funciones'][clave] = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    
    return dbFilms['funciones'][clave]


#24/10/25 - Función modificada para trabajar con asientos de función específica
def sala_tiene_asientos_disponibles_funcion(dbFilms: dict, pelicula_id: int, sala_id: int, horario: str) -> bool:
    """
    Verifica si una función específica tiene asientos disponibles.
    """
    asientos = obtener_asientos_funcion(dbFilms, pelicula_id, sala_id, horario)
    for fila in asientos:
        for asiento in fila:
            if asiento == 0:
                return True
    return False

#24/10/25 - Función modificada para contar asientos de función específica
def contar_asientos_disponibles_funcion(dbFilms: dict, pelicula_id: int, sala_id: int, horario: str) -> int:
    """
    Cuenta los asientos disponibles de una función específica.
    """
    asientos = obtener_asientos_funcion(dbFilms, pelicula_id, sala_id, horario)
    contador = 0
    for fila in asientos:
        for asiento in fila:
            if asiento == 0:
                contador += 1
    return contador

#24/10/25 - Función modificada para usar sistema de funciones
def seleccionar_sala(pelicula: dict, todas_las_salas: List[dict], dbFilms: dict) -> Optional[dict]:
    """
    Permite seleccionar una sala para una película.
    Ahora verifica disponibilidad por función específica (película + sala + horario).
    Crea salas automáticamente si no existen.
    """
    while True:
        print(f"\n🏢 Salas disponibles para '{pelicula['titulo']}':")
        print("="*50)
        
        salas_con_disponibilidad = []
        
        for i, sala_info in enumerate(pelicula['salas'], 1):
            # Obtener o crear la sala completa
            sala_completa = buscar_sala_por_id(todas_las_salas, sala_info['salaId'])
            
            # Si la sala no existe, crearla (esto se hace en obtener_asientos_funcion)
            # Pero primero verificamos si necesita ser agregada a todas_las_salas
            if not sala_completa:
                # Forzar la creación de la función para que se cree la sala
                obtener_asientos_funcion(dbFilms, pelicula['id'], sala_info['salaId'], sala_info['horario'])
                # Ahora buscar de nuevo
                sala_completa = buscar_sala_por_id(todas_las_salas, sala_info['salaId'])
            
            #24/10/25 - Verificar disponibilidad de la función específica
            if sala_completa:
                asientos_libres = contar_asientos_disponibles_funcion(
                    dbFilms, pelicula['id'], sala_info['salaId'], sala_info['horario']
                )
                tiene_disponibles = sala_tiene_asientos_disponibles_funcion(
                    dbFilms, pelicula['id'], sala_info['salaId'], sala_info['horario']
                )
                
                if tiene_disponibles:
                    print(f"{i}. Sala {sala_info['salaId']} - Horario: {sala_info['horario']} - Precio: ${sala_info['precio']} - ({asientos_libres} asientos libres) ✅")
                    salas_con_disponibilidad.append((i, sala_info))
                else:
                    print(f"{i}. Sala {sala_info['salaId']} - Horario: {sala_info['horario']} - COMPLETA ❌")
        
        print("\n0. Volver atrás")
        print("="*50)
        
        if not salas_con_disponibilidad:
            print("\n⚠️ Lo sentimos, todas las funciones están completas para esta película.")
            input("Presiona ENTER para continuar...")
            return None
        
        try:
            opcion = int(input("\n➤ Selecciona una sala (número): ").strip())
            
            if opcion == 0:
                print("🔙 Volviendo...")
                return None
            
            sala_valida = None
            for idx, sala_info in salas_con_disponibilidad:
                if idx == opcion:
                    sala_valida = sala_info
                    break
            
            if sala_valida:
                print(f"\n✅ Sala seleccionada: Sala {sala_valida['salaId']} - {sala_valida['horario']}")
                return sala_valida
            else:
                print(f"❌ Opción inválida o función completa. Elige una sala con asientos disponibles.")
                input("Presiona ENTER para continuar...")
        
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
            input("Presiona ENTER para continuar...")


def asiento_mas_centrado(asientos):
    """Devuelve el asiento libre más centrado de la matriz (fila, columna)."""
    if not asientos or not asientos[0]:
        return None

    filas = len(asientos)
    columnas = len(asientos[0])
    centro_fila = (filas - 1) / 2
    centro_columna = (columnas - 1) / 2

    mejor_asiento = None
    mejor_distancia = float("inf")

    for f in range(filas):
        for c in range(columnas):
            if asientos[f][c] == 0:  # libre
                distancia = ((f - centro_fila) ** 2 + (c - centro_columna) ** 2) ** 0.5
                if distancia < mejor_distancia:
                    mejor_distancia = distancia
                    mejor_asiento = (f, c)

    return mejor_asiento


#24/10/25 - Función modificada para mostrar asientos de función específica
def mostrar_asientos_disponibles_funcion(dbFilms: dict, pelicula_id: int, sala: dict, horario: str, 
                                         asientos_seleccionados: List[Tuple[int, int]] = None):
    """
    Muestra los asientos de una función específica.
    """
    if asientos_seleccionados is None:
        asientos_seleccionados = []
    
    #24/10/25 - Obtener asientos de la función específica
    asientos = obtener_asientos_funcion(dbFilms, pelicula_id, sala['id'], horario)
   
    print(f"\n🎟️ Asientos en {sala['nombre']} - Horario: {horario}:")
    print("="*50)
    print("PANTALLA 🎬".center(50))
    print("="*50)
    print()
    
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    
    print("    ", end="")
    num_columnas = len(asientos[0]) if asientos else 0
    for col in range(1, num_columnas + 1):
        print(f"  {col} ", end="")
    print("\n")
    
    for idx_fila, fila in enumerate(asientos):
        letra_fila = filas[idx_fila] if idx_fila < len(filas) else str(idx_fila)
        print(f" {letra_fila}  ", end="")
        
        for idx_col, asiento in enumerate(fila):
            if (idx_fila, idx_col) in asientos_seleccionados:
                print(" ❌ ", end="")
            elif asiento == 0:
                print(" ⬜ ", end="")
            else:
                print(" ❌ ", end="")
        print()
    
    print("\n" + "="*50)
    print("⬜ = Disponible | ❌ = Ocupado")
    
    #24/10/25 - Mostrar asiento más centrado usando asientos de la función
    resultado = asiento_mas_centrado(asientos)
    if resultado:
        f, c = resultado
        print(f"🎯 Asiento más centrado disponible: {codigo_asiento(f, c)}")
    print("="*50)

#24/10/25 - Función modificada para trabajar con asientos de función específica
def pedir_cantidad_asientos_funcion(dbFilms: dict, pelicula_id: int, sala_id: int, horario: str) -> Optional[int]:
    """
    Pide la cantidad de asientos para una función específica.
    """
    asientos_disponibles = contar_asientos_disponibles_funcion(dbFilms, pelicula_id, sala_id, horario)
    
    while True:
        print("\n" + "="*50)
        print("👥 ¿Cuántas personas van al cine?")
        print(f"   (Asientos disponibles en esta función: {asientos_disponibles})")
        print("="*50)
        print("\n💡 Ejemplos: 1 (solo tú), 2 (tú y un amigo), 4 (familia)")
        
        try:
            cantidad = int(input("\n➤ Número de personas (o 0 para cancelar): ").strip())
            
            if cantidad == 0:
                print("🔙 Cancelando...")
                return None
            
            if cantidad < 1:
                print("❌ Debes reservar al menos 1 asiento.")
                input("Presiona ENTER para continuar...")
                continue
            
            if cantidad > asientos_disponibles:
                print(f"❌ Solo hay {asientos_disponibles} asientos disponibles en esta función.")
                input("Presiona ENTER para continuar...")
                continue
            
            return cantidad
        
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
            input("Presiona ENTER para continuar...")

#24/10/25 - Función modificada para seleccionar asientos de función específica
def seleccionar_multiples_asientos_funcion(dbFilms: dict, pelicula_id: int, sala: dict, 
                                          horario: str, cantidad: int) -> Optional[List[Tuple[int, int]]]:
    """
    Permite seleccionar múltiples asientos de una función específica.
    """
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    asientos_seleccionados = []
    
    #24/10/25 - Obtener asientos de la función específica
    asientos_funcion = obtener_asientos_funcion(dbFilms, pelicula_id, sala['id'], horario)
    
    if cantidad == 1:
        print(f"\n📍 Selecciona tu asiento")
    else:
        print(f"\n📍 Vas a seleccionar {cantidad} asientos")
    
    for i in range(cantidad):
        while True:
            mostrar_asientos_disponibles_funcion(dbFilms, pelicula_id, sala, horario, asientos_seleccionados)
            
            if cantidad == 1:
                print(f"\n📍 Selecciona tu asiento")
            else:
                print(f"\n📍 Selecciona el asiento #{i+1} de {cantidad}")
            
            print("   Formato: FILA NÚMERO (ejemplo: A 1)")
            print("   O escribe 'salir' para cancelar")
            
            entrada = input("\n➤ Asiento: ").strip().upper()
            
            if entrada.lower() == 'salir':
                print("🔙 Cancelando selección de asientos...")
                return None
            
            try:
                partes = entrada.split()
                if len(partes) != 2:
                    print("❌ Formato incorrecto. Usa: FILA NÚMERO (ejemplo: A 1)")
                    input("Presiona ENTER para continuar...")
                    continue
                
                fila_letra = partes[0]
                numero_asiento = int(partes[1])
                
                if fila_letra not in filas[:len(asientos_funcion)]:
                    print(f"❌ Fila inválida. Usa letras de A a {filas[len(asientos_funcion)-1]}")
                    input("Presiona ENTER para continuar...")
                    continue
                
                fila_idx = filas.index(fila_letra)
                
                if numero_asiento < 1 or numero_asiento > len(asientos_funcion[fila_idx]):
                    print(f"❌ Número de asiento inválido. Usa números de 1 a {len(asientos_funcion[fila_idx])}")
                    input("Presiona ENTER para continuar...")
                    continue
                
                asiento_idx = numero_asiento - 1
                
                #24/10/25 - Verificar si está ocupado en la función específica
                if asientos_funcion[fila_idx][asiento_idx] == 1:
                    print(f"❌ El asiento {fila_letra}{numero_asiento} ya está ocupado.")
                    input("Presiona ENTER para continuar...")
                    continue
                
                if (fila_idx, asiento_idx) in asientos_seleccionados:
                    print(f"❌ Ya seleccionaste el asiento {fila_letra}{numero_asiento}.")
                    input("Presiona ENTER para continuar...")
                    continue
                
                asientos_seleccionados.append((fila_idx, asiento_idx))
                print(f"\n✅ Asiento {fila_letra}{numero_asiento} añadido ({i+1}/{cantidad})")
                
                if i < cantidad - 1:
                    input("\nPresiona ENTER para seleccionar el siguiente asiento...")
                break
            
            except (ValueError, IndexError):
                print("❌ Entrada inválida. Intenta de nuevo.")
                input("Presiona ENTER para continuar...")
    
    return asientos_seleccionados

#24/10/25 - Función modificada para marcar asientos en función específica
def marcar_asientos_ocupados_funcion(dbFilms: dict, pelicula_id: int, sala_id: int, 
                                     horario: str, asientos: List[Tuple[int, int]]) -> bool:
    """
    Marca asientos como ocupados en una función específica.
    """
    try:
        asientos_funcion = obtener_asientos_funcion(dbFilms, pelicula_id, sala_id, horario)
        
        # Verificar primero que todos estén disponibles
        for fila, columna in asientos:
            if asientos_funcion[fila][columna] != 0:
                return False
        
        # Marcar todos como ocupados
        for fila, columna in asientos:
            asientos_funcion[fila][columna] = 1
            
        return True
    except (IndexError, KeyError):
        return False

def asientos_a_codigo(asientos: List[Tuple[int, int]]) -> List[str]:
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    codigos = []
    
    for fila, columna in asientos:
        letra_fila = filas[fila] if fila < len(filas) else str(fila)
        codigos.append(f"{letra_fila}{columna + 1}")
    
    return codigos

def codigo_asiento(fila, columna):
    filas_letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    return f"{filas_letras[fila]}{columna + 1}"


#24/10/25 - Función modificada para guardar funciones en JSON
def guardar_funciones_json(dbFilms: dict, dbFilmsRuta ) -> bool:
    """
    Guarda el estado de todas las funciones en el archivo JSON.
    """
    try:
        with open(dbFilmsRuta, 'w', encoding='utf-8') as f:
            json.dump(dbFilms, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        return False

    
def guardar_salas_json(salas: List[dict], archivo="dbFilms.json") -> bool:
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)

        data['salas'] = salas

        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        return False