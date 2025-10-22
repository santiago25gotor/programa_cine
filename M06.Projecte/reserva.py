from dataclasses import dataclass
from typing import List
from datetime import datetime
import json
import random
import string

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


#22/10/25 
def generar_id_reserva():
    letra = random.choice(string.ascii_uppercase)
    numeros = random.randint(100, 999)
    return f"{letra}{numeros}"


#22/10/25 -  para crear reserva
def crear_reserva(idUser, sala, asientos, pelicula, formato="4K"):
   
    reserva_id = generar_id_reserva()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    asientos_str = ", ".join(asientos)
    
    reserva = {
        "id": reserva_id,
        "idUser": idUser,
        "timeStamp": timestamp,
        "sala": sala,
        "asiento": asientos_str,
        "pelicula": pelicula,
        "formato": formato
    }
    
    return reserva

#22/10/25 -  guardar reserva en JSON
def guardar_reserva_json(reserva, dbFilms, archivo="dbFilms.json"):
   
    try:
        # Añadir la reserva a la estructura de datos en memoria
        if 'reserva' not in dbFilms:
            dbFilms['reserva'] = []
        
        dbFilms['reserva'].append(reserva)
        
        # Guardar el archivo JSON actualizado
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(dbFilms, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Reserva guardada en {archivo}")
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar reserva en JSON: {e}")
        return False


# 22/10/2025 - Buscar reserva por ID
def buscar_reserva_por_id(reservas, id_reserva):
   
    for reserva in reservas:
        if reserva['id'] == id_reserva:
            return reserva
    
    return None


# 22/10/2025 -  Mostrar una reserva detallada
def mostrar_reserva_detallada(reserva):
    """
    Muestra los detalles completos de una reserva
    """
    print("\n" + "="*60)
    print("📋 DETALLES DE LA RESERVA".center(60))
    print("="*60)
    print(f"🆔 ID Reserva:     {reserva['id']}")
    print(f"👤 Usuario:        {reserva['idUser']}")
    print(f"📅 Fecha:          {reserva['timeStamp']}")
    print("-"*60)
    print(f"🎬 Película:       {reserva['pelicula']}")
    print(f"🏢 Sala:           {reserva['sala']}")
    print(f"💺 Asientos:       {reserva['asiento']}")
    print(f"📺 Formato:        {reserva['formato']}")
    print("="*60)


# 22/10/2025 - El ticket esta hecho para buscar solo por id
def proceso_buscar_reserva(dbFilms):
   
    if 'reserva' not in dbFilms or len(dbFilms['reserva']) == 0:
        print("\n❌ No hay reservas registradas en el sistema.")
        input("\nPresiona ENTER para continuar...")
        return
    
    print("\n" + "="*60)
    print("🔍 BUSCAR RESERVA POR ID".center(60))
    print("="*60)
    print("\n💡 El ID de tu reserva se mostró al confirmar la compra")
    print("   Ejemplo: V157")
    
    id_reserva = input("\n🆔 Ingresa el ID de tu reserva (o 'salir' para volver): ").strip()
    
    if id_reserva.lower() == 'salir':
        print("🔙 Volviendo al menú principal...")
        return
    
    if not id_reserva:
        print("❌ Debes ingresar un ID.")
        input("\nPresiona ENTER para continuar...")
        return
    
    reserva = buscar_reserva_por_id(dbFilms['reserva'], id_reserva)
    
    if reserva:
        print("\n✅ Reserva encontrada:")
        mostrar_reserva_detallada(reserva)
    else:
        print(f"\n❌ No se encontró ninguna reserva con el ID '{id_reserva}'.")
        print("   Verifica que el ID sea correcto.")
    
    input("\nPresiona ENTER para continuar...")