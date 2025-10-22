from dataclasses import dataclass
from typing import List

@dataclass
class Descuento:
    id: str
    name: str
    description: str
    descount: str
    
def mostrar_descuentos(descuentos):
    print("\n🎁 Descuentos disponibles:")
    for d in descuentos:
        print(f"- {d['name']} ({d['descount']}%): {d['description']}")
