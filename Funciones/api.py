from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
import pandas as pd
from datetime import datetime
from Funciones.json_func import *


#ROOT
'''--------------------------------------------------------------------------------
Autor   :   Ing. Fernando G. Cofone
Fecha   :   13 de Septiembre de 2023
Objetivo:   Obtiene la información de la API.
Params  :    
Returns :   str: Información sobre la API. 
--------------------------------------------------------------------------------'''
def getIndex():

    try:
        texto = "API Creada por Ing. Fernando G. Cofone" + "\n"
        texto += "MLOPs - Recomendacion de Juegos."
        return texto
    
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
            raise HTTPException(status_code=400, detail="El parámetro 'user_id' es obligatorio y no puede estar vacío.")

        # Validar que user_id sea alfanumérico con caracteres especiales permitidos
        if not user_id.isalnum():
            raise HTTPException(status_code=400, detail="El parámetro 'user_id' debe ser alfanumérico con caracteres especiales permitidos.")
        
        #Abrimos archivos
        df_spent     = leerJsonGz("Datos/","spent_by_user.json.gz",1)
        df_recommend = leerJsonGz("Datos/","perc_recommend_by_user.json.gz",1)
        df_count     = leerJsonGz("Datos/","count_items_by_user.json.gz",1)

        # Filtramos los df por user_id
        df_spent     = df_spent[df_spent['user_id'] == user_id]
        df_recommend = df_recommend[df_recommend['user_id'] == user_id][['user_id', 'perc_recommend']]
        df_count     = df_count[df_count['user_id'] == user_id]

        # Combinamos DFs
        result = df_spent.merge(df_recommend, on='user_id', how='outer').merge(df_count, on='user_id', how='outer')
        
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
            raise HTTPException(status_code=400, detail="Los parámetros 'start_date' y 'end_date' son obligatorios y no pueden estar vacíos.")

        # Validar el formato de las fechas
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date   = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="Las fechas deben estar en formato YYYY-MM-DD.")
        
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
        data = {'START DATE':   [start_date_str],
                'END DATE':     [end_date_str],
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
            raise HTTPException(status_code=400, detail="El parámetro 'genre' es obligatorio y no puede estar vacío.")

        # Validar que genre contenga solo letras y espacios
        if not all(char.isalpha() or char.isspace() for char in genre):
            raise HTTPException(status_code=400, detail="El parámetro 'genre' debe contener solo letras y espacios.")
        
        #Abrimos archivos
        df_genre_ranking = leerJsonGz("Datos/","genre_ranking.json.gz",1)
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
        genre = genre.strip()

        # Validar que genre esté presente
        if not genre:
            raise HTTPException(status_code=400, detail="El parámetro 'genre' es obligatorio y no puede estar vacío.")

        # Validar que genre contenga solo letras y espacios
        if not all(char.isalpha() or char.isspace() for char in genre):
            raise HTTPException(status_code=400, detail="El parámetro 'genre' debe contener solo letras y espacios.")
        
        #Abrimos archivos
        df_user_genre = leerJsonGz("Datos/","user_genre_ranking.json.gz",1)

        #Filtramos el DF
        df_user_genre = df_user_genre[df_user_genre['genres'].str.lower() == genre.lower()]

        #Agrupamos y sumamos playtime_forever
        df_user_genre = df_user_genre.groupby(['user_id', 'user_url'])['playtime_forever'].sum().reset_index()
        #Ordenamos por Playtime_forever
        df_user_genre = df_user_genre.sort_values(by='playtime_forever', ascending=False)
        # Restablecer los índices del DataFrame ordenado
        df_user_genre.reset_index(drop=True, inplace=True)

        # Renombramos Columnas
        df_user_genre.columns = ['USER ID', 'USER URL', 'PLAYTIME FOREVER']

        result_list = df_user_genre.head(5).to_dict(orient='records')

        return JSONResponse(content = result_list)
    
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
            raise HTTPException(status_code=400, detail="El parámetro 'developer' es obligatorio y no puede estar vacío.")

        # Validar que developer sea alfanumérico con caracteres especiales permitidos
        if not developer.isalnum():
            raise HTTPException(status_code=400, detail="El parámetro 'developer' debe ser alfanumérico con caracteres especiales permitidos.")
        
        #Abrimos archivos
        df_developer = leerJsonGz("Datos/","content_developer.json.gz",1)

        # Filtramos los df por user_id
        df_developer = df_developer[df_developer['developer'].str.lower() == developer.lower()]

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
            raise HTTPException(status_code=400, detail="El parámetro 'developer' es obligatorio y no puede estar vacío.")

        # Validar que developer sea alfanumérico con caracteres especiales permitidos
        if not developer.isalnum():
            raise HTTPException(status_code=400, detail="El parámetro 'developer' debe ser alfanumérico con caracteres especiales permitidos.")
        
        #Abrimos archivos
        df_developer = leerJsonGz("Datos/","content_developer.json.gz",1)

        # Filtramos los df por user_id
        df_developer = df_developer[df_developer['developer'].str.lower() == developer.lower()]

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
            raise HTTPException(status_code=400, detail="El parámetro 'year' es obligatorio y no puede estar vacío.")

        # Validar que year sea un número de 4 dígitos
        if not year.isdigit() or len(year) != 4:
            raise HTTPException(status_code=400, detail="El parámetro 'year' debe ser un número de 4 dígitos.")
        
        #convertimos a int
        year = int(year)

        #Abrimos archivos
        df_sentiment = leerJsonGz("Datos/","reviews_year.json.gz",1)

        #filtramos
        df_sentiment = df_sentiment[df_sentiment['year'] == year]

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
def getRecomendationByItem(item_id: str = Query(..., description="Item Id Numerico")):

    #Declaramos una variable para la cantidad de elementos a Recomendar
    N = 5

    try:

        # Validar que year esté presente
        if not item_id:
            raise HTTPException(status_code=400, detail="El parámetro 'item_id' es obligatorio y no puede estar vacío.")

        # Validar que year sea un número
        if not item_id.isdigit():
            raise HTTPException(status_code=400, detail="El parámetro 'item_id' debe ser un Numerico.")
        
        #Abrimos archivos
        df_similarities = leerJsonGz("Datos/","df_similarities.json.gz",1)

        # Establecer 'item_id' como el índice
        df_similarities.set_index('item_id', inplace=True)
        #convertimos el indice en int
        df_similarities.index = df_similarities.index.astype(int)
        
        if item_id not in df_similarities.index:
            return []
        
        similar_games = df_similarities.loc[item_id].sort_values(ascending=False)
        top_similar_games = similar_games.drop(item_id).index[:N]
        
        return top_similar_games
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en getRecomendationByItem: {str(e)}")
