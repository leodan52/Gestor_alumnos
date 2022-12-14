# Clases para alumno

from TOOLS.tools import *
import json
from tabulate import tabulate as tabla
import TOOLS.busqueda as bq
from shutil import rmtree
from datetime import datetime


#*-------------------------------------------------------------------------------------------*
#*------ Clases -----------------------------------------------------------------------------*
#*-------------------------------------------------------------------------------------------*


class TodosMisAlumnos:

	def __init__(self,lista_,ruta_pdf,ruta_base_datos):

		''' Clase que contiene las listas de todos los alumnos '''

		self.lista = lista_
		self.ruta_pdf = ruta_pdf
		self.ruta_base_datos = ruta_base_datos
		self.ruta_h = f'.CACHE'
		self.ruta_ = os.path.dirname(self.ruta_base_datos)
		#self.ruta_historial = f'{os.path.dirname(self.ruta_base_datos)}/.CACHE/historial_cambios.txt'
		self.Arch_dir_historial()

		self.Control_version()
		self.EntregarPDF()
		self.UsedData()
		self.Cambios_base()

		self.CambiosSinGuardar = []

	#---------------------------------------------------------------------------------------------

	def Arch_dir_historial(self):
		self.ruta_historial = f'historial_cambios.txt'
		self.base_status = f'base_estatus.json'
		self.lineasF_status = f'lineas_estatus.json'
		aux = "/"

		if self.ruta_ == "":
			aux = ""

		self.ruta_ = f'{self.ruta_}{aux}'
		self.ruta_historial = f'{self.ruta_}{self.ruta_h}/{self.ruta_historial}'
		self.base_status = f'{self.ruta_}{self.ruta_h}/{self.base_status}'
		self.lineasF_status = f'{self.ruta_}{self.ruta_h}/{self.lineasF_status}'

	#---------------------------------------------------------------------------------------------

	def Control_version(self):
		versiones_ruta = f'{self.ruta_}{self.ruta_h}/Historial_versiones'
		maxi = 50

