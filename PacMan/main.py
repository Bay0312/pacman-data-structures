# principal.py
import pygame
from mapa import Mapa
from pacman import PacMan
import time
from config import *


class JuegoPacman:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Pac-Man")

        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 74)
        self.fuente_pequeña = pygame.font.Font(None, 36)

        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.mapa = Mapa()
        self.TAMAÑO_CELDA = TAMAÑO_CELDA
        self.pacman = PacMan(posicion=(1, 1), tamaño_celda=self.TAMAÑO_CELDA)
        self.contador_fruta = 0
        self.estado = EstadoJuego.PREPARADO
        self.tiempo_inicio = time.time()
        self.puntos_totales = self.mapa.contar_puntos_iniciales()
        self.puntos_recolectados = 0

    def mostrar_mensaje(self, texto, y_offset=0, tamaño_grande=True):
        fuente = self.fuente_grande if tamaño_grande else self.fuente_pequeña
        texto_surface = fuente.render(texto, True, COLOR_TEXTO)
        texto_rect = texto_surface.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + y_offset))
        self.pantalla.blit(texto_surface, texto_rect)

    def actualizar_estado(self):
        if self.puntos_recolectados >= self.puntos_totales:
            self.estado = EstadoJuego.VICTORIA

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN and self.estado == EstadoJuego.VICTORIA:
                if evento.key == pygame.K_RETURN:
                    self.reiniciar_juego()
        return True

    def capturar_movimiento(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            return (-1, 0)
        elif teclas[pygame.K_RIGHT]:
            return (1, 0)
        elif teclas[pygame.K_UP]:
            return (0, -1)
        elif teclas[pygame.K_DOWN]:
            return (0, 1)
        return None

    def dibujar_juego(self):
        self.pantalla.fill(COLOR_FONDO)
        texto = self.fuente_pequeña.render(
            f"Puntuación: {self.pacman.puntuacion}   Vidas: {self.pacman.vidas}",
            True, COLOR_TEXTO
        )
        self.pantalla.blit(texto, (20, 10))

        self.mapa.dibujar(self.pantalla)
        self.pacman.dibujar(self.pantalla)

        # Mostrar mensajes según el estado
        if self.estado == EstadoJuego.PREPARADO:
            self.mostrar_mensaje("READY!")
        elif self.estado == EstadoJuego.VICTORIA:
            self.mostrar_mensaje("¡VICTORIA!", -40)
            self.mostrar_mensaje("Presiona ENTER para jugar de nuevo", 40, False)

    def ejecutar(self):
        jugando = True
        reloj = pygame.time.Clock()

        while jugando:
            jugando = self.manejar_eventos()
            movimiento = self.capturar_movimiento()

            if self.estado == EstadoJuego.PREPARADO:
                if time.time() - self.tiempo_inicio >= TIEMPO_INICIO_JUEGO:
                    self.estado = EstadoJuego.JUGANDO

            elif self.estado == EstadoJuego.JUGANDO and movimiento:
                self.pacman.mover(movimiento, self.mapa)
                self.puntos_recolectados = self.pacman.puntos_recolectados
                self.actualizar_estado()

            # Generar fruta ocasionalmente durante el juego
            if self.estado == EstadoJuego.JUGANDO:
                self.contador_fruta += 1
                if self.contador_fruta > 800:
                    self.mapa.generar_fruta_aleatoria()
                    self.contador_fruta = 0

            self.dibujar_juego()
            pygame.display.flip()
            reloj.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    juego = JuegoPacman()
    juego.ejecutar()
