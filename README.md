# Gestor Alumnos

Este proyecto fue desarrollado para gestionar las listas de Alumnos en cursos de preparación para el examen PAA. Este examen es aplicado en varias universidades para seleccionar entre los aspirantes a carreras nivel licenciatura a aquellos que serán us nuevos estudiantes. Entre aquellas casas de estudios que aplican la PAA se encuentran la Universidad de Guadalajara (UDG).

A lo largo de los años, la necesidad de prepararse para este examen siempre ha estado presente para los ciudadanos de la Ciudad de Guadalajara, así como los habitantes del estado de Jalisco y varias partes más de la República Mexicana. Debido a esto, ha surgido un gran número de empresas que se dedican a ofrecer esta clase de cursos.

El presente proyecto fue el resultado de la necesidad de automatizar la gestión de los cursos que me fueron asignados durante mi tiempo laborando para una de esas empresas; la cantidad de grupos fácilmente llegaba a los 12, con 20 alumnos en promedio en cada uno. El programa necesitaba tener una serie de funciones simples para facilitar la gestión:

+ **Búsqueda**: Una forma de localizar a un alumno por nombre o apellido rápidamente, y obtener su información.
+ **Visualización**: Una forma cómoda de consultar los datos de cada aspirante, así como de un grupo entero.
+ **Administrar documento de aspirante**: Se le solicita a cada alumno un documento en formato PDF entregado por la UDG que los identificara como aspirantes.
+ **Archivado**: Una forma cómoda para archivar los datos de los alumnos para posibles consultas futuras o compartirlos con la empresa de ser necesario.
+ **Lectura de dictamen**: Una vez que el dictamen de admitidos fuera publicado (normalmente se distribuye en un PDF), revisar qué alumnos fueron admitidos, y cuantos no.

## Requerimientos
El proyecto se realizó en Python 3.8.10 y se ha trabajado en Linux Mint 20 (prueba en Windows pendiente). Algunos requerimientos son:

+ PyQt5==5.14.1
+ openpyxl==3.1.2
+ pdf2image==1.16.0
+ pytesseract==0.3.10
+ tabulate==0.8.9
+ Unidecode==1.1.1

Los requerimientos completos están en [requirements.txt](requirements.txt).

## Desglose

En primer instancia, los datos de los alumnos que se capturan son los siguientes:

+ *Nombre*: Nombre completo del alumno.
+ *Carrera*: A qué carrera desea ingresar el aspirante.
+ *Centro Universitario (CU)*: En cual de las sedes de la UDG se encuentra esa carrera.
+ *Curso*: Nombre del curso que eligió para la preparación.
+ *Plantel*: Nombre de la sede de la empresa que oferta el curso.
+ *Horario*: La hora de clase a la que asiste el alumno al curso.

Los tres primeros datos son los datos personales y de aspiración a UDG, los siguientes tres son los datos relativos a la empresa de preparación.

Como se puede observar, cada grupo dentro de la empresa de preparación se identifica por el nombre del curso, la sede de la misma --o plantel-- y el horario de clase.

### Iniciamos el gestor

Para comenzar el proyecto, es necesario crear una carpeta como la siguiente
> `preparacion_2030A/`

Es opcional que el nombre termine con el año y la letra que identifica el calendario al cual ingresarán los alumnos que serán admitidos. Este será nuestra Área de Trabajo.

> **Nota**: En la Universidad de Guadalajara se abren se abre proceso de admisión dos veces al año, para dos inicios diferentes: Calendario A, que inicia en Enero-Febrero, o calendario B, para iniciar en Agosto-Septiembre.
>
>Por ende, el proceso de admisión para calendario A inicia en Septiembre, y para calendario B en Febrero.

Una vez que se cree el proyecto, abrimos una terminal para el área de trabajo, y ejecutamos el archivo `main.py`del proyecto desde lo tengamos guardado. En Linux,

```bash
 cd path/to/preparacion_2030A/
 python path/to/project/Gestor_Alumnos/main.py
```

y el proyecto iniciará y desplegará la ventana principal. También notarás que se han creado dos directorios --visibles-- dentro del Área de Trabajo, llamados `BASE/` y `PDFs`. Estos directorios serán donde se guarde la base de datos y los documentos de los alumnos, respectivamente.

Una vez que ha iniciado el programa, ya podemos comenzar a ingresar los datos de los alumnos de nuestros cursos. Poco a poco iremos explorando las funcionalidades que nos ofrece este proyecto.

