# Proyecto Final: Bootcamp BigData&MachineLearning

**Equipo:** The Crash  
**Nombre de los componentes:**  
Fernando Parada   
Luis Bastos  
Miguel Escudero Lucena  
Veronica Fuentealba Riquelme  
Juan Antonio Roldan Paco  
**Fecha:** agosto - 2020  
**Bootcamp:** BIG DATA & MACHINE LEARNING - KEEPCODING

## Índice:

**Índice**
1. [Objetivo](#id1)
2. [Conjunto de datos](#id2)
3. [Creación latitud y longitud en el dataset inicial](#id3)
4. [Cálculo distancia a zonas de ocio y distancia a radares](#id4)
5. [Visualización de datos Tableau](#id5)
6. [Limpieza, análisis exploratorio y procesamiento de datos](#id6)
7. [Modelado con algoritmos de Machine Learning](#id7)
8. [Modelado con algoritmos de Deep Learning](#id8)
9. [Elección del modelo final](#id9)
10. [Arquitectura](#id10)
11. [Creación bot](#id11)
12. [Creación web](#id12)
13. [Metodología de trabajo](#id13)
14. [Conclusiones y mejoras](#id14)

## Objetivo <a name="id1"></a>
El objetivo del proyecto es poder predecir la lesividad en caso de accidente de tráfico. Para ello el usuario tendría que introducir unos datos en un bot de Telegram, o en una página web, y obtendría, en caso de accidente, la probabilidad de la lesividad.

## Conjunto de datos <a name="id2"></a>
El conjunto principal de datos los obtenemos del portal de datos abiertos de la Comunidad de Madrid, en concreto: Accidentes de tráfico de la Ciudad de Madrid.
Hemos cogido los datos del 2010 al 2018, puesto que los de 2019 y 2020 estaban incompletos, y los hemos unido en un único dataset:  
[Datos accidentes madrid](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=7c2843010d9c3610VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

Datos ocio nocturno. Cruzaremos nuestros datos con la distancia a los lugares de ocio, para saber si cerca de estos lugares hay más accidentes:  
[Datos ocio nocturno](https://www.esmadrid.com/opendata/noche_v1_es.xml)

Datos radares. Cruzaremos los datos con la distancia a los radares, para saber si hay menos accidentes en estos lugares:  
[Datos radares](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=4678f7de62435510VgnVCM2000001f4a900aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

Datos calendario. Cruzaremos los datos con los dias laborables y festivos de la comunidad de Madrid:  
[Datos calendario](https://datos.madrid.es/portal/site/egob/menuitem.3efdb29b813ad8241e830cc2a8a409a0/?vgnextoid=6cec1a94eae69510VgnVCM1000001d4a900aRCRD&vgnextchannel=102612b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default)

Datos distritos. Utilizaremos estos datos para mejorar la visualización de los datos en tableau:  
[Datos distritos](https://datos.madrid.es/portal/site/egob/menuitem.c05c1f754a33a9fbe4b2e4b284f1a5a0/?vgnextoid=46b55cde99be2410VgnVCM1000000b205a0aRCRD&)

## Creación latitud y longitud en el dataset inicial <a name="id3"></a>
Lo primero que hemos tenido que hacer es conseguir la latitud y la longitud en el dataset inicial para poderlo unir a los demás dataset; para ello hemos creado 2 Notebooks que a partir de las calles obtiene la latitud y longitud:  
[Notebook 1 Creación Latitud y Longitud](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Creaci%C3%B3n%20dataset/1-%20CoordenadasFinal.ipynb)  
[Notebook 2 Creación Latitud y Longitud](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Creaci%C3%B3n%20dataset/2-%20Dataset%20limpio.ipynb)

## Cálculo distancia a zonas de ocio y distancia a radares <a name="id4"></a>
Para calcular las distancias a las zonas de ocio lo que hemos hecho ha sido extraer la latitud y longitud de los datos de ocio nocturno, que estaba en un XML, y crear un CSV; para ello hemos creado un Notebook:  
[Notebook extracción latitud y longitud XML](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Creaci%C3%B3n%20dataset/3-%20Extracci%C3%B3n%20noche_ocio.xml%20y%20creando%20Coordenadas_ocio.csv.ipynb)

Por último hemos extraído latitud y longitud del dataset de radares, dias festivos del dataset calendario y hemos unido todos los datasets en un mismo Notebook:  
[Notebook union datasets](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Creaci%C3%B3n%20dataset/4-%20Union%20Accidentes%20con%20los%20demas%20datasets.ipynb)

## Visualización de datos Tableau <a name="id5"></a>  
La visualización de TABLEAU es un paso previó a todos los análisis para tener una idea de los datos que se quieren explotar, para ello, se cargó la base de accidentes y se separa en 4 graficas:
1. Resumen General en el cual se muestran:    
a. Top 5 barrios con más accidentes    
b. top 3 meses con más accidentes    
c. Accidentes por día de la semana    
d. Top 5 horarios con mayor cantidad de Accidentes    
e. Top 5 con Tipos de Accidentes
2. Accidentes por año, mes y día, además muestra un mapa con los Barrios y % de accidentes
3. Análisis por Lesividad separado por mes, días hábiles, días no hábiles y rango horario, tiene como filtro el año.
4. Tipo de Vehículo, se pude ver el top 5 de rango horario  y Lesividad por semana, tiene como filtro el año.

[Archivos Tableau](https://github.com/TheCrashKeepcoding/Practica-Final/tree/master/Visualizaci%C3%B3n%20Tableau)

## Limpieza, análisis exploratorio y procesamiento de datos <a name="id6"></a>
Para este paso decidimos realizar tres análisis por separado, ya que no estábamos seguros de que la variable lesividad fuera la mejor. Analizamos sexo, tipo de vehículo y lesividad. Finalmente nos decidimos por lesividad, que, además de ser nuestro objetivo principal, dio mejores resultados en los modelos de machine learning:  
[Notebook analisis sexo](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Analisis%20exploratorio%20y%20Modelos/ANALISIS%20EXPLORATORIO%20SEXO.ipynb)  
[Notebook analisis Tipo vehiculo](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Analisis%20exploratorio%20y%20Modelos/ANALISIS%20EXPLORATORIO%20TIPO_VEHICULO%20Y%20ML.ipynb)  
[Notebook analisis lesividad](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Analisis%20exploratorio%20y%20Modelos/ANALISIS%20EXPLORATORIO%20LESIVIDAD.ipynb)

## Modelado con algoritmos de Machine Learning <a name="id7"></a>
Hemos comparado varios modelos de Machine learning (Lasso, regresión logística, árbol de decisión, Random Forest), y hemos elegido el que mejores resultados da, que es Random Forest:  
[Notebook Comparacion modelos Machine Learning](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Analisis%20exploratorio%20y%20Modelos/ALGORITMOS%20MACHINE%20LEARNING.ipynb)

## Modelado con algoritmos de Deep Learning <a name="id8"></a>  
Para nuestro proyecto, hemos probado algunos modelos de Deep Learning para ver si podemos mejorar el score conseguido con ML. Para ello, hemos probado modelos con y sin regularizadores , y con varias capas, sin conseguir en ningún caso mejorar lo obtenido en ML:  
[Notebook Comparacion modelos Deep Learning](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Analisis%20exploratorio%20y%20Modelos/ALGORITMOS%20DEEP%20LEARNING.ipynb)

## Elección del modelo final <a name="id9"></a>  
Nuestro modelo elegido es Random Forest, de Machine Learning, con este modelo haremos las predicciones de lesividad:  
[Notebook y datos train y test del modelo definitivo](https://github.com/TheCrashKeepcoding/Practica-Final/tree/master/Modelo%20ML%20definitivo)  
[Conclusiones para elección del modelo](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Modelo%20ML%20definitivo/CONCLUSIONES.ipynb)

## Arquitectura <a name="id10"></a>  
Hemos montado todo nuestro sistema en Google Cloud Service, para ello hemos utilizado lo siguiente:  
*	Google Storage
*	App Engine
*	Cloud source repositories
*	Notebook de Jupyter

1. Entrenamiento del modelo en jupyter.  
Limpieza del dataset y entrenamiento del modelo en un notebook de jupyter, desde el cual se realizara un pickle del modelo y se subirá directamente al Google Storage, tanto el modelo como el dataset.
2. Web desde App Engine.  
Montamos un servicio en App Engine donde estará nuestra web, que accedera al Storage de Google para acceder tanto al modelo como a los datos.
3. Desde el repositorio del cloud tenemos un fichero en Python que se va relanzado para que el bot este disponible siempre.
  
![Imagen arquitectura](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Imagenes/Arquitectura.png)

## Creación bot <a name="id11"></a>  
Para el bot emos puesto el main.py (Telegram.py) en Google Cloud Repositories y lo lanzamos a través del 'shell' con un script.sh para hacer un bucle y que no se desconecte automáticamente.  Tenemos un Pickle subido a un bucket del cual cogemos la información del modelo y lo juntamos con las respuestas del usuario de Telegram para darle la predicción.  
El usuario mediante la interacción con un bot introduciendo en una breve frase todos los datos necesarios, recibirá una predicción.  
@ChrashBot

[Archivo para crear bot Telegram](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Creaci%C3%B3n%20bot%20Telegram/telegram.py)

## Creación web <a name="id12"></a>  
En el caso de interactuar via web, el usuario se dirigirá a una API donde introduciendo los datos anteriormente descritos, el modelo le devolverá una predicción.  
[enlace web lesisvidad](https://calcium-spanner-264710.ew.r.appspot.com/)
 
[Archivos para crear web](https://github.com/TheCrashKeepcoding/Practica-Final/tree/master/Web)

## Metodología de trabajo<a name="id13"></a>  
Para la metodología de trabajo, hemos optado por usar la herramienta Trello, ya que nos ayuda a organizarnos mejor.

![Imagen Trello](https://github.com/TheCrashKeepcoding/Practica-Final/blob/master/Imagenes/Trello.png)

## Conclusiones y mejoras <a name="id14"></a>  
Inicialmente las ideas eran muchas, pero dado el tiempo de entrega se acordó tener un proyecto acotado el cual pudiéramos finalizar y entregar un PMV. Dentro de esos proyectos estaban:
1. Predictor de accidentes.
2. Seleccionar ruta origen y ruta destino e indicar la probabilidad de accidente.
3. Obtener datos climáticos de una web meteorológica.
4. Suscripción a mail para información respecto a Accidentes.
5. Predictor de Lesividad.  
Debido al tiempo nos quedamos con el predictor de lesividad. Los proyectos que no se abordaron quedan como mejoras esto, debido al volumen de información que se debe procesar y al poco tiempo que contamos para ello. 
Es importante destacar que para hacer un análisis se requiere mucho tiempo en extraer la información, que está sea fiable y verídica.
En el BigData las grandes V son Volumen, Velocidad, Veracidad, Variedad y Valor, con esto quiero indicar que en este proyecto se trato de abordar de mejor manera estás 5v’s, se trabajo con un volumen de data, nos preocupamos de que la información sea real, se complemento la información con otros dataset, como lugares de Ocio, días festivos, radares, y se entrega como resultado una predicción, que en este caso fue la lesividad.
Esperamos seguir trabajando en las mejoras, solo estamos viendo la punta de iceberg, hay mucho que trabajar y aprender en este camino de conocimiento constante.

