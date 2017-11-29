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
			ranking = input("Ranking (numero del 1-99): ")
		return ranking

def cargar_informacion():
	# Es el primer metodo que se ejecuta, aqui cargamos toda la informacion del partido
	global equipoA, equipoB, ranking_eqA, ranking_eqB, fecha, hora

	print("## Ingrese la informacion del partido ##")

	equipoA = input("Nombre del equipo local: ")
	ranking_eqA = valid_ranking(input("Ranking (numero del 1-99): "))

	equipoB = input("Nombre del equipo visitante: ")
	ranking_eqB = valid_ranking(input("Ranking (numero del 1-99): "))

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

def sorteo_saque(equipo1, equipo2):
	lista = [equipo1, equipo2]
	ganador_sorteo = random.choice(lista)

	if ganador_sorteo.nombre == equipo1.nombre:
		equipos = {'gano_balon': equipo1, 'gano_cancha': equipo2}
	else:
		equipos = {'gano_balon': equipo2, 'gano_cancha': equipo1}

	return equipos

def tiempo_de_juego(saca_primero, defiende_primero, duracion):
	starttime=time.time()
	tiempo = 0
	# creo la barra de progreso
	bar = progressbar.ProgressBar(widgets=[
        progressbar.Percentage(),
        progressbar.Bar(),
    ], max_value=duracion).start()

	# hacemos que el juego tarde aproximadamente 10seg en simularse.
	while tiempo < duracion:
		time.sleep(1 - ((time.time() - starttime) % 1))

		jugar(saca_primero, defiende_primero)
		
		tiempo = time.time() - starttime
		bar.update(int(tiempo))
	bar.finish() # Para que finalice la barra de progreso

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

	eqA.cargar_probabilidades()
	eqB.cargar_probabilidades()

	result_sorteo = sorteo_saque(eqA, eqB)

	saca_primero = result_sorteo["gano_balon"]
	defiende_primero = result_sorteo["gano_cancha"]

	tiempo_de_juego(saca_primero, defiende_primero, 50)
	
	resultados_finales(eqA, eqB) # Mostramos el resultado final del partido.
	