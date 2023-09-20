# main.py
from fastapi import FastAPI
from Funciones.api import *

#Creamos una instancia
app = FastAPI()

#END POINTs

#ROOT
@app.get("/")
async def index():
    return getIndex()

#1
@app.get("/userdata/{user_id:path}")
async def userData(user_id: str):
    return getUserData(user_id)

#2
@app.get("/countreviews/")
async def countReviews(start_date: str, end_date: str):
    return getCountReviews(start_date,end_date)

#3
@app.get("/genre/{genre:path}")
async def genre(genre: str):
    return getGenreRank(genre)

#4
@app.get("/userForGenre/{genre:path}")
async def userForGenre(genre: str):
    return getUserForGenre(genre)

#5
@app.get("/developer/{developer:path}")
async def developer(developer: str):
    return getDeveloperDataHtml(developer)

#6
@app.get("/sentimentAnalysis/{year:path}")
async def sentimentAnalysis(year: str):
    return getSentimentAnalysisForYear(year)


#7 - Machine Learning - Recomendacion by Item
@app.get("/recommendation/{item_id:path}")
async def recommendation(item_id: str):
    return getRecommendationByItem(item_id)