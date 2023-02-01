# Herrammientas para buscar

def buscar(entrada,Lista):
	# La lista es la lista de alumnos, clases de alumnos
	# Entrada es la busqueda ingreada por el usuario

	if entrada.strip() == "exit":
		return "Abortar"

	print()

	entrada = entrada.strip().lower().split(" ")

	n = 0

	coin_totales = dict()
	coin_parciales = dict()

	for alumno in Lista:
		comparar = alumno.comparar_nombre.split(" ")

		indice = 0

		for i in entrada:
			if i in comparar:
				indice += 1

		if indice == len(entrada):
			coin_totales[alumno.nombre] = n
		elif indice > 0:
			coin_parciales[alumno.nombre] = n

		n += 1

	if len(coin_totales) == 0 and len(coin_parciales) != 0:
		print("\tNo se encontraron coincidencias totales con tu búsqueda. Aquí te mostramos algunas parciales.")
		print("\tElige la opcion para continuar:")
		coincidencias = coin_parciales
	elif len(coin_totales) == 1:
		print("\tSe encontró una coicidencia:")
		aux = list(coin_totales.values())[0]

		print("\t\t" + Lista[aux].nombre, sep="")

		opcion = ""

		while opcion not in ["s", "n"]:
			opcion = input("\t¿Desea continuar? (s/n)>> ").strip().lower()

			if opcion not in ["s","n"]:
				print("\tNo se ingresó una opcion válida. Intentelo de nuevo.")

		if opcion == "s":
			return aux
		else:
			return "Abortar"

	elif len(coin_totales) == 0 and len(coin_parciales) == 0:
		print("\tNo se encontraron coincidencias")
		return "Abortar"

	else:
		print("\tSe encontraron varias coincidencias con tu búsqueda. Elige:")
		coincidencias = coin_totales


	Num = list(range(len(coincidencias))) + ["*"]
	opciones = sorted(coincidencias) + ["Abortar"]

	for i in range(len(Num)):
		try:
			print( "\t\t" + str(Num[i]+1) + ") " + opciones[i], sep="")
		except TypeError:
			print( "\t\t" + Num[i] + ") " + opciones[i], sep="")

	opcion = ""

	while opcion not in Num:
		opcion = input("\t\t>>> ").strip()

		try:
			opcion = int(opcion) - 1
		except ValueError:
			pass

		if opcion not in Num:
			print("\tIngrese una opción válida.")

	if opcion == "*":
		return "Abortar"

	return coincidencias[opciones[opcion]]

def buscar_GUI(entrada,Lista):
	# La lista es la lista de alumnos, clases de alumnos
	# Entrada es la busqueda ingreada por el usuario

	if entrada.strip() == "exit":
		return "Abortar"

	entrada = entrada.strip().lower().split(" ")

	n = 0

	coin_totales = dict()
	coin_parciales = dict()

	for alumno in Lista:
		comparar = alumno.comparar_nombre.split(" ")
		nombre_ = alumno.nombre

		indice = 0

		for i in entrada:
			if i in comparar:
				indice += 1

		while nombre_ in dict(coin_totales, **coin_parciales):
			nombre_ += "+"


		if indice == len(entrada):
			coin_totales[nombre_] = n
		elif indice > 0:
			coin_parciales[nombre_] = n

		n += 1

	if len(coin_totales) == 0 and len(coin_parciales) != 0:
		coincidencias = coin_parciales
	elif len(coin_totales) == 1:
		coincidencias = coin_totales
	elif len(coin_totales) == 0 and len(coin_parciales) == 0:
		return []
	else:
		coincidencias = coin_totales


	return coincidencias
