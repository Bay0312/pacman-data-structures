import pygame
from config import *


class ElementoJuego:
    def __init__(self, posicion, valor):
        self.posicion = posicion
        self.valor = valor


class Punto(ElementoJuego):
    def __init__(self, posicion, valor=10):
        super().__init__(posicion, valor)

    def dibujar(self, pantalla, tamanio_celda, desplazamiento_y=0):
        x_pix = self.posicion[0] * tamanio_celda + tamanio_celda // 2
        y_pix = self.posicion[1] * tamanio_celda + tamanio_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, COLOR_PUNTO, (x_pix, y_pix), 3)


class PildoraDePoder(ElementoJuego):
    def __init__(self, posicion, valor=100):
        super().__init__(posicion, valor)

    def dibujar(self, pantalla, tamanio_celda, desplazamiento_y=0):
        x_pix = self.posicion[0] * tamanio_celda + tamanio_celda // 2
        y_pix = self.posicion[1] * tamanio_celda + tamanio_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, COLOR_PILDORA, (x_pix, y_pix), 10)


class Fruta(ElementoJuego):
    def __init__(self, posicion, tamanio_celda, valor=50):
        super().__init__(posicion, valor)
        self.imagen = pygame.image.load(os.path.join(RUTA_IMAGEN_CEREZA)).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (tamanio_celda, tamanio_celda))
        self.tamanio_celda = tamanio_celda

    def dibujar(self, pantalla, tamanio_celda, desplazamiento_y=0):
        x_pix = self.posicion[0] * tamanio_celda
        y_pix = self.posicion[1] * tamanio_celda + desplazamiento_y
        pantalla.blit(self.imagen, (x_pix, y_pix))
