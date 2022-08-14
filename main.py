# Descripcion

from UI.Ventana_madre import *
from UI.Ventana_coincidencias import *
from UI.Ventana_alerta import *
from UI.Ventana_editar import *
from UI.Ventana_agregar import *
from TOOLS.alumno import *
from PyQt5.QtWidgets import QFileDialog

'''
Pendientes:

- QFileDialog.getExistingDirectory(self, "Guardar archivo","." ) para seleccionar directorios
- Cambiar nombre a menus Importar y Exportar

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

		rutas = extraer_historial(".rutas.json")
		self.Ruta_Base = rutas["Base_datos"]
		self.Ruta_PDF = rutas["Base_PDF"]
		self.Ruta_Historial = ".historial.json"

		self.Listas = self.Extraer_()

		self.MensajeUser(f'Bienvenido. El fichero {self.Ruta_Base}/ ha sido cargado')

		self.actionImportar.triggered.connect(self.Importar_)
		self.actionExportar.triggered.connect(self.Exportar_)
		self.actionGenerar_lista.triggered.connect(self.GenerarListas_)
		self.actionOrganizar_PDFs.triggered.connect(self.Org_PDFs_)
		self.actionImportar_JSON.triggered.connect(self.ImportarJSON)
		self.actionExportar_JSON.triggered.connect(self.ExportarJSON)

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

	#--------Mostrar mensajes al usuario -----------------------------------------------------------

	def MensajeUser(self,cadena):
		self.Mensajes2Usuario.setText(cadena)

	#--------Exportar a archivo JSON ----------------------------------------------------------------

	def ExportarJSON(self):
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
		ruta = extraer_historial(self.Ruta_Historial)["Entrada_JSON"]
		archivo = QFileDialog.getOpenFileName(self,"Elige el archivo", ruta, "Archivo JSON (*.json)")[0]

		if archivo.strip() == "":
			return

		r_historial("Entrada_JSON",archivo,self.Ruta_Historial)

		self.Listas.ImportJSON(archivo)
		self.MensajeUser(f'Archivo {archivo} cargado. Recuerde actualizar la base de datos')

	#--------Generar Listas Completas.txt -----------------------------------------------------

	def GenerarListas_(self):
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
		self.Listas.organizarPDF(False)

		self.MensajeUser(f'Los archivos PDF han sido organizados en {self.Ruta_PDF}/')

	# ------ Refrescar desde base de datos --------------------------------------------------------

	def Importar_(self):
		self.Listas = self.Extraer_()
		self.MensajeUser(f'La base de datos {self.Ruta_Base}/ ha sido cargada')

	# ------ Reescribir base de datos ----------------------------------------------------------------

	def Exportar_(self):
		self.Listas.ReescribirBaseDatos(False)
		self.MensajeUser(f'La base de datos {self.Ruta_Base}/ ha sido actualizada')

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
			self.Alerta = V_Alerta()
			self.Alerta.show() 							# Desplegamos ventana con mensaje cuando
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


	#---- Funcion para editar en pesataña busqueda-----------------------------------------------

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
		self.Listas.lista[self.indice].CambiarDato(dato,nuevo)
		self.Desplegar_alumnos(self.indice)

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
		for i in self.resultados:
			self.ListaCoincidencias.addItem(i)

	#------Funcion vinculada al boton Ok, para activar la funcion --------------------------------------

	def Aceptar(self):
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
#|------------------------------------------------------------------------------------------------------|


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	Ventana = MainWindow()
	Ventana.show()
	app.exec_()
