# Descripcion

from UI.Ventana_madre import *
from UI.Ventana_coincidencias import *
from UI.Ventana_alerta import *
from UI.Ventana_editar import *
from UI.Ventana_agregar import *
from UI.Ventana_directorios import *
from UI.Ventana_cerrar import *
from TOOLS.alumno import *
from PyQt5.QtWidgets import QFileDialog

'''
Pendientes:

- Consola
- Guardar versiones anteriores de la base de datos

'''


#|------------------------------------------------------------------------------------------------------|
#|------							 Clase ventana madre                                   -------------|
#|------------------------------------------------------------------------------------------------------|


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

	''' Ventana principal, donde se hace la magia '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)
		self.tabWidget.setCurrentIndex(0)

#		self.Ruta_main = os.path.dirname(os.path.abspath(__file__))
		self.Ruta_dir = ".rutas.json"
		self.Ruta_Historial = ".historial.json"
		self.Necesario_files()
		self.Set_RutasBases()

		self.Listas = self.Extraer_()

		self.MensajeUser(f'Bienvenido. El fichero {self.Ruta_Base}/ ha sido cargado')

		self.actionImportar.triggered.connect(self.Importar_)
		self.actionExportar.triggered.connect(self.Exportar_)
		self.actionGenerar_lista.triggered.connect(self.GenerarListas_)
		self.actionOrganizar_PDFs.triggered.connect(self.Org_PDFs_)
		self.actionImportar_JSON.triggered.connect(self.ImportarJSON)
		self.actionExportar_JSON.triggered.connect(self.ExportarJSON)
		self.actionEditar_directorios.triggered.connect(self.Editar_Dir)

		self.BotonBuscar.clicked.connect(self.Buscar)
		self.BotonAgregar.clicked.connect(self.AgregarBoton)
		self.AbrirPDF.clicked.connect(self.AbrirPDFBoton)
		self.BotonEditar.clicked.connect(self.EditarBoton)

	#------- Exportar los arlumnos desde la base de datos-------------------------------------------

	def Extraer_(self):

		''' Extraemos los alumnos del directorio elegido. Estos se reparten en de archivos TXT mediante
			el siguiente árbol: ./base_de_datos/PLANTEL/NOMBRE_CURSO/HORARIO.txt '''

		alumnos = extraer(self.Ruta_Base)

		L = []

		for alumno in alumnos:
			L.append(Alumno(*alumno))

		return TodosMisAlumnos(L, self.Ruta_PDF, self.Ruta_Base)


	#-------- Archivos necesarios --------------------------------------------------------------------


	def Necesario_files(self):

		''' Genera los archivos necesarios para que el programa funcione correctamente '''

		Rutas = [self.Ruta_dir, self.Ruta_Historial]

		rutas_dict = {"Base_datos": "Cursos", "Base_PDF": "Cursos_pdf"}
		historial = {"Salida_listas": "./", "Entrada_JSON": "./sin_titulo.json", "Salida_JSON": "./"}
		conte = [rutas_dict, historial]


		for i,j in zip(Rutas, conte):
			Existe_con(i,j)

	#-------- Elegir directorios de las bases de datos----------------------------------------------

	def Set_RutasBases(self):

		''' Busca en el archivo .rutas.json las rutas de las bases de datos que el usuario elija.
			Sí el archivo se borra, se crean directorios temporales '''

		rutas = extraer_historial(self.Ruta_dir)

		if check_dir(rutas["Base_datos"], self.Desplegar_Alerta):
			self.Ruta_Base = rutas["Base_datos"]
		else:
			self.Ruta_Base = "./Cursos_Temporal_"
			r_historial("Base_datos", self.Ruta_Base,self.Ruta_dir)

		self.Ruta_PDF = rutas["Base_PDF"]

	#--------Mostrar mensajes al usuario -----------------------------------------------------------

	def MensajeUser(self,cadena):

		''' Entrega al usuario mensajes del sistema '''

		self.Mensajes2Usuario.setText(cadena)

	#--------Exportar a archivo JSON ----------------------------------------------------------------

	def ExportarJSON(self):

		''' Exporta los datos de los alumnos cargados de la base de datos en un archivo JSON
			elegido por el usuario '''

		ruta = extraer_historial(self.Ruta_Historial)["Salida_JSON"]

		archivo = QFileDialog.getSaveFileName(self, "Guardar archivo",
											f'{ruta}/sin_titulo.json',
											"Archivo JSON (*.json)" )[0]

		ruta = os.path.dirname(archivo)
		r_historial("Salida_JSON",ruta,self.Ruta_Historial)

		self.Listas.Todos2JSON(archivo)
		self.MensajeUser(f'Datos de alumnos exportados a {archivo}')

	#------- Import JSON----------------------------------------------------------------------------

	def ImportarJSON(self):

		''' Importa datos de un archivo JSON proporcionado por el usuario. La información debe
			importarse a la base de datos posteriormente para mantener los datos '''

		ruta = extraer_historial(self.Ruta_Historial)["Entrada_JSON"]
		archivo = QFileDialog.getOpenFileName(self,"Elige el archivo", ruta, "Archivo JSON (*.json)")[0]

		if archivo.strip() == "":
			return

		r_historial("Entrada_JSON",archivo,self.Ruta_Historial)

		self.Listas.ImportJSON(archivo)
		self.MensajeUser(f'Archivo {archivo} cargado. Recuerde actualizar la base de datos')

	#--------Generar Listas Completas.txt -----------------------------------------------------

	def GenerarListas_(self):

		''' Usa el método de la clase TodosMisAlumnos para generar listas tabuladas de los datos
			de los alumnos proporcionados por la base de datos '''

		# Por alguna razon que desconozco, usar el método directo de TodosMisAlumnos GenerarListas()
		# en el Qaction generaba un problema: Al Importar_(), ya no funcionaba nuevamente

		ruta = extraer_historial(self.Ruta_Historial)["Salida_listas"]

		archivo = QFileDialog.getSaveFileName(self, "Generar archivo",
											"{ruta}/Listas_sin_nombre.txt",
											"Archivo TXT (*.txt)" )[0]

		if archivo.strip() == "":
			return

		ruta = os.path.dirname(archivo)
		r_historial("Salida_listas",ruta,self.Ruta_Historial)

		self.Listas.GenerarListas(archivo)
		self.MensajeUser(f'Las listas completas han sido generadas en {archivo}')

	#------- Organizar PDF -------------------------------------------------------------------------

	def Org_PDFs_(self):

		'''	Utiliza método de TodosMisAlumnos para organizar los PDFs que los alumnos proporcionan
			como respaldo al número de registro '''

		self.Listas.organizarPDF(False)

		self.MensajeUser(f'Los archivos PDF han sido organizados en {self.Ruta_PDF}/')

	# ------ Refrescar desde base de datos --------------------------------------------------------

	def Importar_(self):

		''' Extrae la información de la base de datos '''

		self.Listas = self.Extraer_()
		self.MensajeUser(f'La base de datos {self.Ruta_Base}/ ha sido cargada')

	# ------ Reescribir base de datos ----------------------------------------------------------------

	def Exportar_(self):

		''' Actualiza la información de la base de datos agregado los cambios y/o la información
			importada '''

		if self.Listas.ruta_base_datos != self.Ruta_Base:
			print("Problemas")
			return
		if check_dir(self.Ruta_Base, self.Desplegar_Alerta):
			pass
		else:
			self.MensajeUser(f'No se actualizó la base de datos {self.Ruta_Base}')
			return

		self.Listas.ReescribirBaseDatos(False)
		self.MensajeUser(f'La base de datos {self.Ruta_Base}/ ha sido actualizada')

	# ------ Editar los directorio de trabajo -------------------------------------------------------

	def Editar_Dir(self):

		''' Proporciona al usuario la opción de elegir la ubicación de las bases de datos: la base
			principal y la base que contiene los PDFs '''

		self.VentanaEditar_dir = V_EditarDirectorios()
		self.VentanaEditar_dir.EditarDirectorios(self.Ruta_dir, self.Set_RutasBases, self.MensajeUser)
		self.VentanaEditar_dir.show()

	# ------- Filtro de señales de teclado -----------------------------------------------------------

	def keyPressEvent(self,event):
		IndexTab = self.tabWidget.currentIndex()
		NameTab	= self.tabWidget.tabText(IndexTab)
		if event.key() == QtCore.Qt.Key_Return:
			if NameTab == "Buscar":				# Usar tecla enter para activar la busqueda
				self.Buscar()					# o la ejecucion de comandos
			elif NameTab == "Consola":
				self.EnterConsola()
		elif event.modifiers() == QtCore.Qt.ControlModifier:
			if event.key() == QtCore.Qt.Key_Tab: # Navegar entre pestañas con CTRL + Tab
				IndexTab += 1
				self.tabWidget.setCurrentIndex(IndexTab)
			elif event.key() == QtCore.Qt.Key_Backtab:
				IndexTab += 1
				self.tabWidget.setCurrentIndex(IndexTab)


	#---------- Funcion consola ----------------------------------------------------------------------

	def EnterConsola(self):

		''' Motor para consola. Sin terminar '''

		text = self.Consola.text().strip()
		if text == "":
			return

		self.Listas.consolaEditar_GUI(text,self.PantallaConsola)

	def PantallaConsola(self,mensaje):
		self.MensajesConsola.setText(mensaje)

	#--------- Función busqueda --------------------------------------------------------------------

	def Buscar(self):

		''' Busca mediente nombre o apellido un alumno'''

		busqueda = self.CuadroBuscar.text().strip()	 	# Recuperamos la cadena escrita en el cuadro de texto
		if busqueda == "":
			return

		self.MensajeUser("Buscando...")
		coincidencias = self.Listas.Buscar_(busqueda)	# buscamos en la base de datos
		self.MensajeUser("Hecho")

		if len(coincidencias) == 0:
			self.Desplegar_Alerta()
#			self.Alerta = V_Alerta()
#			self.Alerta.show() 							# Desplegamos ventana con mensaje cuando
			return										# la busqueda no arreje nada
		elif len(coincidencias) == 1:
			indice = list(coincidencias.values())[0]
			self.Desplegar_alumnos(indice)
			return 										# Si solo hay un resultado se despliega inmediatamente

		self.Ventana_Elegir = V_Coincidencias(coincidencias,self.Desplegar_alumnos)
		self.Ventana_Elegir.show() 						# Si hay mas de una coincidencia se despliega
														# otra ventana para elegir

	# ------ Función para desplegar datos de alumno -----------------------------------------------

	def Desplegar_alumnos(self,indice):

		''' Muestra los datos del alumno en el cuadro de texto'''

		self.indice = indice					# La busqueda arroja el indice del alumno
		self.CuadroBuscar.clear()
		self.Mostrar.clear()					# Limpiamos la busqueda pasada
		self.Listas.lista[indice].DiccAlumno()
		datos = self.Listas.lista[indice].datos # Obtenemos los datos del alumno

		for i in datos:							# Imprimimos los datos
			self.Mostrar.addItem(i + ": " + datos[i]  )

		self.MensajeUser("Datos del alumno:")

	#------ Funcion para agregar alumno --------------------------------------------------------

	def AgregarBoton(self):

		''' Despliega ventana formulario para agregar alumno y sus datos '''

		self.V_Add = V_Agregar()
		self.V_Add.infuncion(self.Agregar_2)
		self.V_Add.show()

	def Agregar_2(self,lista):
		self.Listas.AddAlumno(lista)

	# ----- Funcion para boton Abrir PDF -------------------------------------------------------

	def AbrirPDFBoton(self):

		''' Abre el PDF del documento que contiene el número de registro el alumno '''

		try:
			self.Listas.AbrirPDF_GUI(self.indice)
		except AttributeError:
			self.MensajeUser("No hay PDF disponible")


	#---- Funcion para editar en pestaña busqueda-----------------------------------------------

	def EditarBoton(self):

		''' Elige algun dato del alumno para editarlo'''

		index = self.Mostrar.currentRow()
		try:
			datos = datos = self.Listas.lista[self.indice].datos
			atri = list(datos.keys())[index]
		except AttributeError:
			return

		if atri == "¿PDF entregado?":
			self.MensajeUser("Error. Elige un atributo editable")
			return

		self.V_E = V_Editar()
		self.V_E.EditarAtributo(datos["Nombre"], atri, self.EditarBoton_2)
		self.V_E.show()

	def EditarBoton_2(self,dato,nuevo):
		self.Listas.MotorEditar_GUI(self.indice, dato, nuevo)
		self.Desplegar_alumnos(self.indice)

	#----- Desplegar ventana alerta ---------------------------------------------------------

	def Desplegar_Alerta(self, mensaje = ""):

		''' Despliega ventana de alerta. El mensaje es elegible '''

		# Mensaje predeterminado: No hay resultados

		self.Alerta = V_Alerta()
		if mensaje != "":
			self.Alerta.CambiarMensaje(mensaje)
		self.Alerta.show()

	#-----Evento cerrar---------------------------------------------------------------------------------

	def closeEvent(self,event):

		''' Despliega ventana al cerrar si aún hay cambios sin guardar en la base de datos '''

		event.ignore()

		try:
			tama = len(self.Listas.CambiosSinGuardar)
		except AttributeError:
			event.accept()
			return

		if tama != 0:
			self.cerrar_V = V_Cerrar()
			self.cerrar_V.MostrarCambios(self.Listas.CambiosSinGuardar, self.closeEvent_2)
			self.cerrar_V.show()
		else:
			event.accept()


	def closeEvent_2(self, eleccion = "No"):
		if eleccion == "Si":
			self.Listas.ReescribirBaseDatos(False)
		else:
			self.Listas.CambiosSinGuardar = []
		self.close()

#|------------------------------------------------------------------------------------------------------|
#|------ Clase ventana para coincidencias de búsqueda                                      -------------|
#|------------------------------------------------------------------------------------------------------|

class V_Coincidencias(QtWidgets.QDialog, Ui_Ventana_Coincidencias):

	'''	Clase ventana para coincidencias de búsqueda. Se mostrará cuando la búsqueda
		coincida con varios alumnos'''


	def __init__(self,dicc,funcion, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.resultados = dicc				# Entra un diccionario con las coincidencias {nombre: indice}
		self.eleccion = funcion				# La funcion para mostrarla al usuario

		self.Imprimir()
		self.buttonBox.accepted.connect(self.Aceptar)

	#----- Funcion para imprimir las coincidencias y que el usuario eliga la requerida ----------------

	def Imprimir(self):

		# Imprime los rsultados en pantalla

		for i in self.resultados:
			self.ListaCoincidencias.addItem(i)

	#------Funcion vinculada al boton Ok, para activar la funcion --------------------------------------

	def Aceptar(self):

		# Selecciona el alumno y acepta

		nombre = self.ListaCoincidencias.currentItem().text()
		self.eleccion(self.resultados[nombre])

#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para edición de búsqueda                                      -------------|
#|------------------------------------------------------------------------------------------------------|

class V_Editar(QtWidgets.QDialog, Ui_VentanaEditar):

	''' Clase ventana para edición de búsqueda. Se desplegará cuando se requiera editar
		algún dato de un alumno dado desde la pestaña de busqueda. '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.buttonBox.accepted.connect(self.Aceptar)

	def Aceptar(self):
		nuevo = self.EntradaEditar.text().strip()
		if nuevo == "":
			return

		self.F(self.d, nuevo)

	def EditarAtributo(self, nombre ,dato, funcion):

		''' Importa datos de la clase principal. Admite el nombre del alumno, el dato a editar y
			la función necesaria para editar en la base de datos: EditarAtributo(nombre ,dato, funcion) '''

		self.NombreAlumno.setText(nombre)
		self.AtributoEditar.setText(dato + ": ")
		self.F = funcion
		self.d = dato

