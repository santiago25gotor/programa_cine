from dataclasses import dataclass
from typing import List, Optional, Tuple

@dataclass
class Sala:
    id: int
    nombre: str
    asientos: List[List[int]]


def mostrar_salas(salas):
    print("\n🎟️ Salas y Asientos:")
    for sala in salas:
        print(f"- {sala['nombre']} (ID {sala['id']})")
        for fila in sala['asientos']:
            print("  Asientos:", fila)


def buscar_sala_por_id(salas: List[dict], sala_id: int) -> Optional[dict]:
    for sala in salas:
        if sala['id'] == sala_id:
            return sala
    return None


def sala_tiene_asientos_disponibles(sala: dict) -> bool:
    for fila in sala['asientos']:
        for asiento in fila:
            if asiento == 0:
                return True
    return False


def contar_asientos_disponibles(sala: dict) -> int:
    contador = 0
    for fila in sala['asientos']:
        for asiento in fila:
            if asiento == 0:
                contador += 1
    return contador


def seleccionar_sala(pelicula: dict, todas_las_salas: List[dict]) -> Optional[dict]:
    while True:
        print(f"\n🏢 Salas disponibles para '{pelicula['titulo']}':")
        print("="*50)
        
        salas_con_disponibilidad = []
        
        for i, sala_info in enumerate(pelicula['salas'], 1):
            sala_completa = buscar_sala_por_id(todas_las_salas, sala_info['salaId'])
            
            if sala_completa and sala_tiene_asientos_disponibles(sala_completa):
                asientos_libres = contar_asientos_disponibles(sala_completa)
                print(f"{i}. Sala {sala_info['salaId']} - Horario: {sala_info['horario']} - Precio: ${sala_info['precio']} - ({asientos_libres} asientos libres) ✅")
                salas_con_disponibilidad.append((i, sala_info))
            else:
                print(f"{i}. Sala {sala_info['salaId']} - Horario: {sala_info['horario']} - COMPLETA ❌")
        
        print("\n0. Volver atrás")
        print("="*50)
        
        if not salas_con_disponibilidad:
            print("\n⚠️ Lo sentimos, todas las salas están completas para esta película.")
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
                print(f"❌ Opción inválida o sala completa. Elige una sala con asientos disponibles.")
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


def mostrar_asientos_disponibles(sala: dict, asientos_seleccionados: List[Tuple[int, int]] = None):
    if asientos_seleccionados is None:
        asientos_seleccionados = []
   
    print(f"\n🎟️ Asientos en {sala['nombre']}:")
    print("="*50)
    print("PANTALLA 🎬".center(50))
    print("="*50)
    print()
    
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    
    print("    ", end="")
    num_columnas = len(sala['asientos'][0]) if sala['asientos'] else 0
    for col in range(1, num_columnas + 1):
        print(f"  {col} ", end="")
    print("\n")
    
    for idx_fila, fila in enumerate(sala['asientos']):
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
     # Mostrar asiento más centrado sugerido
    resultado = asiento_mas_centrado(sala['asientos'])
    if resultado:
        f, c = resultado
        print(f"🎯 Asiento más centrado disponible: {codigo_asiento(f, c)}")
    print("="*50)


def pedir_cantidad_asientos(sala: dict) -> Optional[int]:
    asientos_disponibles = contar_asientos_disponibles(sala)
    
    while True:
        print("\n" + "="*50)
        print("👥 ¿Cuántas personas van al cine?")
        print(f"   (Asientos disponibles: {asientos_disponibles})")
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
                print(f"❌ Solo hay {asientos_disponibles} asientos disponibles.")
                input("Presiona ENTER para continuar...")
                continue
            
            return cantidad
        
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
            input("Presiona ENTER para continuar...")


def seleccionar_multiples_asientos(sala: dict, cantidad: int) -> Optional[List[Tuple[int, int]]]:
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    asientos_seleccionados = []
    
    if cantidad == 1:
        print(f"\n📍 Selecciona tu asiento")
    else:
        print(f"\n📍 Vas a seleccionar {cantidad} asientos")
    
    for i in range(cantidad):
        while True:
            mostrar_asientos_disponibles(sala, asientos_seleccionados)
            
            if cantidad == 1:
                print(f"\n🔍 Selecciona tu asiento") ## aqui añadir el numero de asientos
            else:
                print(f"\n🔍 Selecciona el asiento #{i+1} de {cantidad}")
            
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
                
                if fila_letra not in filas[:len(sala['asientos'])]:
                    print(f"❌ Fila inválida. Usa letras de A a {filas[len(sala['asientos'])-1]}")
                    input("Presiona ENTER para continuar...")
                    continue
                
                fila_idx = filas.index(fila_letra)
                
                if numero_asiento < 1 or numero_asiento > len(sala['asientos'][fila_idx]):
                    print(f"❌ Número de asiento inválido. Usa números de 1 a {len(sala['asientos'][fila_idx])}")
                    input("Presiona ENTER para continuar...")
                    continue
                
                asiento_idx = numero_asiento - 1
                
                if sala['asientos'][fila_idx][asiento_idx] == 1:
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


def marcar_asientos_ocupados(sala: dict, asientos: List[Tuple[int, int]]) -> bool:
    try:
        for fila, columna in asientos:
            if sala['asientos'][fila][columna] == 0:
                sala['asientos'][fila][columna] = 1
            else:
                return False
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


def marcar_asiento_ocupado(sala: dict, fila: int, columna: int) -> bool:
    try:
        if sala['asientos'][fila][columna] == 0:
            sala['asientos'][fila][columna] = 1
            return True
        return False
    except (IndexError, KeyError):
        return False