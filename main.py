# Descripcion

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
import time, csv


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
		self.Ruta_Base = "Ruta de la base"
		self.Ruta_PDF = "Ruta de los PDFs"
		self.PalabrasClaves = "Coincidencias de búsqueda para cuadro"
		self.indice = None
		self.PDF_disponible = "No Data"

		self.arbolPlantel = []
		self.arbolCurso = []
		self.arbolHorario = []

		self.Necesario_files()
		self.Set_RutasBases()

		self.Listas = self.Extraer_()
		GuardarBinario(self.Listas, "./", "Binario")

		self.MensajeUser(f'Bienvenido. El fichero {self.Ruta_Base}/ ha sido cargado')

		self.ActualizarCom()

		self.actionImportar.triggered.connect(self.Importar_)
		self.actionExportar.triggered.connect(self.Exportar_)
		self.actionGenerar_lista.triggered.connect(self.GenerarListas_)
		self.actionImportar_JSON.triggered.connect(self.ImportarJSON)
		self.actionExportar_JSON.triggered.connect(self.ExportarJSON)
		self.actionImportacion_masiva.triggered.connect(self.ImportarMasivo)

		self.actionOrganizar_PDFs.triggered.connect(self.Org_PDFs_)
		self.actionEscanear_PDF.triggered.connect(self.Scan_PDFs_)
		self.actionEditar_directorios.triggered.connect(self.Editar_Dir)
		self.actionConfirmar_admision.triggered.connect(self.BuscarAdmitidos)

		self.BotonBuscar.clicked.connect(self.Buscar)
		self.BotonAgregar.clicked.connect(self.AgregarBoton)
		self.buttonActualizarInfo.clicked.connect(self.ActualizarDespliegue)
		self.BotonEditar.clicked.connect(self.EditarBoton)
		self.AbrirPDF.clicked.connect(self.AbrirPDFBoton)
		self.BotonEliminar.clicked.connect(self.EliminarAlumno)

		self.buttonActualizarArbol.clicked.connect(self.EscribirArbol)
		self.buttonEliminarTabListas.clicked.connect(self.EliminardesdeArbol)
		self.buttonGuardarCSV.clicked.connect(self.GuardarListaArchivo)
		self.buttonAgregarTabListas.clicked.connect(self.AgregarASalon)

		self.CuadroBuscar.returnPressed.connect(self.BotonBuscar.animateClick)

		self.BotonesDes()


	#------- Exportar los arlumnos desde la base de datos-------------------------------------------

	def Extraer_(self):

		''' Extraemos los alumnos del directorio elegido. Estos se reparten en de archivos TXT mediante
			el siguiente árbol: ./base_de_datos/PLANTEL/NOMBRE_CURSO/HORARIO.txt '''

		alumnos = extraer(self.Ruta_Base)

		L = []

		for alumno in alumnos:
			L.append(Alumno(*alumno))

		return TodosMisAlumnos(L, self.Ruta_PDF, self.Ruta_Base)

	#........ Actualizar completador -----------------------------------------------------------------

	def ActualizarCom(self):
		self.PalabrasClaves = QCompleter(self.Listas.ClavesBusqueda)
		self.PalabrasClaves.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.CuadroBuscar.setCompleter(self.PalabrasClaves)

	#--------Habilitar botones o deshabilitar segun sean necesarios o no -----------------------------

	def BotonesDes(self):
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
		if self.Mostrar.count() != 0:
			self.BotonEditar.setEnabled(True)
			self.BotonEliminar.setEnabled(True)
			self.buttonActualizarInfo.setEnabled(True)

