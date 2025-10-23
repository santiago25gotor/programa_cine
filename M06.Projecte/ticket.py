from dataclasses import dataclass
from typing import List
import json
import os
import csv
from datetime import datetime
import random
import string

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
    precioTotal: float
    descuento: str
    tipoDescuento: str
    formato: str
    pelicula: str
    sala: int
    asientos: List[str]
    horario: str

def mostrar_tickets(tickets):
    print("\n💳 Tickets:")
    for t in tickets:
        print(f"- {t['idUser']} pagó {t['precioTotal']}€ con descuento {t['descuento']} ({t['tipoDescuento']})")
        for p in t['precio']:
            print(f"  Entrada {p['idEntrada']}: {p['precio']}€")


def generar_id_ticket():
    letra = random.choice(string.ascii_uppercase)
    numeros = random.randint(100, 999)
    return f"{letra}{numeros}"


def crear_ticket(idUser, pelicula, sala, asientos, horario, precio_unitario, cantidad_asientos, descuento=None):
   
    ticket_id = generar_id_ticket()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Crear lista de precios por entrada
    precios_entradas = []
    for i in range(cantidad_asientos):
        precios_entradas.append({
            "idEntrada": i + 1,
            "precio": precio_unitario
        })
    
    # Calcular precio total
    precio_total = precio_unitario * cantidad_asientos
    
    # Aplicar descuento si existe
    descuento_porcentaje = "0%"
    tipo_descuento = "Ninguno"
    
    if descuento:
        descuento_porcentaje = f"{descuento['descount']}%"
        tipo_descuento = descuento['name']
        precio_total = precio_total * (1 - float(descuento['descount']) / 100)
    
    ticket = {
        "id": ticket_id,
        "idUser": idUser,
        "timeStamp": timestamp,
        "pelicula": pelicula,
        "sala": sala,
        "asientos": asientos,
        "horario": horario,
        "precio": precios_entradas,
        "precioTotal": round(precio_total, 2),
        "descuento": descuento_porcentaje,
        "tipoDescuento": tipo_descuento,
    }
    
    return ticket


#22/10/25 - Función modificada para guardar en estructura de datos en memoria
def guardar_ticket_json(ticket, dbFilms, archivo="dbFilms.json"):
  
    try:
        # Añadir el ticket a la estructura de datos en memoria
        if 'ticket' not in dbFilms:
            dbFilms['ticket'] = []
        
        dbFilms['ticket'].append(ticket)
        
        # Guardar el archivo JSON actualizado
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(dbFilms, f, indent=2, ensure_ascii=False)
        
       # print(f"✅ Ticket guardado en {archivo}")
        return True
        
    except Exception as e:
        # print(f"❌ Error al guardar ticket en JSON: {e}")
        return False


def guardar_ticket_csv(ticket, archivo="tickets.csv"):
    
    try:
        # Verificar si el archivo existe para saber si escribir encabezados
        archivo_existe = os.path.isfile(archivo)
        
        # Preparar datos del ticket para CSV
        asientos_str = ", ".join(ticket['asientos'])
        
        # Calcular precio sin descuento
        precio_sin_descuento = sum([p['precio'] for p in ticket['precio']])
        
        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Escribir encabezados si el archivo es nuevo
            if not archivo_existe:
                writer.writerow([
                    'ID Ticket',
                    'Usuario',
                    'Fecha y Hora',
                    'Película',
                    'Sala',
                    'Asientos',
                    'Horario',
                    'Cantidad Entradas',
                    'Precio por Entrada',
                    'Precio Sin Descuento',
                    'Descuento',
                    'Tipo Descuento',
                    'Precio Total',
                ])
            
            # Escribir datos del ticket
            writer.writerow([
                ticket['id'],
                ticket['idUser'],
                ticket['timeStamp'],
                ticket['pelicula'],
                ticket['sala'],
                asientos_str,
                ticket['horario'],
                len(ticket['precio']),
                ticket['precio'][0]['precio'] if ticket['precio'] else 0,
                precio_sin_descuento,
                ticket['descuento'],
                ticket['tipoDescuento'],
                ticket['precioTotal']
            ])
        
        print(f"✅ Ticket guardado en {archivo}")
        return True
        
    except Exception as e:
        print(f"❌ Error al guardar ticket en CSV: {e}")
        return False


def mostrar_ticket(ticket):
    print("\n" + "="*60)
    print("🎫 TICKET DE COMPRA".center(60))
    print("="*60)
    print(f"🆔 ID Ticket:      {ticket['id']}")
    print(f"👤 Usuario:        {ticket['idUser']}")
    print(f"📅 Fecha:          {ticket['timeStamp']}")
    print("-"*60)
    print(f"🎬 Película:       {ticket['pelicula']}")
    print(f"🏢 Sala:           {ticket['sala']}")
    print(f"🕒 Horario:        {ticket['horario']}")
    print(f"💺 Asientos:       {', '.join(ticket['asientos'])}")
    print("-"*60)
    print(f"🎟️  Entradas:       {len(ticket['precio'])}")
    
    for entrada in ticket['precio']:
        print(f"   Entrada #{entrada['idEntrada']}: ${entrada['precio']}")
    
    print("-"*60)
    
    if ticket['tipoDescuento'] != "Ninguno":
        precio_sin_descuento = sum([p['precio'] for p in ticket['precio']])
        print(f"💰 Subtotal:       ${precio_sin_descuento:.2f}")
        print(f"🎁 Descuento:      {ticket['descuento']} ({ticket['tipoDescuento']})")
    
    print(f"💵 TOTAL PAGADO:   ${ticket['precioTotal']:.2f}")
    print("="*60)