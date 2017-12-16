#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

# Import pygame and libraries
from pygame.locals import *
from random import randrange
import os
import pygame
import time
import datetime

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

# Import files for play
from equipo import Equipo
import main
import threading

RANKINGS = [('1-10',1),('11-20',2),('21-30',3),('31-40',4),('41-50',5)]

EQUIPOS = main.lista_equipos()
FORMACIONES = main.lista_formaciones()
FECHAS = main.lista_fechas()
HORAS = main.lista_horas()
ETAPAS =  main.lista_etapas()

ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         TEXT_NEWLINE,
         'Soccer Simulator {0}'.format("v1.0"),
         'Developers:',
         'Jose Camacaro','Carlos Torrealba','Laura Rincon',
         'Genesis Campos']

COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (700, 540)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Futbol Simulator')
clock = pygame.time.Clock()
dt = 1 / FPS

# Global variables
EQUIPO1 = ['ALEMANIA']
RANK_EQ1 = [1]
FORM_EQ1 = ['4-4-2']

EQUIPO2 = ['ALEMANIA']
RANK_EQ2 = [1]
FORM_EQ2 = ['4-4-2']

FECHA = ['14/06/18']
HORA = ['14:00']
ETAPA = ['Fase de Grupos']
# Para el reloj
timer = [0.0]
timer_font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)

# -----------------------------------------------------------------------------

def select_equipo1(e):
    EQUIPO1[0] = e

def rank_equipo1(r):
    RANK_EQ1[0] = r

def form_equipo1(f):
    FORM_EQ1[0] = f

def select_equipo2(e):
    EQUIPO2[0] = e

def rank_equipo2(r):
    RANK_EQ2[0] = r

def form_equipo2(f):
    FORM_EQ2[0] = f

def fechas(f):
    FECHA[0] = f

def horas(h):
    HORA[0] = h

def etapas(e):
    ETAPA[0] = e

def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except(pygame.error, message):
            raise(SystemExit, message)
    image = image.convert()
    if transparent:
            color = image.get_at((0,0))
            image.set_colorkey(color, RLEACCEL)
    return image

def eventos_de_teclado():
    # Application events
    playevents = pygame.event.get()
    for e in playevents:
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                if main_menu.is_disabled():
                    main_menu.enable()
    return playevents

def display_final(font):
    exit_font = pygame.font.Font(pygameMenu.fonts.FONT_OXYGEN, 20)
    sonido = pygame.mixer.Sound("resources/n.mp3")
    sonido.play() # Pitido final

    f_salir = exit_font.render('Presione Esc para salir', 2, COLOR_BLACK)
    f_width = f_salir.get_size()[0]

    while True:

        # Clock tick
        clock.tick(60)

        # Pass events to main_menu
        main_menu.mainloop(eventos_de_teclado())
        
        surface.blit(f_salir, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 1.1))
        pygame.display.flip()


