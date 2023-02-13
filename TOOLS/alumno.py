# Clases para alumno

from TOOLS.tools import *
import json, csv
from tabulate import tabulate as tabla
import TOOLS.busqueda as bq
from shutil import rmtree
from datetime import datetime


#*-------------------------------------------------------------------------------------------*
#*------ Clases -----------------------------------------------------------------------------*
#*-------------------------------------------------------------------------------------------*


class TodosMisAlumnos:

	def __init__(self,lista_,ruta_pdf, ruta_base_datos):

		''' Clase que contiene las listas de todos los alumnos '''

		self.lista = lista_
		self.ruta_pdf = ruta_pdf
		self.ruta_base_datos = ruta_base_datos
		self.ruta_h = os.path.join(os.path.dirname(self.ruta_base_datos), ".CACHE")
		self.ruta_historial = f'historial_cambios.txt'
#		self.base_status = f'base_estatus.json'
#		self.lineasF_status = f'lineas_estatus.json'
		self.Arch_dir_historial()
		self.Data = dict()
		self.estructuraArbol = dict()
		self.CambiosSinGuardar = dict()
		self.ClavesBusqueda = []

		self.Control_version()
		self.EntregarPDF()
		self.UsedData()



	#---------------------------------------------------------------------------------------------

	def Arch_dir_historial(self):

		''' Construye las rutas de archivos de historial '''

		self.ruta_historial = os.path.join(self.ruta_h, self.ruta_historial)
#		self.base_status = os.path.join(self.ruta_h, self.base_status)
#		self.lineasF_status = os.path.join(self.ruta_h, self.lineasF_status)

	#---------------------------------------------------------------------------------------------

	def Control_version(self):

		''' Guarda hasta 50 versiones pasadas en formato JSON '''

		versiones_ruta = os.path.join(self.ruta_h, "Historial_versiones")
		maxi = 50

		os.makedirs(versiones_ruta, exist_ok = True)

		versiones = os.listdir(versiones_ruta)

		date = datetime.today().strftime('%Y-%m-%d %H_%M_%S')
		add_version = os.path.join(versiones_ruta, f'{date}.json')

		if versiones == []:
			self.Todos2JSON(add_version)
			return

		versiones.sort()
		ruta_ulti = os.path.join(versiones_ruta, versiones[-1])
		ulti = self.ImportJSON(ruta_ulti, False)

		nueva = self.Todos2JSON("", False)

		if nueva == ulti:
			return

		self.Todos2JSON(add_version)
		versiones.append("")

		if len(versiones) > maxi:
			n = len(versiones)
			delta = n - maxi
		else:
			return

		for i in versiones:
			if versiones.index(i) == delta:
				break
			os.remove(os.path.join(versiones, i))

	#--------------------------------------------------------------------------------------------

	def EntregarPDF(self):

		''' Revisa la base de PDFs para verificar si cada alumno entregó o no su archivo PDF '''

		try:
			cursos = os.listdir(self.ruta_pdf)
		except FileNotFoundError:
			os.mkdir(self.ruta_pdf)
			cursos = os.listdir(self.ruta_pdf)

		entregado = dict()

		for curso in cursos:

			try:
				PDFs = os.listdir( os.path.join(self.ruta_pdf, curso))
			except NotADirectoryError:
				continue

			#datos_curso = curso.split("_")

			for PDF in PDFs:

				rutaPDF = os.path.join(self.ruta_pdf, curso, PDF)
				PDF = quitaracentos(PDF)

				if "pdf" not in PDF.split("."):
					continue

				entregado[PDF.replace(".pdf","")] = rutaPDF

		for alumno in self.lista:
			alumno.ReiniciarPDFs()

		for alumno in self.lista:
			nombre = alumno.comparar_nombre

			if nombre in entregado:
				alumno.NR_entregado = "Sí"
				alumno.RutaPDF = entregado[nombre]
			else:
				alumno.NR_entregado = "*No*"

	#---------------------------------------------------------------------------------------------

	def UsedData(self):

		''' Mantiene un control de los datos en común para cada alumno '''

		self.Data["Plantel"] = []
		self.Data["Curso"] = []
		self.Data["Horario"] = []

		self.Data["Carrera"] = []
		self.Data["Centro Universitario"] = []

		for alumno in self.lista:
			if alumno.plantel not in self.Data["Plantel"]:
				self.Data["Plantel"].append(alumno.plantel)
			if alumno.curso not in self.Data["Curso"]:
				self.Data["Curso"].append(alumno.curso)
			if alumno.horario not in self.Data["Horario"]:
				self.Data["Horario"].append(alumno.horario)

			if alumno.carrera not in self.Data["Carrera"]:
				self.Data["Carrera"].append(alumno.carrera)
			if alumno.CU not in self.Data["Centro Universitario"]:
				self.Data["Centro Universitario"].append(alumno.CU)

			claves = procesar(alumno.nombre).lower().split(" ")
			for clave in claves:
				if clave not in self.ClavesBusqueda:
					self.ClavesBusqueda.append(clave)

		for i in self.Data:
			self.Data[i].sort()


	#---------------------------------------------------------------------------------------------

	def Cambios_realizados(self,cadena):

		''' Hace un seguimiento de los cambios sin guardar realizados a la base de datos '''

		fecha = datetime.today().strftime('%Y-%m-%d %H:%M:')

		try:
			self.CambiosSinGuardar[fecha].append(cadena)
		except KeyError:
			self.CambiosSinGuardar[fecha] = [cadena]
		except TypeError:
			self.CambiosSinGuardar = {fecha: [cadena]}


	def Eventos_control(self,cadena):

		''' Hace seguimiento de eventos relevantes para la gestion '''

		Agregar2TXT(self.ruta_historial, [cadena])


	#---------------------------------------------------------------------------------------------

	def add_cHistorial(self):

		''' Al importar los cambios a la base de datos, guarda los cambios en el archivo historial y
			vacía el seguimiento de cambios sin guardar '''

