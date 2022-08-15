# Herramientas externas para el sistema

import os, sys, subprocess
from webbrowser import open_new
import json

def main():

	historial("../.rutas.json")


#*-------------------------------------------------------------------------------------------*
#*------ Funciones especiales----------------------------------------------------------------*
#*-------------------------------------------------------------------------------------------*

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

		for Curso in Cursos:
			ruta2 = ruta1 + "/" + Curso
			Horarios = os.listdir(ruta2)

			for Horario in Horarios:
				ruta3 = ruta2 + "/" + Horario
				horario = Horario.replace(".txt", "")

				Alumnos = open(ruta3,"r")

				for Alumno in Alumnos:
					Alumno = Alumno.strip()
					#print(Alumno)
					nombre,numRegistro,carrera,CU = Alumno.split("&")
					nombre,numRegistro,carrera,CU = nombre.strip(), \
					numRegistro.strip(),carrera.strip(),CU.strip()

					lista.append((nombre,numRegistro,carrera,CU,Curso,Plantel,horario))

				Alumnos.close()

	return lista

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
	entrada = open(ruta_historial, "r")
	dcc = "".join(entrada.readlines())
	entrada.close()

	return json.loads(dcc)

#--------------------------------------------------------------------------------------------

def r_historial(dic, nuevo, ruta):
	aux = extraer_historial(ruta)

	aux[dic] = nuevo
	aux = json.dumps(aux)
	salida = open(ruta, "w")

	print(aux, file=salida)

	salida.close()


if __name__ == "__main__":
	main()