def jugar_function(team1, team2, rank_eq1, rank_eq2, form_eq1, form_eq2, fecha, hora, etapa, font):  
    starttime=time.time()
    tiempo = 0
    duracion = 91
    fecha = fecha[0]
    hora = hora[0]
    etapa = etapa[0]

    # Info de los equipos
    equipo_local = team1[0]
    rank_local = rank_eq1[0]
    form_local = form_eq1[0]
    equipo_visitante = team2[0]
    rank_visitante = rank_eq2[0]
    form_visitante = form_eq2[0]


    eq1 = Equipo(equipo_local, rank_local, form_local)
    eq2 = Equipo(equipo_visitante, rank_visitante, form_visitante)

    eq1.cargar_probabilidades()
    eq2.cargar_probabilidades()

    prediccion = main.prediccion_partido(eq1, eq2)

    result_sorteo = main.sorteo_saque(eq1, eq2)

    saca_primero = result_sorteo["gano_balon"]
    defiende_primero = result_sorteo["gano_cancha"]

    # Carga la imagen de fondo 
    background_image = load_image('resources/wall2.jpg')
    ball_image = load_image('resources/SoccerBall.png', True)
    f_prediccion = font.render("Favorito: " + prediccion, 1, COLOR_WHITE)
    f_fecha = font.render(fecha, 1, COLOR_WHITE)
    f_hora = font.render(hora + "h", 1, COLOR_WHITE)
    f_etapa = font.render(etapa, 1, COLOR_WHITE)

    # Comienza el sonido ambiente
    pygame.mixer.music.load("resources/crowdSound.mp3")
    pygame.mixer.music.play(1)

    main_menu.disable()
    main_menu.reset(1)

    # Para ver quien gano el saque
    print("Saca primero: ",saca_primero.nombre)

    # Comienza el partido
    main.jugar(saca_primero, defiende_primero, duracion)

    while main.partido_transcurso:
        
        minutos = int(main.tiempo)

        # Definiendo los labels de los equipos
        nomb_team1 = font.render(eq1.nombre, 1, COLOR_WHITE)
        form_team1 = font.render(eq1.formacion, 1, COLOR_WHITE)
        goles_team1 = font.render('Goles: ' + str(eq1.goles), 1, COLOR_WHITE)
        fallidos_team1 = font.render('Remates fuera: ' + str(eq1.fallidos), 1, COLOR_WHITE)
        pases_team1 = font.render('Pases exitosos: ' + str(eq1.pases_exitosos), 1, COLOR_WHITE)
        
        nomb_team2 = font.render(eq2.nombre, 1, COLOR_WHITE)
        form_team2 = font.render(eq2.formacion, 1, COLOR_WHITE)
        goles_team2 = font.render('Goles: ' + str(eq2.goles), 1, COLOR_WHITE)
        fallidos_team2 = font.render('Remates fuera: ' + str(eq2.fallidos), 1, COLOR_WHITE)
        pases_team2 = font.render('Pases exitosos: ' + str(eq2.pases_exitosos), 1, COLOR_WHITE)

        # Dibujar tiempo
        time_string = str(int(minutos)) + " min"
        time_blit = timer_font.render(time_string, 1, COLOR_WHITE)
        time_blit_size = time_blit.get_size()

        # Actualizo la pantalla
        surface.blit(background_image, (0,-30))
        surface.blit(f_prediccion, (WINDOW_SIZE[0] / 2, 120))
        surface.blit(f_etapa, (WINDOW_SIZE[0] / 2, 0))
        surface.blit(f_fecha, (WINDOW_SIZE[0] / 2, 40))
        surface.blit(f_hora, (WINDOW_SIZE[0] / 2, 78))

        surface.blit(time_blit, (
            WINDOW_SIZE[0] / 2 - time_blit_size[0] / 2, WINDOW_SIZE[1] / 2 - time_blit_size[1] / 1))

        if eq1.balon:
            surface.blit(ball_image,((WINDOW_SIZE[0] - 500) / 2, WINDOW_SIZE[1] / 1.2))
        surface.blit(nomb_team1,((WINDOW_SIZE[0] - 500) / 2, WINDOW_SIZE[1] / 2))
        surface.blit(goles_team1,((WINDOW_SIZE[0] - 500) / 2, WINDOW_SIZE[1] / 1.7))
        surface.blit(fallidos_team1,((WINDOW_SIZE[0] - 500) / 2, WINDOW_SIZE[1] / 1.55))
        surface.blit(pases_team1,((WINDOW_SIZE[0] - 500) / 2, WINDOW_SIZE[1] / 1.4))
        surface.blit(form_team1,((WINDOW_SIZE[0] - 500) / 2, WINDOW_SIZE[1] / 1.3))
        
        if eq2.balon:
            surface.blit(ball_image,((WINDOW_SIZE[0] + 100) / 2, WINDOW_SIZE[1] / 1.2))
        surface.blit(nomb_team2,((WINDOW_SIZE[0] + 100) / 2, WINDOW_SIZE[1] / 2))
        surface.blit(goles_team2,((WINDOW_SIZE[0] + 100) / 2, WINDOW_SIZE[1] / 1.7))
        surface.blit(fallidos_team2,((WINDOW_SIZE[0] + 100) / 2, WINDOW_SIZE[1] / 1.55))
        surface.blit(pases_team2,((WINDOW_SIZE[0] + 100) / 2, WINDOW_SIZE[1] / 1.4))
        surface.blit(form_team2,((WINDOW_SIZE[0] + 100) / 2, WINDOW_SIZE[1] / 1.3))
        
        pygame.display.flip() # Para mostrar los cambios en la pantalla
        
        time.sleep(0.1 - ((time.time() - starttime) % 0.1)) # para que el sonido no se distorsione


    main_menu.disable()
    main_menu.reset(1)
    pygame.mixer.music.stop()
    display_final(font)