> **Nota**: Este es un proyecto hecho para mi propio uso, por lo que no me he preocupado por la comodidad al iniciarlo; por lo general uso un archivo `RUN.sh` con permisos de ejecución donde dentro del Área de trabajo para iniciarlo rápidamente.
>
> En futuras versiones quizás mejore el proyecto en ese aspecto.

## Guardando los datos

Para guardar los datos contamos con el botón llamado `Agregar nuevo`, que se encuentra casi en la esquina superior derecha. Al ingresar en el se desplegará una ventana secundaria donde tendremos un formulario para agregar al alumnos.

Como se puede observar, se pueden ingresar los seis datos del alumno anteriormente mencionados, adicionando el Número de Registro. Este último dato suele dejarse en blanco, ya que que los alumnos pueden contar o no contar al inicio del curso.

Una peculiaridad es que el proyecto irá dado sugerencias de carreras, centros universitarios, cursos, planteles y horarios, según los datos que ya hayas ingresado.

### Agregando alumnos por grupo en formato CSV

Una forma alternativa es agregar varios alumnos a la vez usando el formato CSV. Esta funcionalidad se puede ingresar desde el menú `Archivo>Agregar con CSV`. Se desplegará una ventana como la siguiente

En la parte superior se colocará la información del curso al que pertenecen, y en la parte inferior hay un espacio de texto donde se podrá escribir la lista de alumnos con los datos separados por coma, en el siguiente orden

```csv
 Nombre, Número de registro, carrera, CU
```

En este caso, también se puede omitir el número de registro.

> **Nota**: En sentido estricto, los únicos datos que pueden ser omitidos son *Número de registro*, *Carrera* y *Centro Universitario (CU)*. Omitir cualquier otro dará un error como resultado.

También es posible cargar un archivo CSV creado de forma externa usando el botón `Cargar CSV`. Los datos de ese archivo serán vaciados automáticamente en el cuadro correspondiente para que, al oprimir el botón `Agregar alumnos`, sean agregados a la base de datos.

Con los datos guardados, el programa funcionará correctamente, pero para que los datos persistan es necesario ir al menú `Archivo>Guardar`; la base de datos será guardada en un archivo binario en la carpeta `BASE/`. De cualquier forma, si existen cambios en la base de datos sin guardar, se desplegará una advertencia al intentar cerrar la ventana principal.

## Búsqueda y visualización

### Pestaña Buscar

En la ventana principal podremos encontrar un par de pestañas, en las cuales nos situaremos siempre en la llamada `Buscar` al iniciar. Esta pestaña tiene como propósito la búsqueda de alumnos de forma individual.

En la parte superior podemos encontrar un cuadro de búsqueda donde podemos buscar al alumnos por nombre y/o apellido. El mismo cuadro de búsqueda nos dará inmediatamente algunas coincidencias que podemos seleccionar con las flechas de navegación. La búsqueda se puede realizar oprimiendo enter.

Una vez hecho, se desplegará la información completa del alumno en el cuadro inferior; los datos que mencionamos anteriormente y uno más al final que nos dice si el alumno ha entregado su documento. A su vez tenemos en el lateral derecho algunos botones que nos permitirán hacer algunas acciones:

+ `Actualizar`: Actualiza la información mostrada en el cuadro.
+ `Editar`: Edita el dato seleccionado --también es posible hacerlo dado doble click en el dato.
+ `Abrir PDF`: Usa el programa preferido del sistema para abrir el documento del alumno ---si el documento no está disponible, el botón estará inactivo.
+ `Eliminar`: Elimina al alumno de la base de datos.

### Pestaña Listas

Al desplazarnos a la siguiente pestaña, encontramos un par de cuadros y un pequeño botón en la parte superior llamado `Cargar`. Al oprimirlo se desplegará un diagrama de árbol donde podremos navegar por los cursos de la empresa de preparación de la siguiente forma:

```
 Plantel
 	curso
		horario
```

Al dar doble click en un horario en concreto, se listará en el cuadro más grande la lista de nombres de los alumnos que pertenezcan a ese horario; a ese grupo. Los botones que aparecen nos permiten realizar las siguientes acciones

+ `Guardar Archivo`: Nos permite exportar a los alumnos de ese grupo en un archivo CSV o JSON.
+ `Eliminar`: Nos permite eliminar al alumno seleccionado de la base de datos.
+ `Agregar`: Nos permite agregar a un alumno nuevo directamente a ese grupo.

