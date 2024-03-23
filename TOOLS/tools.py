# Herramientas externas para el sistema

import os, hashlib, sys
from subprocess import call as sp_call
from webbrowser import open_new
import json, fitz, pickle
from pytesseract import pytesseract
	# necesario
	# sudo apt install tesseract-ocr
	# sudo apt-get install tesseract-ocr-spa
from PIL import Image
from pdf2image import convert_from_path
from unidecode import unidecode
from time import time

def main():

	ruta = "../Cursos"


#*-------------------------------------------------------------------------------------------*
#*------ Funciones especiales----------------------------------------------------------------*
#*-------------------------------------------------------------------------------------------*


def GuardarBinario(objeto, ruta):

	with open(ruta, "wb") as salida:
		pickle.dump(objeto, salida)


def CargarBinario(ruta):

	with open(ruta, "rb") as salida:
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

#--------------------------------------------------------------------------------------------

def Agregar2TXT(ruta,lista): # Prestar atención a que siempre agregue en nueva linea

	with open(ruta, "a") as salida:
		for j in lista:
			print(j, file=salida)

#--------------------------------------------------------------------------------------------

def quitaracentos(cadena):

	cadena = cadena.strip().lower()
	cadena = cadena.replace('ñ', 'XXXX')
	cadena = unidecode(cadena)
	cadena = cadena.replace('XXXX', 'ñ')

	return cadena

#--------------------------------------------------------------------------------------------

def QuitarMEspacios(cadena):
	aux = cadena.strip().split()

	return ' '.join(aux)

#--------------------------------------------------------------------------------------------

def procesar(cadena):
	aux = quitaracentos(cadena)

	return QuitarMEspacios(aux)


#--------------------------------------------------------------------------------------------

def abrete(ruta):

	print(f'Abriendo archivo en: {ruta}')

	if sys.platform == "linux":
		os.system(f'xdg-open "{ruta}" >/dev/null 2>&1 &')
	elif sys.platform == "win32":
		os.startfile(f'"{ruta}"')
	elif sys.platform == "darwin":
		sp_call(('open', ruta))
	else:
		open_new(ruta)

#--------------------------------------------------------------------------------------------

def extraer_historial(ruta_historial):
	try:
		with open(ruta_historial, "r") as entrada:
			lineas = entrada.read()
	except FileNotFoundError:
		with open(ruta_historial, "w") as salida:
			print("{}",file=salida)
		lineas = "{}"

	return json.loads(lineas)

#--------------------------------------------------------------------------------------------

def Existe_con(ruta,dicc):
	try:
		with open(ruta, "r") as entrada:
			lineas = entrada.read()
	except FileNotFoundError:
		lineas = "{}"

	dicc_in = json.loads(lineas)
	aux = 0

	for i in dicc:
		if i not in dicc_in:
			dicc_in[i] = dicc[i]
			aux += 1
		elif dicc_in[i].strip():
			dicc_in[i] = dicc[i]
			aux += 1

	if aux != 0:
		dicc_in = json.dumps(dicc_in, ensure_ascii = False, indent = 4)

		with open(ruta, "w") as salida:
			print(dicc_in, file=salida)

#--------------------------------------------------------------------------------------------

def historial_rutas(dic, nuevo, ruta):
	aux = extraer_historial(ruta)

	aux[dic] = nuevo
	aux = json.dumps(aux, ensure_ascii = False, indent = 4)

	with open(ruta, "w") as salida:
		print(aux, file=salida)

#------------------------------------------------------------------------------------------------------------

def PDF2Cadena(ruta):
	hashes_file = '.hashes_pdf'

	try:
		hashes = CargarBinario(hashes_file)
	except FileNotFoundError:
		hashes = dict()

	hash = calculate_hash_file(ruta)

	if ruta in hashes:
		if hashes[ruta][0] == hash:
			if hashes[ruta][2] == 1:
				print(f'PDF imagen se obtiene de \'{hashes_file}\': \'{ruta}\'. ')
			return hashes[ruta][1]
		else:
			print('El archivo {ruta} ha sido modificado')

	PDF = ProcesarTextPDF(ruta).split(" ")

	if len(PDF) == 1 and not PDF[0].strip():
		PDF = Image2texto(ruta)
		tipo = 1
	else:
		PDF = ' '.join(PDF)
		tipo = 0

	hashes[ruta] = [hash, PDF, tipo]

	GuardarBinario(hashes, hashes_file)

	return PDF


def calculate_hash_file(ruta):
	hasher = hashlib.sha512()
	with open(ruta, 'rb') as file_:
		b = file_.read()
		hasher.update(b)

	return hasher.hexdigest()

#------------------------------------------------------------------------------------------------------------

def BuscarEnCadena(cadena1, lista):
	Palabras = cadena1.split()
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
		if i in lista2cadena:
			m += 1

	porc = 100*m/n

	return porc

#------------------------------------------------------------------------------------------------------------

def ProcesarTextPDF(ruta):

	salida = ExtraerTextPDF(ruta).lower()
	salida = salida.split()

	return ' '.join(salida)

#------------------------------------------------------------------------------------------------------------

def ExtraerTextPDF(ruta):

	with fitz.open(ruta) as doc:
		text = ""

		for page in doc:
			text_ = page.get_text()
			#text += text_.replace('�','').strip()
			text += quitaracentos(text_).strip() # Experimento

	return text

#------------------------------------------------------------------------------------------------------------

def ChecarDictamen(lista):

	check = []

	for i in lista:
		check.append(i[-1] != "No data")

	if not any(check):
		for i in lista:
			i.pop(-1)

	return any(check)

#*-------------------------------------------------------------------------------------------*
#*------ Decoradores         ----------------------------------------------------------------*
#*-------------------------------------------------------------------------------------------*

def MensajeClase(funcion):
	def infuncion(clase, *args, **kwargs):
		original_stdout = sys.stdout
		class TabbedStdout:
			def write(self, text):
				original_stdout.write('\t' + text)

		print(f'\n<Iniciando: Mensaje de clase \'{clase.__class__.__name__}\': Ejecutando \'{funcion.__name__}\'>')

		sys.stdout = TabbedStdout()

		r = funcion(clase, *args, **kwargs)

		sys.stdout = original_stdout

		print(f'\n<Finalizado \'{funcion.__name__}\'>\n')

		return r
	return infuncion

def TiempoEjecucion(funcion):
	def infuncion(*args, **kwargs):
		inicio = time()
		r = funcion(*args, **kwargs)
		fin = time()

		print(f'Hecho en {fin - inicio} segundos')

		return r
	return infuncion



if __name__ == "__main__":
	main()