def main_background():
    """
    Function used by menus, draw on background while menu is active.
    
    :return: None
    """
    surface.fill(COLOR_BACKGROUND)


# -----------------------------------------------------------------------------
# PLAY MENU
play_menu = pygameMenu.Menu(surface,
                            window_width=WINDOW_SIZE[0],
                            window_height=WINDOW_SIZE[1],
                            font=pygameMenu.fonts.FONT_OXYGEN,
                            title='Menu de juego',
                            menu_alpha=100,
                            font_size=30,
                            menu_width=int(WINDOW_SIZE[0] * 0.8),
                            menu_height=int(WINDOW_SIZE[1] * 0.9),
                            bgfun=main_background,
                            menu_color=MENU_BACKGROUND_COLOR,
                            option_shadow=False,
                            font_color=COLOR_BLACK,
                            color_selected=COLOR_WHITE,
                            onclose=PYGAME_MENU_DISABLE_CLOSE
                            )

play_menu.add_selector('Equipo  local', EQUIPOS, onreturn=None, onchange=select_equipo1)
play_menu.add_selector('Ranking  local',RANKINGS, onreturn=None, onchange=rank_equipo1)
play_menu.add_selector('Formacion  local',FORMACIONES, onreturn=None, onchange=form_equipo1)
play_menu.add_selector('Equipo  visitante', EQUIPOS,onreturn=None, onchange=select_equipo2)
play_menu.add_selector('Ranking  visitante',RANKINGS, onreturn=None, onchange=rank_equipo2)
play_menu.add_selector('Formacion  visitante',FORMACIONES, onreturn=None, onchange=form_equipo2)

play_menu.add_option('Jugar ', jugar_function, EQUIPO1, EQUIPO2, RANK_EQ1, RANK_EQ2, FORM_EQ1,FORM_EQ2,
                    FECHA, HORA, ETAPA, pygame.font.Font(pygameMenu.fonts.FONT_OXYGEN, 30))

# ABOUT MENU
about_menu = pygameMenu.TextMenu(surface,
                                 window_width=WINDOW_SIZE[0],
                                 window_height=WINDOW_SIZE[1],
                                 font=pygameMenu.fonts.FONT_OXYGEN,
                                 font_title=pygameMenu.fonts.FONT_OXYGEN,
                                 title='Acerca',
                                 # Disable menu close (ESC button)
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 font_color=COLOR_BLACK,
                                 text_fontsize=20,
                                 font_size_title=30,
                                 menu_color_title=COLOR_WHITE,
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_width=int(WINDOW_SIZE[0] * 0.9),
                                 menu_height=int(WINDOW_SIZE[1] * 0.9),
                                 option_shadow=False,
                                 color_selected=COLOR_WHITE,
                                 text_color=COLOR_BLACK,
                                 bgfun=main_background)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(TEXT_NEWLINE)
about_menu.add_option('Volver al menu', PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            window_width=WINDOW_SIZE[0],
                            window_height=WINDOW_SIZE[1],
                            font=pygameMenu.fonts.FONT_OXYGEN,
                            title='Menu principal',
                            menu_alpha=100,
                            font_size=30,
                            menu_width=int(WINDOW_SIZE[0] * 0.8),
                            menu_height=int(WINDOW_SIZE[1] * 0.8),
                            onclose=PYGAME_MENU_CLOSE,  # ESC disabled
                            bgfun=main_background,
                            menu_color=MENU_BACKGROUND_COLOR,
                            option_shadow=False,
                            font_color=COLOR_BLACK,
                            color_selected=COLOR_WHITE,
                            )

main_menu.add_selector('Dia ',FECHAS, onreturn=None, onchange=fechas)
main_menu.add_selector('Hora ',HORAS, onreturn=None, onchange=horas)
main_menu.add_selector('Etapa',ETAPAS, onreturn=None, onchange=etapas)
main_menu.add_option('Avanzar', play_menu)
main_menu.add_option('Acerca', about_menu)
main_menu.add_option('Salir', PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------
# Main loop
while True:

    # Tick
    clock.tick(60)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()

    # Main menu
    main_menu.mainloop(events)

    # Flip surface
    pygame.display.flip()