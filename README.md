<div style="text-align:center; color:#FCCf33;"> 
  <h1>MLOps - Sistema de Recomendación de Videojuegos</h1>
</div>

<div style="text-align:center;"> 
  <h2>Proyecto Individual N°1 - Data Science Part Time (Henry BootCamp)</h2>
</div>

<p align="center">
  <img src="src/steam.png"  height=300>
</p>

# Autor
### Ing. Fernando G. Cofone
<br>

## Enlaces

<table style="border-collapse: collapse; margin-left: auto; margin-right: auto; width: 80%;">
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/fcofone" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
        <img src="src/linkedin.png" alt="LinkedIn" width="75" height="75">
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
    <td align="center">
      <a href="https://www.youtube.com.ar" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
        <img src="src/youtube.png" alt="Presentacion" width="75" height="75">
        <br>Presentación
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

La API posibilita la interacción con el usuario para obtener datos específicos sobre videojuegos y proporcionar recomendaciones en función de similitudes con otros juegos, todo ello según las entradas proporcionadas por el usuario.
</p>

### <span style="color: #ff5733;">Roles a Desempeñar</span>

<p style="text-align: justify;">
En mi rol como Data Scientist, me encontré ante el desafío de concebir y desarrollar un sistema de recomendación de videojuegos para los usuarios de la plataforma. Sin embargo, me topé con un obstáculo importante: los datos disponibles eran crudos y carecían de madurez en términos de estructura y automatización. Esto me llevó a realizar un trabajo significativo en el ámbito de la Ingeniería de Datos antes de llegar a un Producto Mínimo Viable (MVP).

Además, en calidad de MLOps Engineer, desarrollé un modelo de recomendación de videojuegos que permite ingresar un item_id o un user_id como entrada, y la API recomendará los mejores 5 juegos para cada caso en particular.
</p>

<br></br>

## Etapas del Proyecto


### <span style="color: #ff5733;">1. Particionamiento de Archivos </span>

<p style="text-align: justify;">
Los tres archivos de entrada resultaron ser demasiado grandes para cargarlos en su totalidad en GitHub. Por lo tanto, se diseñó un conjunto de funciones específicas para gestionar estos archivos de manera eficiente. Además, se desarrolló un proceso que utiliza estas funciones para generar archivos particionados.

Gracias a esta solución, fue posible cargar los archivos de manera eficiente y sin contratiempos en GitHub.
</p>


### <span style="color: #ff5733;">2. EDA Preliminar (Análisis Exploratorio de Datos)</span>

<p style="text-align: justify;">
En esta  fase, se llevó a cabo un proceso de Análisis Exploratorio de Datos (EDA) preliminar. El objetivo principal de esta etapa fue cargar los archivos JSON y evaluar su contenido para identificar qué tipo de datos contenían y determinar la calidad de los mismos. Si bien este análisis no fue exhaustivo en su alcance, fue fundamental para obtener una visión general de la información contenida en cada columna y en cada conjunto de datos.

Durante esta tarea de EDA preliminar, se realizó una revisión inicial de las características clave de los archivos JSON, se identificaron las variables relevantes y se obtuvo una comprensión inicial de la estructura y la complejidad de los datos. Este proceso fue esencial para establecer las bases y orientar las acciones posteriores en el proyecto, proporcionando información valiosa sobre el alcance y la naturaleza de los datos con los que se trabajaría.
</p>

### <span style="color: #ff5733;">3. ETL</span>

<p style="text-align: justify;">
Una vez que obtuve una comprensión profunda del vasto conjunto de datos con el que estábamos lidiando, surgió la oportunidad de mejorar significativamente la eficiencia tanto de la API como del proceso de entrenamiento de los modelos. Esto se logró al implementar una lectura adecuada del dataset en el formato correcto, llevando a cabo las transformaciones necesarias y aplicando una exhaustiva limpieza de los datos para asegurar un funcionamiento óptimo de nuestra API.

Este proceso, sin duda, representó uno de los desafíos más intensos, ya que los datos presentaban numerosas impurezas y carencias. Mi máxima prioridad fue minimizar al máximo la pérdida de información, incluso trabajando en la reconstrucción de campos en los que la información era especialmente parcial o incompleta. El esfuerzo invertido en este paso crítico se tradujo en una base de datos más robusta y confiable, lo que a su vez se reflejó en la calidad de las recomendaciones ofrecidas por nuestra API y en la eficiencia de los modelos de entrenamiento.
</p>

### <span style="color: #ff5733;">4. Feature Engineering</span>

