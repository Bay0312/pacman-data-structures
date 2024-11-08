import pygame
from config import *
import random

class Pinky:
    def __init__(self, mapa, tamanio_celda, velocidad=1, intervalo_movimiento=1):
        self.mapa = mapa
        self.tamanio_celda = tamanio_celda
        self.velocidad = velocidad
        self.direccion_actual = (0, 1)
        self.frame_actual = 0
        self.intervalo_movimiento = intervalo_movimiento
        self.ciclos_movimiento = 0
        
        # Calcular el centro del mapa
        centro_x = mapa.num_columnas // 2
        centro_y = mapa.num_filas // 2

        # Definir posición inicial
        self.posicion_inicial = (centro_x + 1, centro_y)
        self.posicion = self.posicion_inicial

        # Cargar imágenes de Pinky
        self.imagenes_base = [
            pygame.transform.scale(
                pygame.image.load(ruta).convert_alpha(),
                (self.tamanio_celda, self.tamanio_celda)
            ) for ruta in RUTA_IMAGEN_PINKY
        ]

    def restablecer_posicion(self):
        """Restablece la posición de Pinky a su posición inicial."""
        self.posicion = self.posicion_inicial

    def predecir_posicion_pacman(self, pacman):
        """Calcula una posición futura de Pac-Man en base a su dirección actual."""
        prediccion_x = pacman.posicion[0] + pacman.direccion_actual[0] * 4
        prediccion_y = pacman.posicion[1] + pacman.direccion_actual[1] * 4
        return (prediccion_x, prediccion_y)

    def mover(self, pacman, mapa):
        """Movimientos de Pinky para perseguir a PacMan."""
        self.ciclos_movimiento += 1
        
        # Verificar intervalo de movimiento
        if self.ciclos_movimiento < self.intervalo_movimiento:
            return

        self.ciclos_movimiento = 0

        # AI para predecir movimiento
        objetivo = self.predecir_posicion_pacman(pacman)

        # Calcular dirección hacia el objetivo
        direccion_x = 1 if objetivo[0] > self.posicion[0] else -1 if objetivo[0] < self.posicion[0] else 0
        direccion_y = 1 if objetivo[1] > self.posicion[1] else -1 if objetivo[1] < self.posicion[1] else 0

        # Generar direcciones posibles
        posibles_direcciones = [(direccion_x, 0), (0, direccion_y), (direccion_x, direccion_y)]
        random.shuffle(posibles_direcciones)

        # Intentar moverse en una de las direcciones posibles
        for direccion in posibles_direcciones:
            nueva_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])
            if not mapa.es_pared(nueva_posicion):
                self.posicion = nueva_posicion
                self.direccion_actual = direccion
                break

    def verificar_colision_con_pacman(self, pacman):
        """Verificar si Pinky colisiona con PacMan."""
        if self.posicion == pacman.posicion:
            pacman.perder_vida()
            self.restablecer_posicion()

    def dibujar(self, pantalla):
        """Dibujar a Pinky en la pantalla."""
        x_pix = self.posicion[0] * self.tamanio_celda + self.tamanio_celda // 2
        y_pix = self.posicion[1] * self.tamanio_celda + self.tamanio_celda // 2 + ESPACIO_HUD

        imagen_base = self.imagenes_base[self.frame_actual]
        self.frame_actual = (self.frame_actual + 1) % len(self.imagenes_base)

        pantalla.blit(imagen_base, (x_pix - self.tamanio_celda // 2, y_pix - self.tamanio_celda // 2))