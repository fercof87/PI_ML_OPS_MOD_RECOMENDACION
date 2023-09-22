from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
import pandas as pd
from datetime import datetime
from Funciones.json_func import *


#ROOT
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   20 de Septiembre de 2023
Objetivo:   Obtiene la información de la API.
Params  :    
Returns :   str: Información sobre la API. 
--------------------------------------------------------------------------------'''
def getIndex():

    try:
        html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Información General de la API</title>
            </head>
            <body>
                <h1>API Creada por Ing. Fernando G. Cofone</h1>
                <hr> <!-- Línea horizontal -->
                <h2>MLOPs - Recomendación de Juegos</h2>
                <hr> <!-- Línea horizontal -->
                <h2>Enlaces:</h2>
                    <p align="center">
                        <a href="https://pi-ml-ops-mod-recomendacion.onrender.com/docs" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
                            API DOCs
                        </a> 
                        <a href="https://www.linkedin.com/in/fcofone" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
                            Mi Linkedin
                        </a> 
                        <a href="https://github.com/fercof87/PI_ML_OPS_MOD_RECOMENDACION" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
                            Proyecto GitHub
                        </a> 
                    </p>
                <h2>Endpoints:</h2>
                <ol>
                    <li><code><strong style="color: #ff5733">/userdata/</strong> (User_id: str)</code>:<br>&nbsp;&nbsp;&nbsp;Proporciona detalles sobre el gasto del usuario, el porcentaje de recomendación basado en reseñas y la cantidad de ítems.</li>
                    <li><code><strong style="color: #ff5733">/countreviews/</strong> (YYYY-MM-DD1: str, YYYY-MM-DD2: str)</code>:<br>&nbsp;&nbsp;&nbsp;Calcula la cantidad de usuarios que realizaron reseñas entre las fechas proporcionadas y el porcentaje de recomendación basado en reseñas.</li>
                    <li><code><strong style="color: #ff5733">/genre/</strong> (género: str)</code>:<br>&nbsp;&nbsp;&nbsp;Muestra el puesto en el ranking para un género de videojuegos específico según la columna PlayTimeForever.</li>
                    <li><code><strong style="color: #ff5733">/userforgenre/</strong> (género: str)</code>:<br>&nbsp;&nbsp;&nbsp;Ofrece el top 5 de usuarios con más horas de juego en el género especificado, junto con su URL y user_id.</li>
                    <li><code><strong style="color: #ff5733">/developer/</strong> (desarrollador: str)</code>:<br>&nbsp;&nbsp;&nbsp;Presenta información sobre la cantidad de ítems y el porcentaje de contenido gratuito por año, según la empresa desarrolladora.</li>
                    <li><code><strong style="color: #ff5733">/sentiment_analysis/</strong> (año: int)</code>:<br>&nbsp;&nbsp;&nbsp;Devuelve una lista con la cantidad de registros de reseñas de usuarios categorizados con análisis de sentimiento para un año de lanzamiento dado.</li>
                    <li><code><strong style="color: #ff5733">/recommendationByItem/</strong> (item_id: int)</code>:<br>&nbsp;&nbsp;&nbsp;Devuelve una lista de recomendación de 5 juegos similares al item_id suministrado. En caso de no encontrar el item_id, recomendará los 5 juegos con más calificaciones positivas detectadas en las reviews.</li>
                    <li><code><strong style="color: #ff5733">/recommendationByUser/</strong> (user_id: int)</code>:<br>&nbsp;&nbsp;&nbsp;Devuelve una lista de recomendación de 5 juegos en funcion al usuario suministrado. En caso de no encontrar el user_id, recomendará los 5 juegos con más calificaciones positivas detectadas en las reviews.</li>
                </ol>
            </body>
            </html>
        """
        return HTMLResponse(content=html_content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getIndex: {str(e)}")


#1
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   14 de Septiembre de 2023
Objetivo:   Obtiene datos de usuario filtrados por ID.
Params  :   user_id (str): ID del usuario.
Returns :   JSONResponse: Datos del usuario en formato JSON.
--------------------------------------------------------------------------------'''
def getUserData(user_id: str = Query(..., description="ID del usuario (alfanumérico con caracteres especiales permitidos)")):

    try:

        # Quitar espacios en blanco del principio y el final
        user_id = user_id.strip()

        # Validar que user_id esté presente
        if not user_id:
            return JSONResponse(content = ["El parámetro 'user_id' es obligatorio y no puede estar vacío."])
        
        #Abrimos archivos
        df_user_data  = leerJsonGz("Datos/","user_data.json.gz",1)

        # Validamos que exista el user_id en los 3 DFs
        if (user_id not in df_user_data['user_id'].values):
            return JSONResponse(content = ["Usuario No Encontrado"]) 

        # Combinamos DFs
        result = df_user_data[df_user_data['user_id'] == user_id][['user_id', 'spent', 'perc_recommend', 'count_items']]
        
        # Renombramos las columnas
        result.columns = ['USER ID', 'SPENT', '% RECOMMEND', 'ITEMs COUNT']
        
        #convertimos el DF a diccionario y luego JSON
        result_list = result.to_dict(orient = 'records')

        return JSONResponse(content = result_list)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getCountReviews: {str(e)}")


