import pandas as pd
from datetime import datetime
from fuzzywuzzy import fuzz
import re

'''---------------------------------------------------------------------------
CONSTANTES
---------------------------------------------------------------------------'''

DEFAULT_DATE        = "1900-01-01"
DEFAULT_DATE_LONG   = "January 1, 1900"


'''---------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      10 de Septiembre de 2023
Objetivo:   Realiza la transformacion de la fecha de posteo
Entrada:    Datos a Analizar
Salida:     Datos calificados
---------------------------------------------------------------------------'''
def convertPosted(date_str):
    try:
        # Intenta analizar la fecha en el formato original
        date = pd.to_datetime(date_str, format='%B %d, %Y')
    except ValueError:
        try:
            # Si falla, intenta analizar la fecha sin el año
            date = pd.to_datetime(date_str + ' 1900', format='%B %d %Y')
        except ValueError:
            # Si aún falla, asigna una fecha predeterminada (January 1, 1900)
            date = pd.to_datetime(DEFAULT_DATE)
    return date.strftime('%Y-%m-%d')



'''---------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      10 de Septiembre de 2023
Objetivo:   Realiza la transformacion de la fecha de RELEASE APLICANDO 
            COINCIDENCIA DISFUZA (FUZZY)
Entrada:    RELEASE DATE
Salida:     FECHA ADAPTADA A YYYY-MM-DD
---------------------------------------------------------------------------'''
def convertReleaseFuzzy(date_str):
    
    # Si dateParser devuelve el valor DEFAULT_DATE, simplemente devolvemos ese valor
    if date_str == DEFAULT_DATE:
        return pd.to_datetime(DEFAULT_DATE).date().strftime("%Y-%m-%d")
    
    # Verifica si la fecha ya está en uno de los formatos deseados antes de aplicar otros tratamientos
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        # Intenta convertir la fecha al formato "YYYY-MM-DD"
        try:
            return pd.to_datetime(date_str, format="%Y-%m-%d").date().strftime("%Y-%m-%d")
        except ValueError:
            # Si no se puede convertir al formato "YYYY-MM-DD", intenta con "YYYY-DD-MM"
            try:
                return pd.to_datetime(date_str, format="%Y-%d-%m").date().strftime("%Y-%m-%d")
            except ValueError:
                pass
    
    #Modificaciones Especiales
    date_str = dateParser(date_str)
    
    known_formats = ['%Y-%m-%d', '%Y', '%b %Y', '%B %Y', '%d %m %Y', '%B %Y', '%B %d %Y', '%b %d %Y', '%d %b, %Y', '%Y %d %m']

    for format_str in known_formats:
        try:
            # Intenta convertir la fecha usando el formato conocido
            return pd.to_datetime(date_str, format=format_str).date().strftime("%Y-%m-%d")
        except ValueError:
            # Si no se puede convertir con este formato, continúa probando con otros formatos
            pass

    # Si no se pudo convertir con ninguno de los formatos conocidos, busca coincidencias difusas
    for format_str in known_formats:
        for known_date_str in known_formats:
            if fuzz.ratio(date_str, known_date_str) > 80:  # Umbral de Similitud 
                return pd.to_datetime(known_date_str, format=format_str).date().strftime("%Y-%m-%d")

    # Si no se puede convertir y no se encuentra una coincidencia aproximada, devuelve DEFAULT_DATE = 1900-01-01
    return pd.to_datetime(DEFAULT_DATE).date().strftime("%Y-%m-%d")



'''---------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      10 de Septiembre de 2023
Objetivo:   Realiza el PARSING de RELEASE DATE
Entrada:    RELEASE DATE
Salida:     FECHA ADAPTADA A YYYY-MM-DD
---------------------------------------------------------------------------'''
def dateParser(date_str):

    #quitamos posibles espacios
    date_str = date_str.strip()
    # Modificación de las fechas que vienen con Quarters of...
    date_str = re.sub(r'q1\b', '15 01', date_str.lower())
    date_str = re.sub(r'q2\b', '15 04', date_str.lower())
    date_str = re.sub(r'q3\b', '15 07', date_str.lower())
    date_str = re.sub(r'q4\b', '15 10', date_str.lower())
    # Modificación de casos particulares
    date_str = date_str.replace('(ish),', '')
    date_str = date_str.replace('(tentative)', '')
    date_str = date_str.replace(',', '')
    date_str = date_str.replace('.', ' ')

    # Divide la cadena en palabras
    words = date_str.lower().split(" ")
    
    seasons = ["spring", "summer", "fall", "autumn", "winter"]

    # Limpiza de fechas informadas como soon o coming, etc.
    if "soon" in date_str.lower() or "coming" in date_str.lower():
        date_str = DEFAULT_DATE

    # Limpiza de fechas informadas como "season" + YYYY
    if any(keyword in words for keyword in seasons) and len(words) == 2:
        season  = words[0]
        year    = words[1]
        if season == "spring":
            date_str = year + "-" + "05-20"
        elif season == "summer":
            date_str = year + "-" + "07-21"
        elif season == "fall" or season == "autumn":
            date_str = year + "-" + "09-22"
        elif season == "winter":
            date_str = year + "-" + "12-21" 

    # Limpiza de fechas informadas con early, end, late, h1, h2 + YYYY
    
    # Expresión regular para reconocer años en formatos como "early 2018" o "2018 early"
    year_pattern = re.compile(r'\b(early|end|late|h[12]?)?\s?(\d{4})\b', re.IGNORECASE)

    # Busca una coincidencia en el texto
    match = year_pattern.search(date_str)

    if match:
        # Extrae el año y el tipo (early, end, late, h1, h2)
        year = match.group(2)
        type_str = match.group(1).lower() if match.group(1) else ""

        # Mapea el tipo a un mes si es necesario
        if "early" in type_str:
            month = "01"  # Enero
        elif "end" in type_str or "late" in type_str:
            month = "12"  # Diciembre
        else:
            month = "07"  # Por defecto, usa julio

        # Combina el año y el mes en el formato deseado
        formatted_date = f"{year}-{month}-01"
        return formatted_date

    return date_str