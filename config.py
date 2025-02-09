
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env, si existe.
# Esto permite mantener sensibles (por ejemplo, credenciales) fuera del código fuente.
load_dotenv()

class Config:
    """
    Clase de configuración para la aplicación.
    
    Se utilizan variables de entorno para definir los parámetros de configuración, 
    permitiendo mayor flexibilidad y seguridad en el despliegue.
    """
    
    # ------------------------
    # Configuración de Flask
    # ------------------------
    # Modo de depuración: se habilita si la variable FLASK_DEBUG es "True", "1" o "yes"
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1", "yes"]
    
    # Clave secreta para la aplicación (necesaria para el manejo de sesiones y CSRF).
    # Debe cambiarse en producción a un valor seguro y difícil de adivinar.
    SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave-secreta")

    # ------------------------
    # Configuración de Twilio
    # ------------------------
    # SID de la cuenta de Twilio
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    
    # Token de autenticación de Twilio
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    
    # Número de WhatsApp asignado por Twilio (debe incluir el prefijo 'whatsapp:')
    TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "")

    # ------------------------
    # Otras configuraciones (opcional)
    # ------------------------
    # Por ejemplo, se podría agregar la URL de una base de datos o endpoints externos.
    # DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///app.db")

# Cómo utilizar esta configuración en su aplicación Flask:
#
# from flask import Flask
# from config import Config
#
# app = Flask(__name__)
# app.config.from_object(Config)
#
# De esta manera, se cargan todas las configuraciones definidas en la clase Config
# y se pueden utilizar a lo largo de la aplicación.