#2
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   14 de Septiembre de 2023
Objetivo:   Obtiene el recuento de revisiones en un rango de fechas.
Params  :   start_date (str): Fecha de inicio.
            end_date   (str): Fecha de finalización.
Returns :   JSONResponse: Resultados del recuento de reviews en formato JSON.
--------------------------------------------------------------------------------'''
def getCountReviews(start_date: str = Query(..., description="Fecha de inicio en formato YYYY-MM-DD"),
                    end_date: str = Query(..., description="Fecha de finalización en formato YYYY-MM-DD")):

    try:

        # Quitar espacios en blanco del principio y el final
        start_date = start_date.strip()
        end_date   = end_date.strip()

        # Validar que start_date y end_date estén presentes
        if not start_date or not end_date:
            return JSONResponse(content = ["Los parámetros 'start_date' y 'end_date' son obligatorios y no pueden estar vacíos."])

        # Validar el formato de las fechas
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date   = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return JSONResponse(content = ["Las fechas deben estar en formato YYYY-MM-DD."]) 
        
        #Abrimos archivos
        df_user_reviews = leerJsonGz("Datos/","user_reviews_posted.json.gz",1)

        #Genero copias en formato str
        start_date_str = start_date
        end_date_str = end_date
        
        # Convertir las variables start_date y end_date al tipo de dato datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Convertir la columna 'posted' al tipo de dato datetime
        df_user_reviews['posted'] = pd.to_datetime(df_user_reviews['posted'])
        
        #Filtramos todo el DF por las fechas recibidas
        df_user_reviews = df_user_reviews[(df_user_reviews['posted'] >= start_date) & (df_user_reviews['posted'] <= end_date)]

   
        # Validamos que tengamos resultados
        if (df_user_reviews.shape[0] == 0):
            return JSONResponse(content = ["No se Han Encontrado Datos entre las Fechas Ingresadas"]) 
           
        #Usuarios Unicos 
        unique_users   = df_user_reviews['user_id'].unique().shape[0]
        recommend_0    = df_user_reviews[df_user_reviews['recommend'] == 0]['recommend'].shape[0]
        recommend_1    = df_user_reviews[df_user_reviews['recommend'] == 1]['recommend'].shape[0]

        #Precaucion para no generar divisiones por cero
        if recommend_1 == 0:
            perc_recommend = 0.0
        else:
            perc_recommend = (recommend_1 / (recommend_0 + recommend_1)) * 100
    
        #Creamos un DF
        data = {'START DATE':   [start_date_str.strftime('%Y-%m-%d')],
                'END DATE':     [end_date_str.strftime('%Y-%m-%d')],
                'USERs COUNT':  [unique_users],
                '% RECOMMEND':  ['{:.2f}%'.format(perc_recommend)]}

        result = pd.DataFrame(data)

        #convertimos el DF a diccionario y luego JSON
        result_list = result.to_dict(orient = 'records')

        return JSONResponse(content = result_list)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getCountReviews: {str(e)}")


#3
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   14 de Septiembre de 2023
Objetivo:   Obtiene el ranking de un género específico.
Params  :   genre  (str): Género a consultar.
Returns :   JSONResponse: Resultado del ranking en formato JSON.
--------------------------------------------------------------------------------'''
def getGenreRank(genre: str = Query(..., description="Género (letras y espacios)")):

    try:
        
        # Quitar espacios en blanco del principio y el final
        genre = genre.strip()

        # Validar que genre esté presente
        if not genre:
            return JSONResponse(content = ["El parámetro 'genre' es obligatorio y no puede estar vacío."])

        # Validar que genre contenga solo letras y espacios
        if not all(char.isalpha() or char.isspace() for char in genre):
            return JSONResponse(content = ["El parámetro 'genre' debe contener solo letras y espacios."])
        
        #Abrimos archivos
        df_genre_ranking = leerJsonGz("Datos/","genre_ranking.json.gz",1)

        #Validamos que el genero este rankeado
        if not (df_genre_ranking['genre'].str.lower() == genre.lower()).any():
            return JSONResponse(content = ["El Genero no Se encuentra Rankeado"]) 

        #Obtenemos el ranking
        ranking = (df_genre_ranking[df_genre_ranking['genre'].str.lower() == genre.lower()].index).values[0] + 1

        #Creamos un DF
        data = {'GENRE':   [genre.capitalize()],
                'RANKING': [ranking]}
        
        result = pd.DataFrame(data)

        # Eliminar el índice del DataFrame
        result.reset_index(drop=True, inplace=True)

        #convertimos el DF a diccionario y luego JSON
        result_list = result.to_dict(orient = 'records')

        return JSONResponse(content = result_list)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getGenreRank: {str(e)}")


