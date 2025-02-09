"""
logger_setup.py

Este módulo configura el sistema de logging para la aplicación.
Utiliza el módulo 'logging' de Python para:
  - Crear el directorio "logs" (si no existe).
  - Configurar un archivo de log ("logs/app.log") donde se registrarán
    los mensajes de información, advertencia y error.
  - Establecer un formato de log que incluya la fecha, hora, nivel del mensaje,
    mensaje, y la ubicación (archivo y línea) desde donde se emitió.
  - Configurar además el log para que también se imprima en la consola.

Buenas prácticas:
  - Uso de 'basicConfig' para establecer la configuración inicial.
  - Agregar un StreamHandler para que los logs se muestren en la consola,
    lo que facilita la depuración durante el desarrollo.
  - Comentarios y docstrings para facilitar la comprensión y mantenimiento.
"""

import os
import logging

def setup_logging():
    """
    Configura el logging para la aplicación.

    - Crea el directorio "logs" si no existe.
    - Define el archivo de log "logs/app.log".
    - Establece el nivel de logging en INFO.
    - Define el formato del log con información de timestamp, nivel, mensaje,
      y ubicación en el código.
    - Añade también un handler para imprimir los mensajes en la consola.
    """
    # Definir el directorio donde se almacenarán los logs
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Definir la ruta completa del archivo de log
    log_file = os.path.join(log_dir, "app.log")
    
    # Formato del log: incluye fecha, hora, nivel, mensaje y origen (archivo y línea)
    log_format = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    
    # Configurar el logging básico para escribir en el archivo de log
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        filename=log_file,
        filemode='a',  # 'a' para agregar mensajes al final del archivo (append)
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configurar un StreamHandler para también enviar los logs a la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    
    # Añadir el handler de consola al logger raíz
    logging.getLogger('').addHandler(console_handler)
    
    logging.info("El sistema de logging se ha configurado correctamente.")

# Si se ejecuta este módulo de forma independiente, se configura el logging y se emite un mensaje de prueba.
if __name__ == "__main__":
    setup_logging()
    logging.info("Mensaje de prueba: El sistema de logging está funcionando correctamente.")