#		self.Mostrar.itemDoubleClicked.connect(self.BotonEditar.animateClick)
		self.Mostrar.itemActivated.connect(self.BotonEditar.animateClick)

		if self.PDF_disponible == "Sí":
			self.AbrirPDF.setEnabled(True)
		else:
			self.AbrirPDF.setEnabled(False)
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

		if archivo.strip() == "":
			return

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

	#--- Importación masiva -------------------------------------------------------------------------

	def ImportarMasivo(self):

		''' Despliega ventana para importación masiva '''

		self.VentanaAgregarCSV = V_AgregarCSV()
		self.VentanaAgregarCSV.AgregarCVS(self.Listas.ImportarCSV, self.Listas.Data)
		self.VentanaAgregarCSV.show()

	#------- Organizar PDF -------------------------------------------------------------------------

	def Org_PDFs_(self):

		'''	Utiliza método de TodosMisAlumnos para organizar los PDFs que los alumnos proporcionan
			como respaldo al número de registro '''

		self.Listas.organizarPDF(False)

		self.MensajeUser(f'Los archivos PDF han sido organizados en {self.Ruta_PDF}/')

	#-.----- Escanear PDFs--------------------------------------------------------------------------

	def Scan_PDFs_(self):
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

	# ------ Refrescar desde base de datos --------------------------------------------------------

	def Importar_(self):

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

	# -----------Cargar PDF con dictamen y buscar admitidos ----------------------------------------

	def BuscarAdmitidos(self):

		''' Cuando el dictamen UDG de admitidos sea publicado, se puede usar el PDF para buscar
			si los alumnos del curso fueron admitidos '''
		try:
			ruta = extraer_historial(self.Ruta_Historial)["Dictamen"]
		except KeyError:
			ruta = "./"

		archivo = QFileDialog.getOpenFileName(self,"Elige el PDF que contiene el dictamen", ruta, "Archivo PDF (*.pdf)")[0]

		self.Listas.LeerDictamen(archivo)
		self.MensajeUser(f'Un total de {self.Listas.num_Admitidos} fueron admitidos.')

		ruta = os.path.dirname(archivo)
		r_historial("Dictamen", ruta, self.Ruta_Historial)

	# ------- Filtro de señales de teclado -----------------------------------------------------------

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

		self.PDF_disponible = datos["¿PDF entregado?"]

		for i in datos:							# Imprimimos los datos
			self.Mostrar.addItem(i + ": " + datos[i]  )

		self.MensajeUser("Datos del alumno:")
		self.BotonesOn()

	# ------- Función para botón actualizar para mirar datos de alumno -----------------------------

	def ActualizarDespliegue(self):

		''' Actualiza los datos de alumno mostrados en pantalla para cuando los datos cambien '''

		self.Desplegar_alumnos(self.indice)


	#------ Funcion para agregar alumno --------------------------------------------------------

	def AgregarBoton(self):

		''' Despliega ventana formulario para agregar alumno y sus datos '''

		self.V_Add = V_Agregar()
		self.V_Add.infuncion(self.Agregar_2, self.Listas.Data)
		self.V_Add.show()

	def Agregar_2(self,lista):
		self.Listas.AddAlumno(lista)
		self.ActualizarCom()

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
		self.Listas.MotorEditar_GUI(self.indice, dato, nuevo)
		self.Desplegar_alumnos(self.indice)
		self.ActualizarCom()

	#----- Funcion eliminar alumno --------------------------------------------------------------

	def EliminarAlumno(self, f = lambda x = None: x):

		nombre = self.Listas.lista[self.indice].nombre

		self.Alerta = V_Alerta()
		self.Alerta.CambiarMensaje(f'¿Estás seguro de borrar al alumno {nombre}?')
		self.Alerta.ActFun(self.Eliminar_, f)
		self.Alerta.show()

	def Eliminar_(self):
		self.Listas.RmAlumno(self.indice)
		self.indice = None

		self.Mostrar.clear()
		self.BotonesDes()

	#----- General arbol para pestaña listas ---------------------------------------------------------

	def EscribirArbol(self):

		arbol = self.Listas.getArbol()

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

		self.ArbolListas.itemActivated.connect(self.ImprimirdeArbol)

	def ImprimirdeArbol(self):
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


		self.MostrarListas.itemActivated.connect(self.MostrarDatosdTabListas)

	# ---- Funcions para botones de la pestaña Listas -------------------------------------------------


	def MostrarDatosdTabListas(self):

		numLista = self.MostrarListas.currentRow()
		indice = self.aulaLista[numLista]["indice"]

		self.tabWidget.setCurrentIndex(0)

		self.Desplegar_alumnos(indice)

	def EliminardesdeArbol(self):
		numLista = self.MostrarListas.currentRow()

		self.MostrarDatosdTabListas()

		self.EliminarAlumno(lambda x = numLista: self.RegresarATabYEliminar(x))

	def RegresarATabYEliminar(self, row):

		self.tabWidget.setCurrentIndex(1)

		if self.indice == None:
			self.MostrarListas.takeItem(row)

	def GuardarListaArchivo(self):

		historial_rutas =extraer_historial(self.Ruta_Historial)

		try:
			ruta = historial_rutas["GuardaSalonArchivo"]
		except KeyError:
			ruta = "."

		datosCurso ="_".join(self.aulaDatos)

		OpenFile = QFileDialog.getSaveFileName(self,"Elige el archivo",
												 f'.{ruta}{datosCurso}.csv;;./{datosCurso}.json',
												 "Archivo CSV (*.csv);;Archivo JSON (*.json)")
		archivo = OpenFile[0]

		if archivo == "":
			return

		path_archivo = os.path.dirname(archivo)
		r_historial("GuardaSalonArchivo", path_archivo, self.Ruta_Historial)

		indices = []

		for i in self.aulaLista:
			indices.append(i["indice"])


		if OpenFile[1].startswith("Archivo CSV"):
			self.Listas.ExportarCSV(archivo, *indices)
		else:
			self.Listas.ExportarAulaJSON(archivo, *indices)

	def AgregarASalon(self):

		datos_key = ["Plantel", "Curso", "Horario"]
		datos = {d: cadena for d, cadena in zip(datos_key, self.aulaDatos)}


		self.V_Add = V_Agregar()
		self.V_Add.infuncion(self.Agregar_2, self.Listas.Data)
		self.V_Add.LlenarDatos(datos)
		self.V_Add.show()



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
			self.Listas.Control_version()
			self.Listas.Cambios_base(cargar = True)
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
		self.buttonBox.rejected.connect(self.F2)

	def Funciones(self):
		self.F()
		self.F2()

