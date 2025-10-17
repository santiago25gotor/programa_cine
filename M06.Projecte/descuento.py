from dataclasses import dataclass
from typing import List

@dataclass
class Descuento:
    id: str
    name: str
    description: str
    descount: str  # porcentaje (string numérico)

def mostrar_descuentos(descuentos):
    print("\n🎁 Descuentos disponibles:")
    for d in descuentos:
        print(f"- {d['name']} ({d['descount']}%): {d['description']}")

def aplicar_descuento(descuentos, precio_base):
    """
    Permite aplicar un descuento escribiendo su nombre (por ejemplo 'joven', '+65', etc.).
    """
    if not descuentos:
        print("⚠️ No hay descuentos disponibles en este momento.")
        return None, precio_base

    mostrar_descuentos(descuentos)
    nombre = input("\nEscribe el nombre del descuento (o 0 para cancelar): ").strip().lower()
    if nombre == "0":
        return None, precio_base

    # Buscar descuento por nombre
    descuento_seleccionado = None
    for d in descuentos:
        if d['name'].lower() == nombre:
            descuento_seleccionado = d
            break

    if not descuento_seleccionado:
        print("❌ Descuento no encontrado. No se aplicará ningún descuento.")
        return None, precio_base

    porcentaje = float(descuento_seleccionado['descount'])
    precio_final = round(precio_base * (1 - porcentaje / 100), 2)

    # 💸 Mostrar precios formateados a 2 decimales
    print(f"\n💸 Precio original: ${precio_base:.2f}")
    print(f"🏷️ Descuento aplicado: {porcentaje:.0f}%")
    print(f"✅ Nuevo precio con descuento: ${precio_final:.2f}")

    return descuento_seleccionado, precio_final
