import pygame
from config import *
import random

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
        
        # Calcular el centro del mapa
        centro_x = mapa.num_columnas // 2
        centro_y = mapa.num_filas // 2

        # Definir posición inicial
        self.posicion_inicial = (centro_x + 1, centro_y)
        self.posicion = self.posicion_inicial

        # Cargar imágenes de Pinky (normales y asustadas)
        self.imagenes_base = [
            pygame.transform.scale(
                pygame.image.load(ruta).convert_alpha(),
                (self.tamanio_celda, self.tamanio_celda)
            ) for ruta in RUTA_IMAGEN_PINKY
        ]
        
        # Cargar imágenes asustado
        if os.path.exists(RUTA_IMAGEN_ASUSTADO):  # Verificar que la ruta sea correcta
            self.imagen_frightened = pygame.transform.scale(
                pygame.image.load(RUTA_IMAGEN_ASUSTADO).convert_alpha(),
                (self.tamanio_celda, self.tamanio_celda)
            )
        else:
            print("Error: No se encontró la imagen asustada de Clyde.")
            self.imagen_frightened = None
    
    def restablecer_posicion(self):
        self.posicion = self.posicion_inicial

    def predecir_posicion_pacman(self, pacman):
        prediccion_x = pacman.posicion[0] + pacman.direccion_actual[0] * 4
        prediccion_y = pacman.posicion[1] + pacman.direccion_actual[1] * 4
        return (prediccion_x, prediccion_y)

    def mover(self, pacman, mapa):
        self.ciclos_movimiento += 1

        if self.ciclos_movimiento < self.intervalo_movimiento:
            return

        self.ciclos_movimiento = 0

        # Frightened
        if self.estado_frightened:
            self.mover_aleatoriamente(mapa)
            
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.inicio_frightened >= self.duracion_frightened:
                self.desactivar_frightened()
            return

        objetivo = self.predecir_posicion_pacman(pacman)

        direccion_x = 1 if objetivo[0] > self.posicion[0] else -1 if objetivo[0] < self.posicion[0] else 0
        direccion_y = 1 if objetivo[1] > self.posicion[1] else -1 if objetivo[1] < self.posicion[1] else 0

        posibles_direcciones = [(direccion_x, 0), (0, direccion_y), (direccion_x, direccion_y)]
        random.shuffle(posibles_direcciones)

        for direccion in posibles_direcciones:
            nueva_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])
            if not mapa.es_pared(nueva_posicion):
                self.posicion = nueva_posicion
                self.direccion_actual = direccion
                break

    def verificar_colision_con_pacman(self, pacman):
        if self.posicion == pacman.posicion:
            pacman.perder_vida()
            self.restablecer_posicion()

    def dibujar(self, pantalla):
        x_pix = self.posicion[0] * self.tamanio_celda + self.tamanio_celda // 2
        y_pix = self.posicion[1] * self.tamanio_celda + self.tamanio_celda // 2 + ESPACIO_HUD

        # Usar imagen de estado asustado si está activado
        if self.estado_frightened:
            imagen_base = self.imagen_frightened  # Solo una imagen, no un índice
        else:
            imagen_base = self.imagenes_base[self.frame_actual]
        
        self.frame_actual = (self.frame_actual + 1) % len(self.imagenes_base)

        pantalla.blit(imagen_base, (x_pix - self.tamanio_celda // 2, y_pix - self.tamanio_celda // 2))
    
    def activar_frightened(self, duracion):
        self.estado_frightened = True
        self.duracion_frightened = duracion
        self.inicio_frightened = pygame.time.get_ticks()

    def desactivar_frightened(self):
        self.estado_frightened = False

    # Ayuda de IA para sacar direcciones
    def mover_aleatoriamente(self, mapa):
        direcciones = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(direcciones)

        for direccion in direcciones:
            nueva_posicion = (self.posicion[0] + direccion[0], self.posicion[1] + direccion[1])
            if not mapa.es_pared(nueva_posicion):
                self.posicion = nueva_posicion
                self.direccion_actual = direccion
                break