#		if os.path.dirname(self.ruta_base_datos) == "":
#			versiones_ruta = f'.CACHE/Historial_versiones'
#			self.ruta_historial = f'.CACHE/historial_cambios.txt'

		os.makedirs(versiones_ruta,exist_ok = True)

		versiones = os.listdir(versiones_ruta)

		date = datetime.today().strftime('%Y-%m-%d %H_%M_%S')
		add_version = f'{versiones_ruta}/{date}.json'

		if versiones == []:
			self.Todos2JSON(add_version)
			return

		versiones.sort()
		ruta_ulti = f'{versiones_ruta}/{versiones[-1]}'
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
			os.remove(f'{versiones_ruta}/{i}')

	#---------------------------------------------------------------------------------------------

	def Cambios_base(self, cargar = False):

		arbol = dict()

		self.Grupos_ruta = dict()

		for ruta,direc,arch in os.walk(self.ruta_base_datos):
			arbol[ruta] = {"directorios":direc, "archivos":arch}
			if len(arch) != 0:
				self.Grupos_ruta[ruta] = arch.copy()

		Cambios_lineas = self.Cambios2Files(cargar)
		para_w = PrepararJSON(arbol, cadena_not = True)

		try:
			entrada = open(self.base_status, "r")
			antiguo = entrada.readlines()
			entrada.close()

			antiguo = Entrada4JSON(antiguo)
		except FileNotFoundError:
			cargar = True

		salida = open(self.base_status, "w")
		print(para_w, file=salida)
		salida.close()
		if cargar:
			return

		Cambios = []

		for ruta in antiguo:
			for objeto in antiguo[ruta]:
				try:
					eli, agr = comparar_C(antiguo[ruta][objeto], arbol[ruta][objeto])
				except KeyError:
					continue
				if len(eli) == 0 and len(agr) == 0:
					continue
				Cambios.append({"ruta":ruta, "Obj":objeto, "rm":eli.copy(), "add":agr.copy()})

		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
		Cam_ = [f'{fecha}:']
		for i in Cambios:
			Cam_.append(f'\tEn la ruta {i["ruta"]}/, en cuanto a {i["Obj"]}:')

			if len(i["add"]) != 0:
				Cam_.append(f'\t\tSe agreg??:')

				for j in i["add"]:
					Cam_.append(f'\t\t\t{j}')

			if len(i["rm"]) != 0:
				Cam_.append(f'\t\tSe elimin??:')

				for j in i["rm"]:
					Cam_.append(f'\t\t\t{j}')

		Cam_ = Cam_ + Cambios_lineas

		if len(Cam_) != 1:
			Agregar2TXT(self.ruta_historial, Cam_)

	#---------------------------------------------------------------------------------------------

	def Cambios2Files(self,cargar = False):

		Lineas = dict()

		for ruta in self.Grupos_ruta:
			for grupo in self.Grupos_ruta[ruta]:
				Lineas[f'{ruta}/{grupo}'] = Extraer2TXT(f'{ruta}/{grupo}')

		para_w = PrepararJSON(Lineas, cadena_not = True)

		try:
			Lineas_old = Extraer2TXT(self.lineasF_status)
			Lineas_old = Entrada4JSON(Lineas_old)
		except FileNotFoundError:
			cargar = True

		salida = open(self.lineasF_status, "w")
		print(para_w, file=salida)
		salida.close()

		if cargar:
			return []

		inter_rutas = Inter_C(Lineas.keys(), Lineas_old.keys())

		salida = []

		for r in inter_rutas:
			eli, agr = comparar_C(Lineas_old[r], Lineas[r])
			if len(eli + agr) == 0:
				continue

			salida.append(f'\tSe realizaron cambios en el archivo {r}:')

			if len(eli) != 0:
				salida.append(f'\t\tSe eliminaron las lineas:')
				for i in eli:
					salida.append(f'\t\t\tLinea {Lineas_old[r].index(i) + 1}: {i}')

			if len(agr) != 0:
				salida.append(f'\t\tSe agregaron las lineas:')
				for i in agr:
					salida.append(f'\t\t\tComo linea {Lineas[r].index(i) + 1}: {i}')

		return salida
	#---------------------------------------------------------------------------------------------

	def UsedData(self):

		if hasattr(self, "Data"):
			pass
		else:
			self.Data = dict()

			self.Data["Plantel"] = []
			self.Data["Curso"] = []
			self.Data["Horario"] = []

			self.Data["Carrera"] = []
			self.Data["Centro Universitario"] = []

		self.ClavesBusqueda = []

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

		try:
			self.CambiosSinGuardar.append(cadena)
		except AttributeError:
			self.CambiosSinGuardar = []
			self.CambiosSinGuardar.append(cadena)

	def Eventos_control(self,cadena):

		''' Hace seguimiento de eventos relevantes para la gestion '''
		Agregar2TXT(self.ruta_historial, [cadena])


	#---------------------------------------------------------------------------------------------

	def add_cHistorial(self):

		''' Al importar los cambios a la base de datos, guarda los cambios en el archivo historial y
			vac??a el seguimiento de cambios sin guardar '''
		if self.CambiosSinGuardar != []:
			Agregar2TXT(self.ruta_historial, self.CambiosSinGuardar)
			self.CambiosSinGuardar = []

	#---------------------------------------------------------------------------------------------

#	def NombreListas(self, nombre):

#		''' M??todo para cambiar la ruta de las bases de datos '''

#		self.ruta_base_datos = nombre

	#--------------------------------------------------------------------------------------------

	def AddAlumno(self,lista):

		''' Agrega alumno a la lista de alumnos '''

