# Bot de WhatsApp para Análisis Exploratorio de Datos (EDA)

##  Descripción
Este proyecto es un bot automatizado de WhatsApp desarrollado para la asignatura **Electiva de Profundización IV**. Permite a los usuarios enviar un enlace de un conjunto de datos público (vía JSON, CSV o XLSX), procesarlo dinámicamente y generar un reporte gerencial en formato PDF que es enviado directamente por correo electrónico.

## Tecnologías y Arquitectura
* **Lenguaje Core:** Python 3.x
* **Framework Web:** Flask
* **Motor Analítico:** Pandas, Matplotlib, Seaborn
* **Integraciones y APIs:** Twilio Sandbox (WhatsApp), servidor SMTP (Correos)
* **Base de Datos:** PostgreSQL alojada en la nube (Neon.tech) para auditoría e historial de conversaciones.
* **Túnel Local:** Ngrok

## Instalación y Despliegue Local

Para ejecutar este proyecto en un entorno local, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/bot-eda-whatsapp.git](https://github.com/TU_USUARIO/bot-eda-whatsapp.git)
   cd bot-eda-whatsapp
2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Mac/Linux:
   source venv/bin/activate
3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
4. **Configurar Variables de Entorno:**
   Crea un archivo .env en la raíz del proyecto y configura las credenciales (Base de Datos y Correo SMTP).
5. **Ejecutar el servidor Flask:**
   ```bash
   python app.py

# Autores
[LUIS OVIEDO DIAZ]

[JOSUE BURGOS]
