from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SalaHorario:
    salaId: int
    horario: str
    precio: float

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
            print(f"  🕒 Sala {sala['salaId']} - {sala['horario']} - ${sala['precio']}")
            
            
def seleccionar_pelicula(peliculas: List[Pelicula]) -> Optional[Pelicula]:
    
    while True:  
        mostrar_peliculas(peliculas)
        
        print("\n📝 Escribe el nombre de la película que deseas seleccionar")
        print("   (o escribe 'salir' para volver al menú principal)")
        
        nombre = input("➤ Película: ").strip()
        
        if nombre.lower() == 'salir':
            print("🔙 Volviendo al menú principal...")
            return None
        
        
        pelicula_encontrada = None
        for peli in peliculas:
            if peli['titulo'].lower() == nombre.lower():
                pelicula_encontrada = peli
                break
        
        if pelicula_encontrada:
            print(f"\n✅ Película seleccionada: {pelicula_encontrada['titulo']}")
            return pelicula_encontrada
        else:
            print(f"\n❌ No se encontró la película '{nombre}'.")
            print("Por favor, inténtalo de nuevo.\n")
            input("Presiona ENTER para continuar...")
            
            
            
            

            
    