#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para alertas                                                  -------------|
#|------------------------------------------------------------------------------------------------------|

class V_Alerta(QtWidgets.QDialog, Ui_VentanaAlerta):

	''' Mensajes de alerta para el usuario '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

	def CambiarMensaje(self,cadena):

		''' Elige el mensaje a desplegar '''

		# Predeterminado: No hay resultados

		self.MensajeNoHay.setText(cadena)

#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para agregar                                                  -------------|
#|------------------------------------------------------------------------------------------------------|

class V_Agregar(QtWidgets.QDialog, Ui_VentanaAgregar):

	''' Formulario para agregar alumno '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.buttonBox.accepted.connect(self.addAlumno)

	def infuncion(self,funcion):
		self.f = funcion

	def addAlumno(self):
		n = self.a_nombre.text().strip()
		nr = self.a_nregistro.text().strip()
		c = self.a_carrera.text().strip()
		cu = self.a_CU.text().strip()
		curso = self.a_curso.text().strip()
		plantel = self.a_plantel.text().strip()
		horario = self.a_horario.text().strip()

		self.f([n, nr, c, cu, curso, plantel, horario])

#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para agregar                                                  -------------|
#|------------------------------------------------------------------------------------------------------|

class V_EditarDirectorios(QtWidgets.QDialog, Ui_Ventana_Directorios):

	''' Formulario para editar los directorios para la base de datos y los PDF de los alumnos '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.Boton_BaseDatos.clicked.connect(lambda: self.Botonelegir("Base_datos"))
		self.Boton_BasePDF.clicked.connect(lambda: self.Botonelegir("Base_PDF"))

		self.buttonBox.accepted.connect(self.Aceptado)

	def EditarDirectorios(self,ruta,f,f_m):

		''' Importar datos a la clase '''

		self.F = f				# funcion para actualizar las rutas de los directorios
		self.F_m = f_m			# Funcion para mostrar mensajes al usuario
		self.Ruta = ruta		# Lugar donde se guardan las rutas de las bases de datos

		self.dicc = extraer_historial(ruta)

		self.Entrada_BaseDatos.setText(self.dicc["Base_datos"])
		self.Entrada_BasePDF.setText(self.dicc["Base_PDF"])


	def Botonelegir(self, eleccion):
		ruta = QFileDialog.getExistingDirectory(self, eleccion.replace("_"," "), self.dicc[eleccion])

		if eleccion == "Base_datos":
			self.Entrada_BaseDatos.setText(ruta)
		else:
			self.Entrada_BasePDF.setText(ruta)


	def Aceptado(self):
		base = self.Entrada_BaseDatos.text()
		base_pdf = self.Entrada_BasePDF.text()

		r_historial("Base_datos",base,self.Ruta)
		r_historial("Base_PDF",base_pdf,self.Ruta)

		self.F()
		self.F_m(f'Las bases de datos han sido cambiadas. No olvides importar.')


#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para alertar durante el cierre                                -------------|
#|------------------------------------------------------------------------------------------------------|

class V_Cerrar(QtWidgets.QDialog, Ui_VentanaCerrar):

	''' Si al cerrar hay cambios sin exportar a la base de datos esta ventana se desplegará '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.buttonBox.accepted.connect(self.si_eleccion)
		self.buttonBox.rejected.connect(self.no_eleccion)
		self.NoCerrar.clicked.connect(self.close)

	def MostrarCambios(self,lista, f):
		self.F = f

		cadena = "\n".join(lista)

		self.MostrarContenido.setText(cadena)

	def si_eleccion(self):
		self.F("Si")

	def no_eleccion(self):
		self.F()



#|------------------------------------------------------------------------------------------------------|
#|------------------------------------------------------------------------------------------------------|


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	Ventana = MainWindow()
	Ventana.show()
	app.exec_()
