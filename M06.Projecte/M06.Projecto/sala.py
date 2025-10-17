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
    """
    Busca una sala por su ID.
    """
    for sala in salas:
        if sala['id'] == sala_id:
            return sala
    return None


def sala_tiene_asientos_disponibles(sala: dict) -> bool:
    """
    Verifica si una sala tiene al menos un asiento disponible.
    Retorna True si hay asientos libres (0), False si está llena.
    """
    for fila in sala['asientos']:
        for asiento in fila:
            if asiento == 0:  # Si encuentra al menos un asiento libre
                return True
    return False  # Todos los asientos están ocupados


def contar_asientos_disponibles(sala: dict) -> int:
    """
    Cuenta cuántos asientos disponibles tiene una sala.
    """
    contador = 0
    for fila in sala['asientos']:
        for asiento in fila:
            if asiento == 0:
                contador += 1
    return contador


def seleccionar_sala(pelicula: dict, todas_las_salas: List[dict]) -> Optional[dict]:
    """
    Muestra las salas disponibles para la película y permite seleccionar una.
    Verifica que la sala tenga asientos disponibles antes de permitir la selección.
    """
    while True:
        print(f"\n🏢 Salas disponibles para '{pelicula['titulo']}':")
        print("="*50)
        
        salas_con_disponibilidad = []
        
        for i, sala_info in enumerate(pelicula['salas'], 1):
            # Buscar la sala completa para verificar disponibilidad
            sala_completa = buscar_sala_por_id(todas_las_salas, sala_info['salaId'])
            
            if sala_completa and sala_tiene_asientos_disponibles(sala_completa):
                asientos_libres = contar_asientos_disponibles(sala_completa)
                print(f"{i}. Sala {sala_info['salaId']} - Horario: {sala_info['horario']} - Precio: ${sala_info['precio']} - ({asientos_libres} asientos libres) ✅")
                salas_con_disponibilidad.append((i, sala_info))
            else:
                print(f"{i}. Sala {sala_info['salaId']} - Horario: {sala_info['horario']} - COMPLETA ❌")
        
        print("\n0. Volver atrás")
        print("="*50)
        
        # Si no hay salas disponibles
        if not salas_con_disponibilidad:
            print("\n⚠️ Lo sentimos, todas las salas están completas para esta película.")
            input("Presiona ENTER para continuar...")
            return None
        
        try:
            opcion = int(input("\n➤ Selecciona una sala (número): ").strip())
            
            if opcion == 0:
                print("🔙 Volviendo...")
                return None
            
            # Verificar si la opción corresponde a una sala con disponibilidad
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


def mostrar_asientos_disponibles(sala: dict):
    """
    Muestra visualmente los asientos de la sala.
    """
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
        
        for asiento in fila:
            if asiento == 0:
                print(" ⬜ ", end="") 
            else:
                print(" ❌ ", end="") 
        print() 
    
    print("\n" + "="*50)
    print("⬜ = Disponible | ❌ = Ocupado")
    print("="*50)


def seleccionar_asiento(sala: dict) -> Optional[Tuple[int, int]]:
    """
    Permite al usuario seleccionar un asiento disponible.
    """
    filas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    
    while True:
        mostrar_asientos_disponibles(sala)
        
        print("\n🔍 Selecciona tu asiento")
        print("   Formato: FILA NÚMERO (ejemplo: A 1)")
        print("   O escribe 'salir' para cancelar")
        
        entrada = input("\n➤ Asiento: ").strip().upper()
        
        if entrada.lower() == 'salir':
            print("🔙 Cancelando selección de asiento...")
            return None
        
        try:
            partes = entrada.split()
            if len(partes) != 2:
                print("❌ Formato incorrecto. Usa: FILA NÚMERO (ejemplo: A 1)")
                input("Presiona ENTER para continuar...")
                continue
            
            fila_letra = partes[0]
            numero_asiento = int(partes[1])
            
            # Validar fila
            if fila_letra not in filas[:len(sala['asientos'])]:
                print(f"❌ Fila inválida. Usa letras de A a {filas[len(sala['asientos'])-1]}")
                input("Presiona ENTER para continuar...")
                continue
            
            fila_idx = filas.index(fila_letra)
            
            # Validar número de asiento
            if numero_asiento < 1 or numero_asiento > len(sala['asientos'][fila_idx]):
                print(f"❌ Número de asiento inválido. Usa números de 1 a {len(sala['asientos'][fila_idx])}")
                input("Presiona ENTER para continuar...")
                continue
            
            asiento_idx = numero_asiento - 1
            
            # Verificar si está disponible
            if sala['asientos'][fila_idx][asiento_idx] == 1:
                print(f"❌ El asiento {fila_letra}{numero_asiento} ya está ocupado.")
                input("Presiona ENTER para continuar...")
                continue
            
            # Asiento válido y disponible
            print(f"\n✅ Asiento seleccionado: {fila_letra}{numero_asiento}")
            return (fila_idx, asiento_idx)
        
        except (ValueError, IndexError):
            print("❌ Entrada inválida. Intenta de nuevo.")
            input("Presiona ENTER para continuar...")


def marcar_asiento_ocupado(sala: dict, fila: int, columna: int) -> bool:
    """
    Marca un asiento como ocupado (cambia 0 a 1).
    Retorna True si se pudo marcar, False si hubo error.
    """
    try:
        if sala['asientos'][fila][columna] == 0:
            sala['asientos'][fila][columna] = 1
            return True
        return False
    except (IndexError, KeyError):
        return False