# Gestor de Cursos

from TOOLS.alumno import *

def main():

	alumnos = extraer("./Cursos")

	L = []

	for alumno in alumnos:
		L.append(Alumno(*alumno))

	Listas = TodosMisAlumnos(L,"./Cursos_pdf","./Cursos")

	opcion = "I"

	while opcion != "*":

		opcion = "I"

		print('''¿Qué acción desea hacer?
a) Organizar PDF de número de registro
b) Generar lista completa
c) Editar datos de un alumno
d) Buscar alumno
e) Abrir PDF
*) Salir
	''')

		opciones = ["a","b","c","d","e","f","*"]

		while opcion not in opciones or opcion == "I":
			opcion = input("Opcion>>> ").strip().lower()

			if opcion not in opciones:
				print("Entrada inválida.Intente de nuevo")


		if opcion == "a":
			Listas.organizarPDF()
		elif opcion == "b":
			Listas.GenerarListas()
		elif opcion == "*":
			print("\nAdiosito\n")
		elif opcion == "c":
			Listas.EditarDatosAlumnos()
		elif opcion == "d":
			Listas.BuscarAlumno()
		elif opcion == "e":
			Listas.AbrirPDFmenu()

main()