#		if self.CambiosSinGuardar != []:
#			Agregar2TXT(self.ruta_historial, self.CambiosSinGuardar)
#			self.CambiosSinGuardar = []

		if len(self.CambiosSinGuardar) == 0:
			return

		lista = []

		for i in self.CambiosSinGuardar:
			if i not in lista:
				lista.append(i)
			lista += self.CambiosSinGuardar[i]

		Agregar2TXT(self.ruta_historial, lista)
		self.CambiosSinGuardar = dict()

		# Aquí

	#--------------------------------------------------------------------------------------------

	def AddAlumno(self,lista):

		''' Agrega alumno a la lista de alumnos '''

#		n, nr, c, cu, curso, plantel, horario

#		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')

		cambio = f'\tSe agregó el alumno {lista[0]}:\n\t\tNúmero de registro: {lista[1]}, Carrera: {lista[2]}, Centro universitario: {lista[3]}, Curso: {lista[4]}, Plantel: {lista[5]}, Horario: {lista[6]}'

		self.lista.append(Alumno(*lista))
		self.Cambios_realizados(cambio)
		self.UsedData()

	#-------------------------------------------------------------------------------------------------

	def RmAlumno(self,indice):

		''' Eliminar alumno '''

		self.lista[indice].DiccAlumno()
		d = self.lista[indice].datos