<p style="text-align: justify;">
Se llevó a cabo un análisis de sentimiento mediante el procesamiento de lenguaje natural (NLP) en las reseñas de usuarios, un paso esencial para comprender la percepción y la evaluación subyacentes en los comentarios. Como resultado de este proceso, se generó una nueva columna denominada 'sentiment_analysis', la cual asigna una calificación a las reseñas en una escala Discreta de 0 (negativa) a 2 (positiva), con un punto intermedio representado por el valor 1 (neutral).

Para lograr este análisis de sentimiento, se utilizó la biblioteca TextBlob, una herramienta poderosa en el campo del procesamiento de lenguaje natural. Durante la implementación, se establecieron límites tanto superiores como inferiores en la polaridad, lo que permitió clasificar las reseñas en función de su tono emocional y, a su vez, brindar una valiosa perspectiva sobre la satisfacción y la percepción de los usuarios con respecto a los productos o servicios en cuestión. Esta columna 'sentiment_analysis' resultante se convirtió en un recurso valioso para futuros análisis y para la confeccion de los modelos de Recomendación.
</p>

### <span style="color: #ff5733;">5. Análisis Exploratorio de los Datos (EDA)</span>

<p style="text-align: justify;">
Antes de sumergirnos en el proceso de entrenamiento de modelos de Machine Learning, se llevó a cabo un análisis exploratorio de datos (EDA) de mayor profundidad. Este proceso fue mucho más que una mera exploración superficial de los datos; implicó una investigación exhaustiva para descubrir relaciones entre variables, detectar la presencia de valores atípicos (outliers) y analizar patrones significativos en el conjunto de datos.

Durante esta etapa avanzada de EDA, se utilizaron diversas técnicas estadísticas y visuales para comprender mejor la estructura y el comportamiento de los datos. Se exploraron las relaciones complejas entre las variables, se identificaron las interacciones clave y se investigaron las causas potenciales de los valores atípicos. Además, se aplicaron transformaciones y ajustes específicos para garantizar que los datos estuvieran en condiciones óptimas para el correcto funcionamiento de nuestros modelos de Machine Learning.

En resumen, este análisis exploratorio de datos a un nivel más profundo no solo proporcionó una visión más completa de la información contenida en los datos, sino que también sentó las bases sólidas para un entrenamiento de modelos más preciso y eficaz.
</p>


### <span style="color: #ff5733;">6. Modelo de Aprendizaje Automático</span>

<p style="text-align: justify;">
Se diseñó un modelo de Machine Learning con el propósito de implementar un sistema de recomendación de tipo "item-item". Este sistema se basa en la similitud entre los juegos, lo que le permite sugerir juegos similares al que se introduce como referencia.

Para abordar este desafío, se empleó una técnica de recomendación que implica la creación de una matriz de similitud, la cual se basa en las medidas de distancia de coseno entre los diferentes productos. Esta matriz de similitud es esencial para identificar las relaciones y similitudes entre los juegos, permitiendo así que el sistema realice recomendaciones basadas en esta información.

Además de esto, se ha desarrollado un modelo adicional de recomendación de tipo "User-Item". Este modelo toma como punto de partida el juego más jugado por un usuario y, utilizando el modelo "item-item" como apoyo, genera recomendaciones de 5 juegos similares. De esta manera, se proporciona una experiencia de recomendación más personalizada, adaptada a los gustos y preferencias específicos de cada usuario.
</p>

### <span style="color: #ff5733;">7. Desarrollo de la API</span>

<p style="text-align: justify;">
Se implementó una API utilizando el framework FastAPI para exponer los datos requeridos. La API proporciona una serie de endpoints diseñados para ofrecer información relevante y consultas útiles a los usuarios.
</p>

<p style="text-align: justify;">
Antes de mencionar cada una de las funcionalidades de la API, cabe destacar que se tomó la decisión de generar archivos reducidos para satisfacer las respuestas de la API. El objetivo principal fue optimizar el tiempo de respuesta. No solo se buscó el rendimiento al manipular solo los datos requeridos por cada endpoint, sino que también se optimizó el almacenamiento utilizado en la persistencia de estos archivos en Render. Esto último se logró utilizando el <strong>formato JSON comprimido con GZ</strong>.

**La API incluye los siguientes endpoints:**

- `/userdata(User_id: str)`: Proporciona detalles sobre el gasto del usuario, el porcentaje de recomendación basado en reseñas y la cantidad de ítems. 

- `/countreviews(YYYY-MM-DD1: str, YYYY-MM-DD2: str)`: Calcula la cantidad de usuarios que realizaron reseñas entre las fechas proporcionadas y el porcentaje de recomendación basado en reseñas.

- `/genre(género: str)`: Muestra el puesto en el ranking para un género de videojuegos específico según la columna PlayTimeForever.

