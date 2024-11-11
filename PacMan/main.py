import pygame
from mapa import Mapa
from pacman import PacMan
from blinky import Blinky
from pinky import Pinky
from clyde import Clyde
from inky import Inky
import time
from config import *
import json


class JuegoPacman:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Pac-Man")

        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 74)
        self.fuente_pequenia = pygame.font.Font(None, 36)

        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.mapa = Mapa()
        self.TAMANIO_CELDA = TAMANIO_CELDA
        self.pacman = PacMan(posicion=(1, 1), tamanio_celda=self.TAMANIO_CELDA)

        # Crear todos los fantasmas
        self.pinky = Pinky(self.mapa, self.TAMANIO_CELDA)
        self.blinky = Blinky(self.mapa, self.TAMANIO_CELDA)
        self.clyde = Clyde(self.mapa, self.TAMANIO_CELDA)
        self.inky = Inky(self.mapa, self.TAMANIO_CELDA)

        self.fantasmas = [self.pinky, self.blinky, self.clyde, self.inky]

        self.contador_fruta = 0
        self.estado = EstadoJuego.PREPARADO
        self.tiempo_inicio = time.time()
        self.puntos_totales = self.mapa.contar_puntos_iniciales()
        self.puntos_recolectados = 0

        # Temporizador para alternar entre modos
        self.tiempo_modo = 0
        self.intervalos_modos = [7, 20, 7, 20, 5, 20, 5, 20]  # Alterna entre scatter y chase
        self.indice_modo = 0
        self.modo_actual = 'scatter'

    def guardar_juego(self):
        estado = {
            "pacman": {
                "posicion": self.pacman.posicion,
                "puntuacion": self.pacman.puntuacion,
                "vidas": self.pacman.vidas
            },
            "fantasmas": {
                "pinky": {
                    "posicion": self.pinky.posicion,
                    "frightened": self.pinky.estado_frightened,
                    "tiempo_restante_frightened": self.pinky.duracion_frightened - (
                            pygame.time.get_ticks() - self.pinky.inicio_frightened
                    ) if self.pinky.estado_frightened else 0
                },
                "blinky": {
                    "posicion": self.blinky.posicion,
                    "frightened": self.blinky.estado_frightened,
                    "tiempo_restante_frightened": self.blinky.duracion_frightened - (
                            pygame.time.get_ticks() - self.blinky.inicio_frightened
                    ) if self.blinky.estado_frightened else 0
                },
                "clyde": {
                    "posicion": self.clyde.posicion,
                    "frightened": self.clyde.estado_frightened,
                    "tiempo_restante_frightened": self.clyde.duracion_frightened - (
                            pygame.time.get_ticks() - self.clyde.inicio_frightened
                    ) if self.clyde.estado_frightened else 0
                },
                "inky": {
                    "posicion": self.inky.posicion,
                    "frightened": self.inky.estado_frightened,
                    "tiempo_restante_frightened": self.inky.duracion_frightened - (
                            pygame.time.get_ticks() - self.inky.inicio_frightened
                    ) if self.inky.estado_frightened else 0
                }
            },
            "puntos_recolectados": self.puntos_recolectados,
            "estado_mapa": self.mapa.guardar_estado()
        }
        with open("guardado.json", "w") as archivo:
            json.dump(estado, archivo)
        print("Partida guardada.")

    def cargar_juego(self):
        try:
            with open("guardado.json", "r") as archivo:
                estado = json.load(archivo)

            self.pacman.posicion = tuple(estado["pacman"]["posicion"])
            self.pacman.puntuacion = estado["pacman"]["puntuacion"]
            self.pacman.vidas = estado["pacman"]["vidas"]

            for nombre, fantasma in zip(["pinky", "blinky", "clyde", "inky"], self.fantasmas):
                fantasma.posicion = tuple(estado["fantasmas"][nombre]["posicion"])
                if estado["fantasmas"][nombre]["frightened"]:
                    fantasma.activar_frightened(estado["fantasmas"][nombre]["tiempo_restante_frightened"])
                else:
                    fantasma.desactivar_frightened()

            self.puntos_recolectados = estado["puntos_recolectados"]
            self.mapa.cargar_estado(estado["estado_mapa"])

            print("Partida cargada.")
            return True
        except FileNotFoundError:
            print("No se encontró ninguna partida guardada.")
            return False

        # Mostrar modal es una funcion generada por IA
    def mostrar_modal(self, mensaje, duracion=2, color_fondo=(50, 50, 50), color_texto=(0, 255, 0)):
        """
        Muestra un mensaje modal en el centro de la pantalla.

        :param mensaje: Texto a mostrar en el modal.
        :param duracion: Duración en segundos del modal.
        :param color_fondo: Color de fondo del modal (RGB).
        :param color_texto: Color del texto del mensaje (RGB).
        """
        tiempo_inicial = time.time()

        while time.time() - tiempo_inicial < duracion:
            # Fondo modal
            fondo_modal = pygame.Surface((300, 100))
            fondo_modal.set_alpha(200)  # Fondo semitransparente
            fondo_modal.fill(color_fondo)  # Color de fondo personalizado
            rect_modal = fondo_modal.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

            # Renderizar el mensaje en el modal
            texto = self.fuente_pequenia.render(mensaje, True, color_texto)  # Color de texto personalizado
            texto_rect = texto.get_rect(center=rect_modal.center)

            # Dibujar el modal y el mensaje en pantalla
            self.pantalla.blit(fondo_modal, rect_modal)
            self.pantalla.blit(texto, texto_rect)
            pygame.display.flip()  # Actualizar pantalla

            # Manejar eventos para permitir salir con QUIT sin congelarse
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    # mostrar_menu_pausa es una funcion generada por IA
    def mostrar_menu_pausa(self):
        opciones = ["Continuar", "Guardar", "Cargar", "Salir"]
        seleccion = 0
        mensaje_exito = None  # Mensaje de éxito temporal

        en_pausa = True
        while en_pausa:
            self.pantalla.fill((0, 0, 0))  # Color de fondo negro
            fondo_rect = pygame.Rect(ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2 - 100, 300, 250)
            pygame.draw.rect(self.pantalla, (50, 50, 50), fondo_rect)  # Fondo del menú de pausa
            pygame.draw.rect(self.pantalla, (200, 200, 200), fondo_rect, 3)  # Borde del menú de pausa

            # Dibujar opciones
            for i, opcion in enumerate(opciones):
                color = COLOR_TEXTO if i != seleccion else (255, 0, 0)  # Rojo si está seleccionado
                texto = self.fuente_pequenia.render(opcion, True, color)
                texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 60 + i * 40))
                self.pantalla.blit(texto, texto_rect)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return True
                    elif evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                    elif evento.key == pygame.K_RETURN:
                        if opciones[seleccion] == "Continuar":
                            en_pausa = False
                        elif opciones[seleccion] == "Guardar":
                            self.guardar_juego()
                            mensaje_exito = "Juego guardado con éxito"
                            self.mostrar_modal(mensaje_exito, color_fondo=(0, 100, 0),
                                               color_texto=(255, 255, 255))  # Modal verde con texto blanco
                        elif opciones[seleccion] == "Cargar":
                            # Utilizar el resultado de cargar_juego para mostrar el mensaje correcto
                            if self.cargar_juego():
                                mensaje_exito = "Juego cargado con éxito"
                                self.mostrar_modal(mensaje_exito, color_fondo=(0, 0, 100),
                                                   color_texto=(255, 255, 255))  # Modal azul con texto blanco
                            else:
                                mensaje_exito = "No se encontró archivo de guardado"
                                self.mostrar_modal(mensaje_exito, color_fondo=(100, 0, 0),
                                                   color_texto=(255, 255, 255))  # Modal rojo con texto blanco
                        elif opciones[seleccion] == "Salir":
                            return False

            # Limitar el tiempo de visualización del mensaje de éxito
            if mensaje_exito:
                pygame.time.delay(300)
                mensaje_exito = None

        return True

    def mostrar_mensaje(self, texto, y_offset=0, tamanio_grande=True):
        fuente = self.fuente_grande if tamanio_grande else self.fuente_pequenia
        texto_surface = fuente.render(texto, True, COLOR_TEXTO)
        texto_rect = texto_surface.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 + y_offset))
        self.pantalla.blit(texto_surface, texto_rect)

    def actualizar_estado(self):
        if self.puntos_recolectados >= self.puntos_totales:
            self.estado = EstadoJuego.VICTORIA

        if self.pacman.vidas == 0:
            self.estado = EstadoJuego.DERROTA

        # Cambiar la llamada aquí para pasar activar_modo_frightened
        if self.pacman.recoger_pildora_poder(self.mapa, self.activar_modo_frightened):
            self.activar_modo_frightened(duracion=5000)

        tiempo_actual = time.time()
        if tiempo_actual - self.tiempo_modo >= self.intervalos_modos[self.indice_modo]:
            self.indice_modo = (self.indice_modo + 1) % len(self.intervalos_modos)
            self.tiempo_modo = tiempo_actual
            if self.modo_actual == 'scatter':
                self.modo_actual = 'chase'
                self.desactivar_modo_scatter()
            else:
                self.modo_actual = 'scatter'
                self.activar_modo_scatter()

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return self.mostrar_menu_pausa()
                elif evento.key == pygame.K_RETURN and self.estado == EstadoJuego.VICTORIA:
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
        texto = self.fuente_pequenia.render(
            f"Puntuación: {self.pacman.puntuacion}   Vidas: {self.pacman.vidas}",
            True, COLOR_TEXTO
        )
        self.pantalla.blit(texto, (20, 10))

        self.mapa.dibujar(self.pantalla)
        self.pacman.dibujar(self.pantalla)
        self.pinky.dibujar(self.pantalla)
        self.blinky.dibujar(self.pantalla)
        self.clyde.dibujar(self.pantalla)
        self.inky.dibujar(self.pantalla)

        # Mostrar mensajes según el estado
        if self.estado == EstadoJuego.PREPARADO:
            self.mostrar_mensaje("READY!")
        elif self.estado == EstadoJuego.VICTORIA:
            self.mostrar_mensaje("¡VICTORIA!", -40)
            self.mostrar_mensaje("Presiona ENTER para jugar de nuevo", 40, False)
        elif self.pacman.vidas <= 0:
            self.pacman.mostrar_mensaje(self.pantalla, "¡Has Perdido!", self.fuente_grande, self.fuente_pequenia,
                                        COLOR_TEXTO, True)

    def activar_modo_frightened(self, duracion=300):
        duracion = 7000
        self.pinky.activar_frightened(duracion)
        self.blinky.activar_frightened(duracion)
        self.clyde.activar_frightened(duracion)
        self.inky.activar_frightened(duracion)

    def activar_modo_scatter(self):
        self.pinky.activar_scatter()
        self.blinky.activar_scatter()
        self.clyde.activar_scatter()
        self.inky.activar_scatter()

    def desactivar_modo_scatter(self):
        self.pinky.desactivar_scatter()
        self.blinky.desactivar_scatter()
        self.clyde.desactivar_scatter()
        self.inky.desactivar_scatter()


    def ejecutar(self):
        jugando = True
        reloj = pygame.time.Clock()

        while jugando:
            jugando = self.manejar_eventos()
            movimiento = self.capturar_movimiento()

            if self.estado == EstadoJuego.PREPARADO:
                if time.time() - self.tiempo_inicio >= TIEMPO_INICIO_JUEGO:
                    self.estado = EstadoJuego.JUGANDO

            # Mover PacMan solo si hay movimiento detectado
            if self.estado == EstadoJuego.JUGANDO and movimiento:
                # Pasar la lista de fantasmas al método mover
                self.pacman.mover(movimiento, self.mapa, self.activar_modo_frightened, self.fantasmas)
                self.puntos_recolectados = self.pacman.puntos_recolectados
                self.actualizar_estado()

            # Generar fruta ocasionalmente durante el juego
            if self.estado == EstadoJuego.JUGANDO:
                self.contador_fruta += 1
                if self.contador_fruta > 800:
                    self.mapa.generar_fruta_aleatoria()
                    self.contador_fruta = 0

                if self.contador_fruta % 2 == 0:
                    self.pinky.mover(self.pacman, self.mapa)
                    self.blinky.mover(self.pacman, self.mapa)
                    self.clyde.mover(self.pacman, self.mapa)
                    self.inky.mover(self.pacman, self.blinky, self.mapa)

                self.pinky.actualizar_frightened()
                self.blinky.actualizar_frightened()
                self.clyde.actualizar_frightened()
                self.inky.actualizar_frightened()

                # Verificar colisión entre los fantasmas y PacMan
                self.pinky.verificar_colision_con_pacman(self.pacman)
                self.blinky.verificar_colision_con_pacman(self.pacman)
                self.clyde.verificar_colision_con_pacman(self.pacman)
                self.inky.verificar_colision_con_pacman(self.pacman)

            # Dibujar el estado actual del juego
            self.dibujar_juego()
            pygame.display.flip()
            reloj.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    juego = JuegoPacman()
    juego.ejecutar()