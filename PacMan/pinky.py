import pygame
from config import *
import random
import heapq  # Para la implementación del algoritmo A*
import os

class Pinky:
    def __init__(self, mapa, tamanio_celda, velocidad=1, intervalo_movimiento=1):
        self.mapa = mapa
        self.tamanio_celda = tamanio_celda
        self.velocidad = velocidad
        self.direccion_actual = (0, 1)
        self.frame_actual = 0
        self.intervalo_movimiento = intervalo_movimiento
        self.ciclos_movimiento = 0

        # Para frightened
        self.estado_frightened = False
        self.tiempo_frightened = 0
        self.duracion_frightened = 300
        
        # Posición inicial de Pinky
        centro_x = mapa.num_columnas // 2
        centro_y = mapa.num_filas // 2
        self.posicion_inicial = (centro_x + 1, centro_y)
        self.posicion = self.posicion_inicial

        # Cargar imágenes de Pinky
        self.imagenes_base = [
            pygame.transform.scale(
                pygame.image.load(ruta).convert_alpha(),
                (self.tamanio_celda, self.tamanio_celda)
            ) for ruta in RUTA_IMAGEN_PINKY
        ]
        
        # Cargar imagen asustada
        self.imagen_frightened = pygame.transform.scale(
            pygame.image.load(RUTA_IMAGEN_ASUSTADO).convert_alpha(),
            (self.tamanio_celda, self.tamanio_celda)
        ) if os.path.exists(RUTA_IMAGEN_ASUSTADO) else None

        # Para scatter
        self.estado_scatter = False
        self.objetivo_scatter = (1, 1)  # Esquina superior izquierda del laberinto
    
    def restablecer_posicion(self):
        self.posicion = self.posicion_inicial

    def activar_scatter(self):
        self.estado_scatter = True

    def desactivar_scatter(self):
        self.estado_scatter = False

    def predecir_posicion_pacman(self, pacman):
        prediccion_x = pacman.posicion[0] + pacman.direccion_actual[0] * 4
        prediccion_y = pacman.posicion[1] + pacman.direccion_actual[1] * 4
        return (prediccion_x, prediccion_y)

    def obtener_vecinos(self, nodo):
        x, y = nodo
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        vecinos = []

        for dx, dy in direcciones:
            vecino = (x + dx, y + dy)
            if not self.mapa.es_pared(vecino):
                vecinos.append(vecino)
        
        return vecinos

    def heuristica(self, nodo, objetivo):
        # Distancia Manhattan
        return abs(nodo[0] - objetivo[0]) + abs(nodo[1] - objetivo[1])

    def buscar_camino(self, inicio, objetivo):
        frontera = []
        heapq.heappush(frontera, (0, inicio))
        came_from = {inicio: None}
        costo_hasta_ahora = {inicio: 0}

        while frontera:
            _, nodo_actual = heapq.heappop(frontera)

            if nodo_actual == objetivo:
                break

            for vecino in self.obtener_vecinos(nodo_actual):
                nuevo_costo = costo_hasta_ahora[nodo_actual] + 1
                if vecino not in costo_hasta_ahora or nuevo_costo < costo_hasta_ahora[vecino]:
                    costo_hasta_ahora[vecino] = nuevo_costo
                    prioridad = nuevo_costo + self.heuristica(vecino, objetivo)
                    heapq.heappush(frontera, (prioridad, vecino))
                    came_from[vecino] = nodo_actual

        # Reconstruir camino
        nodo_actual = objetivo
        camino = []
        while nodo_actual != inicio:
            camino.append(nodo_actual)
            nodo_actual = came_from.get(nodo_actual)

            if nodo_actual is None:  # No hay camino encontrado
                return []
        
        camino.reverse()
        return camino

    def mover(self, pacman, mapa):
        self.ciclos_movimiento += 1
        if self.ciclos_movimiento < self.intervalo_movimiento:
            return

        self.ciclos_movimiento = 0

        if self.estado_frightened:
            self.mover_aleatoriamente(mapa)
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.inicio_frightened >= self.duracion_frightened:
                self.desactivar_frightened()
            return

        if self.estado_scatter:
            objetivo = self.objetivo_scatter
        else:
            objetivo = self.predecir_posicion_pacman(pacman)

        camino = self.buscar_camino(self.posicion, objetivo)

        if camino:
            siguiente_paso = camino[0]
            self.posicion = siguiente_paso
            self.direccion_actual = (siguiente_paso[0] - self.posicion[0], siguiente_paso[1] - self.posicion[1])
        
        self.verificar_colision_con_pacman(pacman)

    def verificar_colision_con_pacman(self, pacman):
        if self.posicion == pacman.posicion:
            if not self.estado_frightened:
                pacman.perder_vida()
            elif self.estado_frightened == True:
                self.restablecer_posicion()
                self.desactivar_frightened()

    def dibujar(self, pantalla):
        x_pix = self.posicion[0] * self.tamanio_celda + self.tamanio_celda // 2
        y_pix = self.posicion[1] * self.tamanio_celda + self.tamanio_celda // 2 + ESPACIO_HUD
        imagen_base = self.imagen_frightened if self.estado_frightened else self.imagenes_base[self.frame_actual]
        self.frame_actual = (self.frame_actual + 1) % len(self.imagenes_base)
        pantalla.blit(imagen_base, (x_pix - self.tamanio_celda // 2, y_pix - self.tamanio_celda // 2))

    def activar_frightened(self, duracion):
        self.estado_frightened = True
        self.duracion_frightened = duracion
        self.inicio_frightened = pygame.time.get_ticks()

    def desactivar_frightened(self):
        self.estado_frightened = False
        self.frame_actual = 0
        print('Pinky frightened desactivado. ')
    
    def actualizar_frightened(self):
        if self.estado_frightened:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.inicio_frightened >= self.duracion_frightened:
                self.desactivar_frightened()

    def mover_aleatoriamente(self, mapa):
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(direcciones)
        for direccion in direcciones:
            nueva_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])
            if not mapa.es_pared(nueva_posicion):
                self.posicion = nueva_posicion
                self.direccion_actual = direccion
                break