#4
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   14 de Septiembre de 2023
Objetivo:   Obtiene Top 5 de usuarios por género, segun playtime_forever.
Params  :   genre  (str): Género a consultar.
Returns :   JSONResponse: Lista de usuarios por género en formato JSON.  
--------------------------------------------------------------------------------'''
def getUserForGenre(genre: str = Query(..., description="Género (letras y espacios)")):
    try:
        # Quitar espacios en blanco del principio y el final
        genre = genre.strip().lower()

        # Validar que genre esté presente
        if not genre:
            return JSONResponse(content = ["El parámetro 'genre' es obligatorio y no puede estar vacío."])
        
        #Abrimos archivos
        df_user_genre = leerJsonGz("Datos/","user_genre_ranking.json.gz",1)

        # Filtrar el DF directamente
        df_user_genre = df_user_genre[df_user_genre['genre'].str.lower() == genre]

        # Validar si se encontraron registros
        if df_user_genre.empty:
            return JSONResponse(content=["El Género no ha sido Encontrado"])

        # Seleccionar las columnas necesarias
        df_user_genre = df_user_genre[['user_id', 'user_url', 'playtime_forever']]

        # Renombrar columnas
        df_user_genre.columns = ['USER ID', 'USER URL', 'PLAYTIME FOREVER']

        result_list = df_user_genre.to_dict(orient='records')

        return JSONResponse(content=result_list)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getUserForGenre: {str(e)}")



#5 - Version JSON
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   14 de Septiembre de 2023
Objetivo:   Obtiene datos de desarrolladores filtrados por nombre.
Params  :   developer (str): Nombre del desarrollador.
Returns :   JSONResponse   : Datos del desarrollador en formato JSON.
--------------------------------------------------------------------------------'''
def getDeveloperData(developer: str = Query(..., description="Desarrollador (alfanumérico con caracteres especiales permitidos)")):

    try:

        # Quitar espacios en blanco del principio y el final
        developer = developer.strip()

        # Validar que developer esté presente
        if not developer:
            return JSONResponse(content = ["El parámetro 'developer' es obligatorio y no puede estar vacío."])

        # Validar que developer sea alfanumérico con caracteres especiales permitidos
        if not developer.isalnum():
            return JSONResponse(content = ["El parámetro 'developer' debe ser alfanumérico con caracteres especiales permitidos."])
        
        #Abrimos archivos
        df_developer = leerJsonGz("Datos/","content_developer.json.gz",1)

        # Filtramos los df por user_id
        df_developer = df_developer[df_developer['developer'].str.lower() == developer.lower()]

        # Validar si se encontraron registros
        if df_developer.shape[0] == 0:
            return JSONResponse(content=["El Developer no ha sido Encontrado"])
        
        #formateamos Developer
        df_developer['developer'] = df_developer['developer'].astype(str)
        df_developer['developer'] = df_developer['developer'].str.capitalize()

        # Formateamos perc_recommend
        df_developer['free_content'] = df_developer['free_content'].apply(lambda x: '{:.2f}'.format(x))
        df_developer['free_content'] = df_developer['free_content'].astype(str) + ' %'

        #Ordenamos por Year y generamos DF final
        result = df_developer.sort_values(by='year', ascending=False)
        
        # Renombramos las columnas
        result.columns = ['DEVELOPER', 'YEAR', 'ITEMs COUNT', '% FREE CONTENT']
        
        #convertimos el DF a diccionario y luego JSON
        result_list = result.to_dict(orient = 'records')

        return JSONResponse(content = result_list)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getDeveloperData: {str(e)}")


