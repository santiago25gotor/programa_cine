# Sistema de Reservas de Cine

Sistema completo de gestión de reservas para cines con interfaz de consola y GUI interactiva usando Pygame. Permite gestionar películas, salas, horarios, asientos y descuentos de forma intuitiva.

##  Características Principales

###  Funcionalidades Core
- **Gestión de Películas**: Catálogo completo con información de género, duración y horarios
- **Sistema de Salas**: Múltiples salas con gestión independiente de asientos por función
- **Reservas Inteligentes**: Sistema único de funciones (película + sala + horario)
- **Asientos Visuales**: Visualización clara del estado de cada asiento en tiempo real
- **Descuentos Flexibles**: Sistema de descuentos aplicables (joven, +65, bono cultural)
- **Generación de Tickets**: Tickets en PDF con código QR para validación
- **Exportación CSV**: Registro de todas las transacciones en formato CSV

###  Interfaces Disponibles

#### 1. Interfaz de Consola (`main.py`)
Interfaz tradicional basada en texto con menús interactivos.

#### 2. Interfaz Gráfica (`main_imgui_pygame.py`)
GUI moderna con Pygame que incluye:
- Visualización de asientos en tiempo real
- Selección de múltiples asientos
- Aplicación de descuentos
- Búsqueda de reservas
- Recomendación de asientos centrales

##  Requisitos

### Python
- Python 3.8 o superior

### Dependencias Base
```bash
pip install reportlab qrcode[pil]
```

### Para Interfaz Gráfica (Pygame)
```bash
pip install pygame
```

##  Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/sistema-cine.git
cd sistema-cine
```

### 2. Instalar Dependencias

**Opción A - Solo Consola:**
```bash
pip install reportlab qrcode[pil]
```

**Opción B - Con Interfaz Gráfica:**
```bash
pip install reportlab qrcode[pil] pygame
```

### 3. Verificar Archivos
Asegúrate de que existe el archivo `dbFilms.json` en el directorio principal.

## Uso

### Interfaz de Consola
```bash
python main.py
```

**Opciones del menú:**
1. 🎥 Buscar películas y reservar
2. 🎟️ Buscar mi ticket
3. 💰 Ver descuentos disponibles
4. ❌ Salir

### Interfaz Gráfica (Pygame)
```bash
python main_imgui_pygame.py
```

**Características GUI:**
- Clic en películas para seleccionar
- Visualización de salas y horarios disponibles
- Selección visual de asientos
- Aplicación de descuentos con un clic
- Confirmación instantánea de reservas

##  Estructura del Proyecto

```
sistema-cine/
│
├── main.py                      # Interfaz de consola
├── main_imgui_pygame.py        # Interfaz gráfica (Pygame)
│
├── pelicula.py                 # Gestión de películas
├── sala.py                     # Gestión de salas y asientos
├── reserva.py                  # Sistema de reservas
├── ticket.py                   # Generación de tickets
├── descuento.py               # Sistema de descuentos
├── generar_ticket.py          # Generación de PDF con QR
│
├── dbFilms.json               # Base de datos principal
└── tickets.csv                # Registro de tickets (generado)
```

## 🗂️ Estructura de Datos

### Películas
```json
{
  "id": 101,
  "titulo": "Matrix",
  "duracion": 120,
  "genero": "Ciencia Ficción",
  "salas": [
    {
      "salaId": 1,
      "horario": "18:00",
      "precio": 9.5
    }
  ]
}
```

### Sistema de Funciones
El sistema gestiona cada función (película + sala + horario) de forma **independiente**:
```json
{
  "funciones": {
    "pelicula_101_sala_1_horario_1800": [
      [0, 0, 1, 0],
      [1, 0, 0, 0],
      [0, 0, 0, 1]
    ]
  }
}
```

*Donde:* 
- `0` = Asiento disponible
- `1` = Asiento ocupado

### Descuentos Disponibles
- **Joven**: 20% de descuento
- **+65**: 50% de descuento
- **Bono Cultural**: 40% de descuento

## Generación de Tickets

Cada reserva genera:

1. **PDF con código QR** (`ticket_[ID].pdf`)
   - Información completa de la reserva
   - Código QR para validación
   - Diseño profesional y legible

2. **Registro en CSV** (`tickets.csv`)
   - Histórico de todas las transacciones
   - Fácil importación a Excel/Google Sheets

3. **Entrada en JSON** (actualización de `dbFilms.json`)
   - Persistencia de datos
   - Sincronización entre sesiones

## Funcionalidades Avanzadas

### Sistema de Asientos Inteligente
- Detección automática del asiento más centrado
- Validación en tiempo real de disponibilidad
- Prevención de reservas duplicadas
- Gestión independiente por función

### Búsqueda de Reservas
Busca tus reservas por ID único:
```
ID Ejemplo: A923, X671, D743
```

### Persistencia de Datos
Todos los cambios se guardan automáticamente en:
- `dbFilms.json` - Base de datos principal
- `tickets.csv` - Registro de tickets


### Interfaz de Consola
```
=== RESUMEN DE TU RESERVA ===
🎬 Película: Matrix
🏢 Sala: Sala 1
🕒 Horario: 18:00
💥 Personas: 2
💰 Precio/persona: $9.50
💵 TOTAL A PAGAR: $19.00
```

### Interfaz Gráfica
- Visualización de asientos en formato matricial
- Colores intuitivos (verde=libre, rojo=ocupado, azul=seleccionado)
- Pantalla de cine simulada
- Recomendación del mejor asiento

##  Configuración

### Personalizar Salas
Edita `dbFilms.json` para añadir/modificar salas:
```json
{
  "id": 5,
  "nombre": "Sala VIP",
  "asientos": [
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ]
}
```

### Añadir Películas
```json
{
  "id": 110,
  "titulo": "Nueva Película",
  "duracion": 150,
  "genero": "Acción",
  "salas": [
    {
      "salaId": 1,
      "horario": "20:00",
      "precio": 10.0
    }
  ]
}
```

### Crear Descuentos
```json
{
  "id": "4",
  "name": "estudiante",
  "description": "Descuento para estudiantes",
  "descount": "30"
}
```

##  Solución de Problemas

### Error: "No se pudo cargar el archivo JSON"
**Solución:** Verifica que `dbFilms.json` existe y tiene formato válido.

### Error: "Módulo 'pygame' no encontrado"
**Solución:** 
```bash
pip install pygame
```

### Error: "Módulo 'reportlab' no encontrado"
**Solución:**
```bash
pip install reportlab qrcode[pil]
```

### Asientos no se actualizan
**Solución:** El sistema guarda automáticamente. Si persiste, verifica permisos de escritura en `dbFilms.json`.

## Notas Importantes

- El sistema utiliza **codificación UTF-8** para soportar caracteres especiales
- Cada función (película + sala + horario) tiene su **propia matriz de asientos**
- Los IDs de reserva son **únicos y aleatorios** (formato: Letra + 3 números)
- Los tickets PDF incluyen **código QR** con toda la información de la reserva
- El archivo `tickets.csv` se actualiza automáticamente con cada venta



## Autores

- Cindy Tot, Sergi Fernandez, Santiago Gotor


⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

📧 Para consultas o sugerencias: tu-email@ejemplo.com
