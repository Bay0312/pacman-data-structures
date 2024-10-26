# principal.py

import pygame
from mapa import Mapa
from pacman import PacMan

# Tamaño de la ventana ajustado para incluir espacio para la puntuación y vidas en la parte superior
ANCHO_VENTANA = 838
ALTO_VENTANA = 640  # Espacio extra en la parte superior para el HUD (puntuación y vidas)
ESPACIO_HUD = 50  # Altura reservada para el HUD

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Pac-Man")

COLOR_FONDO = (0, 0, 0)
fuente = pygame.font.Font(None, 36)

mapa = Mapa()
pacman = PacMan(posicion=(1, 1))

jugando = True
reloj = pygame.time.Clock()
contador_fruta = 0  # Contador para generar frutas ocasionalmente

while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        pacman.mover((-1, 0), mapa)
    elif teclas[pygame.K_RIGHT]:
        pacman.mover((1, 0), mapa)
    elif teclas[pygame.K_UP]:
        pacman.mover((0, -1), mapa)
    elif teclas[pygame.K_DOWN]:
        pacman.mover((0, 1), mapa)

    pantalla.fill(COLOR_FONDO)

    # Mostrar puntuación y vidas en la parte superior
    texto = fuente.render(f"Puntuación: {pacman.puntuacion}   Vidas: {pacman.vidas}", True, (255, 255, 255))
    pantalla.blit(texto, (20, 10))

    # Dibujar el mapa y a Pac-Man
    mapa.dibujar(pantalla)
    pacman.dibujar(pantalla)

    # Generar una fruta ocasionalmente
    contador_fruta += 1
    if contador_fruta > 800:  # Aproximadamente cada 80 segundos si el juego corre a 10 FPS
        mapa.generar_fruta_aleatoria()
        contador_fruta = 0

    pygame.display.flip()
    reloj.tick(10)

pygame.quit()