#5 - Version HTML
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   15 de Septiembre de 2023
Objetivo:   Obtiene datos de desarrolladores filtrados por nombre.
Params  :   developer (str): Nombre del desarrollador.
Returns :   JSONResponse   : Datos del desarrollador en formato HTML. 
--------------------------------------------------------------------------------'''
def getDeveloperDataHtml(developer: str = Query(..., description="Desarrollador (alfanumérico con caracteres especiales permitidos)")):

    try:

        # Quitar espacios en blanco del principio y el final
        developer = developer.strip()

        # Validar que developer esté presente
        if not developer:
            return JSONResponse(content = ["El parámetro 'developer' es obligatorio y no puede estar vacío."])

        # Validar que developer sea alfanumérico con caracteres especiales permitidos
        if not developer.isalnum():
            return JSONResponse(content = ["El parámetro 'developer' debe ser alfanumérico con caracteres especiales permitidos."])
        
        #Abrimos archivos
        df_developer = leerJsonGz("Datos/","content_developer.json.gz",1)

        # Filtramos los df por user_id
        df_developer = df_developer[df_developer['developer'].str.lower() == developer.lower()]

        # Validar si se encontraron registros
        if df_developer.shape[0] == 0:
            return JSONResponse(content=["El Developer no ha sido Encontrado"])
        
        # Formateamos perc_recommend
        df_developer['free_content'] = df_developer['free_content'].apply(lambda x: '{:.2f}'.format(x))
        df_developer['free_content'] = df_developer['free_content'].astype(str) + ' %'

        #Ordenamos por Year y generamos DF final
        result = df_developer.sort_values(by='year', ascending=False)
        
        # Renombramos las columnas
        result.columns = ['DEVELOPER', 'YEAR', 'ITEMs COUNT', '% FREE CONTENT']
        
        #convertimos el DF a diccionario y luego JSON
        result_list = result.to_dict(orient = 'records')

        # Generar el contenido HTML de la tabla
        table_html = "<table width='auto' align='left'>"  
        table_html += "<tr><th align='center'>YEAR</th><th align='center'>ITEMs COUNT</th><th align='center'>% FREE CONTENT</th></tr>"

        for item in result_list:
            table_html += f"<tr><td align='center'>{item['YEAR']}</td><td align='center'>{item['ITEMs COUNT']}</td><td align='center'>{item['% FREE CONTENT']}</td></tr>"

        table_html += "</table>"

        developer = developer.title()
        
        # HTML completo con la tabla
        html_content = f"""
        <html>
        <head>
            <style>
                table {{
                    border-collapse: collapse;
                    width: auto;  /* Ajustar al contenido */
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                    text-align: center;  /* Centra el texto en celdas */
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                h1 {{
                    text-align: left;  /* Alinea el título principal a la izquierda */
                }}
            </style>
        </head>
        <body>
            <h1>{developer}</h1>
            {table_html}
        </body>
        </html>
        """

        return HTMLResponse(content=html_content)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getDeveloperDataHtml: {str(e)}")


#6
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   14 de Septiembre de 2023
Objetivo:   Realiza un análisis de sentimiento para un año específico.
Params :    year (int)  : Año para el análisis de sentimiento.
Returns :   JSONResponse: Resultado del análisis de sentimiento en formato JSON. 
--------------------------------------------------------------------------------'''
def getSentimentAnalysisForYear(year: str = Query(..., description="Año (4 dígitos)")):

    try:

        # Quitar espacios en blanco del principio y el final
        year = year.strip()
        
        # Validar que year esté presente
        if not year:
            return JSONResponse(content=["El parámetro 'year' es obligatorio y no puede estar vacío."])

        # Validar que year sea un número
        if not year.isdigit():
            return JSONResponse(content=["El parámetro 'year' debe ser un número."])
        
        # Validar que year sea un número de 4 dígitos
        if len(year) != 4:
            return JSONResponse(content=["El parámetro 'year' debe ser un número de 4 dígitos."])
        

        #convertimos a int
        year = int(year)

        #Abrimos archivos
        df_sentiment = leerJsonGz("Datos/","reviews_year.json.gz",1)

        #filtramos
        df_sentiment = df_sentiment[df_sentiment['year'] == year]

        # Validamos si hay registros para ese año
        if df_sentiment.shape[0] ==0:
            return JSONResponse(content=["No hay registros correspondientes al año ingresado"])

        #recuento de sentiments
        positivos = df_sentiment['Positivos'].iloc[0]
        negativos = df_sentiment['Negativos'].iloc[0]
        neutrales = df_sentiment['Neutros'].iloc[0]

        #Creamos un DF
        data = {'NEGATIVE': [negativos],
                'NEUTRAL':  [neutrales],
                'POSITIVE': [positivos]}

        result = pd.DataFrame(data)

        #convertimos el DF a diccionario y luego JSON
        result_list = result.to_dict(orient = 'records')

        return JSONResponse(content = result_list)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getSentimentAnalysisForYear: {str(e)}")
    

    
