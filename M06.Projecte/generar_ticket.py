## tutorial de como instalar el reportlab y qrcode
### pasar a python versión 10
# pip install qrcode[pil] y pip install reportlab



from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from datetime import datetime
import qrcode
import io

def generar_ticket(reserva, descuento):
    """
    Genera un PDF profesional con QR para la reserva de cine.
    """
    # --- Crear QR ---
    qr_data = (
        f"Reserva ID: {reserva['id']}\n"
        f"Usuario: {reserva['idUser']}\n"
        f"Hora: {reserva['timeStamp']}\n"
        f"Sala: {reserva['sala']}\n"
        f"Asiento: {reserva['asiento']}\n"
        f"Película: {reserva['pelicula']}\n"
        f"Formato: {reserva['formato']}"
    )
    qr_img = qrcode.make(qr_data)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_reader = ImageReader(qr_buffer)

    # --- Crear PDF ---
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A6)

    # --- Diseño base ---
    c.setFillColor(colors.HexColor("#ffffff"))
    c.rect(0, 0, 105*mm, 148*mm, stroke=0, fill=1)  # fondo blanco

    # Borde sutil
    c.setStrokeColor(colors.HexColor("#DDDDDD"))
    c.setLineWidth(0.5)
    c.rect(5*mm, 5*mm, 95*mm, 138*mm)

    # --- Encabezado ---
    c.setFillColor(colors.HexColor("#1E1E1E"))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(52.5*mm, 135*mm, "CINE CAPRI")

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#555555"))
    c.drawCentredString(52.5*mm, 128*mm, "Confirmación de reserva")

    # Línea divisoria
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.line(10*mm, 125*mm, 95*mm, 125*mm)

    # --- Datos principales ---
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#222222"))
    c.drawString(10*mm, 115*mm, f"🎬 {reserva['pelicula']}")

    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#333333"))
    c.drawString(10*mm, 105*mm, f"Sala: {reserva['sala']}    Asiento: {reserva['asiento']}")
    c.drawString(10*mm, 96*mm, f"Codigo: {reserva['id']}")
    c.drawString(10*mm, 87*mm, f"Fecha/Hora: {reserva['timeStamp']}")
    c.drawString(10*mm, 78*mm, f"Formato: {reserva['formato']}")

    # --- Descuento (si existe) ---
    if descuento:
        c.setFillColor(colors.HexColor("#E63946"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(10*mm, 77*mm, f"Descuento aplicado: {descuento['name']} ({descuento['descount']}%)")

    # --- QR ---
    c.drawImage(qr_reader, 60*mm, 20*mm, width=35*mm, height=35*mm, mask='auto')

    # --- Pie ---
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.line(10*mm, 18*mm, 95*mm, 18*mm)

    c.setFont("Helvetica-Oblique", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawCentredString(
        52.5*mm,
        12*mm,
        f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )

    c.save()

    # --- Guardar archivo ---
    nombre_archivo = f"ticket_{reserva['id']}.pdf"
    with open(nombre_archivo, "wb") as f:
        f.write(buffer.getvalue())

    print(f"✅ Ticket PDF generado con éxito: {nombre_archivo}")