#		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
		cambio= f'\tSe eliminó al alumno {d["Nombre"]}:\n\t\t'
		for i in d:
			if i == "Nombre" or i == "¿PDF entregado?":
				continue

			aux = f'{i}: {d[i]}, '
			cambio = cambio + aux

		self.lista.pop(indice)
		self.Cambios_realizados(cambio)
		self.UsedData()

	#--------------------------------------------------------------------------------------------

	def organizarPDF(self, Consola = True ):

		''' Manipula la base (directorio) que contiene los PDFs y los organiza en directorios por salón.
			El PDF debe renombrarse usado el nombre del alumno '''

		try:
			PDFs = os.listdir(self.ruta_pdf)
		except FileNotFoundError:
			os.mkdir(self.ruta_pdf)
			PDFs = os.listdir(self.ruta_pdf)

		control = [datetime.today().strftime('%Y-%m-%d %H:%M'), "\tArchivos desplazados:"]

		for PDF in PDFs:
			ruta1 = os.path.join(self.ruta_pdf, PDF)

			if os.path.isdir(ruta1):
				continue

			nombre = quitaracentos(PDF.replace(".pdf",""))

			for alumno in self.lista:
				nombre2 = alumno.comparar_nombre

				if nombre != nombre2:
					continue

				nueva_ruta = f'{alumno.plantel}_{alumno.curso}_{alumno.horario}'

				if Consola:
					print("\nArchivos desplazados:")
					print(f'{PDF} --> {nueva_ruta}/\n')
				else:
					mensaje = f'\t\t{PDF} --> {nueva_ruta}/'
					control.append(mensaje)


				try:
					os.rename(ruta1, os.path.join(self.ruta_pdf, nueva_ruta, PDF))
				except FileNotFoundError:
					os.mkdir( os.path.join(self.ruta_pdf, nueva_ruta) )
					os.rename(ruta1, os.path.join(self.ruta_pdf, nueva_ruta, PDF) )
				except FileExistsError:
					print("No sé que pasa")

		if len(control) > 2:
			mensaje = "\n".join(control)
			self.Eventos_control(mensaje)

		self.EntregarPDF()

	#--------------------------------------------------------------------------------------------

	def EscanearPDFs(self):

		Error = dict()

		for alumno in self.lista:
			alumno.ConfirmarPDF()
			if hasattr(alumno, "CoinPorcent"):
				if alumno.CoinPorcent < 50.0:
					Error[alumno.nombre] = (alumno.RutaPDF, "Archivo PDF")
				elif alumno.CoinPorcent == 101:
					print(f'El archivo {alumno.RutaPDF} no se puede leer')
				elif alumno.CoinNum == 0.0:
					Error[alumno.nombre] = (alumno.RutaPDF, "Número de registro")

		self.ErrorPDFs = Error

	#--------------------------------------------------------------------------------------------

	def GenerarListas(self, archivo = "Listas completas.txt"):
		#print("Has invocado al héroe japonés")

		''' Genera listas tabuladas de los alumnos divididos por salones '''

		Salones = dict()

		for alumno in self.lista:

			Salon_actual = f'\n\n* Lista del plantel {alumno.plantel}, curso {alumno.curso} del horario {alumno.horario} *\n\n'

			if Salon_actual not in Salones:
				Salones[Salon_actual] = []

			datos_alumno = [alumno.nombre,alumno.nRegistro,alumno.carrera,alumno.CU,alumno.NR_entregado, alumno.admitido]

			Salones[Salon_actual].append(datos_alumno)

		titulos = ["Nombre","Num. de registro", "Carrera", "Centro", "PDF enviado", "¿Admitido?"]

		with open(archivo, "w") as salida:

			for salon in Salones:
				print(salon, file=salida)

				check_dictamen = ChecarDictamen(Salones[salon])

				if not check_dictamen and titulos[-1] == "¿Admitido?":
					titulos.pop(-1)
				elif titulos[-1] != "¿Admitido?":
					titulos.append("¿Admitido?")

				print(tabla(Salones[salon], headers=titulos), file=salida)


			print("\n", file=salida)


	#--------------------------------------------------------------------------------------------

	def MotorEditar_GUI(self,indice,dato,nuevo):

		''' Motor para edición de datos de alumnos para GUI'''

		self.lista[indice].DiccAlumno()
		viejo = self.lista[indice].datos[dato]
#		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')

		cambio = f'\tCambio en {self.lista[indice].nombre} del plantel {self.lista[indice].plantel}, curso {self.lista[indice].curso}, horario {self.lista[indice].horario}:\n\t\t Cambió {dato}: {viejo} --> {nuevo}'

		self.lista[indice].CambiarDato(dato,nuevo)
		self.Cambios_realizados(cambio)
		self.UsedData()


	#--------------------------------------------------------------------------------------------

	def Buscar_(self,cadena):
		indice = bq.buscar_GUI(procesar(cadena),self.lista)

		return indice

	#--------------------------------------------------------------------------------------------

	def GenerarArbol(self):

		indice = 0
		self.estructuraArbol = dict()

		for i in self.lista:
			plantel, curso, horario = i.getDatosSalon()

			if plantel not in self.estructuraArbol:
				self.estructuraArbol[plantel] = dict()

			if curso not in self.estructuraArbol[plantel]:
				self.estructuraArbol[plantel][curso] = dict()

			if horario not in self.estructuraArbol[plantel][curso]:
				self.estructuraArbol[plantel][curso][horario] = []

			self.estructuraArbol[plantel][curso][horario].append(f'{i.nombre}&{indice}')
			indice += 1

	def getArbol(self):
		self.GenerarArbol()

		return self.estructuraArbol



	#--------------------------------------------------------------------------------------------

	def AbrirPDF_GUI(self,indice):

		''' Abrir el documento PDF desde el GUI '''

		ruta = self.lista[indice].RutaPDF

		if ruta == "Sin ruta":
			return
		Abrete(ruta)

	#------------------JSON Exportar -------------------------------------------------------------

	def Todos2JSON(self, archivo = "alumnos.json", salida_file = True):

		''' Exporta los datos de los alumnos en listas a un archivo JSON '''

		todos = dict()
		todos["Alumnos"] = []
		todos["Total alumnos"] = 0
		total = 0
		todos["Planteles"] = []
		todos["Cursos"] = []
		grupos = []
		total_nr = 0

		for i in self.lista:
			i.Alumno2JSON()
			todos["Alumnos"].append(i.datos)
			total += 1

			if i.datos["Plantel"] not in todos["Planteles"]:
				todos["Planteles"].append(i.datos["Plantel"])
			if i.datos["Curso"] not in todos["Cursos"]:
				todos["Cursos"].append(i.datos["Curso"])
			if i.datos["Número de registro"] not in ["n/a", "No data"]:
				total_nr += 1

			grupo = i.datos["Plantel"] + i.datos["Curso"] + i.datos["Horario"]

			if grupo not in grupos:
				grupos.append(grupo)

		todos["Total alumnos"] = total
		todos["Total grupos"] = len(grupos)
		try:
			todos["% de registro entregados"] = 100*total_nr/total
		except ZeroDivisionError:
			todos["% de registro entregados"] = "No data"


		cadena = json.dumps(todos,ensure_ascii=False)

		cadena = PrepararJSON(cadena)

		if salida_file:
			with open(archivo, "w") as salida:
				print(cadena, file=salida)
		else:
			return todos

	#-------- Importar JSON -----------------------------------------------------------------

	def ImportJSON(self, archivo = "alumnos.json", importar = True):

		''' Importa los datos de los alumnos contenidos en un JSON a las listas. Se debe actualizar
			la base de datos principal posteriormente '''

		with open(archivo, "r") as entrada:
			lineas = entrada.readlines()
			lineas = "".join(lineas)
			lineas = lineas.replace("\t","")
			lineas = lineas.replace("\n","")

		datos = json.loads(lineas)

		if len(datos) == 0:
			return

		if importar:
			pass
		else:
			return datos

		for alumno in datos["Alumnos"]:
			n, nr, c = alumno["Nombre"],alumno["Número de registro"],alumno["Carrera"]
			cu = alumno["Centro Universitario"]
			curso,plantel,horario = alumno["Curso"],alumno["Plantel"],alumno["Horario"]

