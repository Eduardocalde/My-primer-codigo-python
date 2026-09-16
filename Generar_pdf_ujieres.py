import os
from datetime import datetime
from PIL import Image as PILImage, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

def procesar_logo_transparente(ruta_origen, ruta_destino="logo_limpio.png"):
    """
    Toma la imagen del logo, elimina los bordes externos 
    y aplica un recorte circular/suave con transparencia (PNG).
    """
    try:
        img = PILImage.open(ruta_origen).convert("RGBA")
        
        # Crear máscara circular para recortar el marco blanco/sombra
        ancho, alto = img.size
        mask = PILImage.new('L', (ancho, alto), 0)
        draw = ImageDraw.Draw(mask)
        
        # Ajuste leve de margen interior (5% de recubrimiento para limpiar bordes)
        margin = int(min(ancho, alto) * 0.05)
        draw.ellipse((margin, margin, ancho - margin, alto - margin), fill=255)
        
        # Aplicar máscara y guardar
        img.putalpha(mask)
        img.save(ruta_destino, "PNG")
        return ruta_destino
    except Exception:
        return ruta_origen

def obtener_rotacion_semanal(numero_semana):
    agua_semana = ["Jeniffer Guerra", "Jenny Maurera"]
    idx_agua = numero_semana % len(agua_semana)
    agua_martes = agua_semana[idx_agua]
    agua_jueves = agua_semana[(idx_agua + 1) % len(agua_semana)]

    apoyo = ["Obdalis Martinez", "Merki Calderon", "Jesus Rodriguez"]
    idx_ap = numero_semana % len(apoyo)
    p_martes = apoyo[idx_ap]
    e_martes = apoyo[(idx_ap + 1) % len(apoyo)]
    b_martes = apoyo[(idx_ap + 2) % len(apoyo)]

    return [
        {"dia": "Martes",  "puerta": p_martes, "agua": agua_martes, "escalera": e_martes, "baños": b_martes},
        {"dia": "Jueves",  "puerta": "Yendery Guerra", "agua": agua_jueves, "escalera": "Karelys de Rodriguez", "baños": "Jesus Rodriguez"},
        {"dia": "Viernes", "puerta": "Karelys de Rodriguez", "agua": agua_martes, "escalera": "Merki Calderon", "baños": "Yendery Guerra"},
        {"dia": "Sábado",  "puerta": "LIBRE", "agua": "LIBRE", "escalera": "LIBRE", "baños": "LIBRE"},
        {"dia": "Domingo", "puerta": "Nakary Torres", "agua": "Obdalis Martinez", "escalera": "Jeniffer Guerra", "baños": "Jesus Rodriguez"}
    ]

