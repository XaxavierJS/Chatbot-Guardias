
import os
import logging
from twilio.rest import Client

def get_twilio_client():
    """
    Inicializa y retorna una instancia del cliente de Twilio utilizando
    las credenciales definidas en las variables de entorno.

    Returns:
        Client: Instancia del cliente de Twilio.

    Raises:
        Exception: Si las credenciales necesarias no se encuentran configuradas.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    if not account_sid or not auth_token:
        raise Exception("Las credenciales de Twilio no están configuradas correctamente en las variables de entorno.")
    return Client(account_sid, auth_token)

def send_message(to, body):
    """
    Envía un mensaje de WhatsApp a través de la API de Twilio.

    Args:
        to (str): Número de destino en formato E.164, por ejemplo "whatsapp:+569XXXXXXXX".
        body (str): Contenido del mensaje a enviar.

    Returns:
        Message: Objeto devuelto por la API de Twilio, que contiene información del mensaje enviado.

    Raises:
        Exception: Si ocurre un error durante el envío del mensaje.
    """
    try:
        client = get_twilio_client()
        # Se obtiene el número asignado a WhatsApp desde las variables de entorno
        from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        if not from_number:
            raise Exception("El número de WhatsApp de Twilio no está configurado en las variables de entorno.")
        message = client.messages.create(
            body=body,
            from_=from_number,
            to=to
        )
        logging.info(f"Mensaje enviado a {to}. SID: {message.sid}")
        return message
    except Exception as e:
        logging.error(f"Error al enviar mensaje a {to}: {e}")
        raise

def send_confirmation(data, to):
    """
    Envía un mensaje de confirmación al usuario mostrando los datos extraídos
    y solicitando que confirme si son correctos.

    Args:
        data (dict): Diccionario con los datos extraídos, por ejemplo:
                     {'nombre': 'Juan', 'apellidos': 'Pérez', 'rut': '12.345.678-9'}
        to (str): Número de destino en formato E.164 (por ejemplo, "whatsapp:+569XXXXXXXX").
    """
    # Construir el mensaje de confirmación a partir de los datos extraídos
    message_body = (
        f"Nombre: {data.get('nombre', 'N/A')}\n"
        f"Apellidos: {data.get('apellidos', 'N/A')}\n"
        f"RUT: {data.get('rut', 'N/A')}\n\n"
        "¿Es correcto? (Sí/No)"
    )
    send_message(to, message_body)

def handle_text_message(body, to):
    """
    Maneja los mensajes de texto entrantes del usuario.

    Dependiendo del contenido del mensaje, se pueden ejecutar diferentes acciones,
    como confirmar los datos extraídos, solicitar la corrección de los mismos o responder a comandos
    (por ejemplo, consultar la lista de guardias registrados).

    Args:
        body (str): Texto del mensaje recibido.
        to (str): Número de destino en formato E.164 para la respuesta.
    """
    # Normalizar el mensaje a minúsculas para facilitar la comparación
    text = body.strip().lower()

    # manejo de respuestas y comandos:
    if text in ["sí", "si"]:
        # El usuario confirma que los datos son correctos
        confirmation_message = "Gracias por confirmar. Sus datos han sido registrados."
        send_message(to, confirmation_message)
        # Aquí se podría agregar la lógica para guardar los datos en un archivo JSON.
    elif text == "no":
        # El usuario indica que los datos no son correctos
        correction_message = "Por favor, ingrese manualmente sus datos: Nombre, Apellidos, RUT."
        send_message(to, correction_message)
    elif "registrados" in text:
        # Si el usuario solicita ver la lista de guardias registrados.
        # En una implementación real, se consultaría un archivo JSON o base de datos para obtener la lista.
        list_message = "Actualmente, los guardias registrados son: [lista de guardias]."
        send_message(to, list_message)
    else:
        # Respuesta por defecto para comandos no reconocidos.
        default_message = "Comando no reconocido. Por favor, responda con 'Sí' o 'No', o envíe un comando válido."
        send_message(to, default_message)


