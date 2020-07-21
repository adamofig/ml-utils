# Dataframe con Pandas la guía esencial del homo sapiens .

La hoja de trucos, el acordeón, el consejero, el Inicio y el fin, etc...  

## El dataframe

Es una estructura de datos tabular que se compone filas y columnas similar a una tabla en un archivo de Excel, especialmente por que a diferencia de otras estructura esta tiene índices lo que garantiza nuevas formas  de acceder a los datos. Por este motivo es una herramienta muy poderosa para trabajar con datos especialmente para hacer análisis de información.

### Comparación con una hoja de calculo

Seguramente que alguna vez utilizaste Excel o Google Sheets, entonces este es un buen punto de partida para explicar el dataframe, mira el siguiente ejemplo. 

![Dataframe%20con%20Pandas%20la%20gu%20a%20esencial%20del%20homo%20sap%20663a6efe25dc4208a7a2c0d8a2d4cf70/Untitled.png](Dataframe%20con%20Pandas%20la%20gu%20a%20esencial%20del%20homo%20sap%20663a6efe25dc4208a7a2c0d8a2d4cf70/Untitled.png)

Cada columna tiene una etiqueta para que tu la identifiques, Iniciando desde la A luego B, C y así sucesivamente y cada renglón tiene un número,  en las hojas de calculo no  podemos cambiar este comportamiento,  sin embargo en el dataframe si, estos se llaman  índices y podemos darle el nombre que queramos.  Y visualmente es fácil saber cual es el peso de María,  y el dataframe nos ayudará a filtrar y encontrar rápidamente la información.

## Pandas.

Pandas es la biblioteca que vamos a utilizar, para aprender a utilizar dataframe, Dependiendo del lenguaje tecnología existen otras opciones, sin embargo pandas  es utilizada por los científicos de datos e ingenieros de ml. 

### Crear un dataframe.

Primero que nada necesitas los datos, puedes escribir directamente cada dato o puedes importarlo desde alguna fuente, CSV es el formato más popular y casi todos las herramientas saben exportar la información en este formato, teniendo este archivo nos basta una línea de código para iniciar tu dataframe, aquí se muestras las pociones

1) Leer el csv, tenemos varias funciones similares casi para cualquier formato 

`df1 = pd.read_csv("archivo.csv")`

`df2 = pd.read_csv("https://alguna_direccion_web.csv")`

2) Leer la lista de arreglos

```python
datos = [
  ["Juan", 16, 1.69], 
  ["Maria",15,1.60], 
  ["Pedro", 1.6, 1.73] 
  ]

df4 = pd.DataFrame(datos, columns=["Nombre", "Edad", "Altura"])
```

3) Leer lista de diccionarios

`datos = [ {"Nombre":"Juan", "Edad":16,"Altura": 1.69}, {"Nombre":"Maria", "Edad":15,"Altura": 1.60} {"Nombre":"Pedro", "Edad":16,"Altura": 1.73}  ] df3 = pd.DataFrame(datos)`

4) Crear dataframe vacío e ir agregando datos

```python
df5 = pd.DataFrame()
df5["Nombre"] = ["Juan","Maria", "Pedro"]
df5["Edad"] = [16,15,16]
df5["Altura"] = [1.69,1.60,1.73]
```

### Descarga rápida de Google Sheets,

Este es mi método favorito, cuando estoy probando a jungando y puedo tener la informacion en Google Sheets, primero hago publico el archivo obteniendo el enlace para compartir, y luego modifico la URL para que termine en lo siguiente /export?format=csv

`pd.read_csv("https://docs.google.com/spreadsheets/d/12MHNWZnbekh6RClFcxRcixMB90ooPsUsg3Tt9L7OllM/export?format=csv")`

Luego puedo leerlo en colab y modificar la información desde sheets siempre que lo necesite. 

### Dataframe vs Serie

Cuando solo tenemos los valores de una única columna con sus respectivos índices,  la llamamos  serie, son datos de una dimensión, saber identitarios a nivel código es importante, ya que uno accede a la serie con corchetes y a un dataframe con doble corchete como se muestra en el ejemplo

