# elementos.py

import pygame
import os

class Punto:
    def __init__(self, posicion, valor=10):
        self.posicion = posicion
        self.valor = valor

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0):
        color_punto = (255, 255, 255)  # Color blanco para el punto
        x_pix = self.posicion[0] * tamaño_celda + tamaño_celda // 2
        y_pix = self.posicion[1] * tamaño_celda + tamaño_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, color_punto, (x_pix, y_pix), 3)


class Fruta(Punto):
    def __init__(self, posicion, tamaño_celda, valor=50):
        super().__init__(posicion, valor)
        # Cargar la imagen de la cereza y redimensionarla al tamaño de la celda
        self.imagen = pygame.image.load(os.path.join("img", "Cereza.png")).convert_alpha()
        self.imagen = pygame.transform.scale(self.imagen, (tamaño_celda, tamaño_celda))
        self.tamaño_celda = tamaño_celda  # Guardamos el tamaño de celda para usar en dibujar

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0):
        x_pix = self.posicion[0] * tamaño_celda
        y_pix = self.posicion[1] * tamaño_celda + desplazamiento_y
        # Dibujar la imagen de la fruta en la posición correspondiente
        pantalla.blit(self.imagen, (x_pix, y_pix))


class PildoraDePoder(Punto):
    def __init__(self, posicion, valor=100):
        super().__init__(posicion, valor)

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0):
        color_pildora = (255, 255, 255)  # Cambiado a color blanco
        x_pix = self.posicion[0] * tamaño_celda + tamaño_celda // 2
        y_pix = self.posicion[1] * tamaño_celda + tamaño_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, color_pildora, (x_pix, y_pix), 10)