'''-------------------------------------------------------------------------------------------
                             SECCION MACHINE LEARNING
-------------------------------------------------------------------------------------------'''


#7 
'''-------------------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   16 de Septiembre de 2023
Objetivo:   Obtener recomendaciones basadas en un ítem específico.
Params  :   item_id (str) - El ID del ítem para el cual se desea obtener recomendaciones.
Returns :   Una lista de los IDs de los ítems recomendados.
-------------------------------------------------------------------------------------------'''
def getRecommendationByItem(item_id: str = Query(..., description="Item Id Numerico")):

    try:

        # Validar que year esté presente
        if not item_id:
            return JSONResponse(content = ["El parámetro 'item_id' es obligatorio y no puede estar vacío."])

        # Validar que year sea un número
        if not item_id.isdigit():
            return JSONResponse(content = ["El parámetro 'item_id' debe ser un Numerico."])
        
        #Casteamos la variable 
        item_id = int(item_id)
        
        #Abrimos archivos
        df_recommendations = leerJsonGz("Datos/","df_recommendations.json.gz",1)

        # Establecer 'item_id' como el índice
        df_recommendations.set_index('item_id', inplace=True)
        #convertimos el indice en int
        df_recommendations.index = df_recommendations.index.astype(int)
        
        if item_id not in df_recommendations.index:
            df_default_recommend_5 = leerJsonGz("Datos/","default_recommend_5.json.gz",1)
            recommendations = df_default_recommend_5['item_id'].tolist()
        else:
            # Obtener las 5 recomendaciones para el item_id especificado
            recommendations = df_recommendations.loc[item_id].tolist()
        
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getRecomendationByItem: {str(e)}")
    

#8
'''-------------------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   21 de Septiembre de 2023
Objetivo:   Obtener recomendaciones basadas en un user.
Params  :   user_id (str) - El ID del user para el cual se desea obtener recomendaciones.
Returns :   Una lista de los IDs de los ítems recomendados para ese user.
-------------------------------------------------------------------------------------------'''
def getRecommendationByUser(user_id: str = Query(..., description="ID del usuario (alfanumérico con caracteres especiales permitidos)")):

    try:

        # Quitar espacios en blanco del principio y el final
        user_id = user_id.strip()

        # Validar que user_id esté presente
        if not user_id:
            return JSONResponse(content = ["El parámetro 'user_id' es obligatorio y no puede estar vacío."])
        
        #Abrimos archivos
        df_most_played_by_user = leerJsonGz("Datos/","most_played_by_user.json.gz",1)

        # Buscar el usuario en df_most_played_by_user
        user_row = df_most_played_by_user[df_most_played_by_user['user_id'] == user_id]

        #Valido si el usuario esta en el archivo
        if user_row.shape[0] > 0:
            # Invoco a getRecommendationByItem con el item mas jugado por el usuario
            most_played_item_id = user_row['most_played_item_id'].values[0]
            most_played_item_id = str(most_played_item_id)
            return getRecommendationByItem(most_played_item_id)
        else:
            # El usuario no existe en el DataFrame retornamos TOP 5 de juegos
            df_default_recommend_5 = leerJsonGz("Datos/","default_recommend_5.json.gz",1)
            recommendations = df_default_recommend_5['item_id'].tolist()

        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getRecommendationByUser: {str(e)}")