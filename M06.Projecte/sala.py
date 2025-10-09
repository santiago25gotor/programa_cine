from dataclasses import dataclass
from typing import List

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
