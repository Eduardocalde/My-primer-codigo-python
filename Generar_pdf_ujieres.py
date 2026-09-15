import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def exportar_cronograma_pdf(datos_cronograma, nombre_archivo="Cronograma_Ujieres.pdf"):
    # 1. Configuración del documento PDF (Hoja Carta, márgenes limpios)
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

    # 2. Estilos personalizados para el texto
    estilo_titulo = ParagraphStyle(
        'TituloCronograma',
        parent=estilos['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#1A2B4C'),
        alignment=1, # Centrado
        spaceAfter=6
    )

    estilo_subtitulo = ParagraphStyle(
        'SubtituloCronograma',
        parent=estilos['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=20
    )

    estilo_encabezado_tabla = ParagraphStyle(
        'HeaderTabla',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.white,
        alignment=1
    )

    estilo_celda = ParagraphStyle(
        'CeldaTabla',
        fontName='Helvetica',
        fontSize=9,
        textColor=colors.HexColor('#333333'),
        alignment=1
    )

    # 3. Título y Subtítulo del Documento
    elementos.append(Paragraph("CRONOGRAMA DE UJIERES", estilo_titulo))
    elementos.append(Paragraph("Asignación de roles por servicio semanal", estilo_subtitulo))

    # 4. Construcción de los datos de la tabla
    # Encabezado
    tabla_datos = [[
        Paragraph("<b>Día</b>", estilo_encabezado_tabla),
        Paragraph("<b>Puerta</b>", estilo_encabezado_tabla),
        Paragraph("<b>Agua</b>", estilo_encabezado_tabla),
        Paragraph("<b>Escalera</b>", estilo_encabezado_tabla),
        Paragraph("<b>Baños</b>", estilo_encabezado_tabla)
    ]]

    # Filas con la asignación
    for fila in datos_cronograma:
        fila_formateada = [
            Paragraph(f"<b>{fila['dia']}</b>", estilo_celda),
            Paragraph(fila['puerta'], estilo_celda),
            Paragraph(fila['agua'], estilo_celda),
            Paragraph(fila['escalera'], estilo_celda),
            Paragraph(fila['baños'], estilo_celda)
        ]
        tabla_datos.append(fila_formateada)

    # Ancho de columnas (Distribución equilibrada en la página)
    anchos_columnas = [90, 110, 110, 110, 110]

    # 5. Creación y Estilizado de la Tabla
    tabla = Table(tabla_datos, colWidths=anchos_columnas)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A2B4C')), # Azul oscuro para el header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D3D3D3')), # Líneas de cuadrícula suaves
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]) # Filas alternadas
    ]))

    elementos.append(tabla)

    # 6. Guardar y generar el PDF
    doc.build(elementos)
    print(f"✅ ¡PDF generado con éxito: {nombre_archivo}!")

# --- DATOS DE PRUEBA ---
datos_ejemplo = [
    {"dia": "Martes",   "puerta": "Carlos Pérez",  "agua": "María Gómez",   "escalera": "Luis Rivas",   "baños": "Ana Torres"},
    {"dia": "Jueves",   "puerta": "José López",    "agua": "Elena Díaz",    "escalera": "Pedro Silva",  "baños": "Sonia Ruiz"},
    {"dia": "Viernes",  "puerta": "Raúl Castro",   "agua": "Carmen Rojas",  "escalera": "Diego Soto",   "baños": "Laura Peña"},
    {"dia": "Domingo",  "puerta": "Gabriel Vera",  "agua": "Patricia Gil",  "escalera": "Jorge Mendoza","baños": "Rosa Blanco"}
]

# Ejecutar función
if __name__ == "__main__":
    exportar_cronograma_pdf(datos_ejemplo)
