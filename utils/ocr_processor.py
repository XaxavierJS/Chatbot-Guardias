"""
utils/ocr_processor.py

Este módulo contiene funciones para:
- Descargar un archivo (en este caso, una imagen enviada por WhatsApp) a partir de su URL.
- Preprocesar la imagen utilizando OpenCV para optimizar la extracción de texto.
- Extraer texto de la imagen utilizando Pytesseract.
- Procesar el texto extraído para obtener datos específicos (por ejemplo, RUT).

Se utilizan buenas prácticas como el manejo de excepciones, docstrings y comentarios explicativos.
"""

import cv2
import numpy as np
import pytesseract
import requests
import io
from pdf2image import convert_from_bytes
from PIL import Image
import re

def download_file(url):
    """
    Descarga un archivo desde una URL y devuelve su contenido en bytes.
    
    En el caso de este proyecto, la URL proviene de la imagen enviada a través de WhatsApp
    (Twilio envía el parámetro 'MediaUrl0' en el webhook).
    
    Args:
        url (str): URL del archivo a descargar.
    
    Returns:
        bytes: Contenido del archivo descargado.
    
    Raises:
        Exception: Si ocurre un error durante la descarga.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP.
        return response.content
    except requests.RequestException as e:
        raise Exception(f"Error al descargar el archivo desde {url}: {e}")

def is_pdf(file_bytes):
    """
    Determina si el contenido del archivo corresponde a un PDF.
    
    Se verifica si los primeros 4 bytes coinciden con el encabezado '%PDF'.
    
    Args:
        file_bytes (bytes): Contenido del archivo.
    
    Returns:
        bool: True si es un PDF, False en caso contrario.
    """
    return file_bytes[:4] == b'%PDF'

def preprocess_image_cv2(cv_image):
    """
    Aplica técnicas de preprocesamiento a una imagen utilizando OpenCV.
    
    Este preprocesamiento incluye:
      - Conversión a escala de grises.
      - Aplicación de desenfoque gaussiano para reducir el ruido.
      - Umbralización (binaria mediante el método de Otsu) para resaltar el texto.
    
    Args:
        cv_image (numpy.ndarray): Imagen en formato OpenCV (BGR).
    
    Returns:
        numpy.ndarray: Imagen preprocesada lista para el OCR.
    """
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque gaussiano para reducir el ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Aplicar umbralización con el método de Otsu
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def extract_text_from_image(cv_image):
    """
    Extrae texto de una imagen preprocesada utilizando Pytesseract.
    
    Se especifica el idioma 'spa' para optimizar el reconocimiento de texto en español.
    
    Args:
        cv_image (numpy.ndarray): Imagen preprocesada lista para OCR.
    
    Returns:
        str: Texto extraído de la imagen.
    """
    text = pytesseract.image_to_string(cv_image, lang='spa')
    return text

def process_media(media_url):
    """
    Procesa un medio (en este caso, una imagen enviada por WhatsApp) a partir de su URL.
    
    La función realiza los siguientes pasos:
      1. Descarga el archivo desde la URL (se espera que la URL provenga de Twilio en el webhook).
      2. Determina si el archivo es un PDF o una imagen.
         - Si es un PDF, utiliza pdf2image para convertir la primera página a imagen.
         - Si es una imagen, la decodifica utilizando OpenCV.
      3. Preprocesa la imagen para mejorar la calidad para el OCR.
      4. Extrae el texto de la imagen preprocesada mediante Pytesseract.
    
    Args:
        media_url (str): URL del archivo a procesar.
    
    Returns:
        str: Texto extraído mediante OCR.
    
    Raises:
        Exception: Si ocurre algún error durante la descarga o el procesamiento.
    """
    # Descargar el archivo desde la URL (esta URL es recibida desde WhatsApp a través de Twilio)
    file_bytes = download_file(media_url)
    
    # Determinar si el archivo es un PDF
    if is_pdf(file_bytes):
        # Convertir el PDF a imagen (se utiliza solo la primera página para simplificar)
        pil_images = convert_from_bytes(file_bytes, dpi=300)
        if not pil_images:
            raise Exception("No se pudo convertir el PDF a imagen.")
        pil_image = pil_images[0]
        # Convertir la imagen PIL a un formato compatible con OpenCV (BGR)
        cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    else:
        # Asumir que es una imagen (por ejemplo, JPEG o PNG) enviada por WhatsApp
        # Convertir los bytes a un arreglo NumPy y decodificar la imagen
        np_array = np.frombuffer(file_bytes, np.uint8)
        cv_image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        if cv_image is None:
            raise Exception("No se pudo decodificar la imagen.")
    
    # Preprocesar la imagen para mejorar el rendimiento del OCR
    preprocessed_image = preprocess_image_cv2(cv_image)
    
    # Extraer y devolver el texto de la imagen preprocesada
    extracted_text = extract_text_from_image(preprocessed_image)
    return extracted_text

def parse_extracted_text(text):
    """
    Procesa el texto extraído para obtener datos específicos, como nombre, apellidos y RUT.
    
    Este ejemplo implementa una lógica básica para extraer un RUT en formato chileno usando
    una expresión regular. Se pueden agregar reglas adicionales para extraer otros datos.
    
    Args:
        text (str): Texto extraído mediante OCR.
    
    Returns:
        dict: Diccionario con los datos extraídos, por ejemplo:
              {'nombre': 'NombreExtraido', 'apellidos': 'ApellidosExtraidos', 'rut': '12.345.678-9'}
    """
    # Expresión regular para extraer un RUT (ejemplo: 12.345.678-9)
    rut_pattern = r'\d{1,2}\.\d{3}\.\d{3}-[\dkK]'
    rut_match = re.search(rut_pattern, text)
    rut = rut_match.group(0) if rut_match else None
    
    # En este ejemplo, los datos de nombre y apellidos se asignan de forma dummy.
    # La lógica se puede extender para extraerlos del texto en función del formato esperado.
    nombre = "NombreExtraido"
    apellidos = "ApellidosExtraidos"
    
    return {
        "nombre": nombre,
        "apellidos": apellidos,
        "rut": rut
    }

# Fin del módulo ocr_processor.py
