# Herramientas externas para el sistema

import os, sys, subprocess
from webbrowser import open_new
import json, fitz, pickle
from pytesseract import pytesseract
	# necesario
	# sudo apt install tesseract-ocr
	# sudo apt-get install tesseract-ocr-spa
from PIL import Image
from pdf2image import convert_from_path

def main():

	ruta = "../Cursos"

	print(check_dir(ruta))


#*-------------------------------------------------------------------------------------------*
#*------ Funciones especiales----------------------------------------------------------------*
#*-------------------------------------------------------------------------------------------*


def GuardarBinario(objeto, ruta, nombreBase):

	with open(f'{ruta}{nombreBase}', "wb") as salida:
		pickle.dump(objeto, salida)

def CargarBinario(ruta, nombreBase):
	with open(f'{ruta}{nombreBase}', "rb") as salida:
		objeto = pickle.load(salida)

	return objeto


def Image2texto(ruta):
	Im_ruta = ruta.replace("pdf", "png")
	Im_ruta = os.path.basename(Im_ruta)

	try:
		os.mkdir(".Imagenes_temp")
	except FileExistsError:
		pass

	try:
		Im = Image.open(f'.Imagenes_temp/{Im_ruta}')
	except FileNotFoundError:
		PDF = convert_from_path(ruta)
		for i in PDF:
			i.save(f'.Imagenes_temp/{Im_ruta}', "PNG", dpi=(300, 300))
		Im = Image.open(f'.Imagenes_temp/{Im_ruta}')

	print(f'Escaneando en imagen "{ruta}"')

	configurar = "-l spa --psm 11"
	text = pytesseract.image_to_string(Im, config=configurar).replace("\n", " ")
	text = QuitarMEspacios(text).lower().strip()

	if text == "":
		print(f'\tFalló escaneo en "{ruta}"')

	Im.close() # Veamos como funciona

	return text


def extraer(ruta):
	# Funcion que recolecta a los alumnos dentro de la carpeta Cursos
	# y devuelve una lista con las tuplas de los datos de cada alumno

	try:
		Planteles = os.listdir(ruta)
	except FileNotFoundError:
		os.mkdir(ruta)
		Planteles = os.listdir(ruta)


	lista = []

	for Plantel in Planteles:
		ruta1 = ruta + "/" + Plantel
		Cursos = os.listdir(ruta1)
		Cursos.sort()

		for Curso in Cursos:
			ruta2 = ruta1 + "/" + Curso
			Horarios = os.listdir(ruta2)
			Horarios.sort()

			for Horario in Horarios:
				ruta3 = ruta2 + "/" + Horario
				horario = Horario.replace(".txt", "")

				with open(ruta3,"r") as Alumnos:

					for Alumno in Alumnos:
						Alumno = Alumno.strip()
						#print(Alumno)
						try:
							nombre,numRegistro,carrera,CU = Alumno.split("&")
						except ValueError:
							mensaje = f'En {Plantel}/{Curso}/{Horario}. La linea debe tener 4 datos separados por &'
							Errores_Escritura(Alumno, mensaje)
							continue
						nombre,numRegistro,carrera,CU = nombre.strip(), \
						numRegistro.strip(),carrera.strip(),CU.strip()

						lista.append((nombre,numRegistro,carrera,CU,Curso,Plantel,horario))

	return lista

#--------------------------------------------------------------------------------------------

def	Errores_Escritura(cadena, mensaje = ""):
	print(f'Error: {mensaje}')
	print(f'\t{cadena}')

#--------------------------------------------------------------------------------------------

def PrepararJSON(cadena, cadena_not = False):

	# Funcion prueba

	if cadena_not:
		cadena = json.dumps(cadena,ensure_ascii=False)


	salida = []

	cadena = cadena.replace(", ", ",")
	for ii in ["{", "[", "("]:
		cadena = cadena.replace(f' {ii}', ii)
		cadena = cadena.replace(f'{ii} ', ii)
	T,n,m = "\t",0,1

	for i in cadena:
		if i in ["[","{"]:
			n += 1
		elif i in ["]","}"]:
			n -= 1
		if i == f'"':
			m = -m

		if i in [",","[","{","("] and m != -1:
			T_ = T*n
			if i not in [","]:
				T_a = "\n" + T*(n-1)
			else:
				T_a = ""
			salida.append(f'{T_a}{i}\n{T_}')
		elif i in ["]","}"]:
			T_ = T*n
			salida.append(f'\n{T_}{i}')
		elif i in [","]:
			salida.append(f'{i} ')
		else:
			salida.append(i)

	aux = "".join(salida)
	salida = []

	for i in aux.split("\n"):
		i = i.rstrip()
		if i == "":
			continue
		salida.append(i)

	return "\n".join(salida)

def Entrada4JSON(lista):

	lineas = "".join(lista)
	lineas = lineas.replace("\t","")
	lineas = lineas.replace("\n","")

	return json.loads(lineas)


#--------------------------------------------------------------------------------------------

def Agregar2TXT(ruta,lista):
	try:
		with open(ruta, "r") as entrada:
			lineas = entrada.readlines()
	except FileNotFoundError:
		lineas = []

	with open(ruta, "w") as salida:

		for i in lineas:
			if i.strip() == "":
				continue
			print(i.rstrip(), file=salida)

		for j in lista:
			print(j, file=salida)



#--------------------------------------------------------------------------------------------

