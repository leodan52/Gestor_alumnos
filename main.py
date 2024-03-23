# Por: Leonardo D. Santiago

from UI.Ventana_madre import *
from UI.Ventana_coincidencias import *
from UI.Ventana_alerta import *
from UI.Ventana_editar import *
from UI.Ventana_agregar import *
from UI.Ventana_directorios import *
from UI.Ventana_cerrar import *
from UI.Ventana_cargarCSV import *

from TOOLS.alumno import *
from TOOLS.objetos import *
from PyQt5.QtWidgets import QFileDialog, QCompleter

identificador = 2

#|------------------------------------------------------------------------------------------------------|
#|------							 Clase ventana madre                                   -------------|
#|------------------------------------------------------------------------------------------------------|


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

	''' Ventana principal, donde se hace la magia '''

	def __init__(self, *args, **kwargs):

		QtWidgets.QMainWindow.__init__(self, *args)
		self.setupUi(self)

		self.tabWidget.setCurrentIndex(0)

		try:
			self.dir_main = kwargs["rutaMain"]
		except KeyError:
			self.dir_main = os.getcwd()

		self.Ruta_dir = os.path.join(self.dir_main, ".rutas.json")
		self.Ruta_Historial = os.path.join(self.dir_main, ".historial.json")
		self.Ruta_Base = os.path.join(self.dir_main, "BASE", f'BASE_{os.path.split(self.dir_main)[1]}')
		self.Ruta_PDF = os.path.join(self.dir_main, "PDFs")

		self.PalabrasClaves = "Coincidencias de búsqueda para cuadro"
		self.indice = None

		self.arbolPlantel = []
		self.arbolCurso = []
		self.arbolHorario = []

		self.Necesario_files()
		self.Set_RutasBases()

		self.Listas = self.Extraer_()

		self.MensajeUser(f'Bienvenido. Estamos trabajando en {self.dir_main}')

		self.ActualizarCompletador()

		# ** Menú Archivo **

		self.actionNuevo.triggered.connect(self.Nuevo_)
