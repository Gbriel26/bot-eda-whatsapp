from fpdf import FPDF
import smtplib
from email.message import EmailMessage
from datetime import datetime
import locale

class ReportePDF(FPDF):
    def header(self):
        # Encabezado (Azul oscuro profundo)
        self.set_fill_color(0, 51, 153) 
        self.rect(0, 0, 210, 35, 'F')
        
        # Título principal
        self.set_y(10)
        self.set_font('Arial', 'B', 16)
        self.set_text_color(255, 255, 255) # Texto blanco
        self.cell(0, 8, 'INFORME - ANÁLISIS EXPLORATORIO DE DATOS', 0, 1, 'C')
        
        # Subtítulo
        self.set_font('Arial', 'I', 11)
        self.cell(0, 8, 'Equipo Consultor: LUIS OVIEDO DIAZ & JOSUE BURGOS', 0, 1, 'C')
        
        # Fecha de emisión automática
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        self.set_font('Arial', '', 10)
        self.cell(0, 8, f'Fecha de emisión: {fecha_actual}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Pie de página a 1.5 cm desde el fondo
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()} | Generado por Motor Analítico de Python - Electiva de Profundización IV', 0, 0, 'C')

def crear_pdf_y_enviar(texto_eda, rutas_imagenes, correo_destino):
    pdf = ReportePDF()
    pdf.add_page()
    
    # Procesamiento inteligente de texto
    lineas = texto_eda.split('\n')
    for linea in lineas:
        if linea.strip():
            if linea[0].isdigit() and "." in linea[:3]:
                pdf.set_font('Arial', 'B', 12)
                pdf.set_text_color(0, 51, 153) # Azul oscuro para los subtítulos
                pdf.cell(0, 10, linea, 0, 1, 'L')
            else:
                # Texto normal del reporte
                pdf.set_font('Arial', '', 11)
                pdf.set_text_color(50, 50, 50) # Gris muy oscuro (facilita lectura)
                pdf.multi_cell(0, 6, linea)
                pdf.ln(2)
        else:
            pdf.ln(2)
    
    # Agregar imágenes centradas y estandarizadas
    pdf.ln(5)
    for img in rutas_imagenes:
        pdf.image(img, x=35, w=140)
        pdf.ln(5)
        
    ruta_pdf = "Reporte_Final.pdf"
    pdf.output(ruta_pdf)
    
    # Lógica de envío de correo
    msg = EmailMessage()
    msg['Subject'] = 'Su Reporte Gerencial de Análisis de Datos'
    msg['From'] = 'luisgabriel200424@gmail.com'
    msg['To'] = correo_destino
    msg.set_content('Cordial saludo.\n\nAdjunto encontrará el informe gerencial con el Análisis Exploratorio de Datos solicitado.\n\nAtentamente,\nEquipo de Consultoría.')

    with open(ruta_pdf, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=ruta_pdf)

    # Configuración SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        # CORREO Y CLAVE DE SEGURIDAD DE 16 LETRAS 
        smtp.login('luisgabriel200424@gmail.com', 'uplumnjxgvmdojnm') 
        smtp.send_message(msg)