```python
# Obtener Serie 
df["Nombre"]
df.Nombre
# Obtener Dataframe
df[["Nombre"]]
df.Nombre.to_frame()
```

## Las primeras **Funciones**

Ya sea que quieras explorar o limpiar datos, estas son las primeas funciones que vas terminar aprendiendo al trabajar con dataframes. 

* head() y tail() muestra el número de registros de ejemplo

- df.sample() obtiene una muestra aleatoria de tus registros.

* df.describe() resumen estadistico de los datos.

* df.dtypes cada columna tiene su propio tipo de dato, y la mayoría de las veces se infiere de la fuente, con este comando puedes saber exactamente que tipo de dato tienes  además puedes revisar su distribución df.dtypes.value_counts()

* df.isnull().sum() Cuenta los nulos datos vacíos, útil cuando intentas descartar los registros que no te sirven. 

* df.COL_NAME.value_counts() Con esta función accedes a la serie y luego cuentas los valores diferentes, útil cuando tienes un catalogo y quieres saber cual es tu distribución de valores. 

### Limpiar un dataset

df.dropna() Elimnas todos los registros que tengan Nulos

* df.dropna(subset=[“fecha”, “token”]) , cuando quieres limpiar los datos, eliminas los registros cuando las columnas fecha y token ambas tienen su registro vacío. 

- df.duplicated(subset=[“correo”], keep=False): encuentra los registros duplicados,  subset puede especificar los campos duplicados keep puede conservar el primero encontrado o el ultimo ‘first’ ‘last’ y no lo marca como duplicado, df[df.duplicated(subset=[“correo”], keep=False)]

**Eliminar nulos NaN y NaT so acrinomos de Not a Number y Not a Time,** 

para muchas funciones es preferible no tenerlos, a veces hasta un valor None o otro default es mejor. 

lo mejor es detectar cuales son las columnas que presentan estos formatos  y vamos a sustituirlos por un valor None

df son las columnas totales y df2 el dataframe  filtrado con las columnas a eliminar o sustituir

df[df2.columns] = df2.replace([float('nan')], [None])

también es útil cuando queremos exportar el resultado a otro sistema. 

Aquí para que a un dataframe sacarle las columnas que nos interesan para que solo esas cambien a null y no todas

Df3= tiene las columnas pequeñas

Df2= tiene todo el dataset

### Trabajar con datos. Crear y filtrar , transformar.

## **Filtrar un dataframe**

La forma facil es

new_df =df[df['col-filter'] = value]

Los dataframes pueden filtrar por varios parámetros de columnas siempre y cuando se separen por parentesis y se agregue el operador indicado &, 

Nota como aqui son operadores especiales

df_colision = df_results[ (df_results["tipoSiniestro"]=='Colision') & (df_results["estado"]=='Distrito Federal')]

- Encontrar las columnas que son numéricas

Las algunas funciones como describe solo aplican sobre valores númericos, si quieres encontrar que columnas son númericas puedes usar una función como la siguiente

df.select_dtypes(include=np.number).columns.tolist()

Buscar un registro por ID

where

Buscar registros que tengan un valor particular. 

