<div style="text-align:center; color:#FCCf33;"> 
  <h1>MLOps - Sistema de Recomendación de Videojuegos</h1>
</div>

<p align="center">
  <img src="src/steam.png"  height=300>
</p>

# Autor

### Ing. Fernando G. Cofone
<br>

## Enlaces
<table>
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/fcofone" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
        <img src="\PI_ML_OPS_MOD_RECOMENDACION\src\linkedin.png" alt="LinkedIn" width="75" height="75">
        <br>Mi LinkedIn
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/fercof87/PI_ML_OPS_MOD_RECOMENDACION" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
        <img src="src/github.png" alt="GitHub" width="75" height="75">
        <br>GitHub
      </a>
    </td>
    <td align="center">
      <a href="https://pi-ml-ops-mod-recomendacion.onrender.com" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
        <img src="src/api.png" alt="Render" width="75" height="75">
        <br>Mi API
      </a>
    </td>
  </tr>
</table>
<hr>
<br>

## Descripción del Problema a Resolver

### <span style="color: #ff5733;">Contexto</span>

<p style="text-align: justify;">
Este proyecto aborda el desafío de crear un sistema de consulta y recomendación de videojuegos a partir de inputs de la plataforma STEAM, disponible a través de una API desplegada en Render.
</p>

### <span style="color: #ff5733;">Roles a Desempeñar</span>

<p style="text-align: justify;">
En el rol de Data Scientist, se nos encomienda la tarea de diseñar y desarrollar un sistema de recomendación de videojuegos para los usuarios de la plataforma. Sin embargo, nos enfrentamos a un obstáculo importante: los datos disponibles son crudos y carecen de madurez en términos de estructura y automatización. Esto requiere un trabajo significativo en Data Engineering antes de llegar a un Minimum Viable Product (MVP).

Además, como MLOps Engineer, debemos construir un modelo de recomendación de videojuegos similares al proporcionado por la API.
</p>

<br></br>

## Propuesta de Trabajo

### <span style="color: #ff5733;">EDA (Análisis Exploratorio de Datos)</span>

<p style="text-align: justify;">
En esta primera instancia, se cargaron los archivos JSON para identificar qué tipo de datos se encuentran y la calidad de los mismos. Se realizó un análisis exploratorio preliminar para comprender la complejidad de los datos a tratar.
</p>

### <span style="color: #ff5733;">ETL</span>

<p style="text-align: justify;">
Una vez comprendido el mundo de datos al que nos enfrentamos, se identificaron oportunidades para mejorar la eficiencia de la API y el entrenamiento de los modelos al leer el dataset en el formato adecuado, realizando las transformaciones y limpieza necesarias para un óptimo funcionamiento de nuestra API.
</p>

### <span style="color: #ff5733;">Feature Engineering</span>

<p style="text-align: justify;">
Se aplicó el análisis de sentimiento con procesamiento de lenguaje natural (NLP) a las reseñas de usuarios. El resultado fue la creación de una columna llamada 'sentiment_analysis', que califica las reseñas en 0 (negativa), 1 (Neutra) y 2 (Positiva).
</p>

### <span style="color: #ff5733;">Desarrollo de la API</span>

<p style="text-align: justify;">
Se implementó una API utilizando el framework FastAPI para exponer los datos requeridos. La API proporciona una serie de endpoints diseñados para ofrecer información relevante y consultas útiles a los usuarios.
</p>

<br></br>

## Endpoints

### La API incluye los siguientes endpoints:

<p style="text-align: justify;">
Antes de mencionar cada una de las funcionalidades de la API, cabe destacar que se tomó la decisión de generar archivos reducidos para satisfacer las respuestas de la API. El objetivo principal fue optimizar el tiempo de respuesta. No solo se buscó el rendimiento al manipular solo los datos requeridos por cada endpoint, sino que también se optimizó el almacenamiento utilizado en la persistencia de estos archivos en Render. Esto último se logró utilizando el formato JSON comprimido con GZ.

- `/userdata(User_id: str)`: Proporciona detalles sobre el gasto del usuario, el porcentaje de recomendación basado en reseñas y la cantidad de ítems.

- `/countreviews(YYYY-MM-DD1: str, YYYY-MM-DD2: str)`: Calcula la cantidad de usuarios que realizaron reseñas entre las fechas proporcionadas y el porcentaje de recomendación basado en reseñas.

- `/genre(género: str)`: Muestra el puesto en el ranking para un género de videojuegos específico según la columna PlayTimeForever.