#		n, nr, c, cu, curso, plantel, horario

		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')

		cambio = f'{fecha}:\n\tSe agreg?? el alumno {lista[0]}:\n\t\tN??mero de registro: {lista[1]}, Carrera: {lista[2]}, Centro universitario: {lista[3]}, Curso: {lista[4]}, Plantel: {lista[5]}, Horario: {lista[6]}'

		self.lista.append(Alumno(*lista))
		self.Cambios_realizados(cambio)
		self.UsedData()

	#-------------------------------------------------------------------------------------------------

	def RmAlumno(self,indice):

		self.lista[indice].DiccAlumno()
		d = self.lista[indice].datos

		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
		cambio= f'{fecha}:\n\tSe elimin?? al alumno {d["Nombre"]}:\n\t\t'
		for i in d:
			if i == "Nombre" or i == "??PDF entregado?":
				continue

			aux = f'{i}: {d[i]}, '
			cambio = cambio + aux

		self.lista.pop(indice)
		self.Cambios_realizados(cambio)
		self.UsedData()

	#--------------------------------------------------------------------------------------------

	def organizarPDF(self, Consola = True ):

		''' Manipula la base (directorio) que contiene los PDFs y los organiza en directorios por sal??n.
			El PDF debe renombrarse usado el nombre del alumno '''

		try:
			PDFs = os.listdir(self.ruta_pdf)
		except FileNotFoundError:
			os.mkdir(self.ruta_pdf)
			PDFs = os.listdir(self.ruta_pdf)

		for PDF in PDFs:
			ruta1 = self.ruta_pdf + "/" + PDF

			try:
				os.listdir(ruta1)
				continue
			except NotADirectoryError:
				pass

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
					fecha = datetime.today().strftime('%Y-%m-%d %H:%M')
					mensaje = f'{fecha}:\n\tArchivos desplazados:\n\t\t{PDF} --> {nueva_ruta}/'
					self.Eventos_control(mensaje)

				try:
					os.rename(ruta1, f'{self.ruta_pdf}/{nueva_ruta}/{PDF}')
				except FileNotFoundError:
					os.mkdir(f'{self.ruta_pdf}/{nueva_ruta}')
					os.rename(ruta1, f'{self.ruta_pdf}/{nueva_ruta}/{PDF}')
				except FileExistsError:
					print("No s?? que pasa")


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
					Error[alumno.nombre] = (alumno.RutaPDF, "N??mero de registro")

		self.ErrorPDFs = Error

	#--------------------------------------------------------------------------------------------

	def GenerarListas(self, archivo = "Listas completas.txt"):
		#print("Has invocado al h??roe japon??s")

		''' Genera listas tabuladas de los alumnos divididos por salones '''

		Salones = dict()

		for alumno in self.lista:

			Salon_actual = f'\n\n* Lista del plantel {alumno.plantel}, curso {alumno.curso} del horario {alumno.horario} *\n\n'

			if Salon_actual not in Salones:
				Salones[Salon_actual] = []

			datos_alumno = [alumno.nombre,alumno.nRegistro,alumno.carrera,alumno.CU,alumno.NR_entregado, alumno.admitido]

			Salones[Salon_actual].append(datos_alumno)

		titulos = ["Nombre","Num. de registro", "Carrera", "Centro", "PDF enviado", "??Admitido?"]

		salida = open(archivo, "w")

		for salon in Salones:
			print(salon, file=salida)

			check_dictamen = ChecarDictamen(Salones[salon])

			if not check_dictamen and titulos[-1] == "??Admitido?":
				titulos.pop(-1)
			elif titulos[-1] != "??Admitido?":
				titulos.append("??Admitido?")

			print(tabla(Salones[salon], headers=titulos), file=salida)


		print("\n", file=salida)

		salida.close()
	#--------------------------------------------------------------------------------------------

	def EntregarPDF(self):

		''' Revisa la base de PDFs para verificar si cada alumno entreg?? o no su archivo PDF '''

		try:
			cursos = os.listdir(self.ruta_pdf)
		except FileNotFoundError:
			os.mkdir(self.ruta_pdf)
			cursos = os.listdir(self.ruta_pdf)

		entregado = dict()

		for curso in cursos:

			try:
				PDFs = os.listdir(self.ruta_pdf + "/" + curso)
			except NotADirectoryError:
				continue

			#datos_curso = curso.split("_")

			for PDF in PDFs:

				rutaPDF = self.ruta_pdf + "/" + curso + "/" + PDF
				PDF = quitaracentos(PDF)

				if "pdf" not in PDF.split("."):
					continue

				entregado[PDF.replace(".pdf","")] = rutaPDF

		for alumno in self.lista:
			alumno.ReiniciarPDFs()

		for alumno in self.lista:
			nombre = alumno.comparar_nombre

			if nombre in entregado:
				alumno.NR_entregado = "S??"
				alumno.RutaPDF = entregado[nombre]
			else:
				alumno.NR_entregado = "*No*"

	#--------------------------------------------------------------------------------------------

	def ReescribirBaseDatos(self, Consola = True):

		''' Reescribe la base de datos principal. Lo anterior se perder?? (por ahora) '''

		Salones = dict()
		rmtree(self.ruta_base_datos)

		for alumno in self.lista:
			directorio = f'{self.ruta_base_datos}/{alumno.plantel}/{alumno.curso}'
			Salon_actual = directorio + "/" + alumno.horario + ".txt"

			try:
				os.listdir(directorio)
			except FileNotFoundError:
				os.makedirs(directorio, exist_ok = True)

			if Salon_actual not in Salones:
				Salones[Salon_actual] = dict()

			datos_alumno = (alumno.nombre,alumno.nRegistro,alumno.carrera,alumno.CU)
			Salones[Salon_actual][alumno.comparar_nombre] = datos_alumno

		for salon in Salones:
			nombres_ordenados = sorted(Salones[salon])

			salida = open(salon,"w")

			for nombre in nombres_ordenados:
				print("\t&\t".join(Salones[salon][nombre]), file=salida )

			salida.close()

		self.add_cHistorial()
		self.Cambios_base(cargar = True)

		if Consola:
			print("\n\t*** La base de datos de alumnos, ha sido actualizada ***")

	#--------------------------------------------------------------------------------------------

	def EditarDatosAlumnos(self):

		''' Men?? para editar alumnos desde terminal '''

		print("\n\tBienvenidos al men?? de edici??n\n")
		print('''
	En este men?? solo puedes editar tres datos de los alumnos: Num.registro, carrera o
	Centro Universitario: para editar cada una ingresa, respectivamente, nr, c o cu al inicio
	de la linea de comando. Seguido del t??rmino de b??squeda (nombre o apellido) para el
	alumno, y luego el nuevo dato. Todo separado por comas. Ejemplo:

		c, Lopez Urquidi, Turismo

	Esto cambiar?? la carrera de un alumno con apellido Lopez Urquidi a Turismo. Si hay m??s
	co??ncidencias se desplegar?? un men?? para elegir. Nota: Los acentos y may??sculas no infieren
	en la b??squeda del nombre del alumno, por lo dem??s tiene que haber una coincidencia
	perfecta.

	Para salir, escribe exit. Si fuerzas el cierre, los cambios no se guardar??n. Para guardar
	sin salir, escribe actualizar.

		''')

		self.operadores = ["nr","c","cu"]
		self.consolaEditar()
		self.GenerarListas()
		self.UsedData()

	#--------------------------------------------------------------------------------------------

	def consolaEditar(self):

		''' Gestor de edici??n para terminal '''

		opcion = [""]

		while opcion[0] != "exit":
			opcion = input("\t>>> ").split(",")

			try:
				opcion[0],opcion[1],opcion[2] = procesar(opcion[0]),procesar(opcion[1]),QuitarMEspacios(opcion[2])
			except IndexError:
				procesar(opcion[0])

			try:
				if opcion[2].strip() == "*":
					opcion[2] = QuitarMEspacios(input("\t\tIngresa el nuevo dato>>> "))
			except IndexError:
				pass

			if opcion[0] == "exit":
				self.ReescribirBaseDatos()
			elif opcion[0] == "actualizar":
				self.ReescribirBaseDatos()
				print()
			elif len(opcion) < 3:
				print("\tERROR. Falta entradas, o no se est?? usando coma para separar.")
			elif len(opcion) > 3:
				print("\tERROR. Se ingres?? m??s de una entrada.")
			elif opcion[0].strip() not in self.operadores:
				print("\tERROR. No se encontr?? el dato a editar. Ingresa nr, c o cu al inicio de la linea.")
			else:
				self.MotorEditar(opcion)

		print()

	#--------------------------------------------------------------------------------------------

	def consolaEditar_GUI(self,cadena,funcion):

		''' Gestor de edici??n desde pesta??a de consola de la GUI. Incompleta '''

		self.operadores = ["nr","c","cu"]

		opcion = cadena.split(",")

		try:
			opcion[0],opcion[1],opcion[2] = procesar(opcion[0]),procesar(opcion[1]),QuitarMEspacios(opcion[2])
		except IndexError:
			procesar(opcion[0])

		if opcion[0] == "actualizar":
			self.ReescribirBaseDatos()
			funcion("Base de datos Actualizada")
		elif len(opcion) < 3:
			funcion("ERROR. Falta entradas, o no se est?? usando coma para separar.")
		elif len(opcion) > 3:
			funcion("ERROR. Se ingres?? m??s de una entrada.")
		elif opcion[0].strip() not in self.operadores:
			funcion("ERROR. No se encontr?? el dato a editar. Ingresa nr, c o cu al inicio de la linea.")
		else:
			self.MotorEditar(opcion)
	#--------------------------------------------------------------------------------------------

	def MotorEditar(self, opcion):

		''' Motor para edici??n de datos de alumnos para terminal '''

		if opcion[0].strip() == "nr":
			dato = "N??mero de registro"
		elif opcion[0].strip() == "c":
			dato = "Carrera"
		elif opcion[0].strip() == "cu":
			dato = "Centro Universitario"

		indice = bq.buscar(opcion[1],self.lista)

		if indice != "Abortar":
