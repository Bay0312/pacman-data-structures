import pygame
import random
from elementos import Punto, Fruta, PildoraDePoder
from config import *


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

        self.tamanio_celda = 31  # tamanio de cada celda en el mapa
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
                    self.tabla_hash[(x, y)] = Fruta((x, y), self.tamanio_celda)
                else:
                    self.tabla_hash[(x, y)] = "VACIO"

        self.num_columnas = len(self.matriz[0])
        self.num_filas = len(self.matriz)

    def es_pared(self, posicion):
        if posicion not in self.tabla_hash:
            #print(f"Posición {posicion} no encontrada en el mapa.")
            return True  # Consideramos que si no se encuentra la posición, es una pared por defecto
        return self.tabla_hash.get(posicion) == "PARED"

    def guardar_estado(self):
        estado_mapa = []
        for y in range(self.num_filas):
            fila = []
            for x in range(self.num_columnas):
                celda = self.tabla_hash.get((x, y))
                if isinstance(celda, Punto):
                    fila.append(2)
                elif isinstance(celda, PildoraDePoder):
                    fila.append(3)
                elif isinstance(celda, Fruta):
                    fila.append(4)
                elif celda == "PARED":
                    fila.append(1)
                else:
                    fila.append(0)  # Vacío
            estado_mapa.append(fila)
        return estado_mapa

    def cargar_estado(self, estado_mapa):
        self.tabla_hash = {}
        for y, fila in enumerate(estado_mapa):
            for x, celda in enumerate(fila):
                if celda == 1:
                    self.tabla_hash[(x, y)] = "PARED"
                elif celda == 2:
                    self.tabla_hash[(x, y)] = Punto((x, y))
                elif celda == 3:
                    self.tabla_hash[(x, y)] = PildoraDePoder((x, y))
                elif celda == 4:
                    self.tabla_hash[(x, y)] = Fruta((x, y), self.tamanio_celda)
                else:
                    self.tabla_hash[(x, y)] = "VACIO"

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
            self.tabla_hash[posicion_fruta] = Fruta(posicion_fruta, self.tamanio_celda)

    def dibujar(self, pantalla):
        for (x, y), item in self.tabla_hash.items():
            if item == "PARED":
                # Calcular la posición de la celda en píxeles
                rect_x = x * self.tamanio_celda
                rect_y = y * self.tamanio_celda + ESPACIO_HUD

                # Verificar si hay paredes adyacentes para decidir qué bordes dibujar
                pared_arriba = self.es_pared((x, y - 1)) if y > 0 else False
                pared_abajo = self.es_pared((x, y + 1)) if y < self.num_filas - 1 else False
                pared_izquierda = self.es_pared((x - 1, y)) if x > 0 else False
                pared_derecha = self.es_pared((x + 1, y)) if x < self.num_columnas - 1 else False

                # Dibujar líneas para cada lado si no hay pared adyacente
                if not pared_arriba:
                    pygame.draw.line(pantalla, COLOR_PARED,
                                     (rect_x, rect_y),
                                     (rect_x + self.tamanio_celda, rect_y),
                                     GROSOR_BORDE)
                if not pared_abajo:
                    pygame.draw.line(pantalla, COLOR_PARED,
                                     (rect_x, rect_y + self.tamanio_celda),
                                     (rect_x + self.tamanio_celda, rect_y + self.tamanio_celda),
                                     GROSOR_BORDE)
                if not pared_izquierda:
                    pygame.draw.line(pantalla, COLOR_PARED,
                                     (rect_x, rect_y),
                                     (rect_x, rect_y + self.tamanio_celda),
                                     GROSOR_BORDE)
                if not pared_derecha:
                    pygame.draw.line(pantalla, COLOR_PARED,
                                     (rect_x + self.tamanio_celda, rect_y),
                                     (rect_x + self.tamanio_celda, rect_y + self.tamanio_celda),
                                     GROSOR_BORDE)

            elif isinstance(item, (Punto, Fruta, PildoraDePoder)):
                item.dibujar(pantalla, self.tamanio_celda, ESPACIO_HUD)

    def contar_puntos_iniciales(self):
        contador = 0
        for fila in self.matriz:
            contador += sum(1 for celda in fila if celda in [2, 3])
        return contador
