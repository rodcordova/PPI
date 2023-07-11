# Proyecto de Recomendación de Películas
Este es un proyecto que consiste en desarrollar un sistema de recomendación de películas basado en un modelo de machine learning. Además, se crea una API utilizando el framework FastAPI para consumir y acceder a los datos y funcionalidades del sistema de recomendación. A continuación, se detalla la estructura y los componentes principales del proyecto.

## Contenido
Transformaciones
Desarrollo de la API
Deployment
Análisis Exploratorio de los Datos (EDA)
Sistema de Recomendación
Transformaciones
En esta etapa, se aplican transformaciones a los datos para prepararlos y limpiarlos antes de su uso en el sistema de recomendación. Las transformaciones especificadas incluyen:

## Desanidar ciertos campos anidados en el dataset.
Rellenar los valores nulos de los campos "revenue" y "budget" con ceros.
Eliminar los valores nulos del campo "release_date".
Dar formato AAAA-mm-dd a las fechas y crear la columna "release_year".
Crear la columna "return" que calcula el retorno de inversión.
Eliminar columnas no utilizadas.
Desarrollo de la API
En esta sección se describe el desarrollo de la API utilizando el framework FastAPI. Se implementan 6 funciones para los endpoints que serán consumidos a través de la API:

## Caracteristica de las funciones
' peliculas_idioma(Idioma: str): 'Devuelve la cantidad de películas producidas en un idioma específico.
** peliculas_duracion(Pelicula: str): ** Devuelve la duración y el año de una película específica.
** franquicia(Franquicia: str): ** Devuelve la cantidad de películas, la ganancia total y el promedio de una franquicia específica.
** peliculas_pais(Pais: str): ** Devuelve la cantidad de películas producidas en un país específico.
** productoras_exitosas(Productora: str): ** Devuelve el revenue total y la cantidad de películas realizadas por una productora específica.
** get_director(nombre_director): ** Devuelve el éxito de un director específico y una lista de películas dirigidas por él, incluyendo la fecha de lanzamiento, el retorno individual, el costo y la ganancia de cada película.
Deployment

## Análisis Exploratorio de los Datos (EDA)
El EDA se realiza con el objetivo de investigar las relaciones entre las variables de los datasets y encontrar patrones interesantes. En esta etapa se exploran los datos limpios y se identifican posibles outliers o anomalías. Se sugiere realizar gráficas y visualizaciones relevantes para entender mejor los datos, como una nube de palabras con las palabras más frecuentes en los títulos de las películas.

## Sistema de Recomendación
El sistema de recomendación se basa en un modelo de machine learning que utiliza la similitud de puntuación entre películas para recomendar películas similares a los usuarios. La función recomendacion(titulo) recibe el nombre de una película y devuelve una lista de las 5 películas más similares, ordenadas por score de similitud.

## Contribuciones
Si deseas contribuir a este proyecto, puedes seguir los siguientes pasos:

Clona este repositorio en tu máquina local.
Crea una rama nueva para realizar tus modificaciones.
Realiza tus cambios y mejoras en la rama creada.
Envía un pull request con tus cambios y una descripción detallada de las modificaciones realizadas.
Licencia