#			self.lista.append(Alumno(n,nr,c,cu,curso,plantel,horario))

			self.addAlumno([n, nr, c, cu, curso, plantel, horario])


#		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
#		cambio = f'{fecha}:\n\tEl archivo {archivo} fue cargado. Mire el contenido para más información'
#		self.Cambios_realizados(cambio)
#		self.UsedData()

	#------------- Importar CSV ---------------------------------------------------------------


	def ImportarCSV(self, archivo, datos_curso):

		''' Importar datos desde un archivo CSV '''

		with open(archivo, newline="") as entrada:
			lector = csv.reader(entrada)

			for row in lector:
				if row == [] or row == [""]:
					continue

				newRow = row + datos_curso
#				self.lista.append(Alumno(*newRow))
				self.AddAlumno(newRow)

#		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
#		cambio = f'{fecha}:\n\tEl archivo {archivo} fue cargado. Mire el contenido para más información'
#		self.Cambios_realizados(cambio)
#		self.UsedData()

	#------------- Exportar CSV ---------------------------------------------------------------

	def ExportarCSV(self, ruta_archivo, *indices):

		''' Crea un archivo CSV con los alumnos seleccionados '''

		with open(ruta_archivo, "w", newline="") as salida:
			writer = csv.writer(salida)

			for i in indices:
				alumno = self.lista[i].getDatosCSV()
				writer.writerow(alumno)

	#----------- Exportar algunos alumnosa JSON ------------------------------------------------

	def ExportarAulaJSON(self, ruta_archivo, *indices):

		''' Crea un archivo CSV con los alumnos seleccionados '''

		salida = {"Alumnos" : []}

		for i in indices:
			self.lista[i].Alumno2JSON()
			salida["Alumnos"].append(self.lista[i].datos.copy())

		salida = json.dumps(salida,ensure_ascii=False)
		salida = PrepararJSON(salida)

		with open(ruta_archivo, "w") as archivo:
			print(salida, end="", file=archivo)


	#-------- Leer dictamen para conocer admitidos -----------------------------------------

	def LeerDictamen(self, archivo):

		''' Lee el dictamen de admitidos UDG en formato PDF para verificar admitidos '''

		cadena = PDF2Cadena(archivo)

		print(f'Mensaje de la clase "{type(self).__name__}": El archivo dictamen tiene una longitud de {len(cadena)}')

		self.num_Admitidos = 0

		for alumno in self.lista:
			alumno.ConfirmarAdmision(cadena)

			if alumno.admitido == "*Sí*":
				self.num_Admitidos += 1



#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