#		self.actionImportar.triggered.connect(self.Importar_)
		self.actionGuardar.triggered.connect(self.Guardar_)
		self.actionGenerar_lista.triggered.connect(self.GenerarListas_)
		self.actionImportar_JSON.triggered.connect(self.ImportarJSON)
		self.actionExportar_JSON.triggered.connect(self.ExportarJSON)
		self.actionImportacion_masiva.triggered.connect(self.ImportarCSV_)

		# ** Menú Cursos **

		self.actionOrganizar_PDFs.triggered.connect(self.Org_PDFs_)
		self.actionEscanear_PDF.triggered.connect(self.Scan_PDFs_)
		self.actionEditar_directorios.triggered.connect(self.Editar_Dir)
		self.actionConfirmar_admision.triggered.connect(self.BuscarAdmitidos)

		# ** Botones pestaña buscar **

		self.BotonBuscar.clicked.connect(self.Buscar)
		self.BotonAgregar.clicked.connect(self.AgregarBoton)
		self.buttonActualizarInfo.clicked.connect(self.ActualizarDespliegue)
		self.BotonEditar.clicked.connect(self.EditarBoton)
		self.AbrirPDF.clicked.connect(self.AbrirPDFBoton)
		self.BotonEliminar.clicked.connect(self.EliminarAlumno)

		# ** Señales pestaña buscar **

		self.CuadroBuscar.returnPressed.connect(self.BotonBuscar.animateClick)
		self.Mostrar.itemActivated.connect(self.BotonEditar.animateClick)

		# ** Botones pestaña Listas **

		self.buttonActualizarArbol.clicked.connect(self.EscribirArbol)
		self.buttonEliminarTabListas.clicked.connect(self.EliminardesdeArbol)
		self.buttonGuardarCSV.clicked.connect(self.GuardarSalonArchivo)
		self.buttonAgregarTabListas.clicked.connect(self.AgregarASalon)

		# ** Señales pestaña Listas **

		self.ArbolListas.itemActivated.connect(self.ImprimirdeArbol)
		self.MostrarListas.itemActivated.connect(self.MostrarDatosdTabListas)

		# ** Gestión de botones **

		self.BotonesDes()

	#-------- Archivos necesarios --------------------------------------------------------------------

	def Necesario_files(self):

		''' Genera los archivos necesarios para que el programa funcione correctamente '''

		Rutas = [self.Ruta_dir, self.Ruta_Historial]

		rutas_dict = ({"Base_datos": self.Ruta_Base,
					 	"Base_PDF": self.Ruta_PDF})
		historial = ({"Salida_listas": self.dir_main,
						"Entrada_JSON": os.path.join(self.dir_main, "sin_titulo.json"),
						"Salida_JSON": self.dir_main})

		conte = [rutas_dict, historial]

		for i,j in zip(Rutas, conte):
			Existe_con(i,j)

	#-------- Elegir directorios de las bases de datos----------------------------------------------

	def Set_RutasBases(self):

		''' Busca en el archivo .rutas.json las rutas de las bases de datos que el usuario elija.
			Sí el archivo se borra, se crean directorios temporales '''

		rutas = extraer_historial(self.Ruta_dir)

		self.Ruta_Base = rutas["Base_datos"]
		self.Ruta_PDF = rutas["Base_PDF"]

	#------- Exportar los alumnos desde la base de datos-------------------------------------------

	def Extraer_(self):

		''' Extraer los datos de los alumnos  de un archivo existente '''

		try:
			return CargarBinario(self.Ruta_Base)
		except FileNotFoundError:
			os.makedirs(os.path.split(self.Ruta_Base)[0], exist_ok = True)
			return TodosMisAlumnos([], self.Ruta_PDF, os.path.split(self.Ruta_Base)[0])

	#--------Mostrar mensajes al usuario -----------------------------------------------------------

	def MensajeUser(self,cadena):

		''' Entrega al usuario mensajes del sistema '''

		self.Mensajes2Usuario.setText(cadena)

	#........ Actualizar completador -----------------------------------------------------------------

	def ActualizarCompletador(self):

		nombres = list(map(lambda a: a.nombre, self.Listas.lista))

		PalabrasClaves = QCompleter(nombres)
		PalabrasClaves.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		PalabrasClaves.setFilterMode(QtCore.Qt.MatchContains)
		self.CuadroBuscar.setCompleter(PalabrasClaves)


	#----- Desplegar ventana alerta ---------------------------------------------------------

	def Desplegar_Alerta(self, mensaje = ""):

		''' Despliega ventana de alerta. El mensaje es elegible '''

		# Mensaje predeterminado: No hay resultados

		self.Alerta = V_Alerta()
		if mensaje != "":
			self.Alerta.CambiarMensaje(mensaje)
		self.Alerta.show()

	#***************************************************************************************
	#*		Funciones para menús
	#***************************************************************************************

	# ------  Definir nueva base de datos ------------------------------------------------------------

	def Nuevo_(self):

		''' Ofrece la opción de abrir una nueva ventana para gestionar otra base de datos
			de forma paralela '''

		nuevoDir_main = QFileDialog.getExistingDirectory(self,
						"Selecciona la ubicación de trabajo", self.dir_main)

		if nuevoDir_main.strip() == "":
			return

		MainWindow.newInstances(nuevoDir_main)

	# ------ Reescribir base de datos ----------------------------------------------------------------

	def Guardar_(self):

		''' Actualiza la información de la base de datos agregado los cambios y/o la información
			importada '''

		self.Listas.Control_version()
		self.Listas.add_cHistorial()
		GuardarBinario(self.Listas, self.Ruta_Base)

		self.MensajeUser(f'La base de datos {self.Ruta_Base}/ ha sido actualizada')


	#--------Generar Listas Completas.txt -----------------------------------------------------

	def GenerarListas_(self):

		''' Usa el método de la clase TodosMisAlumnos para generar listas tabuladas de los datos
			de los alumnos proporcionados por la base de datos '''

		# Por alguna razón que desconozco, usar el método directo de TodosMisAlumnos GenerarListas()
		# en el Qaction generaba un problema: Al Importar_(), ya no funcionaba nuevamente

		ruta = extraer_historial(self.Ruta_Historial)["Salida_listas"]

		archivo = QFileDialog.getSaveFileName(self, "Generar archivo",
											"{ruta}/Listas_sin_nombre.txt",
											"Archivo TXT (*.txt)" )[0]

		if archivo.strip() == "":
			return

		ruta = os.path.dirname(archivo)
		historial_rutas("Salida_listas",ruta,self.Ruta_Historial)

		self.Listas.GenerarListas(archivo)
		self.MensajeUser(f'Las listas completas han sido generadas en {archivo}')

	#------- Import JSON----------------------------------------------------------------------------

	def ImportarJSON(self):

		''' Importa datos de un archivo JSON proporcionado por el usuario. La información debe
			importarse a la base de datos posteriormente para mantener los datos '''

		ruta = extraer_historial(self.Ruta_Historial)["Entrada_JSON"]
		archivo = QFileDialog.getOpenFileName(self,"Elige el archivo", ruta, "Archivo JSON (*.json)")[0]

		if archivo.strip() == "":
			return

		historial_rutas("Entrada_JSON",archivo,self.Ruta_Historial)

		self.Listas.ImportJSON(archivo)
		self.ActualizarCompletador()
		self.MensajeUser(f'Archivo {archivo} cargado. Recuerde actualizar la base de datos')

	#--------Exportar a archivo JSON ----------------------------------------------------------------

	def ExportarJSON(self):

		''' Exporta los datos de los alumnos cargados de la base de datos en un archivo JSON
			elegido por el usuario '''

		ruta = extraer_historial(self.Ruta_Historial)["Salida_JSON"]

		archivo = QFileDialog.getSaveFileName(self, "Guardar archivo",
											f'{ruta}/sin_titulo.json',
											"Archivo JSON (*.json)" )[0]

		if archivo.strip() == "":
			return

		ruta = os.path.dirname(archivo)
		historial_rutas("Salida_JSON",ruta,self.Ruta_Historial)

		self.Listas.Todos2JSON(archivo)
		self.MensajeUser(f'Datos de alumnos exportados a {archivo}')


	#--- Importación masiva -------------------------------------------------------------------------

	def ImportarCSV_(self):

		''' Despliega ventana para importación masiva usando archivos CSV'''

		self.VentanaAgregarCSV = V_AgregarCSV()
		self.VentanaAgregarCSV.AgregarCVS(self.Ruta_Historial,
										self.Listas.ImportarCSV,
										 self.ActualizarCompletador, self.Listas.Data)
		self.VentanaAgregarCSV.show()


	#------- Organizar PDF -------------------------------------------------------------------------

	def Org_PDFs_(self):

		'''	Utiliza método de TodosMisAlumnos para organizar los PDFs que los alumnos proporcionan
			como respaldo al número de registro '''

		self.Listas.organizarPDF(False)

		self.MensajeUser(f'Los archivos PDF han sido organizados en {self.Ruta_PDF}/')

	#-.----- Escanear PDFs--------------------------------------------------------------------------

	def Scan_PDFs_(self):

		''' Lee los archivos PDFs para verificar que pertenecen al alumno en cuestión'''

		self.MensajeUser("Escaneado PDF...")
		self.Listas.EscanearPDFs()

		if len(self.Listas.ErrorPDFs) == 0:
			self.MensajeUser("No se encontraron errores en los archivos PDF")
			return
		else:
			self.MensajeUser(f'Se encontraron {len(self.Listas.ErrorPDFs)} errores en los archivos PDF')

		salida_ = ""

		for nombre in self.Listas.ErrorPDFs:
			fecha = datetime.today().strftime('%Y-%m-%d %H:%M') + ": "
			salida_ = f'{salida_}{fecha}Error en el archivo del alumno {nombre} en "{self.Listas.ErrorPDFs[nombre][0]}":\n'
			salida_ = f'{salida_}\tEl {self.Listas.ErrorPDFs[nombre][1]} es incorrecto\n\n'

		with open("Informe_errores_PDF.txt", "w") as salidaf:
			print(salida_, file=salidaf)

	# ------ Editar los directorio de trabajo -------------------------------------------------------

	def Editar_Dir(self):

		''' Proporciona al usuario la opción de elegir la ubicación de las bases de datos: la base
			principal y la base que contiene los PDFs '''

		self.VentanaEditar_dir = V_EditarDirectorios()
		self.VentanaEditar_dir.EditarDirectorios(self.Ruta_dir, self.Set_RutasBases, self.MensajeUser)
		self.VentanaEditar_dir.show()

	# -----------Cargar PDF con dictamen y buscar admitidos ----------------------------------------

	def BuscarAdmitidos(self):

		''' Cuando el dictamen UDG de admitidos sea publicado, se puede usar el PDF para buscar
			si los alumnos del curso fueron admitidos '''
		try:
			ruta = extraer_historial(self.Ruta_Historial)["Dictamen"]
		except KeyError:
			ruta = self.dir_main

		archivo = QFileDialog.getOpenFileName(self,"Elige el PDF que contiene el dictamen", ruta, "Archivo PDF (*.pdf)")[0]

		self.Listas.LeerDictamen(archivo)
		self.MensajeUser(f'Un total de {self.Listas.num_Admitidos} fueron admitidos.')

		ruta = os.path.dirname(archivo)
		historial_rutas("Dictamen", ruta, self.Ruta_Historial)


	#***********************************************************************************
	#*		Botones de la pestaña buscar
	#***********************************************************************************

	#--------- Función búsqueda --------------------------------------------------------------------

	def Buscar(self):

		''' Busca mediante nombre o apellido un alumno'''

		busqueda = self.CuadroBuscar.text().strip()	 	# Recuperamos la cadena escrita en el cuadro de texto
		if busqueda == "":
			return

		self.MensajeUser("Buscando...")
		coincidencias = self.Listas.Buscar_(busqueda)	# buscamos en la base de datos
		self.MensajeUser("Hecho")

		if len(coincidencias) == 0:
			self.Desplegar_Alerta()
			return
		elif len(coincidencias) == 1:
			indice = list(coincidencias.values())[0]
			self.Desplegar_alumnos(indice)
			return 										# Si solo hay un resultado se despliega inmediatamente

		self.Ventana_Elegir = V_Coincidencias(coincidencias,self.Desplegar_alumnos)
		self.Ventana_Elegir.show() 						# Si hay mas de una coincidencia se despliega
														# otra ventana para elegir

	#------ Función para agregar alumno --------------------------------------------------------

	def AgregarBoton(self):

		''' Despliega ventana formulario para agregar alumno y sus datos '''

		self.V_Add = V_Agregar()
		self.V_Add.infuncion(self.Agregar_2, self.Listas.Data)
		self.V_Add.show()

	def Agregar_2(self,lista):
		self.Listas.AddAlumno(lista)
		self.ActualizarCompletador()

	# ------- Función para botón actualizar para mirar datos de alumno -----------------------------

	def ActualizarDespliegue(self):

		''' Actualiza los datos de alumno mostrados en pantalla para cuando los datos cambien '''

		self.Desplegar_alumnos(self.indice)

	#---- Función para editar en pestaña busqueda-----------------------------------------------

	def EditarBoton(self):

		''' Elige algún dato del alumno para editarlo'''

		index = self.Mostrar.currentRow()
		try:
			datos = self.Listas.lista[self.indice].datos
			atri = list(datos.keys())[index]
		except AttributeError:
			return

		if atri in ["¿PDF entregado?", "¿Admitido?"]:
			self.MensajeUser("Error. Elige un atributo editable")
			return
		viejo = datos[atri]

		self.V_E = V_Editar()
		self.V_E.EditarAtributo(datos["Nombre"], viejo, atri, self.EditarBoton_2, self.Listas.Data)
		self.V_E.show()

	def EditarBoton_2(self,dato,nuevo):

		''' Edita atributo de alumno '''

		self.Listas.MotorEditar_GUI(self.indice, dato, nuevo)
		self.Desplegar_alumnos(self.indice)
		self.ActualizarCompletador()

	# ----- Función para botón Abrir PDF -------------------------------------------------------

	def AbrirPDFBoton(self):

		''' Abre el PDF del documento que contiene el número de registro el alumno '''

		try:
			self.Listas.AbrirPDF_GUI(self.indice)
		except AttributeError:
			self.MensajeUser("No hay PDF disponible")

	#----- Función eliminar alumno --------------------------------------------------------------

	def EliminarAlumno(self, f = None):

		''' Función para preguntar a usuario si está seguro de eliminar alumno '''

		nombre = self.Listas.lista[self.indice].nombre


		if not f:
			f = lambda: None

		self.Alerta = V_Alerta()
		self.Alerta.CambiarMensaje(f'¿Estás seguro de borrar al alumno {nombre}?')
		self.Alerta.ActFun(self.Eliminar_, f)
		self.Alerta.show()

	def Eliminar_(self):

		''' Elimina a alumno '''

		self.Listas.RmAlumno(self.indice)
		self.indice = None

		self.Mostrar.clear()
		self.BotonesDes()

	#****************************************************************************************
	#*		Funciones necesarias para la pestaña buscar
	#****************************************************************************************

	# ------ Función para desplegar datos de alumno en pantalla -----------------------------

	def Desplegar_alumnos(self,indice):

		''' Muestra los datos del alumno en el cuadro de texto'''

		self.indice = indice					# La busqueda arroja el indice del alumno
		self.CuadroBuscar.clear()
		self.Mostrar.clear()					# Limpiamos la busqueda pasada
		datos = self.Listas.lista[indice].datos # Obtenemos los datos del alumno

		for i in datos:							# Imprimimos los datos
			self.Mostrar.addItem(i + ": " + datos[i]  )

		self.MensajeUser("Datos del alumno:")
		self.BotonesOn()

	#****************************************************************************************
	#*			Botones de la pestaña Listas
	#****************************************************************************************

	#----- General arbol para pestaña listas ---------------------------------------------------------

	def EscribirArbol(self):

		''' Genera un diccionario para auxiliar la organización en formato árbol en pantalla '''

		arbol = self.Listas.getArbol()
		self.ArbolListas.clear()

		if len(arbol) == 0:
			return

		self.buttonActualizarArbol.setText("Actualizar")

		planteles = [*arbol.keys()]
		planteles.sort()

		for plantel in planteles:
			cursos = [*arbol[plantel].keys()]
			cursos.sort()

			self.arbolPlantel.append(TreeItem(self.ArbolListas, "plantel"))
			self.arbolPlantel[-1].setText(0, plantel)

			for curso in cursos:
				horarios = [*arbol[plantel][curso].keys()]
				horarios.sort()

				self.arbolCurso.append(TreeItem(self.arbolPlantel[-1], "curso"))
				self.arbolCurso[-1].setText(0, curso)

				for horario in horarios:
					arbol[plantel][curso][horario].sort()

					self.arbolHorario.append(TreeItem(self.arbolCurso[-1], "horario"))
					self.arbolHorario[-1].setText(0, horario)
					self.arbolHorario[-1].setListaAlumnos(arbol[plantel][curso][horario])
					self.arbolHorario[-1].setSalonDatos([plantel, curso, horario])


	#-------- Eliminar alumno desde Lista -------------------------------------------------------------

	def EliminardesdeArbol(self):

		''' Elimina a alumno desde la pestaña Listas. Regresa a la pestaña Busqueda para mostrar los
			datos del alumno y ejecutar la eliminación '''

		numLista = self.MostrarListas.currentRow()

		self.MostrarDatosdTabListas()

		self.EliminarAlumno(lambda x = numLista: self.RegresarATabYEliminar(x))

	def RegresarATabYEliminar(self, row):

		''' Si la eliminación se efectúa, regresa a la pestaña Listas y elimina a alumno de pantalla '''

		self.tabWidget.setCurrentIndex(1)

		if self.indice == None:
			self.MostrarListas.takeItem(row)

	#------ Exporta salon a archivo JSON o CSV -----------------------------------------------------------

	def GuardarSalonArchivo(self):

		''' Guarda los datos de alumnos del salón en pantalla en un archivo ya sea JSON
			o un archivo CSV '''

		historial_rutas =extraer_historial(self.Ruta_Historial)

		try:
			ruta = historial_rutas["GuardaSalonArchivo"]
		except KeyError:
			ruta = self.dir_main

		datosCurso ="_".join(self.aulaDatos)

		nombreArchivo = os.path.join(self.dir_main, datosCurso)

		OpenFile = QFileDialog.getSaveFileName(self,"Elige el archivo",
												 f'{nombreArchivo}.csv;;{nombreArchivo}.json',
												 "Archivo CSV (*.csv);;Archivo JSON (*.json)")
		archivo = OpenFile[0]

		if archivo == "":
			return

		path_archivo = os.path.dirname(archivo)
		historial_rutas("GuardaSalonArchivo", path_archivo, self.Ruta_Historial)

		indices = []

		for i in self.aulaLista:
			indices.append(i["indice"])

		if OpenFile[1].startswith("Archivo CSV"):
			self.Listas.ExportarCSV(archivo, *indices)
		else:
			self.Listas.ExportarAulaJSON(archivo, *indices)

	def AgregarASalon(self):

		''' Agrega a alumno al salón actual mostrado en pantalla '''

		datos_key = ["Plantel", "Curso", "Horario"]
		datos = {d: cadena for d, cadena in zip(datos_key, self.aulaDatos)}

		self.V_Add = V_Agregar()
		self.V_Add.infuncion(self.Agregar_2, self.Listas.Data)
		self.V_Add.LlenarDatos(datos)
		self.V_Add.show()

	#********************************************************************************
	#*   Funciones para señales de widgets de la pestaña Lista
	#********************************************************************************

	def ImprimirdeArbol(self):

		''' Imprime la clase seleccionada en ArbolListas en el cuadro de texto MostrarListas '''

		item = self.ArbolListas.currentItem()

		if item.getTipo() != "horario":
			return

		self.aulaLista = item.getLista()
		self.aulaDatos = item.getSalonDatos()

		self.MostrarListas.clear()

		for i in self.aulaLista:
			self.MostrarListas.addItem(" "*5 + i["nombre"])

		self.buttonEliminarTabListas.setEnabled(True)
		self.buttonAgregarTabListas.setEnabled(True)
		self.buttonGuardarCSV.setEnabled(True)

	def MostrarDatosdTabListas(self):

		''' Cambia a la pestaña buscar para mostrar los datos del alumno seleccionado '''

		numLista = self.MostrarListas.currentRow()
		indice = self.aulaLista[numLista]["indice"]

		self.tabWidget.setCurrentIndex(0)

		self.Desplegar_alumnos(indice)

	#********************************************************************************
	#*   Habilitar botones o deshabilitar según sean necesarios
	#********************************************************************************

	def BotonesDes(self):

		''' Desactivar botones de ambas pestañas según sea necesario '''

		if self.Mostrar.count() == 0:
			self.BotonEditar.setEnabled(False)
			self.BotonEliminar.setEnabled(False)
			self.AbrirPDF.setEnabled(False)
			self.buttonActualizarInfo.setEnabled(False)

		if self.MostrarListas.count() == 0:
			self.buttonEliminarTabListas.setEnabled(False)
			self.buttonAgregarTabListas.setEnabled(False)
			self.buttonGuardarCSV.setEnabled(False)

	def BotonesOn(self):

		''' Activar botones de ambas pestañas cuando puedan ser utilizados '''

		if self.Mostrar.count() != 0:
			self.BotonEditar.setEnabled(True)
			self.BotonEliminar.setEnabled(True)
			self.buttonActualizarInfo.setEnabled(True)

		if self.Listas.lista[self.indice].datos["¿PDF entregado?"] == "Sí":
			self.AbrirPDF.setEnabled(True)
		else:
			self.AbrirPDF.setEnabled(False)

	#***********************************************************************
	#*		Métodos de clase
	#***********************************************************************

	@classmethod
	def newInstances(cls, ruta_):
		global identificador

		if f'add{identificador}' not in globals():
			identificador += 1

		globals()[f'Ventana{identificador}'] = cls(rutaMain = ruta_)
		globals()[f'Ventana{identificador}'].show()


	# ------ Refrescar desde base de datos --------------------------------------------------------

	def Importar_(self): # Destinado a editar o eliminar

		''' Extrae la información de la base de datos '''

		if self.Listas.CambiosSinGuardar != []:
			self.ventana_alerta = V_Alerta()
			self.ventana_alerta.ActFun(self.Actualizar_)
			self.ventana_alerta.CambiarMensaje("Hay cambios sin guardar, ¿Deseas continuar y perderlos?")
			self.ventana_alerta.show()
		else:
			self.Actualizar_()

	def Actualizar_(self):
			self.Listas = self.Extraer_()
			self.MensajeUser(f'La base de datos {self.Ruta_Base}/ ha sido cargada')


	#******************************************************************************
	#*		Señales de teclado
	#******************************************************************************

	def keyPressEvent(self,event):
		IndexTab = self.tabWidget.currentIndex()
		NameTab	= self.tabWidget.tabText(IndexTab)

		if event.key() == QtCore.Qt.Key_P and NameTab == "Buscar":
			self.AbrirPDF.animateClick()
		elif event.key() == QtCore.Qt.Key_A and NameTab == "Buscar":
			self.BotonAgregar.animateClick()
		elif event.modifiers() == QtCore.Qt.ControlModifier:
			if event.key() == QtCore.Qt.Key_Tab: # Navegar entre pestañas con CTRL + Tab
				IndexTab += 1
				self.tabWidget.setCurrentIndex(IndexTab)
			elif event.key() == QtCore.Qt.Key_Backtab:
				IndexTab += 1
				self.tabWidget.setCurrentIndex(IndexTab)
		elif event.modifiers() == QtCore.Qt.AltModifier:
			if event.key() == QtCore.Qt.Key_1:
				self.tabWidget.setCurrentIndex(0)
			elif event.key() == QtCore.Qt.Key_2:
				self.tabWidget.setCurrentIndex(1)


	#**************************************************************************
	#* Gestión del evento de cerrado
	#**************************************************************************

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
			self.Guardar_()
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
		self.ListaCoincidencias.itemDoubleClicked.connect(self.buttonBox.accepted)

	#----- Funcion para imprimir las coincidencias y que el usuario elija la requerida ----------------

	def Imprimir(self):

		# Imprime los resultados en pantalla

		for i in self.resultados:
			self.ListaCoincidencias.addItem(i)

	#------Funcion vinculada al botón Ok, para activar la funcion --------------------------------------

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
		if nuevo == "" or nuevo == self.Old:
			return

		self.F(self.d, nuevo)

	def EditarAtributo(self, nombre, old, dato, funcion, op = ""):

		''' Importa datos de la clase principal. Admite el nombre del alumno, el dato a editar y
			la función necesaria para editar en la base de datos: EditarAtributo(nombre ,dato, funcion) '''

		self.NombreAlumno.setText(nombre)
		self.AtributoEditar.setText(dato + ": ")
		self.F = funcion
		self.d = dato
		self.Old = old
		self.EntradaEditar.setText(self.Old)
		self.EntradaEditar.selectAll()

		if op == "" or dato in ["Nombre", "Número de registro"]:
			return

		self.completa = QCompleter(op[dato])
		self.completa.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.EntradaEditar.setCompleter(self.completa)

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

	def ActFun(self, f, f2):
		self.F = f
		self.F2 = f2

		self.buttonBox.accepted.connect(self.Funciones)
		self.buttonBox.rejected.connect(self.NoEleccion)

	def Funciones(self):
		self.F()
		self.F2()

	def NoEleccion(self):
		self.F2()