Al dar doble click en un alumno en concreto, nos llevará a la pestaña `buscar` donde se desplegará la información de ese alumno.

### Generar lista

Si vamos al menú `Archivo>Generar lista` encontraremos una forma de exportar los datos y escribirlos en un archivo TXT. Esta es una de las funciones más antiguas que ha tenido mi proyecto, y la he utilizado siempre como una forma cómoda de visualización.

El archivo creador dividirá a los alumnos por grupos, y listará todos los datos en una tabla, por ejemplo,

Esta es mi forma favorita de mirar las listas de mis alumnos, sin embargo, cuando debo compartir mis listas con compañeros profesores me encuentro con varios problemas. No todos han trabajado con archivo de texto plano y rara vez pueden visualizar un archivo TXT correctamente. Eso ya no es problema hoy en día.

## Administración de documento de aspirante

Cómo mencionamos anteriormente, a cada alumno de la Empresa de Preparación se le solicita un documento que lo identifica como aspirante a UDG. Este documento debe tener al menos los siguientes datos:

+ Nombre del aspirante
+ Carrera
+ Centro Universitario (CU)
+ Número de Registro

El número de registro es un código numérico de 7 caracteres único para cada aspirante a la UDG.

Por su parte, los documentos que se pueden recibir pueden ser los siguientes:

+ *Orden de pago UDG*: El proceso de admisión tiene costo.
+ *Cédula de Aspirante*: Una especie de credencial con foto.
+ *Cita para obtener Cédula* : Desde pandemia ya no se emite ya que el proceso actualmente es 100% por internet.

Todos estos documentos poseen la información requerida anteriormente listada, y son documentos que se otorgan en formato PDF a los alumnos en diferentes momentos del proceso de aspiración.

Estos documentos se deberán colocar en la carpeta `PDFs/` de nuestra Área de Trabajo; no importa el nombre del archivo, pero es estricto que sea un archivo PDF. Una vez colocados los archivos en esa carpeta se irá al menú `Cursos/Organizar PDFs`.

Una vez realizado esto, el proyecto realizará las siguientes tareas:

+ Vinculará el PDF al alumno en la base de datos mediante el nombre.
+ Renombrará al archivo usando el nombre del alumno correspondiente.
+ Moverá el archivo a una carpeta nombrada con los datos del curso en el formato: `<plantel>_<curso>_<horario>/`.

De esta forma, se podrá acceder al documento de cada alumno desde la pestaña `Buscar`.

### Extracción del Número de Registro

El Número de Registro es el último dato que obtenemos del alumno. Normalmente el primer contacto que tenemos con esa información es con el documento que recibimos del aspirante. Este proyecto es capaz de extraer este dato del documento y agregarlo a la base de datos.

Para realizar esto es necesario haber organizado antes los PDFs como se mencionó anteriormente, para después ir al menú `Cursos/Escanear PDFs`. Una vez hecho esto, el Número de Registro acompañará a los datos del alumno donde queramos visualizarlos.

> **Nota**: En ocasiones, el alumno no habrá conservado el archivo PDF de su documento. Dado esto, es posible que entregue una foto o imagen que posea del mismo. Para que el programa lo acepte es necesario convertir el archivo a PDF.
>
> A la hora de leer el archivo PDF hecho a partir de la imagen, el proyecto usará _tesseract_. Es un motor que usar IA para extraer texto de imagen. El proceso puede ser muy tardado cuando se realiza por primera vez.

## Archivado

Como ya se mencionó antes, la base de datos se guarda como un archivo binario en `BASE/`. Sin embargo, esta forma de persistencia no permite la lectura humana; no hay una razón de peso para guardar la base de datos así, simplemente fue una decisión que se tomó por gustos personales.

