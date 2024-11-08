import pygame
import random
from config import *

class Clyde:
    def __init__(self, mapa, tamanio_celda, intervalo_movimiento=1):
        self.mapa = mapa
        self.tamanio_celda = tamanio_celda
        self.velocidad = 1
        self.direccion = (0, 0)
        self.frame_actual = 0
        self.intervalo_movimiento = intervalo_movimiento
        self.ciclos_movimiento = 0
        
        # Calcular el centro del mapa
        centro_x = mapa.num_columnas // 2
        centro_y = mapa.num_filas // 2

        # Definir posición inicial
        self.posicion_inicial = (centro_x - 1, centro_y)
        self.posicion = self.posicion_inicial

        # Cargar imágenes de Clyde
        self.imagenes_base = [
            pygame.transform.scale(
                pygame.image.load(ruta).convert_alpha(),
                (self.tamanio_celda, self.tamanio_celda)
            ) for ruta in RUTA_IMAGEN_CLYDE
        ]

    def restablecer_posicion(self):
        self.posicion = self.posicion_inicial

    def dibujar(self, pantalla):
        x_pix = self.posicion[0] * self.tamanio_celda
        y_pix = self.posicion[1] * self.tamanio_celda + ESPACIO_HUD

        imagen_base = self.imagenes_base[self.frame_actual]
        self.frame_actual = (self.frame_actual + 1) % len(self.imagenes_base)

        pantalla.blit(imagen_base, (x_pix, y_pix))

    def mover(self, pacman, mapa):
        self.ciclos_movimiento += 1
        if self.ciclos_movimiento < self.intervalo_movimiento:
            return
        
        self.ciclos_movimiento = 0

        pos_pacman = pacman.posicion
        distancia_x = abs(self.posicion[0] - pos_pacman[0])
        distancia_y = abs(self.posicion[1] - pos_pacman[1])
        distancia_total = distancia_x + distancia_y

        if distancia_total < 5:
            self.alejarse_de_pacman(pos_pacman, mapa)
        else:
            self.perseguir_pacman(pos_pacman, mapa)

        nueva_posicion = (self.posicion[0] + self.direccion[0], self.posicion[1] + self.direccion[1])

        if self.es_movimiento_valido(nueva_posicion, mapa):
            self.posicion = nueva_posicion

    def es_movimiento_valido(self, nueva_posicion, mapa):
        x, y = nueva_posicion
        ancho = mapa.num_columnas
        alto = mapa.num_filas

        return (0 <= x < ancho) and (0 <= y < alto) and not mapa.es_pared((x, y))

    def perseguir_pacman(self, pos_pacman, mapa):
        opciones = []

        # Calcular las posibles posiciones para moverse
        posibles_movimientos = {
            (1, 0): (self.posicion[0] + 1, self.posicion[1]),   # Derecha
            (-1, 0): (self.posicion[0] - 1, self.posicion[1]),  # Izquierda
            (0, 1): (self.posicion[0], self.posicion[1] + 1),   # Abajo
            (0, -1): (self.posicion[0], self.posicion[1] - 1)   # Arriba
        }

        # Filtrar movimientos válidos
        for direccion, nueva_pos in posibles_movimientos.items():
            if self.es_movimiento_valido(nueva_pos, mapa):
                opciones.append(direccion)

        # Si hay opciones válidas, elegir la mejor opción en función de la distancia a PacMan
        if opciones:
            mejor_opcion = min(opciones, key=lambda direccion: self.calcular_distancia(
                posibles_movimientos[direccion], pos_pacman))
            self.direccion = mejor_opcion

    def calcular_distancia(self, pos1, pos2):
        """Calcula la distancia de Manhattan entre dos posiciones."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


    def alejarse_de_pacman(self, pos_pacman, mapa):
        opciones = []
        # Buscar dirección válida para alejarse de PacMan
        if self.es_movimiento_valido((self.posicion[0] - 1, self.posicion[1]), mapa):
            opciones.append((-1, 0))  # Izquierda
        if self.es_movimiento_valido((self.posicion[0] + 1, self.posicion[1]), mapa):
            opciones.append((1, 0))   # Derecha
        if self.es_movimiento_valido((self.posicion[0], self.posicion[1] - 1), mapa):
            opciones.append((0, -1))  # Arriba
        if self.es_movimiento_valido((self.posicion[0], self.posicion[1] + 1), mapa):
            opciones.append((0, 1))   # Abajo

        # Elegir aleatoriamente una dirección para evitar predecibilidad
        if opciones:
            self.direccion = random.choice(opciones)

    def verificar_colision_con_pacman(self, pacman):
        """Verifica si Clyde colisiona con PacMan."""
        if self.posicion == pacman.posicion:
            pacman.perder_vida()
            self.restablecer_posicion()
