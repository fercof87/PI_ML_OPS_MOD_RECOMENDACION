import os
import pandas as pd
import json
import gzip
import ast


ERROR_LOG        = "Logs/errores_json_gz.log"
GRAL_LOG         = "Logs/generalLog.log"


'''---------------------------------------------------------------------------
Autor:      Ing. Fernando G. Cofone
Fecha:      07 de Septiembre de 2023
Objetivo:   Realiza la Lectura de un archivo JSON comprimido con GZ
Entrada:    - Nombre del Archivo a Leer (Ruta Relativa); 
            - Modo de apertura (dependiendo el tipo de json a descomprimir)
Salida:     - Data Frame con los datos del JSON.GZ
---------------------------------------------------------------------------'''
def leerJsonGz(raiz, nombre, modo):

    #raiz="Datos/"
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


'''---------------------------------------------------------------------------
Autor:      Ing. Fernando G. Cofone
Fecha:      07 de Septiembre de 2023
Objetivo:   Realiza la Lectura de un archivo JSON Particionado y lo junta
            en un solo DF
Entrada:    - Ruta Relativa al archivo
            - Nombre del Archivo a Leer
            - Modo de apertura (dependiendo el tipo de json a descomprimir)
Salida:     - Data Frame con los datos de todas las particiones.
---------------------------------------------------------------------------'''
def leerJsonGzPart(raiz, nombre, modo, part):

    dataframes = []

    for i in range(part):
        nombre_parte = f"{nombre}_{i}.json.gz"
        df_parte = leerJsonGz(raiz, nombre_parte, modo)
        if df_parte is not None:
            dataframes.append(df_parte)

    if dataframes:
        concatenated_df = pd.concat(dataframes, ignore_index=True)
        return concatenated_df.reset_index(drop=True)
    else:
        return None


'''----------------------------------------------------------------------------------
Autor:      Ing. Fernando G. Cofone
Fecha:      17 de Septiembre de 2023
Objetivo:   Divide un archivo JSON comprimido con GZ en múltiples partes
Entrada:    - nombre_archivo: Nombre del archivo a dividir (Ruta Relativa)
            - cantidad_partes: Número de partes en las que se dividirá el archivo
Salida:     Ninguna (archivos de salida se almacenan en la carpeta "particiones")
----------------------------------------------------------------------------------'''
def particionarJsonGz(nombre_archivo, cantidad_partes, modo):
    raiz = "Datos/"
    nombre_completo = raiz + nombre_archivo
    errores = []
    datos = []

    try:
        # Leer el archivo JSON comprimido segun el Modo
        if (modo == 0):
            with gzip.open(nombre_completo, "rb") as archivo:
                for linea in archivo:
                    descomprimido = linea.decode("UTF-8")
                    obj_json = json.loads(descomprimido)
                    datos.append(obj_json)
        else:
            with gzip.open(nombre_completo, "rt", encoding="UTF-8") as archivo:
                datos = [ast.literal_eval(line.strip()) for line in archivo]

        # Obtener el tamaño total de los datos
        tamano_total = len(datos)

        # Calcular el tamaño aproximado de cada parte
        tamano_parte = tamano_total // cantidad_partes

        # Crear un directorio para las partes si no existe
        carpeta_salida = raiz + "Particiones/"
        if not os.path.exists(carpeta_salida):
            os.makedirs(carpeta_salida)

        # Dividir los datos en partes y guardarlas en archivos separados
        for i in range(cantidad_partes):
            inicio = i * tamano_parte
            fin = (i + 1) * tamano_parte if i < cantidad_partes - 1 else tamano_total
            parte = datos[inicio:fin]

            # Nombre del archivo de salida
            nombre_parte = f"{carpeta_salida}/{nombre_archivo}_{i}.json.gz"

            # Guardar la parte en un archivo comprimido
            with gzip.open(nombre_parte, "wb") as archivo_parte:
                for obj_json in parte:
                    linea = json.dumps(obj_json) + "\n"
                    archivo_parte.write(linea.encode("UTF-8"))

        with open(GRAL_LOG, "a", encoding="UTF-8") as Gral_log_file:
            linea = f"Archivo '{nombre_archivo}' dividido en {cantidad_partes} partes y guardado en '{carpeta_salida}'."
            Gral_log_file.write(linea + "\n")

    except FileNotFoundError as e:
        errores.append(f"Error: El archivo '{nombre_archivo}' no se encuentra. {str(e)}")
    except gzip.BadGzipFile as e:
        errores.append(f"Error: El archivo '{nombre_archivo}' no es un archivo GZ válido. {str(e)}")
    except Exception as e:
        errores.append(f"Error inesperado: {str(e)}")

    if errores:
        with open(ERROR_LOG, "a", encoding="UTF-8") as log_file:
            for error in errores:
                log_file.write(error + "\n")

    return None

'''-------------------------------------------------------------------------------------
Autor:      Ing. Fernando G. Cofone
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
Autor:      Ing. Fernando G. Cofone
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