def quitaracentos(cadena):
	cadena = cadena.strip().lower()
	acentos = [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u")]

	for i in acentos:
		cadena = cadena.replace(*i)

	return cadena

#--------------------------------------------------------------------------------------------

def QuitarMEspacios(cadena):
	aux = cadena.strip().split(" ")
	aux2 = []

	for i in aux:
		i = i.strip()

		if i == "":
			continue

		aux2.append(i)

	return " ".join(aux2)

#--------------------------------------------------------------------------------------------

def procesar(cadena):
	aux = quitaracentos(cadena)

	return QuitarMEspacios(aux)


#--------------------------------------------------------------------------------------------

def Abrete(ruta):

	if sys.platform == "linux":
		try:
			os.system(f'xdg-open "./{ruta}" >/dev/null 2>&1 &')
		except:
			subprocess.call(('xdg-open', ruta))
	elif sys.platform == "win32":
		os.startfile(f'"{ruta}"')
	elif sys.platform == "darwin":
		subprocess.call(('open', ruta))
	else:
		open_new(ruta)

#--------------------------------------------------------------------------------------------

def extraer_historial(ruta_historial):
	try:
		with open(ruta_historial, "r") as entrada:
			lineas = entrada.readlines()
	except FileNotFoundError:
		with open(ruta_historial, "w") as salida:
			print("{}",file=salida)
		lineas = "{}"
	dcc = "".join(lineas)

	return json.loads(dcc)

#--------------------------------------------------------------------------------------------

def Existe_con(ruta,dicc):
	try:
		with open(ruta, "r") as entrada:
			lineas = entrada.readlines()
			lineas = "".join(lineas)
	except FileNotFoundError:
		lineas = "{}"

	dicc_in = json.loads(lineas)
	aux = 0

	for i in dicc:
		if i not in dicc_in:
			dicc_in[i] = dicc[i]
			aux += 1
		elif dicc_in[i].strip() == "":
			dicc_in[i] = dicc[i]
			aux += 1

	if aux != 0:
		dicc_in = json.dumps(dicc_in)

		with open(ruta, "w") as salida:
			print(dicc_in,file=salida)

#--------------------------------------------------------------------------------------------

def r_historial(dic, nuevo, ruta):
	aux = extraer_historial(ruta)

	aux[dic] = nuevo
	aux = json.dumps(aux)

	with open(ruta, "w") as salida:
		print(aux, file=salida)

#------------------------------------------------------------------------------------------------------------

def mensaje_print(cadena):
	print(cadena)
#------------------------------------------------------------------------------------------------------------

def check_dir(ruta, f_m = mensaje_print):

	n = len(ruta.split("/"))
	max_size = 10**6

	for root,dirs,files in os.walk(ruta):
		m = len(root.split("/"))

		if (m == n or m == n+1) and len(files) != 0:
			f_m(f'Ruta inválida para usar.\n{ruta} muestra archivos en el primer nivel.\nSolo debe haber directorios')
			return False
		if m == n + 2 and len(dirs) != 0:
			f_m(f'Ruta inválida para usar.\n{ruta} muestra carpetas en el segundo nivel.\nSolo debe haber archivos TXT')
			return False
		elif m == n + 2:
			for i in files:
				if os.path.splitext(i)[1] != ".txt":
					f_m(f'El archivo {i} en {root} no es un TXT.\nRuta inválida')
					return False

				tama = os.path.getsize(f'{root}/{i}')
				if tama >= max_size:
					f_m(f'El archivo {i} en {root} es un archivo de 1 mb o más.\nCorre el peligro de perderse.\nRuta inválida.')
					return False

	return True


def comparar_C(antiguo,nuevo):

	set_old = set(antiguo)
	set_new = set(nuevo)

	eli = set_old - set_new
	agr = set_new - set_old

	return list(eli), list(agr)


def Inter_C(C1,C2):
	return set(C1) & set(C2)


def Extraer2TXT(ruta):
	Lista = []
	with open(ruta, "r") as salida:
		for i in salida:
			i = i.strip()
			if i == "":
				continue
			Lista.append(i)
	return Lista


def PDF2Cadena(ruta):
	PDF = ProcesarTextPDf(ruta).split(" ")
#	palab = cadena.split(" ")
#	m = 0
#	n = len(palab)

	if len(PDF) == 1 and PDF[0].strip() == "":
		PDF = Image2texto(ruta).split(" ")
		#return 101

#	for i in palab:
#		if i in PDF:
#			m += 1

#	return 100*m/n
	return PDF

def BuscarEnCadena(cadena1, lista):
	Palabras = cadena1.split(" ")
	m = 0
	n = len(Palabras)

	for i in Palabras:
		if i in lista:
			m += 1

	porc = 100*m/n

	if porc != 0:
		return porc
	else:
		lista2cadena = "".join(lista)
		m = 0

	for i in Palabras:
		if lista2cadena.find(i) != -1:
			m += 1

	porc = 100*m/n

	return porc

def ProcesarTextPDf(ruta):

	aux = ExtraerTextPDF(ruta)
	aux = aux.replace("\n", " ").lower()
	aux_ = aux.split(" ")
	aux = []

	for i in aux_:
		i = i.strip()
		if i == "":
			continue
		aux.append(i)

	aux = " ".join(aux)

	return aux

def ExtraerTextPDF(ruta):

	with fitz.open(ruta) as doc:
		lista = []
		text = ""

		for page in doc:
			text_ = page.get_text()
			text += text_.replace('�','').strip()

	return text

def ChecarDictamen(lista):

	check = []

	for i in lista:
		check.append(i[-1] != "No data")

	if not any(check):
		for i in lista:
			i.pop(-1)

	return any(check)

if __name__ == "__main__":
	main()