def generar_pdf_oficial(nombre_archivo="Cronograma_Ujieres_Oficial.pdf"):
    doc = SimpleDocTemplate(
        nombre_archivo,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    elementos = []
    estilos = getSampleStyleSheet()

    COLOR_AZUL = colors.HexColor('#1A2B4C')
    COLOR_DORADO = colors.HexColor('#D4AF37')
    COLOR_GRIS_CLARO = colors.HexColor('#F9F9FB')
    COLOR_VERDE = colors.HexColor('#2E7D32')

    # Estilos de Texto
    estilo_iglesia = ParagraphStyle('TIglesia', parent=estilos['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=COLOR_AZUL, alignment=1)
    estilo_titulo = ParagraphStyle('T1', parent=estilos['Heading1'], fontName='Helvetica-Bold', fontSize=16, textColor=COLOR_AZUL, alignment=1)
    estilo_lema = ParagraphStyle('T2', parent=estilos['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=COLOR_DORADO, alignment=1)
    estilo_cita = ParagraphStyle('T3', parent=estilos['Italic'], fontName='Helvetica-Oblique', fontSize=8.5, textColor=colors.HexColor('#444444'), alignment=1)
    estilo_header = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=1)
    estilo_celda = ParagraphStyle('TC', fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#222222'), alignment=1)
    estilo_libre = ParagraphStyle('TL', fontName='Helvetica-Bold', fontSize=9, textColor=COLOR_VERDE, alignment=1)
    estilo_bendicion = ParagraphStyle('TB', fontName='Helvetica-BoldOblique', fontSize=11, textColor=COLOR_AZUL, alignment=1, spaceBefore=14)

    # 1. PROCESAMIENTO Y BÚSQUEDA DEL LOGO
    logo_path = None
    posibles_nombres = [
        "logo.jpg.jpg",
        "logo.jpg", 
        "logo.png", 
        "logo.jpeg", 
        "17895273626162159072203567740934_92b923.jpg"
    ]
    
    for nombre in posibles_nombres:
        if os.path.exists(nombre):
            # Procesa la imagen para quitar el fondo/recuadrar
            logo_path = procesar_logo_transparente(nombre)
            break

    bloque_texto_header = [
        Paragraph("IGLESIA EVANGÉLICA PENTECOSTÉS \"MANANTIAL DE LUZ\"", estilo_iglesia),
        Spacer(1, 3),
        Paragraph("MINISTERIO DE UJIERES", estilo_titulo),
        Spacer(1, 3),
        Paragraph('"HONRANDO A DIOS CON MI SERVICIO" (Col. 3:23-24)', estilo_lema)
    ]

    if logo_path and os.path.exists(logo_path):
        img_logo = Image(logo_path, width=80, height=80)
        header_tabla = Table([[img_logo, bloque_texto_header]], colWidths=[85, 455])
        header_tabla.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        elementos.append(header_tabla)
    else:
        elementos.extend(bloque_texto_header)

    elementos.append(Spacer(1, 12))

    # 2. SUBTÍTULO Y CITA BÍBLICA
    fecha_actual = datetime.now()
    num_semana = fecha_actual.isocalendar()[1]
    
    info_sub = (
        f"<b>Cronograma Semanal Rotativo — Semana N° {num_semana} ({fecha_actual.strftime('%d/%m/%Y')})</b><br/>"
        '<i>"Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien..." — Romanos 8:28</i>'
    )
    elementos.append(Paragraph(info_sub, estilo_cita))
    elementos.append(Spacer(1, 10))

    # 3. TABLA DEL CRONOGRAMA
    datos_semana = obtener_rotacion_semanal(num_semana)

    tabla_datos = [[
        Paragraph("<b>Día / Servicio</b>", estilo_header),
        Paragraph("<b>Puerta</b>", estilo_header),
        Paragraph("<b>Agua</b>", estilo_header),
        Paragraph("<b>Escalera</b>", estilo_header),
        Paragraph("<b>Baños</b>", estilo_header)
    ]]

    for fila in datos_semana:
        if fila['puerta'] == "LIBRE":
            tabla_datos.append([
                Paragraph(f"<b>{fila['dia']}</b>", estilo_celda),
                Paragraph("<b>LIBRE</b>", estilo_libre),
                Paragraph("<b>LIBRE</b>", estilo_libre),
                Paragraph("<b>LIBRE</b>", estilo_libre),
                Paragraph("<b>LIBRE</b>", estilo_libre)
            ])
        else:
            tabla_datos.append([
                Paragraph(f"<b>{fila['dia']}</b>", estilo_celda),
                Paragraph(fila['puerta'], estilo_celda),
                Paragraph(fila['agua'], estilo_celda),
                Paragraph(fila['escalera'], estilo_celda),
                Paragraph(fila['baños'], estilo_celda)
            ])

    tabla = Table(tabla_datos, colWidths=[100, 110, 110, 110, 110])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_AZUL),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 1, COLOR_DORADO),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_GRIS_CLARO])
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph("¡Dios les bendiga, querido equipo de Ujieres!", estilo_bendicion))

    doc.build(elementos)
    print(f"✅ ¡PDF oficial generado con éxito: {nombre_archivo}!")

    try:
        os.system(f'start {nombre_archivo}')
    except Exception:
        pass

if __name__ == "__main__":
    generar_pdf_oficial()
