import random

class Equipo(object):
	"""docstring for Equipo"""

	def __init__(self, nombre, ranking):
		super(Equipo, self).__init__()
		self.nombre = nombre
		self.ranking = int(ranking)
		self.goles = 0
		self.fallidos = 0
	
	def cargar_probabilidades(self):
		probabilidades = self.__porcentajes_ranking()

		self.prob_ganar = probabilidades['ganar']
		self.prob_anotar = probabilidades['anotar']
		self.prob_encajar = probabilidades['encajar']
		self.prob_pase = probabilidades['pase']

	def __porcentajes_ranking(self):
		if 1 <= self.ranking <= 10:
			return {'ganar': 0.75, 'anotar': 0.60, 'encajar': 0.20, 'pase':0.60}
		elif 11 <= self.ranking <= 20:
			return {'ganar': 0.60, 'anotar': 0.50, 'encajar': 0.30, 'pase':0.50}
		elif 21 <= self.ranking <= 30:
			return {'ganar': 0.50, 'anotar': 0.40, 'encajar': 0.40, 'pase':0.40}
		elif 31 <= self.ranking <= 40:
			return {'ganar': 0.40, 'anotar': 0.30, 'encajar': 0.45, 'pase':0.35}
		else:
			return {'ganar': 0.30, 'anotar': 0.25, 'encajar': 0.50, 'pase':0.30}

	def hacer_pases(self):
		exitoso = True
		cont_pase = 0

		while exitoso and cont_pase < 4:
			pase = random.randint(0,100) + (self.prob_pase * 100)

			if pase >= 100:
				cont_pase = cont_pase + 1
			else:
				exitoso = False
				return False

		if cont_pase == 4:
			return True
		
	def shoot(self, prob_encajarB):
		shoot =  random.randint(0,100) + (self.prob_anotar*100) + (prob_encajarB*100)

		if shoot >= 150:
			self.__actualizar_goles()
		else:
			self.__actualizar_remates_fuera()

	def __actualizar_goles(self):
		self.goles = self.goles + 1

	def __actualizar_remates_fuera(self):
		self.fallidos = self.fallidos + 1

	def mostrar_estadisticas(self):
		print("Goles: ", self.goles, "\n Fallidos: ", self.fallidos)

	def probabilidad_encajar(self):
		return self.prob_encajar