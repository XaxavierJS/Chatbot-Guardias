import json
import os
import logging

# Definir la ruta del archivo JSON donde se almacenarán los registros.
# Se utiliza os.path.join para construir la ruta de forma independiente al sistema operativo.
# En este ejemplo, el archivo se ubicará en el directorio raíz del proyecto.
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "guardias.json")

def save_guardia(data):
    """
    Guarda los datos de un guardia en el archivo JSON.
    
    Si el archivo ya existe, se lee el contenido actual (una lista de registros),
    se añade el nuevo registro y se vuelve a escribir el archivo.
    Si el archivo no existe o está vacío/corrupto, se crea uno nuevo con el registro inicial.

    Args:
        data (dict): Diccionario que contiene los datos del guardia (por ejemplo, nombre, apellidos, RUT).

    Raises:
        Exception: Si ocurre algún error durante la escritura del archivo JSON.
    """
    try:
        # Inicializar la lista de guardias
        guardias = []

        # Si el archivo ya existe, leer el contenido actual
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    guardias = json.load(f)
                except json.JSONDecodeError:
                    # Si el archivo está vacío o corrupto, se continúa con una lista vacía
                    guardias = []

        # Añadir el nuevo registro a la lista
        guardias.append(data)

        # Escribir la lista actualizada en el archivo JSON con formato legible
        with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(guardias, f, ensure_ascii=False, indent=4)

        logging.info("Registro guardado exitosamente en el archivo JSON.")
    except Exception as e:
        logging.error(f"Error al guardar el registro: {e}")
        raise Exception(f"Error al guardar el registro: {e}")

def get_guardias():
    """
    Lee y retorna la lista de guardias registrados desde el archivo JSON.
    
    Returns:
        list: Lista de diccionarios, donde cada diccionario contiene los datos de un guardia.
              Si el archivo no existe o está vacío, se retorna una lista vacía.

    Raises:
        Exception: Si ocurre algún error al leer el archivo JSON.
    """
    try:
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    guardias = json.load(f)
                    return guardias
                except json.JSONDecodeError:
                    # El archivo está vacío o tiene un formato incorrecto; se retorna lista vacía
                    return []
        else:
            return []
    except Exception as e:
        logging.error(f"Error al leer el archivo JSON: {e}")
        raise Exception(f"Error al leer el archivo JSON: {e}")

def clear_guardias():
    """
    Elimina el archivo JSON que contiene los registros de guardias.
    
    Se utiliza para limpiar o reiniciar el registro de datos. Si el archivo no existe,
    la función no realiza ninguna acción.

    Raises:
        Exception: Si ocurre algún error al eliminar el archivo.
    """
    try:
        if os.path.exists(JSON_FILE_PATH):
            os.remove(JSON_FILE_PATH)
            logging.info("Archivo JSON eliminado exitosamente.")
        else:
            logging.info("El archivo JSON no existe, no se requiere eliminarlo.")
    except Exception as e:
        logging.error(f"Error al eliminar el archivo JSON: {e}")
        raise Exception(f"Error al eliminar el archivo JSON: {e}")

def backup_guardias(backup_path):
    """
    Realiza una copia de respaldo del archivo JSON en la ubicación especificada.
    
    Args:
        backup_path (str): Ruta completa donde se almacenará la copia de respaldo.
    
    Raises:
        Exception: Si ocurre algún error durante la operación de respaldo.
    """
    try:
        if os.path.exists(JSON_FILE_PATH):
            # Leer el contenido del archivo original
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as original:
                data = original.read()
            # Escribir el contenido en el archivo de respaldo
            with open(backup_path, "w", encoding="utf-8") as backup_file:
                backup_file.write(data)
            logging.info(f"Respaldo realizado exitosamente en: {backup_path}")
        else:
            logging.info("No se realizó respaldo porque el archivo JSON no existe.")
    except Exception as e:
        logging.error(f"Error al realizar el respaldo del archivo JSON: {e}")
        raise Exception(f"Error al realizar el respaldo del archivo JSON: {e}")
