from dataclasses import dataclass
from typing import List

@dataclass
class PrecioEntrada:
    idEntrada: int
    precio: float

@dataclass
class Ticket:
    id: str
    idUser: str
    timeStamp: str
    precio: List[PrecioEntrada]
    pretioTotal: float
    descuento: str
    tipoDescuento: str
    formato: str

def mostrar_tickets(tickets):
    print("\n💳 Tickets:")
    for t in tickets:
        print(f"- {t['idUser']} pagó {t['pretioTotal']}€ con descuento {t['descuento']} ({t['tipoDescuento']})")
        for p in t['precio']:
            print(f"  Entrada {p['idEntrada']}: {p['precio']}€")