#			self.lista[indice].CambiarDato(dato, opcion[2].strip())
			self.MotorEditar_GUI(indice,dato, opcion[2].strip())

	def MotorEditar_GUI(self,indice,dato,nuevo):

		''' Motor para edici??n de datos de alumnos para GUI'''

		self.lista[indice].DiccAlumno()
		viejo = self.lista[indice].datos[dato]
		fecha = datetime.today().strftime('%Y-%m-%d %H:%M')

		cambio = f'{fecha}:\n\tCambio en {self.lista[indice].nombre} del plantel {self.lista[indice].plantel}, curso {self.lista[indice].curso}, horario {self.lista[indice].horario}:\n\t\t Cambi?? {dato}: {viejo} --> {nuevo}'

		self.lista[indice].CambiarDato(dato,nuevo)
		self.Cambios_realizados(cambio)
		self.UsedData()


	#--------------------------------------------------------------------------------------------

	def BuscarAlumno(self):

		''' Buscar a un alumno por nombre o apellido. Para terminal '''

		print("\n\tAqu?? puedes buscar a un alumno por nombre o apellido.")
		print("\tSe desplegaran los datos completos en pantalla. Para terminar escribe exit.\n")

		opcion = ""

		while opcion != "exit":
			opcion = input("\tBuscar>> ")

			if opcion == "Edicion":
				self.EditarDatosAlumnos()
				continue

			indice = bq.buscar(procesar(opcion),self.lista)

			if indice == "Abortar":
				continue

			print("\n\t**Datos Generales**")
			print("\tNombre: " + self.lista[indice].nombre)
			print("\tN??mero de registro: " + self.lista[indice].nRegistro)
			print("\tCarrera: " + self.lista[indice].carrera)
			print("\tCentro Universitario: " + self.lista[indice].CU)
			print("\t**Datos Lumiere**")
			print("\tPlantel: " + self.lista[indice].plantel + ", Curso: " + self.lista[indice].curso, end="")
			print(", Horario: " + self.lista[indice].horario)
			print("\t??PDF enviado?: " + self.lista[indice].NR_entregado)
			print()

			self.AbrirPDF(indice)

	def Buscar_(self,cadena):
		indice = bq.buscar_GUI(procesar(cadena),self.lista)
