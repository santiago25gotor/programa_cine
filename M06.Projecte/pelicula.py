from dataclasses import dataclass
from typing import List

@dataclass
class SalaHorario:
    salaId: int
    horario: str

@dataclass
class Pelicula:
    id: int
    titulo: str
    duracion: int
    genero: str
    salas: List[SalaHorario]

def mostrar_peliculas(peliculas: List[Pelicula]):
    print("\n🎬 Películas:")
    for peli in peliculas:
        print(f"- {peli['titulo']} ({peli['genero']}, {peli['duracion']} min)")
        for sala in peli['salas']:
            print(f"  🕒 Sala {sala['salaId']} - {sala['horario']}")