- `/userforgenre(género: str)`: Ofrece el top 5 de usuarios con más horas de juego en el género especificado, junto con su URL y user_id.

- `/developer(desarrollador: str)`: Presenta información sobre la cantidad de ítems y el porcentaje de contenido gratuito por año, según la empresa desarrolladora. La particularidad de esta funcion es que retorna la respuesta en formato HTML.

- `/sentiment_analysis(año: int)`: Devuelve una lista con la cantidad de registros de reseñas de usuarios categorizados con análisis de sentimiento para un año de lanzamiento dado.

- `/recommendationByItem(item_id: int)`: Devuelve una lista de recomendación de 5 juegos similares al item_id suministrado. En caso de no encontrar el item_id, recomendará los 5 juegos con más calificaciones positivas detectadas en las reviews (sentiment_analysis).

- `/recommendationByUser(user_id: str)`: Devuelve una lista de recomendación de 5 juegos recomendados para el user_id suministrado. En caso de no encontrar el user, recomendará los 5 juegos con más calificaciones positivas detectadas en las reviews (sentiment_analysis).

</p>
<br></br>


## Implementación

<p style="text-align: justify;">
La API resultante ha sido desplegada en la plataforma Render. Esto habilita la interacción de los usuarios con la API, permitiéndoles acceder y efectuar consultas o solicitudes de recomendaciones de videojuegos de manera sencilla y eficaz.
</p>

<br></br>

## Librerías Utilizadas

<p style="text-align: justify;">
  
- **json/Gzip/ast**: Este conjunto de librerías me sirvió para realizar la lectura y persistencia de los archivos reducidos generados para los endpoints. Además, fueron utilizadas para particionar los inputs de entrada en archivos más pequeños; de esa manera, me fue posible subirlos a GitHub y Render sin problemas.

- **TextBlob**: Utilizada para poder realizar el análisis de sentimientos sobre las reseñas de los usuarios.

- **Pandas**: Utilizado para la carga y manipulación de los datos de entrada.

- **fuzzywuzzy**: Las fechas de nuestros inputs tenían una gran variedad de formatos. Para lograr capturar todos ellos, se utilizó una búsqueda fuzzy con un umbral de coincidencia superior al 80%.

- **FastAPI**:  Se utilizó esta librería de Python para construir la API, utilizando respuestas tanto en formato JSON (JSONResponse) como en formato HTML (HTMLResponse).

- **matplotlib/Seaborn**: Utilizadas para graficar en mi análisis exploratorio (EDA).

- **nltk/collection/wordcloud**: Utilizadas para detectar las palabras más comunes en las reseñas de los usuarios en mi análisis exploratorio (EDA).

- **sklearn**: Utilizada para aplicar la función de distancia de coseno (cosine_similarity) en los modelos de recomendación.

- **uvicorn**: Empleada para realizar pruebas locales de la API.

</p>

<br></br>

## Organización del Repositorio

<p style="text-align: justify;">
  
- **Datos**: Aquí están todos los archivos generados en el proceso de ETL/EDA. Dentro de Datos/Particiones, están los 3 inputs de la plataforma Steam, pero particionados en partes más pequeñas, como se mencionó anteriormente.

- **Funciones**: Conjunto de todas las funciones desarrolladas, las cuales son utilizadas a lo largo del proyecto. Hay funciones de Fechas, Json, API y TextBlob. Se planteó desde el inicio el foco en la modularización y reutilización de código.

- **Logs**: Algunas funciones, sobre todo la de manipulación de los archivos JSON, generan logs en caso de error. Estos logs son guardados en este folder.

- **main.py**: archivo principal de la API.

- **ETL-EDA-ML.py**: Análisis exploratorio, transformación de datos, imputaciones y generación de archivos reducidos (incluidos los modelos de Recomendación).

- **particionamiento.py**: código empleado para fraccionar los inputs en partes más pequeñas.
  
</p>

<br>
<br>
<br>
<hr>

<table style="border-collapse: collapse; margin: 0 auto;">
  <tr>
    <td align="center">
      <a href="https://www.linkedin.com/in/fcofone" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
        <img src="src/linkedin.png" alt="LinkedIn" width="75" height="75">
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
    <td align="center">
      <a href="https://www.youtube.com.ar" style="margin: 0 5px; display: inline-block; padding: 5px; border-radius: 5px;">
        <img src="src/youtube.png" alt="Presentacion" width="75" height="75">
        <br>Presentación
      </a>
    </td>
  </tr>
</table>

<hr>
<br>

<table align="center">
  <tr>
    <td align="center">
      <div style="color:#FCCf33;"> 
        <p style="text-align: center;">
          ¡Gracias por su interés en mi trabajo!
        </p>
      </div>
    </td>
  </tr>
</table>