#		if indice == "Abortar":
#			continue
		return indice

	#--------------------------------------------------------------------------------------------

	def AbrirPDFmenu(self):

		''' Aqu?? puedes hacer uns b??squeda para abrir el PDF correspondiente a la busqueda del alumno.
			Para terminal '''

		print("\n\tAqu?? puedes hacer uns b??squeda para abrir el PDF correspondiente al")
		print("\tn??m??ro de registro del alumno si es que este ya lo entreg??. Busca por")
		print("\tnombre o apellido. Para salir escribe exit.\n")

		opcion = ""

		while opcion != "exit":
			opcion = input("\tBuscar>> ")

			indice = bq.buscar(procesar(opcion),self.lista)

			if indice == "Abortar":
				continue
			elif self.lista[indice].RutaPDF == "Sin ruta":
				print("\n\tEste alumno no ha entregado su PDF\n")
				continue

			print("\n\t** Abriendo archivo **\n")

			Ruta = "\"" + self.lista[indice].RutaPDF + "\""

			os.system("okular " + Ruta + " >/dev/null 2>&1 &")

			#print(Ruta)

	#--------------------------------------------------------------------------------------------

	def AbrirPDF(self,indice):

		''' Abrir el documento PDF desde la terminal '''

		ruta = self.lista[indice].RutaPDF

		if ruta == "Sin ruta":
			print()
			return
		loop = ""

		while loop == "":
			opcion = input("\t??Desea abrir el PDF con el n??mero de registro?(S/N)>>> ").strip().lower()

			if opcion not in ["s","n"]:
				print("\tOpci??n inv??lida")
				continue
			else:
				loop = "s"

			if opcion == "s":
				print("\n\t\t** Abriendo archivo **\n")
				Abrete(ruta)


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
			if i.datos["N??mero de registro"] not in ["n/a", "No data"]:
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
			salida = open(archivo, "w")
			print(cadena, file=salida)
			salida.close()
		else:
			return todos

	#-------- Importar JSON -----------------------------------------------------------------

	def ImportJSON(self, archivo = "alumnos.json", importar = True):

		''' Importa los datos de los alumnos contenidos en un JSON a las listas. Se debe actualizar
			la base de datos principal posteriormente '''

		entrada = open(archivo, "r")
		lineas = entrada.readlines()
		lineas = "".join(lineas)
		lineas = lineas.replace("\t","")
		lineas = lineas.replace("\n","")
		entrada.close()

		datos = json.loads(lineas)

		if importar:
			pass
		else:
			return datos

		self.lista = []

		for alumno in datos["Alumnos"]:
			n, nr, c = alumno["Nombre"],alumno["N??mero de registro"],alumno["Carrera"]
			cu = alumno["Centro Universitario"]
			curso,plantel,horario = alumno["Curso"],alumno["Plantel"],alumno["Horario"]

			self.lista.append(Alumno(n,nr,c,cu,curso,plantel,horario))


	#-------- Leer dictamen para conocer admitidos -----------------------------------------

	def LeerDictamen(self, archivo):

		cadena = PDF2Cadena(archivo)

		print(f'Mensaje de la clase "{type(self).__name__}": El archivo dictamen tiene una longitud de {len(cadena)}')

		self.num_Admitidos = 0

		for alumno in self.lista:
			alumno.ConfirmarAdmision(cadena)

			if alumno.admitido == "*S??*":
				self.num_Admitidos += 1



