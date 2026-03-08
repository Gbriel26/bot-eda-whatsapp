import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

# URL de Neon.tech
DATABASE_URL = "postgresql://neondb_owner:npg_7lYm0aNSGypu@ep-hidden-truth-adiltwvd.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def obtener_conexion():
    return psycopg2.connect(DATABASE_URL)

def registrar_inicio_chat(telefono, nombre):
    """Guarda el inicio de la conversación cuando el usuario da su nombre"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = """
            INSERT INTO historial_conversaciones (telefono_usuario, nombre_usuario) 
            VALUES (%s, %s) RETURNING id;
        """
        cursor.execute(query, (telefono, nombre))
        id_registro = cursor.fetchone()[0]
        
        conexion.commit()
        cursor.close()
        conexion.close()
        return id_registro
    except Exception as e:
        print(f"Error en BD: {e}")
        return None

def registrar_fin_chat(id_registro, url, correo):
    """Actualiza el registro cuando se envía el correo exitosamente"""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = """
            UPDATE historial_conversaciones 
            SET url_datos = %s, correo_destino = %s, fecha_fin = %s, 
                estado_conversacion = 'finalizado', pdf_generado = TRUE
            WHERE id = %s;
        """
        cursor.execute(query, (url, correo, datetime.now(), id_registro))
        
        conexion.commit()
        cursor.close()
        conexion.close()
    except Exception as e:
        print(f"Error actualizando BD: {e}")