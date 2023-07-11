#from typing import Union
import pandas as pd
import numpy as np
import json
import uvicorn
from fastapi import FastAPI
from fastapi import Response
from pydantic import BaseModel
from datetime import datetime

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title='Desarrollo de API',
              description='Sistema de recomendacion de peliculas',
              version='1.0.1')

# Se ingestan los datos y se crea un dataframe
df = pd.read_csv("datos_limpios.csv")
df1 = pd.read_csv("data_ml.csv")

@app.get('/peliculas_idioma/{Idioma}')    
# Se ejecuta cuando se hace una solicitud GET a la raiz de la API
# Asi mismo, procesan las solicitudes desde el cliente y generan las respuestas correspondientes
# desde el servidor


# Se crea la función con un argumento con la forma 'Idioma=es'
def peliculas_idioma(Idioma: str):
    """Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo, 
       algunos idiomas que reconoce: ['en','fr','zh','it','fa','nl','de','cn','ar','es','ru','sv','ja','ko','sr','bn','he' 'pt','wo','ro','hu','cy'"""
    # se filtra esgun el idioma
    peliculas_filtradas = df[df['original_language'] == Idioma]
    
    # calculamos la cantidad de peliculas
    cantidad_peliculas = len(peliculas_filtradas)# .count()
    
    # Se crea el diccionario de respuesta
    respuesta = {'idioma': Idioma,'cantidad_peliculas': cantidad_peliculas}

    # Convertimos el diccionario a JSON
    json_data = json.dumps(respuesta, indent=4)
    response = Response(content=json_data, media_type="application/json")    
    return response

@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    '''Ingresas la pelicula, retornando la duracion y el año'''
    #df=pd.read_csv('archivo_completos.csv')
    filtrado=df[df['title']==pelicula].runtime.item()#.iloc[0]
    anio=df[df['title']=='Toy Story'].release_year.item()#.iloc[0]
    respuesta={'pelicula':pelicula, 'duracion':filtrado, 'anio':anio}

    json_data = json.dumps(respuesta, indent=4)
    response = Response(content=json_data, media_type="application/json")    
    return response

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    #df=pd.read_csv('archivo_completos.csv')
    df1=df[df['belongs_to_collection']==franquicia].drop_duplicates(subset=['id'])
    cantidad=len(df1.title)#.count()
    ganancia=int(df1.revenue.sum())#debo convertir a entero porque json no puede 
    ganancia_promedio=ganancia/ cantidad if cantidad >0 else 0
    
    respuesta= {'franquicia':franquicia, 'cantidad':cantidad, 'ganancia_total':ganancia, 'ganancia_promedio':ganancia_promedio}

    json_data = json.dumps(respuesta, indent=4)
    response = Response(content=json_data, media_type="application/json")    
    return response

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    #df=pd.read_csv('archivo_completos.csv')
    filtrados_pais = df[df['production_countries'].str.contains(pais,na=False,case=False)]
    
    filtrado=filtrados_pais['title'].shape[0]
    respuesta= {'pais':pais, 'cantidad':filtrado}

    json_data = json.dumps(respuesta, indent=4)
    response = Response(content=json_data, media_type="application/json")    
    return response

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
    '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    filtrados_pais = df[df['production_companies'].str.contains(productora,na=False,case=False)]#.apply(lambda lista: isinstance(lista, list) and any(productora in prod for prod in lista))]
    cantPeliculas=filtrados_pais['title'].shape[0]
    revenue=int(filtrados_pais['revenue'].count())
    respuesta= {'productora':productora, 'revenue_total': revenue,'cantidad':cantPeliculas}

    json_data = json.dumps(respuesta, indent=4)
    response = Response(content=json_data, media_type="application/json")    
    return response

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    director=df[df['director_name']==nombre_director]
    
    retorno_pelicula=int(director['return'].sum())
    peliculas=director['title'].tolist()
    anio=director['release_year'].tolist()
    budget_pelicula=int(director['budget'].sum())
    revenue_pelicula=int(director['revenue'].sum())

    respuesta= {'director':nombre_director, 
    'peliculas':peliculas, 'anio':anio, 'retorno_pelicula':retorno_pelicula, 
    'budget_pelicula':budget_pelicula, 'revenue_pelicula':revenue_pelicula}

    json_data = json.dumps(respuesta, indent=4)
    response = Response(content=json_data, media_type="application/json")    
    return response

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    df['title']=df['title'].astype(str)
    titulos=df['title'].head(5000)
    #vectorizador de palabras
    vectorizador=CountVectorizer()
    m_cont=vectorizador.fit_transform(titulos)
    similitud=cosine_similarity(m_cont)
    #obtener indice de peliculas ingresada
    ind_pelicula=titulos[titulos==str(titulo)].index[0]
    puntaje_simil=list(enumerate(similitud[ind_pelicula]))
    puntaje_simil=sorted(puntaje_simil,key=lambda x:x[1],reverse=True)
    peliculas_similares=[titulos[indice] for indice, _ in puntaje_simil[1:6]]
    respuesta= {'lista recomendada': peliculas_similares}
    json_data = json.dumps(respuesta, indent=4)
    response = Response(content=json_data, media_type="application/json")    
    return response