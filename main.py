import time
import random
import progressbar
import threading
from equipo import Equipo

semaforo = threading.Lock() # Inicializamos el semaforo

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
	# Es el primer metodo que se ejecuta, aqui cargamos toda la informacion del partido
	global equipoA, equipoB, ranking_eqA, ranking_eqB, fecha, hora

	print("## Ingrese la informacion del partido ##")

	equipoA = input("Nombre del equipo local: ")
	ranking_eqA = valid_ranking(input("Ranking (numero del 1-100): "))

	equipoB = input("Nombre del equipo visitante: ")
	ranking_eqB = valid_ranking(input("Ranking (numero del 1-100): "))

	fecha = input("Fecha del partido: ")
	hora = input("Hora del partido: ")

def jugar(Equipo1, Equipo2):
	# Busco las probabilidades de encajar por cada equipo
	prob_encajar_eq1 = Equipo1.probabilidad_encajar()
	prob_encajar_eq2 = Equipo2.probabilidad_encajar()

	def jugar_equipo1(defensa_rival):
		# Seccion critica
		semaforo.acquire() # Bloqueo
		if Equipo1.hacer_pases():
			Equipo1.shoot(defensa_rival)
		semaforo.release() # Libero

	def jugar_equipo2(defensa_rival):
		# Seccion critica
		semaforo.acquire() # Bloqueo
		if Equipo2.hacer_pases():
			Equipo2.shoot(defensa_rival)
		semaforo.release() # Libero

	# Inicializo los hilos, en target paso el metodo a ejecutar.
	# en args paso las probabilidades de encajar del equipo rival
	hilo_equipo1 = threading.Thread(name = 'hilo_eq1', target = jugar_equipo1, args = (prob_encajar_eq2,))
	hilo_equipo2 = threading.Thread(name = 'hilo_eq2', target = jugar_equipo2, args = (prob_encajar_eq1,))

	# Se ejecutan ambos hilos
	hilo_equipo1.start()
	hilo_equipo2.start()

	# Si no utilizo el join, entonces el hilo principal de Python (que hace que se ejecute el programa)
	# No esperara a que terminen de ejecutarse los hilos "hijos" y el programa terminara antes.
	hilo_equipo1.join()
	hilo_equipo2.join()
	
def resultados_finales(equipo1, equipo2):
	print("="*16)
	print("FINAL DEL PARTIDO")
	print(equipo1.nombre)
	equipo1.mostrar_estadisticas()
	print(equipo2.nombre)
	equipo2.mostrar_estadisticas()

if __name__ == '__main__':
	cargar_informacion()	

	eqA = Equipo(equipoA, ranking_eqA)
	eqB = Equipo(equipoB, ranking_eqB)

	probabilidades = porcenajes_ranking(ranking_eqA)
	eqA.cargar_probabilidades(probabilidades)

	probabilidades = porcenajes_ranking(ranking_eqB)
	eqB.cargar_probabilidades(probabilidades)

	starttime=time.time()
	tiempo = 0
	# creo la barra de progreso
	bar = progressbar.ProgressBar(widgets=[
        progressbar.Percentage(),
        progressbar.Bar(),
    ], max_value=100).start()

	# hacemos que el juego tarde aproximadamente 10seg en simularse.
	while tiempo < 10:
		time.sleep(0.3 - ((time.time() - starttime) % 0.3))

		jugar(eqA,eqB)
		
		tiempo = time.time() - starttime
		bar += 2.8
	bar.finish() # Para que finalice la barra de progreso
	
	resultados_finales(eqA, eqB) # Mostramos el resultado final del partido.