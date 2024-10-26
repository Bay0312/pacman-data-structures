# mapa.py

import pygame
import random
from elementos import Punto, Fruta, PildoraDePoder

ESPACIO_HUD = 50  # Definimos el espacio en la parte superior para el HUD
class Mapa:
    def __init__(self):
        # Mapa básico donde:
        # 0 = espacio vacío, 1 = pared, 2 = punto, 3 = píldora de poder, 4 = fruta
        self.matriz = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 3, 0, 0, 4, 0, 1],
            [0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 0, 0, 1, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.tamaño_celda = 31
        self.tabla_hash = {}



        for y, fila in enumerate(self.matriz):
            for x, celda in enumerate(fila):
                if celda == 1:
                    self.tabla_hash[(x, y)] = "PARED"
                elif celda == 2:
                    self.tabla_hash[(x, y)] = Punto((x, y))
                elif celda == 3:
                    self.tabla_hash[(x, y)] = PildoraDePoder((x, y))
                elif celda == 4:
                    self.tabla_hash[(x, y)] = Fruta((x, y))
                else:
                    self.tabla_hash[(x, y)] = "VACIO"

        self.num_columnas = len(self.matriz[0])
        self.num_filas = len(self.matriz)

    def es_pared(self, posicion):
        return self.tabla_hash.get(posicion) == "PARED"

    def obtener_objeto(self, posicion):
        obj = self.tabla_hash.get(posicion)
        if isinstance(obj, (Punto, Fruta, PildoraDePoder)):
            return obj
        return None

    def eliminar_objeto(self, posicion):
        if posicion in self.tabla_hash and isinstance(self.tabla_hash[posicion], (Punto, Fruta, PildoraDePoder)):
            self.tabla_hash[posicion] = "VACIO"

    def generar_fruta_aleatoria(self):
        posiciones_vacias = [pos for pos, val in self.tabla_hash.items() if val == "VACIO"]
        if posiciones_vacias:
            posicion_fruta = random.choice(posiciones_vacias)
            self.tabla_hash[posicion_fruta] = Fruta(posicion_fruta)

    def dibujar(self, pantalla):
        color_pared = (0, 0, 255)

        for (x, y), item in self.tabla_hash.items():
            if item == "PARED":
                pygame.draw.rect(pantalla, color_pared,
                                 pygame.Rect(x * self.tamaño_celda, y * self.tamaño_celda + ESPACIO_HUD,
                                             self.tamaño_celda, self.tamaño_celda))
            elif isinstance(item, Punto) or isinstance(item, Fruta) or isinstance(item, PildoraDePoder):
                item.dibujar(pantalla, self.tamaño_celda, ESPACIO_HUD)
