from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_invoice(guest_name, check_in, check_out, price_per_night, template_path='templates/invoice_template.pdf', output_path=None):
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_path = f'invoice_{timestamp}.pdf'
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 50, "Factura")
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 100, f"Nume Oaspete: {guest_name}")
    c.drawString(100, height - 120, f"Check-in: {check_in.strftime('%Y-%m-%d')}")
    c.drawString(100, height - 140, f"Check-out: {check_out.strftime('%Y-%m-%d')}")
    nights = (check_out - check_in).days
    total_price = price_per_night * nights
    c.drawString(100, height - 160, f"Număr de nopți: {nights}")
    c.drawString(100, height - 180, f"Preț pe noapte: {price_per_night} RON")
    c.drawString(100, height - 200, f"Total: {total_price} RON")
    c.drawString(100, height - 220, f"Data: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(100, height - 240, "Vă mulțumim pentru alegerea noastră!")
    c.save()
    return output_path
