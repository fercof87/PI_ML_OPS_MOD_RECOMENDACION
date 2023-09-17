import pandas as pd
import json
import gzip
import ast

ERROR_LOG = "Logs/errores_json_gz.log"

'''---------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      07 de Septiembre de 2023
Objetivo:   Realiza la Lectura de un archivo JSON comprimido con GZ
Entrada:    - Nombre del Archivo a Leer (Ruta Relativa); 
            - Modo de apertura (dependiendo el tipo de json a descomprimir)
Salida:     - Data Frame con los datos del JSON.GZ
---------------------------------------------------------------------------'''
def leerJsonGz(nombre, modo):

    raiz="Datos/"
    nombre = raiz + nombre
    errores = []
    data    = []

    try: 
        if (modo == 0):
            with gzip.open(nombre,"rb") as archivo:
                for linea in archivo:
                    descomprimido = linea.decode("UTF-8")
                    obj_json = json.loads(descomprimido)
                    data.append(obj_json)
        else:
            with gzip.open(nombre,"rt", encoding="UTF-8") as archivo:
                data =  [ast.literal_eval(line.strip()) for line in archivo]

        if data:
            df_json_gz = pd.DataFrame(data)
            return df_json_gz
        else:
            errores.append("El archivo está vacío o no contiene datos válidos.")

    except FileNotFoundError as e:
        errores.append(f"Error: El archivo '{nombre}' no se encuentra. {str(e)}")
    except gzip.BadGzipFile as e:
        errores.append(f"Error: El archivo '{nombre}' no es un archivo GZ válido. {str(e)}")
    except Exception as e:
        errores.append(f"Error inesperado: {str(e)}")

    if errores:
        with open(ERROR_LOG, "a", encoding="UTF-8") as log_file:
            for error in errores:
                log_file.write(error + "\n")

    return None

'''-------------------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      13 de Septiembre de 2023
Objetivo:   Realiza la exportacion de un Dataframe a un archivo JSON comprimido con GZ
Entrada:    - Nombre del Archivo a Grabar  
            - DF con los datos a exportar
Salida:     - None
-------------------------------------------------------------------------------------'''
def grabarJsonGz(df, nombre):

    raiz="Datos/"
    extension = ".json.gz"
    nombre = raiz + nombre + extension
    errores = []

    try:
        with gzip.open(nombre, 'wt', encoding='utf-8') as archivo:
            archivo.write(df.to_json(orient='records', lines=True))
    except Exception as e:
        errores.append(f"Error al guardar el archivo JSON comprimido: {str(e)}")

    if errores:
        with open(ERROR_LOG, "a", encoding="UTF-8") as log_file:
            for error in errores:
                log_file.write(error + "\n")

    return None

'''---------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      09 de Septiembre de 2023
Objetivo:   Desanidar estructuras JSON, haciendo un Flattern del archivo.
Entrada:    - Data Frame a Desanidar 
            - Nombre de Columna a Desanidar
Salida:     - Data Frame desanidado
---------------------------------------------------------------------------'''
def desanidarJson(df, columna):
    
    # Explotamos la lista de 'reviews' para que cada elemento de la lista esté en una fila separada
    df = df.explode(columna).reset_index(drop=True)

    # Utiliza pd.json_normalize para desanidar la columna en múltiples columnas
    df_norm = pd.json_normalize(df[columna])

    # Combina el DataFrame original con las columnas desanidadas y las retorna
    return pd.concat([df.drop(columns=[columna]), df_norm], axis=1)