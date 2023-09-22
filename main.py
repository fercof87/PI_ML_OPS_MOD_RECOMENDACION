# main.py
from fastapi import FastAPI, HTTPException
from Funciones.api import *

#Creamos una instancia
app = FastAPI()


#END POINTs

#ROOT
@app.get("/")
async def index():
    '''Informacion General de la API'''
    return getIndex()

#1
@app.get("/userData/{user_id:path}")
async def userData(user_id: str):
    '''Proporciona detalles sobre el gasto del usuario, el porcentaje de recomendación basado en reseñas 
    y la cantidad de juegos consumidos por el usuario.
    '''
    return getUserData(user_id)

#2
@app.get("/countReviews/")
async def countReviews(start_date: str, end_date: str):
    '''Calcula la cantidad de usuarios que realizaron reseñas entre las fechas proporcionadas y 
    el porcentaje de recomendación basado en reseñas..
    '''
    return getCountReviews(start_date,end_date)

#3
@app.get("/genre/{genre:path}")
async def genre(genre: str):
    '''Muestra el puesto en el ranking para un género de videojuegos específico según el 
    tiempo total jugados por todos los usuarios de la plataforma.
    '''
    return getGenreRank(genre)

#4
@app.get("/userForGenre/{genre:path}")
async def userForGenre(genre: str):
    '''Ofrece el top 5 de usuarios con más horas de juego en el género especificado.
    '''
    return getUserForGenre(genre)

#5
@app.get("/developer/{developer:path}")
async def developer(developer: str):
    '''Presenta información sobre la cantidad de ítems y el porcentaje de contenido gratuito por año, 
    según la empresa desarrolladora.
    '''
    return getDeveloperDataHtml(developer)

#6
@app.get("/sentimentAnalysis/{year:path}")
async def sentimentAnalysis(year: str):
    '''Devuelve una lista con la cantidad de registros de reseñas de usuarios categorizados 
    con análisis de sentimiento para un año de lanzamiento dado.
    '''
    return getSentimentAnalysisForYear(year)


#7 - Machine Learning - Recomendacion by Item
@app.get("/recommendationByItem/{item_id:path}")
async def recommendationByItem(item_id: str):
    '''Devuelve una lista de recomendación de 5 juegos similares al item_id suministrado.
    '''
    return getRecommendationByItem(item_id)


#8 - Machine Learning - Recomendacion by User
@app.get("/recommendationByUser/{user_id:path}")
async def recommendationByUser(user_id: str):
    '''Devuelve una lista de recomendación de 5 juegos de acuerdo al usuario ingresado.
    '''
    return getRecommendationByUser(user_id)