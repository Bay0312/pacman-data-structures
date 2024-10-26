# pacman.py

import pygame

ESPACIO_HUD = 50  # Definimos el espacio en la parte superior para el HUD


class PacMan:
    def __init__(self, posicion, velocidad=1):
        self.posicion = posicion
        self.velocidad = velocidad
        self.puntuacion = 0
        self.vidas = 3

    def mover(self, direccion, mapa):
        nueva_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])

        num_columnas = mapa.num_columnas
        if nueva_posicion[0] < 0:
            nueva_posicion = (num_columnas - 1, nueva_posicion[1])
        elif nueva_posicion[0] >= num_columnas:
            nueva_posicion = (0, nueva_posicion[1])

        if not mapa.es_pared(nueva_posicion):
            self.posicion = nueva_posicion

            objeto = mapa.obtener_objeto(self.posicion)
            if objeto:
                self.puntuacion += objeto.valor
                mapa.eliminar_objeto(self.posicion)

    def dibujar(self, pantalla): # Dibujar Generado por IA
        tamaño_celda = 31
        color_pacman = (255, 255, 0)
        pygame.draw.circle(pantalla, color_pacman,
                           (self.posicion[0] * tamaño_celda + tamaño_celda // 2,
                            self.posicion[1] * tamaño_celda + tamaño_celda // 2 + ESPACIO_HUD), 14)
