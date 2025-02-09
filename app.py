import os
import logging
from flask import Flask, request

import config
from logs.logger_setup import setup_logging
from utils.ocr_processor import process_media, parse_extracted_text
from utils.twilio_client import send_confirmation, handle_text_message
from utils.file_manager import save_guardia

app = Flask(__name__)

# Configurar el logging para capturar eventos y errores, y almacenarlos en logs/app.log
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)
app.logger.setLevel(logging.INFO)
app.logger.info("Aplicación iniciada correctamente.")

@app.route("/")
def index():
    """
    Endpoint raíz para confirmar que la aplicación se despliega correctamente.
    """
    return "¡Hola, mundo! La aplicación se desplegó correctamente."

@app.route("/incoming", methods=["POST"])
def incoming():
    """
    Endpoint para recibir mensajes entrantes de Twilio.
    
    Este endpoint diferencia entre mensajes que incluyen medios (imágenes, PDFs) y mensajes de texto.
    - Si hay medios adjuntos (verificado con el parámetro NumMedia), se descarga el archivo,
      se preprocesa y se aplica OCR para extraer el texto. Luego se analizan los datos y se envía un mensaje
      de confirmación al usuario.
    - Si no hay medios, se procesa el texto recibido (por ejemplo, para manejar confirmaciones o comandos).
    """
    try:
        # Registrar la información recibida para fines de depuración
        app.logger.info("Mensaje entrante recibido: %s", request.form)
        
        # Obtener el número de medios enviados (por defecto es 0 si no se especifica)
        num_media = int(request.form.get("NumMedia", 0))
        # Obtener el número de teléfono del remitente (usado para enviar respuestas)
        sender = request.form.get("From")
        
        if num_media > 0:
            # Si se adjuntó un archivo (imagen o PDF)
            media_url = request.form.get("MediaUrl0")
            app.logger.info("Procesando archivo desde URL: %s", media_url)
            
            # Llamar a la función que descarga y procesa el medio (preprocesamiento y OCR)
            extracted_text = process_media(media_url)
            app.logger.info("Texto extraído mediante OCR: %s", extracted_text)
            
            # Analizar el texto extraído para obtener datos relevantes (por ejemplo, nombre, apellidos, RUT)
            data = parse_extracted_text(extracted_text)
            app.logger.info("Datos extraídos: %s", data)
            
            # Enviar un mensaje de confirmación al usuario con los datos extraídos
            send_confirmation(data, sender)
            
            # Opcional: guardar los datos en un archivo JSON si el usuario posteriormente confirma la información
            # save_guardia(data)
            
            return "Mensaje de medios procesado", 200
        else:
            # Si el mensaje no contiene archivos, se procesa el contenido de texto
            body = request.form.get("Body", "").strip().lower()
            app.logger.info("Procesando mensaje de texto: %s", body)
            
            # Manejar el mensaje de texto (por ejemplo, confirmaciones, comandos de consulta o eliminación)
            handle_text_message(body, sender)
            
            return "Mensaje de texto procesado", 200
    except Exception as e:
        # En caso de error, registrar el error y devolver una respuesta con código 500
        app.logger.error("Error procesando el mensaje entrante: %s", str(e))
        return "Error procesando mensaje", 500

if __name__ == "__main__":
    # Ejecutar la aplicación en modo de desarrollo.
    # En producción se recomienda utilizar un servidor WSGI (por ejemplo, Gunicorn)
    setup_logging()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