class Alumno:

	def __init__(self, nombre, numRegistro, carrera, CU, curso, plantel, horario):

		''' Clase alumnos. Contiene la información de un alumnos '''

		# nombre: Nombre del alumno
		# numRegristro: Proporcionado al hacer tramites UDG
		# carrera: Carrera a aspirar
		# CU: Centro universitario de la red
		# Curso: Nombre del curso en Lumiere
		# plantel: Plantel de Lumiere donde asiste el alumno
		# horario: Horario en el que el alumno asiste

		self.nombre = QuitarMEspacios(nombre)
		self.nRegistro = numRegistro
		self.carrera = QuitarMEspacios(carrera)
		self.CU = CU
		self.curso = curso
		self.plantel = plantel
		self.horario = horario
		self.NR_entregado = "No data"
		self.comparar_nombre = self.nombre
		self.bandera = ""
		self.GenerarComparar()
		self.RutaPDF = "Sin ruta"
		self.admitido = "No data"


		self.ValoresVacios()
		self.DiccAlumno()

	#--------------------------------------------------------------------------------------------

	def ValoresVacios(self):

		aux = [self.nRegistro, self.carrera, self.CU]

		while "" in aux:
			indice = aux.index("")
			if indice == 0:
				self.nRegistro = "n/a"
			elif indice == 1:
				self.carrera = "n/a"
			else:
				self.CU = "n/a"

			aux = [self.nRegistro, self.carrera, self.CU]


	#--------------------------------------------------------------------------------------------

	def ReiniciarPDFs(self):
		self.NR_entregado = "No data"
		self.RutaPDF = "Sin ruta"

	#--------------------------------------------------------------------------------------------

	def GenerarComparar(self):
		self.comparar_nombre = quitaracentos(self.nombre)

	#--------------------------------------------------------------------------------------------

	def CambiarDato(self,dato,nuevo):

		''' Cambiar determinado dato por el alumnos. Si el dato no es un atributo, retornará 0,
			caso contrario, 1 '''

		if dato == "Número de registro":
			self.nRegistro = nuevo
		elif dato == "Carrera":
			self.carrera = nuevo
		elif dato == "Centro Universitario":
			self.CU = nuevo
		elif dato == "Nombre":
			self.nombre = nuevo
			self.GenerarComparar()
		elif dato == "Curso":
			self.curso = nuevo
		elif dato == "Plantel":
			self.plantel = nuevo
		elif dato == "Horario":
			self.horario = nuevo
		else:
			return 0

		self.DiccAlumno()

		return 1
	#--------------------------------------------------------------------------------------------

	def ConfirmarPDF(self):
		if self.RutaPDF == "Sin ruta":
			return

		cadena = PDF2Cadena(self.RutaPDF)

		if cadena == "":
			self.CoinPorcent = 101
		else:
			self.CoinPorcent = BuscarEnCadena(self.comparar_nombre, cadena)

		if self.nRegistro != "n/a":
			self.CoinNum = BuscarEnCadena(self.nRegistro, cadena)
		else:
			self.CoinNum = -1

	#--------------------------------------------------------------------------------------------

	def ConfirmarAdmision(self, dictamen):
		if self.nRegistro == "n/a":
			return

		porc_coicidencia = BuscarEnCadena(self.nRegistro, dictamen)

		if porc_coicidencia == 100:
			self.admitido = "*Sí*"
		else:
			self.admitido = " No"
	#--------------------------------------------------------------------------------------------

	def getDatosSalon(self):
		salida = ([
			self.plantel,
			self.curso,
			self.horario
			])

		return salida

	#--------------------------------------------------------------------------------------------

	def getDatosCSV(self):
		salida = ([
			self.nombre,
			self.nRegistro,
			self.carrera,
			self.CU
		])

		return salida

	#--------------------------------------------------------------------------------------------

	def DiccAlumno(self):

		''' Genera diccionario que contiene la información del alumno '''

		self.datos = ({ "Nombre" : self.nombre, "Número de registro" : self.nRegistro,
						"Carrera" : self.carrera, "Centro Universitario" : self.CU,
						"Curso" : self.curso, "Plantel" : self.plantel, "Horario" : self.horario,
						"¿PDF entregado?" : self.NR_entregado, "¿Admitido?" : self.admitido})

		if self.admitido == "No data":
			self.datos.pop("¿Admitido?")

	#-------------------------------------------------------------------------------------------

	def Alumno2JSON(self):

		''' Genera diccionario con los datos del alumno como preparación para exportar a JSON '''

		self.datos = ({	"Nombre" : self.nombre, "Número de registro" : self.nRegistro,
						"Carrera" : self.carrera, "Centro Universitario" : self.CU,
						"Curso" : self.curso, "Plantel" : self.plantel, "Horario" : self.horario,
						"¿Admitido?" : self.admitido})
