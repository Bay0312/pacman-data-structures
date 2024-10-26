import pygame


class Punto:
    def __init__(self, posicion, valor=10):
        self.posicion = posicion
        self.valor = valor

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0): # Dibujar Generado por IA
        color_punto = (255, 255, 255)
        x_pix = self.posicion[0] * tamaño_celda + tamaño_celda // 2
        y_pix = self.posicion[1] * tamaño_celda + tamaño_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, color_punto, (x_pix, y_pix), 3) # Draw Generado por IA


class Fruta(Punto):
    def __init__(self, posicion, valor=50):
        super().__init__(posicion, valor)

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0): # Dibujar Generado por IA
        color_fruta = (255, 0, 0)
        x_pix = self.posicion[0] * tamaño_celda + tamaño_celda // 2
        y_pix = self.posicion[1] * tamaño_celda + tamaño_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, color_fruta, (x_pix, y_pix), 8)


class PildoraDePoder(Punto):
    def __init__(self, posicion, valor=100):
        super().__init__(posicion, valor)

    def dibujar(self, pantalla, tamaño_celda, desplazamiento_y=0): # Dibujar Generado por IA
        color_pildora = (0, 255, 0)
        x_pix = self.posicion[0] * tamaño_celda + tamaño_celda // 2
        y_pix = self.posicion[1] * tamaño_celda + tamaño_celda // 2 + desplazamiento_y
        pygame.draw.circle(pantalla, color_pildora, (x_pix, y_pix), 10)
