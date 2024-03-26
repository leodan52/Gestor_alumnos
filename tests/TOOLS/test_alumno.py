import pytest
from unidecode import unidecode
from random import choice
from TOOLS.alumno import Alumno

@pytest.fixture
def alumno_1():

	a_dict = {
            "Nombre": "Potter Harry",
            "Número de registro": "01234567",
            "Carrera": "Ing. Magica",
            "Centro Universitario": "CUVV",
            "Curso": "Curso para magos",
            "Plantel": "Calzada",
            "Horario": "09-13hrs"
        }

	salida = Alumno(a_dict['Nombre'], a_dict["Número de registro"],
			a_dict['Carrera'], a_dict['Centro Universitario'], a_dict['Curso'],
			a_dict['Plantel'], a_dict['Horario'])

	return salida, a_dict

@pytest.fixture
def alumno_2():

	a_dict = {
            "Nombre": "Muciño Dealmonte, Aki Arisbéth",
            "Número de registro": "0661464",
            "Carrera": "Lic. en Mercadotecnia",
            "Centro Universitario": "CUCBA",
            "Curso": "Master - Elite",
            "Plantel": "Calzada",
            "Horario": "19-21hrs",
        }

	salida = Alumno(a_dict['Nombre'], a_dict["Número de registro"],
			a_dict['Carrera'], a_dict['Centro Universitario'], a_dict['Curso'],
			a_dict['Plantel'], a_dict['Horario'])

	return salida, a_dict

@pytest.mark.parametrize(
		'fixture',
		[
			('alumno_1'),
			('alumno_2')
		]
	)
class TestAlumno:

	def test_properties(self, fixture, request):
		alumno, dicc = request.getfixturevalue(fixture)

		assert alumno.nombre == dicc['Nombre']
		assert alumno.nRegistro == dicc['Número de registro']
		assert alumno.carrera == dicc['Carrera']
		assert alumno.CU == dicc['Centro Universitario']
		assert alumno.curso == dicc['Curso']
		assert alumno.plantel == dicc['Plantel']
		assert alumno.horario == dicc['Horario']

	def test_properties_2(self, fixture, request):
		alumno, dicc = request.getfixturevalue(fixture)

		nombre_comparar = dicc['Nombre'].lower()
		nombre_comparar = nombre_comparar.replace('ñ', 'NNNN')
		nombre_comparar = unidecode(nombre_comparar)
		nombre_comparar = nombre_comparar.replace('NNNN', 'ñ')
		while '  ' in nombre_comparar:
			nombre_comparar = nombre_comparar.replace('  ', ' ')

		dicc.update({"¿PDF entregado?" : 'No data', "¿Admitido?" : 'No data'})

		print(dicc)

		assert alumno.comparar_nombre == nombre_comparar
		assert alumno.DatosSalon == (
			[
				dicc['Plantel'],
				dicc['Curso'],
				dicc['Horario']
			]
		)
		assert alumno.DatosUDG == (
			[
				dicc['Nombre'],
				dicc['Número de registro'],
				dicc['Carrera'],
				dicc['Centro Universitario']
			]
		)
		dicc2 = dicc.copy()
		dicc2.pop("¿Admitido?")
		assert alumno.datos == dicc2
		dicc3 = dicc.copy()
		dicc3.pop('¿PDF entregado?')
		assert alumno.datos_json == dicc3

	def test_ActualizarDato(self, fixture, request):
		alumno, _ = request.getfixturevalue(fixture)

		nuevo_nombre = choice(
			[
				'Samperio Tecpa, Jesus Emilio',
				'Barro Tellez Giron, Luis Axel',
				'Neaves Michan, Tadao Ryoichi'
			]
		)

		nuevo_nRegistro = '12314212'
		nuevo_otro = '1231231'

		check1 = alumno.ActualizarDato('Nombre', nuevo_nombre)
		check2 = alumno.ActualizarDato('Número de registro', nuevo_nRegistro)
		check3 = alumno.ActualizarDato('NoExistAttribute', nuevo_otro)

		assert [check1, check2, check3] == [1, 1, 0]
		assert alumno.nombre == nuevo_nombre
		assert alumno.nRegistro == nuevo_nRegistro