Por esta razón, se ha implementado formas de exportar los datos en varios tipos de archivos externos. Ya se ha mencionado el [guardado de listas en formato TXT](#generar-lista) como una forma de visualización, y también una forma de [exportar los alumnos de un grupo en CSV o JSON](#pestaña-listas). Pero hay un par más de recursos que se pueden usar.

### Exportar e Importar en JSON

En el menú `Archivo>JSON>...` encontramos las opciones de exportar e importar. Exportar genera un archivo JSON con el siguiente formato

```json
{
  "Alumnos": [
    {
      "Nombre": "Nombre del alumno",
      "Número de registro": "0000000",
      "Carrera": "Lic. en ......",
      "Centro Universitario": "Centro",
      "Curso": "Nombre de curso",
      "Plantel": "Nombre sede",
      "Horario": "00-00hrs",
      "¿Admitido?": "Sí|No"
	},
	{
      "Nombre": "Nombre del alumno",
      "Número de registro": "0000000",
      .
	  .
	  .
	},
	.
	.
	.

  ],
  "Total alumnos": <alumnos en total>,
  "Planteles": [lista de planteles],
  "Cursos": [lista de cursos],
  "Total grupos": <total de grupos>,
  "% de registro entregados": <porcentaje de documentos recibidos>
}
```
Este archivo esta pensado para compartir los datos de los alumnos entre profesores que usen también este programa, así como facilitar su uso en futuros proyectos que se realicen en el área de desarrollo de la empresa.

Para la importación solo es necesario que exista la clave `Alumnos` para que sea posible la lectura del JSON.

### Crear Excel

Como reciente desarrollo, también es posible crear un archivo XLSX. Este será creado en varios _sheets_, tantos como grupos se tengan en la base de datos, cada uno conteniendo un solo grupo. Para generar este archivo solo se necesita ir al menú `Archivo>Generar Excel`.

Esta implementación fue creada para agilizar la comunicación entre los compañeros profesores que comparten grupos. Se pensó para los que no usen este programa, ni sean desarrolladores, ya que el uso de una hoja de cálculo está más extendido que otras formas de gestión de datos.

## Lectura de Dictamen

El Dictamen de Admitidos a la UDG se publica en La Gaceta, que es el diario oficial de la universidad. El dictamen se suele publicar en formato PDF, como un gran listado que contiene los Números de Registro de cada estudiante admitido, acompañado por el resultado de la evaluación realizada. Esa es la razón principal de solicitar esa información a cada alumno.

Al descargar ese archivo es posible revisar de forma automática si nuestros alumnos han sido admitidos o no. Esto al ir al menú `Cursos>Confirmar Admisión` y seleccionar el archivo PDF que contiene el Dictamen. La información de admisión de cada alumno será agregada a los archivos que se exporten, ya sea las listas TXT, el archivo JSON y XLSX.

Esto marcaría la finalización de la gestión del curso.

## Palabras finales: Un poco sobre mí y el proyecto.

Aprovecharé esta sección para compartir mis impresiones personales sobre este proyecto. Hablaré mucho sobre mí, por lo que no es imprescindible leerla para entender el proyecto en sí, aunque sí le dará bastante contexto.

Soy Físico de formación, egresado de la Universidad de Guadalajara. Después de terminar el plan de estudios por ahí del 2016-2017, decidí tomar con calma lo que pasaría después; de seguro que mi asesor de tesis de entonces me habrá odiado por eso.

Fue entonces que a mediados de 2018 comencé a trabajar en esa Empresa de Preparación que menciono. No diré el nombre de la empresa aquí, pero de seguro lo sabrán si entran en mi LinkedIn. Mi objetivo era obtener experiencia en la docencia, ya que mi plan era seguir con el posgrado y dedicarme a la investigación, y dar clases es una de las actividades de un académico.

Sin embargo, me lo tomé con demasiada calma; llegó el 2020, y todo mundo sabe que pasó. Estaba bastante preparado para dejar mi trabajo como docente y continuar con los planes, pero todo quedó en pausa. Entre clases online y clases presenciales con cubrebocas, el trabajo estaba hasta cierto punto asegurado.

No obstante, si hubo una disminución de las horas-clase, lo que me dejó bastante tiempo libre. Pero gracias a ese respiro, logré redescubrir una de mis grandes pasiones: la programación.

Pues aquí estoy, 4 años después de ese fatídico 2020. En ese entonces decidí volver a programar, esta vez en Python, que tantas veces en años anteriores me recomendaron; sinceramente me arrepentí de no haberles hecho caso.

En fin, Gestor_Alumnos fue de los primeros proyectos que realicé para un uso práctico en mi día a día. ¿Saben que tedioso es buscar a los alumnos en listas físicas? Y muchas veces los alumnos no estaban ordenados de ninguna forma.

El proyecto actual no se parece a nada al que hice en ese entonces ---hace 3 años. Comenzó como un programa simple de terminal/interprete, con una base de datos diseñada a base de archivos TXT. Pero poco a poco fue tomando forma, agregando y modificando elementos según iba aprendiendo más sobre Python.

Gestor_Alumnos es mi bebé. Aquel primogénito que dejas caer varias veces por falta de experiencia. Si ven el código, podrán notar a lo que me refiero. Me disculpo por adelantando si están pensando en echarle un vistazo.

Hoy en día, después de varios cursos y un BootCamp en Data Science, puedo decir que estoy más preparado para el manejo de datos. Herramientas como Pandas y Numpy me han mostrado que mi Gestor_Alumnos es nada comparado con todo lo que puedo hacer en el futuro.

Mi ambición actual ya no es seguir el camino de un investigador en Física. Siento que a mi 32 años ese camino se ha cerrado por completo. Sin embargo, he encontrado el área perfecta para mí, aquella área que combina dos tópicos que siempre me apasionaron: las matemáticas y la programación.

Creo que todavía tengo camino por delante para ser un buen Data Scientist. Y definitivamente creo que compartir al mundo este proyecto, aquel que me hizo descubrir que los datos son lo mío, es uno paso importante. Gracias por leer.

## Contacto

Puedes visitarme en mis redes sociales públicas:

* [LinkedIn](https://www.linkedin.com/in/leodansantiago/)
* [X (anteriormente Twitter)](https://twitter.com/LeoDanSantiago)

# Apéndice A: Menús

A continuación se listan los menús que el proyecto cuenta, así como una breve explicación.

+ Archivo:
	+ Nuevo: Abre una nueva ventana para adminstrar otra Área de Trabajo.
	+ Abrir carpeta...: Si función aún.
	+ Recientes: Si función aún
	+ Guardar: Actualiza la base de datos guardada en el archivo binario contenido en `BASE/`
	+ Guardar en...: Sin función aún.
	+ Generar lista: Exporta listas en un archivo TXT. Ver [esta sección](#generar-lista).
	+ Generar Excel: Exporta listas en un archivo XLSX. Ver [esta sección](#crear-excel).
	+ JSON: Ofrece dos menús para exportar o importa un archivo JSON. Ver [esta sección](#exportar-e-importar-en-json).
	+ Agregar con CSV: Agrega alumnos por grupo en formato CSV.  Ver [esta sección](#agregando-alumnos-por-grupo-en-formato-csv).
+ Cursos:
	+ Organizar PDFs: Organiza y vincula los documentos PDF por grupo y alumno.  Ver [esta sección](#administración-de-documento-de-aspirante).
	+ Escanear PDFs: Permite extraer el Número de Registro del documento PDF de cada alumno.  Ver [esta sección](#extracción-del-número-de-registro).
	+ Editar directorios: Permite personalizar el nombre del archivo binario que contiene la base de datos, así como su carpeta contenedora, y el nombre del directorio que contienen los PDFs.
	+ Confirmar admisión: Permite confirmar en el Dictamen (un archivo PDF) que alumnos lograron ser admitidos.  Ver [esta sección](#lectura-de-dictamen).

# Apéndice B: Directorios y archivos.

A continuación se listan los directorios y archivos generados por el proyecto, con una breve explicación.

+ Directorios:
	+ `BASE/`: Nombre por defecto del directorio donde se aloja la base de datos. Puede ser editada en el menú `Cursos>Editar directorios`.
	+ `PDFs/`: Nombre por defecto del directorio donde se alojan y organizan los documentos PDFs. Puede ser editada en el menú `Cursos>Editar directorios`.
	+ `.Imagenes_temp/`: Directorio oculto donde se alojan archivos de imagen temporales correspondientes a los documentos que estén en ese formato.
	+ `.CACHE/`: Directorio oculto que contiene historiales de los cambios realizados.
		+ `Historial_versiones/`: Aquí se guardan hasta 50 versiones antiguas de la base de datos en formato JSON.

+ Archivos:
	+ `.rutas.json`: Aquí se guardan las rutas de la base de datos, y el directorio que contiene los documentos PDF.
	+ `.historial.json`: Aquí se guardan las rutas donde se exporta o importa los archivos TXT, JSON y XLSX.
	+ `.hashes_pdf`: Binario que contiene la información extraída de cada documento PDF, y su respectivo hash.
	+ `.CACHE/historial_cambios.txt`: Registro a lo largo del tiempo de las modificaciones realizadas en la base de datos.