#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para agregar                                                  -------------|
#|------------------------------------------------------------------------------------------------------|

class V_Agregar(QtWidgets.QDialog, Ui_VentanaAgregar):

	''' Formulario para agregar alumno '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.cuadrosTexto = ({"Nombre": self.a_nombre, "Número de registro": self.a_nregistro,
							 "Carrera": self.a_carrera, "Centro Universitario": self.a_CU,
							 "Curso": self.a_curso, "Plantel": self.a_plantel,
							 "Horario": self.a_horario})

		self.buttonBox.accepted.connect(self.addAlumno)

	def infuncion(self, funcion, op = "n"):
		self.f = funcion

		if op == "n":
			return

		self.completa = dict()
		for i in op:
			self.completa[i] = QCompleter(op[i])
			self.completa[i].setCaseSensitivity(QtCore.Qt.CaseInsensitive)

		paraCompleter = ("Carrera", "Centro Universitario", "Curso", "Plantel", "Horario")

		for tipo in paraCompleter:
			self.cuadrosTexto[tipo].setCompleter(self.completa[tipo])

	def LlenarDatos(self, dicc):

		for i in dicc:
			self.cuadrosTexto[i].setText(dicc[i])



	def addAlumno(self):
		n = self.a_nombre.text().strip()
		nr = self.a_nregistro.text().strip()
		c = self.a_carrera.text().strip()
		cu = self.a_CU.text().strip()
		curso = self.a_curso.text().strip()
		plantel = self.a_plantel.text().strip()
		horario = self.a_horario.text().strip()

		if "" in [n, curso, plantel, horario]:
			return

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

		historial_rutas("Base_datos",base,self.Ruta)
		historial_rutas("Base_PDF",base_pdf,self.Ruta)

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

	def MostrarCambios(self,diccionario, f):
		self.F = f

		lista = []

		for i in diccionario:
			if i not in lista:
				lista.append(i)
			lista += diccionario[i]

		cadena = "\n".join(lista)

		self.MostrarContenido.setText(cadena)

	def si_eleccion(self):
		self.F("Si")

	def no_eleccion(self):
		self.F()


#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para alertar durante el cierre                                -------------|
#|------------------------------------------------------------------------------------------------------|

class V_AgregarCSV(QtWidgets.QDialog, Ui_Ventana_CargarCSV):

	''' Si al cerrar hay cambios sin exportar a la base de datos esta ventana se desplegará '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)
		self.historial_ruta = "./"

		self.headers = "Nombre, Número de registro, carrera, CU\n"

		self.buttonCargarCSV.clicked.connect(self.CargarCSV)
		self.ButtonAgregarAlumnos.clicked.connect(self.AgregarABase)


	def AgregarCVS(self, historial_ruta, f,  f_completador, op="n"):
		self.F = f
		self.F_completador = f_completador
		self.historial_ruta = historial_ruta

		self.entradaLineas.setPlainText(self.headers)

		if op == "n":
			return

		self.completa = dict()
		for i in op:
			self.completa[i] = QCompleter(op[i])
			self.completa[i].setCaseSensitivity(QtCore.Qt.CaseInsensitive)

		self.entrada_Curso.setCompleter(self.completa["Curso"])
		self.entrada_Plantel.setCompleter(self.completa["Plantel"])
		self.entrada_Horario.setCompleter(self.completa["Horario"])

	def CargarCSV(self):
		rutas = extraer_historial(self.historial_ruta)
		cadena = ""

		try:
			ruta = rutas["V_AgregarCSV-CargarCSV"]
		except KeyError:
			ruta = os.path.dirname(self.historial_ruta)

		archivo = QFileDialog.getOpenFileName(self,"Elige el archivo", ruta, "Archivo csv (*.csv)")[0]


		# Falta historial

		if archivo.strip() == "":
			return

		with open(archivo, "r") as entrada:
			for i in entrada:
				cadena += i

		contenido = self.entradaLineas.toPlainText()
		texto = contenido.strip() + "\n" + cadena.strip() + "\n"
		texto = texto.replace(",", ", ")
		texto = texto.split(" ")
		while "" in texto:
			texto.remove("")
		texto = " ".join(texto)
		self.entradaLineas.setPlainText(texto)

		ruta = os.path.dirname(archivo)
		historial_rutas("V_AgregarCSV-CargarCSV", ruta, self.historial_ruta)

	def AgregarABase(self):
		curso = V_AgregarCSV.CrearNombresporDefecto(self.entrada_Curso.text())
		plantel = V_AgregarCSV.CrearNombresporDefecto(self.entrada_Plantel.text())
		horario = V_AgregarCSV.CrearNombresporDefecto(self.entrada_Horario.text())

		datos_curso = [curso, plantel, horario]
		texto = self.entradaLineas.toPlainText()
		texto = texto.replace(self.headers.strip(), "").strip()

		if texto == "":
			return

		archivo = ".archivoCSV.csv"

		with open(archivo, "w") as salida:
			print(texto, file=salida, end="")

		self.F(archivo, datos_curso)
		self.F_completador()
		self.entradaLineas.clear()


	@staticmethod
	def CrearNombresporDefecto(nombre):
		if nombre.strip() == "":
			return "n/a"
		else:
			return nombre.strip()


#|------------------------------------------------------------------------------------------------------|
#|------------------------------------------------------------------------------------------------------|


if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	Ventana = MainWindow()
	Ventana.show()
	app.exec_()
