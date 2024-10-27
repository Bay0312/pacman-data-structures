# pacman.py

import pygame
import os
from elementos import Punto, PildoraDePoder

ESPACIO_HUD = 50  # Definimos el espacio en la parte superior para el HUD

class PacMan:
    def __init__(self, posicion, tamaño_celda, velocidad=1):
        self.posicion = posicion
        self.velocidad = velocidad
        self.puntuacion = 0
        self.vidas = 3
        self.frame_actual = 0
        self.direccion_actual = (1, 0)
        self.tamaño_celda = tamaño_celda
        self.puntos_recolectados = 0

        # Cargar y redimensionar las imágenes de animación desde la carpeta img
        self.imagenes_base = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("img", f"Pacman{i}.png")).convert_alpha(),
                (self.tamaño_celda, self.tamaño_celda)
            ) for i in range(1, 5)
        ]

    def mover(self, direccion, mapa):
        nueva_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])

        num_columnas = mapa.num_columnas
        if nueva_posicion[0] < 0:
            nueva_posicion = (num_columnas - 1, nueva_posicion[1])
        elif nueva_posicion[0] >= num_columnas:
            nueva_posicion = (0, nueva_posicion[1])

        if not mapa.es_pared(nueva_posicion):
            self.posicion = nueva_posicion
            self.direccion_actual = direccion

            # Detectar colisión con objetos en el mapa
            objeto = mapa.obtener_objeto(self.posicion)
            if objeto:
                self.puntuacion += objeto.valor
                # Solo aumentar el contador para puntos normales y píldoras de poder
                from elementos import Punto, PildoraDePoder
                if isinstance(objeto, (Punto, PildoraDePoder)):
                    self.puntos_recolectados += 1
                mapa.eliminar_objeto(self.posicion)

    def dibujar(self, pantalla):
        x_pix = self.posicion[0] * self.tamaño_celda + self.tamaño_celda // 2
        y_pix = self.posicion[1] * self.tamaño_celda + self.tamaño_celda // 2 + ESPACIO_HUD

        # Alternar imágenes para el efecto de "masticado"
        imagen_base = self.imagenes_base[self.frame_actual]
        self.frame_actual = (self.frame_actual + 1) % len(self.imagenes_base)

        # Rotar o voltear la imagen según la dirección actual
        if self.direccion_actual == (1, 0):  # Derecha
            imagen_pacman = imagen_base
        elif self.direccion_actual == (-1, 0):  # Izquierda
            imagen_pacman = pygame.transform.flip(imagen_base, True, False)
        elif self.direccion_actual == (0, -1):  # Arriba
            imagen_pacman = pygame.transform.rotate(imagen_base, 90)
        elif self.direccion_actual == (0, 1):  # Abajo
            imagen_pacman = pygame.transform.rotate(imagen_base, -90)

        # Dibujar la imagen en la posición de Pac-Man
        pantalla.blit(imagen_pacman, (x_pix - self.tamaño_celda // 2, y_pix - self.tamaño_celda // 2))