#|------------------------------------------------------------------------------------------------------|
#|------       Clase ventana para agregar                                                  -------------|
#|------------------------------------------------------------------------------------------------------|

class V_Agregar(QtWidgets.QDialog, Ui_VentanaAgregar):

	''' Formulario para agregar alumno '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.buttonBox.accepted.connect(self.addAlumno)

	def infuncion(self, funcion, op = "n"):
		self.f = funcion

		if op == "n":
			return

		self.completa = dict()
		for i in op:
			self.completa[i] = QCompleter(op[i])
			self.completa[i].setCaseSensitivity(QtCore.Qt.CaseInsensitive)

		self.a_carrera.setCompleter(self.completa["Carrera"])
		self.a_CU.setCompleter(self.completa["Centro Universitario"])
		self.a_curso.setCompleter(self.completa["Curso"])
		self.a_plantel.setCompleter(self.completa["Plantel"])
		self.a_horario.setCompleter(self.completa["Horario"])

		self.cuadrosTexto = ({"Nombre": self.a_nombre, "Número de registro": self.a_nregistro,
							 "Carrera": self.a_carrera, "Centro Universitario": self.a_CU,
							 "Curso": self.a_curso, "Plantel": self.a_plantel,
							 "Horario": self.a_horario})

	def LlenarDatos(self, dicc):

		for i in dicc:
			self.cuadrosTexto[i].setText(dicc[i])


#		for i in dicc:
#			if i == "Plantel":
#				self.a_plantel.setText(dicc[i])
#			elif i == "Curso":
#				self.a_curso.setText(dicc[i])
#			elif i == "Horario":
#				self.a_horario.setText(dicc[i])


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
#|------       Clase ventana para alertar durante el cierre                                -------------|
#|------------------------------------------------------------------------------------------------------|

class V_AgregarCSV(QtWidgets.QDialog, Ui_Ventana_CargarCSV):

	''' Si al cerrar hay cambios sin exportar a la base de datos esta ventana se desplegará '''

	def __init__(self, *args, **kwargs):
		QtWidgets.QDialog.__init__(self, *args, **kwargs)
		self.setupUi(self)

		self.headers = "Nombre, Número de registro, carrera, CU\n"

		self.buttonCargarCSV.clicked.connect(self.CargarCSV)
		self.ButtonAgregarAlumnos.clicked.connect(self.AgregarABase)


	def AgregarCVS(self, f, op="n"):
		self.F = f

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

		archivo = QFileDialog.getOpenFileName(self,"Elige el archivo", "./", "Archivo csv (*.csv)")[0]
		cadena = ""

		# Falta historial

		if archivo.strip() == "":
			return

		with open(archivo, "r") as entrada:
			for i in entrada:
				cadena += i

		contenido = self.entradaLineas.toPlainText()

		self.entradaLineas.setPlainText(contenido.strip() + "\n" + cadena.strip() + "\n")

	def AgregarABase(self):
		curso = V_AgregarCSV.CrearNombresporDefecto(self.entrada_Curso.text())
		plantel = V_AgregarCSV.CrearNombresporDefecto(self.entrada_Plantel.text())
		horario = V_AgregarCSV.CrearNombresporDefecto(self.entrada_Horario.text())

		datos_curso = [curso, plantel, horario]
		texto = self.entradaLineas.toPlainText().strip().replace(self.headers, "")
		archivo = ".archivoCSV.csv"

		with open(archivo, "w") as salida:
			print(texto, file=salida, end="")

		self.F(archivo, datos_curso)
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