#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

class Alumno:

	def __init__(self, nombre, numRegistro, carrera, CU, curso, plantel, horario):

		''' Clase alumnos. Contiene la informaci??n de un alumnos '''

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
		self.GenerarComparar()
		self.RutaPDF = "Sin ruta"
		self.admitido = "No data"

		self.ValoresVacios()

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

		''' Cambiar determinado dato por el alumnos. Si el dato no es un atributo, retornar?? 0,
			caso contrario, 1 '''

		if dato == "N??mero de registro":
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
			self.admitido = "*S??*"
		else:
			self.admitido = " No"

	#--------------------------------------------------------------------------------------------

	def DiccAlumno(self):

		''' Genera diccionario que contiene la informaci??n del alumno '''

		self.datos = ({ "Nombre" : self.nombre, "N??mero de registro" : self.nRegistro,
						"Carrera" : self.carrera, "Centro Universitario" : self.CU,
						"Curso" : self.curso, "Plantel" : self.plantel, "Horario" : self.horario,
						"??PDF entregado?" : self.NR_entregado, "??Admitido?" : self.admitido})

	#-------------------------------------------------------------------------------------------

	def Alumno2JSON(self):

		''' Genera diccionario con los datos del alumno como preparaci??n para exportar a JSON '''

		self.datos = ({"Nombre" : self.nombre, "N??mero de registro" : self.nRegistro,
						"Carrera" : self.carrera, "Centro Universitario" : self.CU,
						"Curso" : self.curso, "Plantel" : self.plantel, "Horario" : self.horario,
						 "??Admitido?" : self.admitido})
