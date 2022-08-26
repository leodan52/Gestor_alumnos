# Herramientas externas para el sistema

import os, sys, subprocess
from webbrowser import open_new
import json

def main():

	ruta = "../Cursos"

	print(check_dir(ruta))


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
		Cursos.sort()

		for Curso in Cursos:
			ruta2 = ruta1 + "/" + Curso
			Horarios = os.listdir(ruta2)
			Horarios.sort()

			for Horario in Horarios:
				ruta3 = ruta2 + "/" + Horario
				horario = Horario.replace(".txt", "")

				Alumnos = open(ruta3,"r")

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

				Alumnos.close()

	return lista

#--------------------------------------------------------------------------------------------

def	Errores_Escritura(cadena, mensaje = ""):
	print(f'Error: {mensaje}')
	print(f'\t{cadena}')

#--------------------------------------------------------------------------------------------

def PrepararJSON(cadena):

	# Funcion prueba

	salida = []

	cadena = cadena.replace(" {", "{").replace(", ", ",")
	T,n,m = "\t",0,1

	for i in cadena:
		if i in ["[","{"]:
			n += 1
		elif i in ["]","}"]:
			n -= 1
		if i == f'"':
			m = -m

		if i in [",","[","{"] and m != -1:
			T_ = T*n
			salida.append(f'{i}\n{T_}')
		elif i in ["]","}"]:
			T_ = T*n
			salida.append(f'\n{T_}{i}')
		elif i == ",":
			salida.append(f'{i} ')
		else:
			salida.append(i)

	return "".join(salida)

#--------------------------------------------------------------------------------------------

def Agregar2TXT(ruta,lista):
	try:
		entrada = open(ruta, "r")
		lineas = entrada.readlines()
		entrada.close()
	except FileNotFoundError:
		lineas = []

	salida = open(ruta, "w")

	for i in lineas:
		if i.strip() == "":
			continue
		print(i.rstrip(), file=salida)

	for j in lista:
		print(j, file=salida)

	salida.close()


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
		entrada = open(ruta_historial, "r")
		lineas = entrada.readlines()
		entrada.close()
	except FileNotFoundError:
		salida = open(ruta_historial, "w")
		print("{}",file=salida)
		salida.close()
		lineas = "{}"

	dcc = "".join(lineas)

	return json.loads(dcc)

#--------------------------------------------------------------------------------------------

def Existe_con(ruta,dicc):
	try:
		entrada = open(ruta, "r")
		lineas = entrada.readlines()
		lineas = "".join(lineas)
		entrada.close()
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

		salida = open(ruta, "w")
		print(dicc_in,file=salida)
		salida.close()

#--------------------------------------------------------------------------------------------

def r_historial(dic, nuevo, ruta):
	aux = extraer_historial(ruta)

	aux[dic] = nuevo
	aux = json.dumps(aux)
	salida = open(ruta, "w")

	print(aux, file=salida)

	salida.close()

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

if __name__ == "__main__":
	main()
