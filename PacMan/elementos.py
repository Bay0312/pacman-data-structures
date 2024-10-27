# elementos.py
import pygame
from config import *


class ElementoJuego:
    def __init__(self, posicion, valor):
        self.posicion = posicion
        self.valor = valor


class Punto(ElementoJuego):
    def __init__(self, posicion, valor=10):
        super().__init__(posicion, valor)

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0):
        x_pix = self.posicion[0] * tamaño_celda + tamaño_celda // 2
        y_pix = self.posicion[1] * tamaño_celda + tamaño_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, COLOR_PUNTO, (x_pix, y_pix), 3)


class PildoraDePoder(ElementoJuego):
    def __init__(self, posicion, valor=100):
        super().__init__(posicion, valor)

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0):
        COLOR_PILDORA = (255, 255, 255)  # Color blanco
        x_pix = self.posicion[0] * tamaño_celda + tamaño_celda // 2
        y_pix = self.posicion[1] * tamaño_celda + tamaño_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, COLOR_PILDORA, (x_pix, y_pix), 10)


class Fruta(ElementoJuego):
    def __init__(self, posicion, tamaño_celda, valor=50):
        super().__init__(posicion, valor)
        self.imagen = pygame.image.load(os.path.join(RUTA_IMAGEN_CEREZA)).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (tamaño_celda, tamaño_celda))
        self.tamaño_celda = tamaño_celda

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0):
        x_pix = self.posicion[0] * tamaño_celda
        y_pix = self.posicion[1] * tamaño_celda + desplazamiento_y
        pantalla.blit(self.imagen, (x_pix, y_pix))
