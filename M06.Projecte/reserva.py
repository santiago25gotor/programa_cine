from dataclasses import dataclass
from typing import List

@dataclass
class Reserva:
    id: str
    idUser: str
    timeStamp: str
    sala: int
    asiento: str
    pelicula: str
    formato: str

def mostrar_reservas(reservas):
    print("\n📌 Reservas:")
    for r in reservas:
        print(f"- {r['idUser']} reservó '{r['pelicula']}' en sala {r['sala']}, asiento {r['asiento']} a las {r['timeStamp']} (formato: {r['formato']})")

