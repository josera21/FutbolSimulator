import time
import random
import progressbar
from equipo import Equipo

def valid_ranking(ranking):
	"""Si el ranking esta bien colocado, lo retorno, si no obligo a que lo coloquen bien"""
	if ranking.isdigit() and 1 <= int(ranking) < 100:
		return ranking
	else:
		while not(ranking.isdigit() and 1 <= int(ranking) < 100):
			print("Por favor introduce un numero valido.")
			ranking = input("Ranking (numero del 1-100): ")
		return ranking

def porcenajes_ranking(ranking):
	"""Verifico en que rango esta el ranking para retornar las probabilidades indicadas"""
	ranking = int(ranking)

	if 1 <= ranking <= 10:
		return {'ganar': 0.75, 'anotar': 0.60, 'encajar': 0.20, 'pase':0.60}
	elif 11 <= ranking <= 20:
		return {'ganar': 0.60, 'anotar': 0.50, 'encajar': 0.30, 'pase':0.50}
	elif 21 <= ranking <= 30:
		return {'ganar': 0.50, 'anotar': 0.40, 'encajar': 0.40, 'pase':0.40}
	elif 31 <= ranking <= 40:
		return {'ganar': 0.40, 'anotar': 0.30, 'encajar': 0.45, 'pase':0.35}
	else:
		return {'ganar': 0.30, 'anotar': 0.25, 'encajar': 0.50, 'pase':0.30}

def cargar_informacion():
	global equipoA, equipoB, ranking_eqA, ranking_eqB, fecha, hora

	print("## Ingrese la informacion del partido ##")

	equipoA = input("Nombre del equipo local: ")
	ranking_eqA = valid_ranking(input("Ranking (numero del 1-100): "))

	equipoB = input("Nombre del equipo visitante: ")
	ranking_eqB = valid_ranking(input("Ranking (numero del 1-100): "))

	fecha = input("Fecha del partido: ")
	hora = input("Hora del partido: ")

def jugar(Equipo1, Equipo2):
	prob_encajar_eq1 = Equipo1.probabilidad_encajar()
	prob_encajar_eq2 = Equipo2.probabilidad_encajar()

	starttime=time.time()
	tiempo = 0
	# creo la barra de progreso
	bar = progressbar.ProgressBar(widgets=[
        progressbar.Percentage(),
        progressbar.Bar(),
    ], max_value=100).start()


	while tiempo < 10:
		time.sleep(0.3 - ((time.time() - starttime) % 0.3))

		if Equipo1.hacer_pase():
			Equipo1.shoot(prob_encajar_eq2)
		else:
			if Equipo2.hacer_pase():
				Equipo2.shoot(prob_encajar_eq1)
		tiempo = time.time() - starttime
		bar += 2.8
	bar.finish()
		


	print("="*12)
	print("FINAL DEL PARTIDO")
	print(Equipo1.nombre)
	Equipo1.mostrar_estadisticas()
	print(Equipo2.nombre)
	Equipo2.mostrar_estadisticas()

if __name__ == '__main__':
	cargar_informacion()	

	eqA = Equipo(equipoA, ranking_eqA)
	eqB = Equipo(equipoB, ranking_eqB)
	probabilidades = porcenajes_ranking(ranking_eqA)
	eqA.cargar_probabilidades(probabilidades)
	probabilidades = porcenajes_ranking(ranking_eqB)
	eqB.cargar_probabilidades(probabilidades)
	jugar(eqA,eqB)