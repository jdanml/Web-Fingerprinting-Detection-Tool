# Web-Fingerprinting-Detection-Tool
# Herramienta de detección de *fingerprinting*

# Indice

* [Introducción](#Introducción)
* [Requisitos](#Requisitos)
* [OpenWPM](#OpenWPM)
* [Implementando un script de análisis](#Implementando-un-script-de-análisis)
* [Recomendaciones adicionales](#Recomendaciones-adicionales)
* [Comentarios](#Comentarios)

# Introducción

Para la detección de técnicas de extracción de huellas o *fingerprinting* activo, se implementan diversos scripts que consultan la base de datos en busca de parámetros como objetos JavaScript para verificar el cumplimiento de los criterios que caracterizan dichas técnicas (ej. Canvas, Objetos informativos, Canvas-Fuentes, WebRTC, etc.)

Este documento describe el entorno de la aplicación e incluye las formas en que el desarrollador puede implementar nuevos criterios de detección basado en la metodología aplicada a los scripts de análisis existentes.

# Requisitos

## Sistema Operativo 
Se recomienda Ubuntu 16.04/17.10/18.04.

## Versión de Python
* Python 3.5 o superior
* pip

## Dependencias
* OpenWPM (https://github.com/citp/OpenWPM). Para instalar OpenWPM, ejecuté el script **install.sh**. Si desea desarrollar la extensión que emplea OpenWPM para instrumentar o ejecutar ejecutar pruebas específicas a esta herramienta, emplee el script **install-dev.sh**.
* Anaconda (Recomendado) (https://docs.anaconda.com/anaconda/install/). Incluye los paquetes Pandas y Jupyter Notebook.
* Opcional. Para la correcta visualización de los elementos del notebook se recomienda:
    * Jupyter notebook extensions (https://github.com/ipython-contrib/jupyter_contrib_nbextensions)
    * Habilite las siguientes extensiones:
        * jupyter nbextension enable init_cell/main
        * jupyter nbextension enable hide_input/main

## Manejo de archivos
* El notebook de la aplicación esta diseñado para ejecutarse dentro de la misma carpeta donde se encuentra OpenWPM.
* Los scripts que ejecutan OpenWPM almacenan los resultados en la misma carpeta deonde se encuentra la herramienta.
* El nombre por defecto del fichero que contiene la base de datos es "crawl-data.sqlite". Los scripts de análisis implementados asumen por defecto que este fichero se encuentra en la carpeta con este nombre.

## OpenWPM
La herramienta empleada como *crawler*. Accede a diversos sitios web y almacena en una base de datos sqlite todos los elementos instrumentados. Consideraciones con respecto a OpenWPM:
* La documentación se encuentra disponible en https://github.com/citp/OpenWPM/wiki.
* Para habilitar la tabla "javascript" en la base de datos y almacenar los contenidos JavaScript de los sitios web, se debe habilitar la instrumentación de objetos JavaScript. Para ello, edite el fichero **automation/default_browser_params.json** y modifiqué la línea **"js_instrument": false** para establecerla en **"js_instrument": true**.
* Por defecto, OpenWPM ejecuta tres instancias del navegador.
* La tabla "javascript" de la base de datos presenta la siguiente estructura:

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>crawl_id</th>
      <th>visit_id</th>
      <th>script_url</th>
      <th>script_line</th>
      <th>script_col</th>
      <th>func_name</th>
      <th>script_loc_eval</th>
      <th>call_stack</th>
      <th>symbol</th>
      <th>operation</th>
      <th>value</th>
      <th>arguments</th>
      <th>time_stamp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2</td>
      <td>2</td>
      <td>https://www.google.es/?gws_rd=ssl</td>
      <td>1</td>
      <td>4003</td>
      <td></td>
      <td></td>
      <td></td>
      <td>window.navigator.userAgent</td>
      <td>get</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>None</td>
      <td>2018-05-17T07:55:55.380Z</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>https://www.google.es/?gws_rd=ssl</td>
      <td>1</td>
      <td>4092</td>
      <td></td>
      <td></td>
      <td></td>
      <td>window.navigator.userAgent</td>
      <td>get</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>None</td>
      <td>2018-05-17T07:55:55.380Z</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>2</td>
      <td>2</td>
      <td>https://www.google.es/?gws_rd=ssl</td>
      <td>1</td>
      <td>4093</td>
      <td></td>
      <td></td>
      <td></td>
      <td>window.navigator.userAgent</td>
      <td>get</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>None</td>
      <td>2018-05-17T07:55:55.380Z</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>3</td>
      <td>3</td>
      <td>https://www.google.es/?gws_rd=ssl</td>
      <td>1</td>
      <td>4003</td>
      <td></td>
      <td></td>
      <td></td>
      <td>window.navigator.userAgent</td>
      <td>get</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>None</td>
      <td>2018-05-17T07:55:55.878Z</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>3</td>
      <td>3</td>
      <td>https://www.google.es/?gws_rd=ssl</td>
      <td>1</td>
      <td>4092</td>
      <td></td>
      <td></td>
      <td></td>
      <td>window.navigator.userAgent</td>
      <td>get</td>
      <td>Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko...</td>
      <td>None</td>
      <td>2018-05-17T07:55:55.878Z</td>
    </tr>
  </tbody>
</table>
</div>



* Otra tabla de la base de datos que es de relevancia para la realización de consultas es "site_visits". Esta tabla nos permite conocer la URL del sitio web original (site_url) que llama al script.

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>visit_id</th>
      <th>crawl_id</th>
      <th>site_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>http://google.es</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>http://google.es</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
      <td>http://google.es</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>2</td>
      <td>http://blogspot.com.es</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>3</td>
      <td>http://blogspot.com.es</td>
    </tr>
  </tbody>
</table>
</div>



## Implementando un script de análisis
El desarrollo de un script de análisis puede descomponerse en 4 pasos:
1. Conexión con la base de datos.
2. Definición de variables.
3. Consulta de la base de la base de datos.
4. Representación de resultados.

### 1. Conexión con la base de datos.
Para conectarse a la base de datos, se realiza lo siguiente:


```python
#import sqlite3 as lite
wpm_db = "crawl-data.sqlite"
conn = lite.connect(wpm_db)
cur = conn.cursor()
```

### 2. Definición de variables. 

Se recomienda definir como variables los objetos JavaScript que permiten comprobar las condiciones de *fingerprinting*. Por ejemplo, para la técnica de Canvas se tendría:


```python
canvas_h = "HTMLCanvasElement.height"
canvas_w = "HTMLCanvasElement.width"
canvas_cf= "CanvasRenderingContext2D.fillStyle"
canvas_cs= "CanvasRenderingContext2D.strokeStyle"
canvas_ff= "CanvasRenderingContext2D.fillText"
canvas_fs= "CanvasRenderingContext2D.strokeText"
canvas_save= "CanvasRenderingContext2D.save"
canvas_rest= "CanvasRenderingContext2D.restore"
canvas_el= "HTMLCanvasElement.addEventListener"
canvas_data= "HTMLCanvasElement.toDataURL"
canvas_img= "CanvasRenderingContext2D.getImageData"
```

También se recomienda definir estrcuturas de datos para almacenar resultados parciales de acada criterio a verificar. Se destacan:
* Sets: Contienen valores únicos y sin ordenar. La primera característica es útil ya que permite evitar evitar duplicados por ejecutar diferentes instancias del navegador.
* Lists: Conjuntos modificables de valores. Pueden contener elementos duplicados.

Un ejemplo de lo mencionado para la técnica de Canvas es el siguiente:


```python
fp_1 = set()
fp_2 = set()
fp_3 = set()
fp_4 = set()
veri_1 = set()
veri_2 = set()
fp_sites = set()
```

* fp_1, fp_2, fp_3, fp_4: Almacenan resultados parciales por cada criterio asociado a la técnica de Canvas.
* veri_1, veri_2: Empleados para verificaciones parciales dentro de criterios específicos.
* fp_sites: Para almacenar los resultados finales.

### 3. Consulta de la base de la base de datos. 

Se empieza por ejecutar una consulta para buscar en la base de datos los objetos JavaScript de interés. Por ejemplo, para la verificación de la técnica de Canvas se puede ejecutar una consulta como la siguiente:


```python
for url, symbol, op, val, arg, top_url in cur.execute("SELECT distinct j.script_url, j.symbol, j.operation, j.value, j.arguments, v.site_url FROM javascript as j JOIN site_visits as v ON j.visit_id = v.visit_id WHERE j.symbol LIKE '%Canvas%' ORDER BY v.site_url;"):
```

Si ejecutáramos la consulta directamente a la base de datos, obtendríamos un resultado como el siguiente:

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>script_url</th>
      <th>symbol</th>
      <th>operation</th>
      <th>value</th>
      <th>arguments</th>
      <th>site_url</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>https://rs.20m.es/videoplayer/jw8/jwplayer.js?...</td>
      <td>HTMLCanvasElement.height</td>
      <td>set</td>
      <td>1</td>
      <td>None</td>
      <td>http://20minutos.es</td>
    </tr>
    <tr>
      <th>1</th>
      <td>https://rs.20m.es/videoplayer/jw8/jwplayer.js?...</td>
      <td>HTMLCanvasElement.width</td>
      <td>set</td>
      <td>1</td>
      <td>None</td>
      <td>http://20minutos.es</td>
    </tr>
    <tr>
      <th>2</th>
      <td>https://rs.20m.es/videoplayer/jw8/jwplayer.js?...</td>
      <td>HTMLCanvasElement.getContext</td>
      <td>call</td>
      <td></td>
      <td>{"0":"2d"}</td>
      <td>http://20minutos.es</td>
    </tr>
    <tr>
      <th>3</th>
      <td>https://rs.20m.es/videoplayer/jw8/jwplayer.js?...</td>
      <td>CanvasRenderingContext2D.fillStyle</td>
      <td>set</td>
      <td>#000000</td>
      <td>None</td>
      <td>http://20minutos.es</td>
    </tr>
    <tr>
      <th>4</th>
      <td>https://rs.20m.es/videoplayer/jw8/jwplayer.js?...</td>
      <td>CanvasRenderingContext2D.fillRect</td>
      <td>call</td>
      <td></td>
      <td>{"0":0,"1":0,"2":1,"3":1}</td>
      <td>http://20minutos.es</td>
    </tr>
  </tbody>
</table>
</div>



En este caso, recorremos toda la tabla resultante, verificando los criterios relacionados a la técnica de *fingerprinting* analizada. En el ejemplo que se presenta a continuación para la técnica de Canvas, se siguen los siguientes pasos:
* Se compara el valor de las variables que hacen referencia a objetos JavaScript con los valores de la columna symbol. 
* Al coincidir se verifica, según sea el caso, que los valores de la columna "value" o de la columna "arguments" se corresponden con los umbrales conocidos de un criterio que define la técnica analizada.
* Se emplean conjuntos como sets para almacenar resultados parciales en formato "URL_Sitio URL_Script".


```python
    if canvas_h in symbol: 
        if val != "null" and float(val) >= 16:
            veri_1.add(symbol + url)
            if (canvas_w + url) in veri_1:
                fp_1.add(top_url + ' ' + url)
    elif canvas_w in symbol:
        if val != "null" and float(val) >= 16:
            veri_1.add(symbol + url)
            if (canvas_h + url) in veri_1:
                fp_1.add(top_url + ' ' + url)
            
    if canvas_cf in symbol:
        veri_2.add(symbol + url + val)
        if (canvas_cs + url + val) in veri_2:
            fp_2.add(top_url + ' ' + url)
        elif (sum((canvas_cf + url) in s for s in veri_2)) > 1:
            fp_2.add(top_url + ' ' + url)
    elif canvas_cs in symbol:
        veri_2.add(symbol + url + val)
        if (canvas_cf + url + val) in veri_2:
            fp_2.add(top_url + ' ' + url)
        elif (sum((canvas_cs + url) in s for s in veri_2)) > 1:
            fp_2.add(top_url + ' ' + url)
    elif canvas_ff in symbol and (len(set(arg[arg.find('0":"')+4:arg.find(',"1"')-1])))>= 10:	
        fp_2.add(top_url + ' ' + url)
    elif canvas_fs in symbol and (len(set(arg[arg.find('0":"')+4:arg.find(',"1"')-1])))>= 10:	
        fp_2.add(top_url + ' ' + url)

    if canvas_save in symbol:
        fp_3.add(top_url + ' ' + url)
    elif canvas_rest in symbol:
        fp_3.add(top_url + ' ' + url)
    elif canvas_el in symbol:
        fp_3.add(top_url + ' ' + url)

    if canvas_data in symbol:
        fp_4.add(top_url + ' ' + url)
    elif canvas_img in symbol:
        if float(arg[arg.find('"2":')+4:arg.find(',"3"')]) >= 16:
            if float(arg[arg.find('"3":')+4:arg.find('}')]) >= 16:
                fp_4.add(top_url + ' ' + url)
```

Finalmente, se combinan los conjuntos de resultados parciales en uno que almacene los resultados finales. Para ello se emplean operaciones como unión, intersección, diferencia y diferencia simétrica. En el ejemplo que se presenta de la técnica de Canvas, interesa que el conjunto final almacene todos los sitios que cumplen con los criterios 1, 2 y 4 (intersección de fp_1, fp_2 y fp_4) y no cumplan con el criterio 3 (diferencia de fp_3):


```python
fp_sites = (fp_1 & fp_2 & fp_4) - fp_3
```

### 4. Representación de resultados. 

Se emplea un dataframe (pandas) para manejar y mostrar los resultados finales. Para ello se realizan dos cosas:
* Se separan los sets obtenidos en tuplas. Considérese los valores guardados y los caracteres de separación utilizados.
* Se construye el dataframe con las tuplas obtenidas.

Para el ejemplo desarrollado de Canvas, se realiza lo siguiente:


```python
c, d = zip(*(s.split(' ') for s in fp_sites))
df2 = pd.DataFrame({'URL Sitio Web': c, 'URL Script': d})
df2 = df2[['URL Sitio Web', 'URL Script']]
```

Con lo anterior, es posible mostrar el dataframe con los resultados. Se puede definir una función para escribir hipervínculos por cada URL, como se muestra en el caso desarrollado a continuación:


```python
def make_clickable(val):
    return '<a href="{}">{}</a>'.format(val,val)
#pd.set_option('max_colwidth', -1)
print('Los sitios web que aplican Canvas Fingerprinting según los criterios analizados son los siguientes:')
display(df2.style.format(make_clickable))
```

## Recomendaciones adicionales

* Puede reutilizar los widgets (elementos gráficos, botones, etc.) empleados en el notebook copiando las celdas. En el caso de los botones que ejecutan una acción, nótese que su función es ejecutar la celda de código siguiente. Ejemplo:


```python
def run_cell(ev):
    display(Javascript('IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+1, IPython.notebook.get_selected_index()+2)'))

button = widgets.Button(button_style='info',description="Ejecutar OpenWPM")
button.on_click(run_cell)
display(button)
```

* Para evitar errores, puede verificar que el fivhero de base de datos existe. Una manera de hacerlo se presenta a continuación:


```python
if os.path.isfile("crawl-data.sqlite"):
```

* Dependiendo del tamaño de la base de datos y de la consulta realizada, el tiempo que tarda un script de análisis desde la ejecución hasta la presentación de los resultados finales puede variar entre unos pocos segundos a varios minutos. Puede agregar un mensaje para indicar que se esta ejecutando la operación. Una manera de hacerlo se muestra a continuación:


```python
print("Procesando...")
clear_output(wait=True)
```

* Es recomendable verificar que los sets que contienen los resultados finales no estén vacíos. Por ejemplo, en el caso del análisis de Canvas:


```python
if len(fp_sites) == 0:
    print('Ninguno de los sitios evaluados aplica esta técnica de fingerprinting')
```

## Comentarios

* Para seleccionar el fichero CSV, se emplea una ventana de diálogo de Tkinter.
* Para mayor información sobre los widgets empleados, así como de los widgets en general, se recomienda consultar el siguiente enlace: https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html

<div style="text-align: right"> © 2018 Juan D. Márquez Lagalla </div>
