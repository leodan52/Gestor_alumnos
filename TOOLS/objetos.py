# Descripcion

from PyQt5.QtWidgets import QTreeWidgetItem

class TreeItem(QTreeWidgetItem):

	def __init__(self, padre, tipo, indice = None):
		super().__init__(padre)

		self.tipo = tipo
		self.indice = indice
		self.ListaAlumnos = []

	def getTipo(self):
		return self.tipo

	def getIndiceAlumno(self):
		return self.indice

	def setListaAlumnos(self, Lista):

		if self.tipo != "horario":
			return self.ListaAlumnos

		for i in Lista:
			i = i.split("&")

			self.ListaAlumnos.append({"nombre": i[0], "indice": int(i[1])})

	def getLista(self):
		return self.ListaAlumnos


	def setSalonDatos(self, lista):
		self.salon = lista

	def getSalonDatos(self):
		return self.salon
