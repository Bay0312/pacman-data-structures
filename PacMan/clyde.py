import heapq
import random
import os
import pygame
from config import RUTA_IMAGEN_CLYDE, RUTA_IMAGEN_ASUSTADO, ESPACIO_HUD

class Clyde:
    def __init__(self, mapa, tamanio_celda):
        filas = len(mapa.matriz)
        columnas = len(mapa.matriz[0])
        self.posicion_inicial = (columnas // 2, filas // 2)  # Posición central
        self.posicion = self.posicion_inicial
        self.mapa = mapa  # Mapa representado como un grafo ponderado
        self.tamanio_celda = tamanio_celda
        self.velocidad = 1
        self.direccion = (0, 0)
        self.frame_actual = 0
        self.intervalo_movimiento = 1
        self.ciclos_movimiento = 0
        self.visitados = set()
        self.estado_frightened = False
        self.tiempo_frightened = 0
        self.duracion_frightened = 300
        self.comportamiento = random.choice([0, 1])  # Comportamiento de Clyde: 0 - perseguir, 1 - alejarse

        # Definir posición inicial
        self.posicion = self.posicion_inicial

        self.imagenes_base = [
            pygame.transform.scale(
                pygame.image.load(ruta).convert_alpha(),
                (self.tamanio_celda, self.tamanio_celda)
            ) for ruta in RUTA_IMAGEN_CLYDE
        ]
        
        # Imagen para estado frightened
        if os.path.exists(RUTA_IMAGEN_ASUSTADO):
            self.imagen_frightened = pygame.transform.scale(
                pygame.image.load(RUTA_IMAGEN_ASUSTADO).convert_alpha(),
                (self.tamanio_celda, self.tamanio_celda)
            )
        else:
            print("Error: No se encontró la imagen asustada de Clyde.")
            self.imagen_frightened = None

        # Para scatter
        self.estado_scatter = False
        self.objetivo_scatter = (1, 17)  # Esquina inferior izquierda del laberinto

    def restablecer_posicion(self):
        """Restablece la posición de Clyde a su posición inicial"""
        self.posicion = self.posicion_inicial

    def activar_scatter(self):
        self.estado_scatter = True

    def desactivar_scatter(self):
        self.estado_scatter = False

    def dibujar(self, pantalla):
        """Dibuja a Clyde en la pantalla en la posición actual"""
        x_pix = self.posicion[0] * self.tamanio_celda
        y_pix = self.posicion[1] * self.tamanio_celda + ESPACIO_HUD
        pantalla.blit(self.imagenes_base[self.frame_actual], (x_pix, y_pix))

    def activar_frightened(self, duracion):
        self.estado_frightened = True
        self.tiempo_frightened = duracion
        
        if self.imagen_frightened:
            self.frame_actual = 1

    def actualizar_frightened(self):
        """Actualiza el estado asustado de Clyde."""
        if self.estado_frightened:
            self.tiempo_frightened -= 1
            if self.tiempo_frightened <= 0:
                self.estado_frightened = False
                self.frame_actual = 0  # Cambia de nuevo a la imagen normal
                print("Clyde ya no está asustado.")

    def desactivar_frightened(self):
        self.estado_frightened = False

    def mover(self, pacman, mapa):
        """Mueve a Clyde hacia su objetivo usando el algoritmo de Dijkstra."""
        self.ciclos_movimiento += 1
        if self.ciclos_movimiento < self.intervalo_movimiento:
            return
        self.ciclos_movimiento = 0

        # Actualiza el estado "frightened" de Clyde
        self.actualizar_frightened()

        # Si está en estado "frightened", mueve aleatoriamente
        if self.estado_frightened:
            self.mover_aleatoriamente(mapa)
            return

        if self.estado_scatter:
            objetivo = self.objetivo_scatter
        else:
            # Si no está asustado, decide el comportamiento
            if self.comportamiento == 0:
                objetivo = pacman.posicion  # Perseguir a Pac-Man
            else:
                # Alejarse de Pac-Man
                nodos_posibles = list(self.mapa.tabla_hash.keys())
                nodos_lejos = sorted(nodos_posibles, key=lambda nodo: self.heuristica(nodo, pacman.posicion), reverse=True)
                if nodos_lejos:
                    objetivo = nodos_lejos[0]
                else:
                    objetivo = pacman.posicion

        camino = self.buscar_camino(objetivo)

        if camino and len(camino) > 1:
            self.posicion = camino[1]  # Mueve a Clyde al siguiente nodo en el camino
        else:
            # Si no se encuentra un camino válido, mover aleatoriamente
            self.mover_aleatoriamente(mapa)

        self.comportamiento = random.choice([0, 1])


    def es_movimiento_valido(self, nueva_posicion, mapa):
        """Verifica si el movimiento a la nueva posición es válido en el mapa"""
        x, y = nueva_posicion
        ancho = mapa.num_columnas
        alto = mapa.num_filas
        return (0 <= x < ancho) and (0 <= y < alto) and not mapa.es_pared((x, y))

    def heuristica(self, nodo, objetivo):
        """Calcula la distancia Manhattan entre dos nodos"""
        return abs(nodo[0] - objetivo[0]) + abs(nodo[1] - objetivo[1])

    def buscar_camino(self, objetivo):
        """Implementa el algoritmo de Dijkstra para encontrar el camino más corto"""
        if not self.es_movimiento_valido(objetivo, self.mapa):
            return []

        # Usamos un min-heap para Dijkstra
        frontera = []
        heapq.heappush(frontera, (0, self.posicion))  # Cola de prioridad (costo, nodo)
        costos = {self.posicion: 0}
        padres = {self.posicion: None}

        while frontera:
            costo_actual, nodo_actual = heapq.heappop(frontera)

            if nodo_actual == objetivo:
                return self.reconstruir_camino(padres, nodo_actual)

            for vecino, costo in self.obtener_vecinos(nodo_actual):
                nuevo_costo = costo_actual + costo
                if vecino not in costos or nuevo_costo < costos[vecino]:
                    costos[vecino] = nuevo_costo
                    heapq.heappush(frontera, (nuevo_costo, vecino))
                    padres[vecino] = nodo_actual

        return []  # No se encontró camino


    def obtener_vecinos(self, nodo):
        # Obtener los vecinos de un nodo
        vecinos = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Direcciones: izquierda, derecha, arriba, abajo
            vecino = (nodo[0] + dx, nodo[1] + dy)
            if not self.mapa.es_pared(vecino):
                costo = 1  # Ajustar cálculo del costo si es necesario
                vecinos.append((vecino, costo))
        return vecinos

    def reconstruir_camino(self, padres, nodo):
        """Reconstruye el camino desde el nodo objetivo hasta el inicio"""
        camino = []
        while nodo is not None:
            camino.append(nodo)
            nodo = padres[nodo]
        return camino[::-1]  # Devuelve el camino en orden correcto

    def mover_aleatoriamente(self, mapa):
        """Mueve a Clyde aleatoriamente"""
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(direcciones)
        for direccion in direcciones:
            nueva_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])
            if not mapa.es_pared(nueva_posicion):
                self.posicion = nueva_posicion
                break

    def verificar_colision_con_pacman(self, pacman):
        if self.posicion == pacman.posicion:
            pacman.perder_vida()
            self.restablecer_posicion()