- `/userforgenre(género: str)`: Ofrece el top 5 de usuarios con más horas de juego en el género especificado, junto con su URL y user_id.

- `/developer(desarrollador: str)`: Presenta información sobre la cantidad de ítems y el porcentaje de contenido gratuito por año, según la empresa desarrolladora.

- `/sentiment_analysis(año: int)`: Devuelve una lista con la cantidad de registros de reseñas de usuarios categorizados con análisis de sentimiento para un año de lanzamiento dado.

- `/recommendation(item_id: int)`: Devuelve una lista de recomendación de 5 juegos similares al item_id suministrado. En caso de no encontrar el item_id, recomendará los 5 juegos con más calificaciones positivas detectadas en las reviews (sentiment_analysis).
</p>

## Análisis Exploratorio de los Datos (EDA)

<p style="text-align: justify;">
Antes de abordar el entrenamiento de modelos de Machine Learning, se realizó un análisis exploratorio de datos (EDA). Este proceso involucró la investigación de relaciones entre variables, la identificación de outliers y patrones en los datos. Se ajustaron los datos para que nuestro ML pueda funcionar correctamente.
</p>

## Modelo de Aprendizaje Automático

<p style="text-align: justify;">
Se desarrolló un modelo de Machine Learning para implementar un sistema de recomendación item-item: Basado en la similitud entre juegos, este sistema recomienda juegos similares al juego ingresado.

Para abordar el problema, se utilizó un sistema de recomendación, construyendo una matriz de similitudes con las distancias de coseno entre los productos.
</p>

## Implementación

<p style="text-align: justify;">
La API resultante se desplegó en la plataforma RENDER, facilitando el acceso a los usuarios para obtener recomendaciones de juegos.
</p>

<br></br>

## Librerías Utilizadas

<p style="text-align: justify;">
- **json/Gzip/ast**: Este conjunto de librerías me sirvió para realizar la lectura y persistencia de los archivos reducidos generados para los endpoints. Además, fueron utilizadas para particionar los inputs de entrada en archivos más pequeños, de esa manera me fue posible subirlos a GitHub y Render sin problemas.

- **TextBlob**: Utilizada para poder realizar el análisis de sentimientos sobre las reviews de los usuarios.

- **fuzzywuzzy**: Las fechas de nuestros inputs tenían una gran variedad de formatos. Para lograr capturar todos ellos, se utilizó una búsqueda fuzzy con un umbral de coincidencia superior al 80%.

- **FastAPI**: Se utilizó esta librería de Python para construir la API, utilizando respuestas tanto en formato JSON (JSONResponse) como en formato HTML (HTMLResponse).
</p>

<br></br>

## Organización del Repositorio

<p style="text-align: justify;">
- **Datos**: Aquí están todos los archivos generados en el proceso de ETL/EDA. Dentro de Datos/Particiones, están los 3 inputs de la plataforma Steam, pero particionados en partes más pequeñas, como se mencionó anteriormente.

- **Funciones**: Conjunto de todas las funciones desarrolladas, las cuales son utilizadas a lo largo del proyecto. Hay funciones de Fechas, Json, API y TextBlob. Se planteó desde el inicio el foco en la modularización y reutilización de código.

- **Logs**: Algunas funciones, sobre todo la de manipulación de los archivos JSON, generan logs en caso de error. Estos logs son guardados en este folder.

- **main.py**: archivo principal de la API.

- **ETL.py**: Análisis exploratorio, transformación de datos, imputaciones y generación de archivos reducidos.

- **particionamiento.py**: código empleado para fraccionar los inputs en partes más pequeñas.
</p>

<br>
<br>
<br>
<hr>

<p align="center">
  <a href="https://www.linkedin.com/in/fcofone" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
    <img src="src/linkedin.png" alt="LinkedIn" width="75" height="75">
    <br>Mi LinkedIn
  </a>
  <a href="https://github.com/fercof87/PI_ML_OPS_MOD_RECOMENDACION" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
    <img src="src/github.png" alt="GitHub" width="75" height="75">
    <br>GitHub
  </a>
  <a href="https://pi-ml-ops-mod-recomendacion.onrender.com" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
    <img src="src/api.png" alt="Render" width="75" height="75">
    <br>Mi API
  </a>
</p>
<hr>
<br>
<div style="text-align:center; color:#FCCf33;"> ¡Gracias por su interés en mi trabajo! </div>