- seleccionar files con id específicos df_filter = df[‘ID’].isin([‘A001’,’C022',…])

### Crear más datos

Uno puede crear nuevas columnas con más datos, aplicando operadores lógicos sobre las columanas ya existentes 

df["data"]= df["col1"] + df["col2"]

df["data"]= df["col1"] + df["col2"]

Sin embargo habrá ocasiones en que el resultado es una lógica muy compleja, para esto  tenemos que usar una función lambda. ver al final 

* Cambiar una columnas con claves de catálogos ordinales por su valor descriptivo:

## **Funciones Lamda:**

### Problema al generar nuevas columnas

Siempre es posible hacer  operaciones aritméticas con dataframes para crear nuevas columnas, pero estamos limitados en operaciones, no podemos concatenar texto adiciona  entre 2 columnas. `col["uno"] + " : " + col["dos"]` y operaciones con lógicas complejas. 

Por eso va a ser útil hacer mapeos con apply, x puede representar toda la columna o cada fila dependiendo de eje, `axis = 1` , para ir tomando los valores como si fueran filas.

**Ejemplo** 

```python
data= [
	{"anio":2020, "mes": 4, "dia":20, "hora":0, "tipoSiniestro": "Colision", "estado": "Oaxaca" },
	{"anio":2020, "mes": 4, "dia": 21 , "hora":14 , "tipoSiniestro": "Colision", "estado": "Distrito Federal"}
	]

df = pd.DataFrame(data)

def get_dia(anio, mes, dia):
	return datetime.date(anio, mes, dia).weekday()

df["diaSemana"] = df.apply(lambda x: get_dia(x["anio"], x["mes"], x["dia"]), axis=1)
```

"x" representa cada columna del registro, con esto podemos pasar los datos a una función personalizada, que nos regresa el día de la semana. 

### Transformar y sustituir datos por un catálogo

En ocasiones vamos a tener una lista de valores clave que significan otra cosa, y para obtener la descripción tendríamos que cruzar con su catalogo descriptivo, sin embargo también podemos aplicar un mapeo, ejemplo si tenemos los valores [1,2,3,1,2] y tenemos el diccionario de valores para cada clave.

level_map = {1: ‘high’, 2: ‘medium’, 3: ‘low’}

Podemos sustituir el valor original y obtener la nueva columna con sus respectivos valores (desnormalizada)  

df[‘descripcion’] = df[‘claves’].map(level_map)

o usar una categoria y sustituir from_code

apply df[‘campo’].apply(lambda time: time.total_seconds() < 300)

## **Gráficar**

value counts.

Pandas tiene integrado plot con sus diferentes tipos como scatter line etc.

Regresa la referencia de ax, por lo que es posible si ejecutamos en la misma **celda**¡ visualizar multiples gráficas.

ax = dfp.plot(kind=”scatter”, x=”peso”, y=”altura”, color=”r”)

ax2 = df_pr.plot(kind=”scatter” , x = “peso”, y = “altura_pre”, ax=ax)

**Restar dataframes**

Si un dataframe se le resta una series, el valor de los índices se le resta a la columna.

Dataframe1

Series1

Dataframe1 - Series1

Esto es muy similar a su versión menos elegante, restar utilizando los valores en código duro.

Dataframe1['Valor1'] = Dataframe1['Valor1'] - 2

Dataframe1['Valor2'] = Dataframe1['Valor2'] - 1

Dataframe1['Valor3'] = Dataframe1['Valor3'] - 3

### Más avanzado, agrupar y agregar y unir

## **Agrupaciones.**

Agrupar nos regresa un objeto DataFrameGroupBy. este no muestra nada por si solo. ya que solo separó a nivel espacios de memoria pero no ha desempeñado ninguna operación de suma o conteo por ejemplo. de modo que en este estado es posible obtener cada grupo por una tabla con las claves del grupo por ejemplo como agrupe por día mes y hora, quiero el grupo que me dé día 30, mes 7 y hora 11.

Agrupamos porque queremos hacerle una operación de agregación como sumar los registros, pero hasta este momento no la hemos desempeñado.

Solo al momento de obtener los registros que tengan sentido para la agrupación podemos ejecutar las funciones de agregación.

Ejemplo grouped tiene todos los grupos ‘desagregados’, en la imagen previa se muestra el grupo resultante correspondiente al día 30, mes 7, hora 11, que pasaría sin contamos cualquiera de sus registros, como registros? o hora, no importa el resultado siempre va a ser 3, entonces el resultado sería

30,7,11,(3)

30,7,12,(X)

30,7,13,(X)

….

# Nota por default intenta hacer día mes y hora como índice, pero #para que se parezca a sql tenemos que desactivarlo

grouped = df.groupby(["dia", "mes", "hora"], as_index=False)

grouped[[“registros”]].count()

Nota por default nos da un indice por cada grupo y sus valores correspondientes pero no nos los registros continuos, esto hace que no se parezca a SQL , con la propiedad as_index=False evitará este problema y podremos trabajar de una forma mas natural.

Ahora otro punto importante es que hay una diferencia entre size() y count()

count no cuenta los valores NAN, mientras que size cuenta por registro, solo hay que pensar que queremos, valores con algún valor, o registros en general.

grouped[[“registros”]].size().to_frame(‘count’).reset_index()

### Agrupación y Agregación

Puedo agrupar y desempañear una función de agregación justo despues

df.groupby('estado').agg({'registros':sum}).sort_values('registros', ascending=False)

## **Unir datasets joins.**

Existe join y concat.

concat podemos verlo como una forma de union y join. ya que depende el Eje.

Nota por default agrupa por el indice, lo que significa que si antes trabajamos el dataframe nos dará un problema.

Ejemplo X y labels_df_1hot_encoder son 2 dataframes distintos. aunque tengan los mismos registros

Por Defaul axis es 0, signica que va a unir registros, estos deben concidir, y cuando axis es 1 va a juntar 2 dataframes por default deben concidir sus indices.

df_transformed = pd.concat([X, labels_df_1hot_encoder], axis=1)

Suponiendo que queremos un join donde 2 caracteristicas sean iguales podemos hacer, merge y usar el parámetro on para decir que caracteristicas debe igualar simiar a

Select * from tabla1 inner join tabla2 on tabla1.a=tabla2.a & tabla1.b = tabla2.b

df_cdmx = df_cdmx.merge(df_bq_c_cdmx[["mes","dia","Prediccion_TimeSeries"]], on=["mes","dia"],how="left" )

## Acceder a los datos por ubicación (location)

loc nos ayuda a obtener por registros por el nombre de tus indices y columnas 

df.loc[ _indices_ , _columnas_ ]

`df.loc[ [1,5], ["Nombre", "Peso"] ] # indices 1 y 5 , columnas Nombre y Peso`

si quieres todos los valores de  indices o columnas puedes poner  ":" 

`df.loc[ : , ["Nombre", "Edad"] ] # todos los registros , columnas nombre y edad`

si quieres el valor único no dataframe ni serie

`df.loc[ 1, "Nombre" ]`

 

iloc hace lo mismo pero por número de indice, es decir en vez de pongas el nombre con texto pon el número que le corresponde iniciando en 0.

Con el siguiente ejemplo tendríamos el registro 0,1, y 4 

`df.iloc[[1,2], [0,1,4]]`

Para el ejemplo, la columna cero uno y 4 correspondiete a 

Profundizar clic aqui 

**[Using iloc, loc, & ix to select rows and columns in Pandas DataFrames](https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/)**

Loc es más parecido a trabajar con numpy, porque tenemos rangos. luego iloc es igual pero nosotros debemos de darle un nombre.

## **Artículos y Referencias interesantes**

**SQL VS Pandas Sintaxis**

[https://medium.com/jbennetcodes/how-to-rewrite-your-sql-queries-in-pandas-and-more-149d341fc53e](https://medium.com/jbennetcodes/how-to-rewrite-your-sql-queries-in-pandas-and-more-149d341fc53e)

[https://towardsdatascience.com/10-python-pandas-tricks-that-make-your-work-more-efficient-2e8e483808ba](https://towardsdatascience.com/10-python-pandas-tricks-that-make-your-work-more-efficient-2e8e483808ba)

documentación de FOLIUM [https://python-visualization.github.io/folium/modules.html](https://python-visualization.github.io/folium/modules.html)

Iconos compatibles [https://getbootstrap.com/docs/3.3/components/](https://getbootstrap.com/docs/3.3/components/)

#cambiar tipos de datos dataframe

**puedes dejar todos los datos como string**

dataframe = dataframe.astype(str)