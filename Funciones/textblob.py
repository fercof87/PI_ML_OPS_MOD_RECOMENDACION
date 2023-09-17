import pandas as pd
from textblob import TextBlob


'''---------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      09 de Septiembre de 2023
Objetivo:   Realiza el Analisis de Sentimiento
            Utiliza como Threshold 0.2 en ambos extremos de la polaridad.
            No utiliza Subjetividad para evaluar.
Entrada:    Datos a Analizar
Salida:     Datos calificados
---------------------------------------------------------------------------'''
def sentimientoTextblob(columna,nombre_obj):
    sentimientos = []
    for texto in columna:
        if isinstance(texto, str) and texto.strip():
            analysis = TextBlob(texto)
            # Establece un umbral para determinar si es negativo, neutro o positivo
            if analysis.sentiment.polarity < -0.2:
                sentimientos.append(0)      # Sentimiento negativo
            elif analysis.sentiment.polarity > 0.2:
                sentimientos.append(2)      # Sentimiento positivo
            else:
                sentimientos.append(1)      # Sentimiento neutro
        else:
            sentimientos.append(1)              # Si no hay información en la celda, considerarlo neutro
    return pd.Series(sentimientos, name=nombre_obj)

'''---------------------------------------------------------------------------
Autor:      Fernando Cofone
Fecha:      09 de Septiembre de 2023
Objetivo:   Realiza el Analisis de Sentimiento
Entrada:    Datos a Analizar
Salida:     Probabilidades del Sentimiento
---------------------------------------------------------------------------'''
def sentimientoTextblob_Proba(columna,nombre_obj):
    sentimientos = []
    for texto in columna:
            if isinstance(texto, str) and texto.strip():
                analysis = TextBlob(texto)
                polaridad = analysis.sentiment.polarity
                sentimientos.append(polaridad)
            else:
                sentimientos.append(0)
    return pd.Series(sentimientos, name=nombre_obj)