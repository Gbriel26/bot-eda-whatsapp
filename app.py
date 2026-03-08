from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from eda_core import AnalizadorExploratorio
from generador_pdf import crear_pdf_y_enviar
import db_core  
import os

app = Flask(__name__)

# Diccionario en memoria para manejar el estado de cada número de teléfono
sesiones = {}

@app.route("/webhook", methods=['POST'])
def whatsapp_webhook():
    telefono = request.values.get('From', '')
    mensaje = request.values.get('Body', '').strip()
    resp = MessagingResponse()

    # No aceptar campos vacíos
    if not mensaje:
        resp.message("Error: No puede dejar campos vacíos. Por favor responda a la pregunta anterior.")
        return str(resp)

    # Inicializar sesión si el número nos escribe por primera vez
    if telefono not in sesiones:
        sesiones[telefono] = {"estado": "inicio"}

    estado_actual = sesiones[telefono]["estado"]

    # MÁQUINA DE ESTADOS SECUENCIAL

    if estado_actual == "inicio":
        resp.message("¿Hola como estas? ¿Como te llamas?")
        sesiones[telefono]["estado"] = "esperando_nombre"

    elif estado_actual == "esperando_nombre":
        nombre_usuario = mensaje
        sesiones[telefono]["nombre"] = nombre_usuario
        
        # GUARDAR EN BASE DE DATOS: Inicia la conversación
        id_db = db_core.registrar_inicio_chat(telefono, nombre_usuario)
        sesiones[telefono]["id_db"] = id_db
        
        resp.message(f"Entendido, {nombre_usuario}. ¿Deseas realizar un análisis exploratorio de datos? Si o no")
        sesiones[telefono]["estado"] = "esperando_confirmacion"

    elif estado_actual == "esperando_confirmacion":
        if mensaje.lower() in ["no", "n"]:
            resp.message("Gracias por usar nuestros servicios. Hasta luego.")
            del sesiones[telefono] 
        elif mensaje.lower() in ["si", "s", "sí"]:
            resp.message("1.-Datos medianos o pequeños con Pandas con CSV o\n2.-Datos medianos o pequeños con Pandas con XLSX\n\nPor favor, copie y pegue el link de la data (API JSON, CSV o XLSX):")
            sesiones[telefono]["estado"] = "esperando_url"
        else:
            resp.message("Respuesta no válida. ¿Deseas realizar un análisis exploratorio de datos? Si o no")

    elif estado_actual == "esperando_url":
        url = mensaje
        sesiones[telefono]["url"] = url
        
        # Instanciamos el EDA y cargamos los datos
        analizador = AnalizadorExploratorio(url)
        if analizador.cargar_datos():
            sesiones[telefono]["analizador"] = analizador # Guardamos el objeto para usarlo después
            columnas_disponibles = ", ".join(analizador.df.columns.tolist())
            
            respuesta = "Conjunto de datos cargados exitosamente.\n"
            respuesta += "Se tienen las siguientes columnas:\n"
            respuesta += f"{columnas_disponibles}\n\n"
            respuesta += "Indique sus columnas CUANTITATIVAS (escríbalas separadas por coma):"
            
            resp.message(respuesta)
            sesiones[telefono]["estado"] = "esperando_cuantitativas"
        else:
            resp.message("Error al cargar la data. Verifique el link y vuelva a enviarlo.")

    elif estado_actual == "esperando_cuantitativas":
        sesiones[telefono]["cuantitativas"] = mensaje
        resp.message("Indique sus columnas CUALITATIVAS (escríbalas separadas por coma):")
        sesiones[telefono]["estado"] = "esperando_cualitativas"

    elif estado_actual == "esperando_cualitativas":
        sesiones[telefono]["cualitativas"] = mensaje
        
        # Procesamos los gráficos y el texto con las columnas que dio el usuario
        analizador = sesiones[telefono]["analizador"]
        resultados = analizador.procesar_analisis(
            sesiones[telefono]["cuantitativas"], 
            sesiones[telefono]["cualitativas"]
        )
        sesiones[telefono]["resultados"] = resultados
        sesiones[telefono]["estado"] = "esperando_correo"
        
        resp.message("Generando análisis exploratorio en un informe en PDF. Espere unos minutos por favor...\n\nInforme generado. Indique su correo electrónico para enviarlo:")

    elif estado_actual == "esperando_correo":
        correo = mensaje
        resp.message("Un momento por favor, se esta enviando el informe a su correo...")
        
        # Extraer datos guardados
        datos_eda = sesiones[telefono]["resultados"]
        nombre_usuario = sesiones[telefono]["nombre"]
        
        # Generar PDF y Enviar
        crear_pdf_y_enviar(datos_eda["texto"], datos_eda["imagenes"], correo)
        
        # GUARDAR EN BASE DE DATOS: Fin de la conversación
        db_core.registrar_fin_chat(
            sesiones[telefono].get("id_db"), 
            sesiones[telefono]["url"], 
            correo
        )
        
        resp.message("Informe enviado.")
        resp.message(f"Muchas gracias por usar nuestros servicios señor(a) {nombre_usuario}")
        
        # Limpiar datos para que el usuario pueda volver a empezar
        del sesiones[telefono] 

    return str(resp)

if __name__ == "__main__":
    # Creamos la carpeta de gráficos si no existe
    if not os.path.exists("graficos"):
        os.makedirs("graficos")
    app.run(port=5000, debug=True)