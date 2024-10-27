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
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1, 3, 2, 2, 4, 2, 1],
            [0, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 0],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 4, 2, 2, 1, 2, 2, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1],
            [1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.tamaño_celda = 31  # Tamaño de cada celda en el mapa
        self.tabla_hash = {}

        # Inicializar objetos en el mapa
        for y, fila in enumerate(self.matriz):
            for x, celda in enumerate(fila):
                if celda == 1:
                    self.tabla_hash[(x, y)] = "PARED"
                elif celda == 2:
                    self.tabla_hash[(x, y)] = Punto((x, y))
                elif celda == 3:
                    self.tabla_hash[(x, y)] = PildoraDePoder((x, y))
                elif celda == 4:
                    self.tabla_hash[(x, y)] = Fruta((x, y), self.tamaño_celda)
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
            self.tabla_hash[posicion_fruta] = Fruta(posicion_fruta, self.tamaño_celda)

    def dibujar(self, pantalla):
        color_pared = (0, 0, 255)  # Color azul para las paredes
        grosor_borde = 4  # Grosor del borde de las paredes

        for (x, y), item in self.tabla_hash.items():
            if item == "PARED":
                # Calcular la posición de la celda en píxeles
                rect_x = x * self.tamaño_celda
                rect_y = y * self.tamaño_celda + ESPACIO_HUD

                # Verificar si hay paredes adyacentes para decidir qué bordes dibujar
                pared_arriba = self.es_pared((x, y - 1)) if y > 0 else False
                pared_abajo = self.es_pared((x, y + 1)) if y < self.num_filas - 1 else False
                pared_izquierda = self.es_pared((x - 1, y)) if x > 0 else False
                pared_derecha = self.es_pared((x + 1, y)) if x < self.num_columnas - 1 else False

                # Dibujar líneas para cada lado si no hay pared adyacente
                if not pared_arriba:
                    pygame.draw.line(pantalla, color_pared,
                                     (rect_x, rect_y),
                                     (rect_x + self.tamaño_celda, rect_y),
                                     grosor_borde)
                if not pared_abajo:
                    pygame.draw.line(pantalla, color_pared,
                                     (rect_x, rect_y + self.tamaño_celda),
                                     (rect_x + self.tamaño_celda, rect_y + self.tamaño_celda),
                                     grosor_borde)
                if not pared_izquierda:
                    pygame.draw.line(pantalla, color_pared,
                                     (rect_x, rect_y),
                                     (rect_x, rect_y + self.tamaño_celda),
                                     grosor_borde)
                if not pared_derecha:
                    pygame.draw.line(pantalla, color_pared,
                                     (rect_x + self.tamaño_celda, rect_y),
                                     (rect_x + self.tamaño_celda, rect_y + self.tamaño_celda),
                                     grosor_borde)

            elif isinstance(item, (Punto, Fruta, PildoraDePoder)):
                item.dibujar(pantalla, self.tamaño_celda, ESPACIO_HUD)
