import pygame, asyncio, sys
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
        pygame.font.init()  # Necesario antes de usar pygame.font

        # Plataforma
        self.IS_WEB = (sys.platform == "emscripten")

        # UI/estado
        self.modal = None

        # --- AUDIO SEGURO PARA WEB/ESCRITORIO ---
        self.AUDIO_OK = False
        try:
            pygame.mixer.init()  # parámetros por defecto
            self.AUDIO_OK = True
        except pygame.error:
            self.AUDIO_OK = False

        # Pantalla
        flags = 0
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), flags)
        pygame.display.set_caption("Pacman")

        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 74)
        self.fuente_pequenia = pygame.font.Font(None, 36)

        # Cargar sonidos de forma segura
        self.sonido_inicio = None
        self.sonido_fin_juego = None
        self.sonido_fantasmas = RUTA_SONIDO_FANTASMAS  # mixer.music.load usa ruta

        if self.AUDIO_OK:
            try:
                self.sonido_inicio = pygame.mixer.Sound(RUTA_SONIDO_INICIO)
            except pygame.error:
                self.sonido_inicio = None
                # No desactivamos completamente AUDIO_OK para permitir música de fondo

        if self.AUDIO_OK:
            try:
                self.sonido_fin_juego = pygame.mixer.Sound(RUTA_SONIDO_FIN_JUEGO)
            except pygame.error:
                self.sonido_fin_juego = None

        # Control del arranque de audio (deferido en web)
        self._audio_armed = True                 # esperar primer click/tecla en web
        self._start_ch = None                    # canal del jingle
        self._wait_channel_end = False           # esperar a que el jingle termine

        # Auto-start en ESCRITORIO (opcional): en web se requiere interacción del usuario
        if self.AUDIO_OK and self.sonido_inicio and not self.IS_WEB:
            self._audio_armed = False
            try:
                self._start_ch = self.sonido_inicio.play()
                self._wait_channel_end = True
            except pygame.error:
                self._start_ch = None
                self._wait_channel_end = False

        # Estado inicial del juego
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

        # Temporizador para alternar entre modos (no bloqueante)
        self.tiempo_modo = 0
        self.intervalos_modos = [7, 20, 7, 20, 5, 20, 5, 20]
        self.indice_modo = 0
        self.modo_actual = 'scatter'

    def dibujar_pausa(self):
        # Fondo oscurecido
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.pantalla.blit(overlay, (0, 0))

        fondo_rect = pygame.Rect(ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2 - 100, 300, 250)
        pygame.draw.rect(self.pantalla, (50, 50, 50), fondo_rect)
        pygame.draw.rect(self.pantalla, (200, 200, 200), fondo_rect, 3)

        opciones = ["Continuar (ESC)", "Guardar (G)", "Cargar (C)", "Salir (Q)"]
        for i, opcion in enumerate(opciones):
            texto = self.fuente_pequenia.render(opcion, True, COLOR_TEXTO)
            texto_rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2 - 60 + i * 40))
            self.pantalla.blit(texto, texto_rect)

    def programar_modal(self, mensaje, duracion=2.0, color_fondo=(50, 50, 50), color_texto=(255, 255, 255)):
        self.modal = {
            "msg": mensaje,
            "hasta": time.time() + duracion,
            "cfondo": color_fondo,
            "ctexto": color_texto,
        }

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

    def mostrar_mensaje(self, texto, desplazamiento_y=0, color=(255, 255, 255)):
        fuente = pygame.font.Font(None, 48)
        mensaje = fuente.render(texto, True, color)
        rect_mensaje = mensaje.get_rect(center=(self.pantalla.get_width() // 2,
                                                self.pantalla.get_height() // 2 + desplazamiento_y))
        self.pantalla.blit(mensaje, rect_mensaje)

    def actualizar_estado(self):
        if self.puntos_recolectados >= self.puntos_totales:
            self.estado = EstadoJuego.VICTORIA
            if self.AUDIO_OK:
                try:
                    pygame.mixer.music.stop()
                except pygame.error:
                    pass
                try:
                    if self.sonido_fin_juego is not None:
                        self.sonido_fin_juego.play()
                except pygame.error:
                    pass

        if self.pacman.vidas == 0:
            self.estado = EstadoJuego.DERROTA
            if self.AUDIO_OK:
                try:
                    pygame.mixer.music.stop()
                except pygame.error:
                    pass
                try:
                    if self.sonido_fin_juego is not None:
                        self.sonido_fin_juego.play()
                except pygame.error:
                    pass

        # Píldora de poder → frightened
        if self.pacman.recoger_pildora_poder(self.mapa, self.activar_modo_frightened):
            self.activar_modo_frightened(duracion=5000)

        # Alternar modos scatter/chase
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

            # 1) Arranque de audio tras la PRIMERA interacción (tecla o click)
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if self._audio_armed and self.AUDIO_OK:
                    self._audio_armed = False  # desarmar antes para evitar doble disparo
                    try:
                        if self.sonido_inicio is not None:
                            self._start_ch = self.sonido_inicio.play()
                            self._wait_channel_end = True
                    except pygame.error:
                        self._start_ch = None
                        self._wait_channel_end = False

            # 2) Manejo de teclas (además del engagement)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    # Toggle pausa
                    if self.estado in (EstadoJuego.JUGANDO, EstadoJuego.PREPARADO):
                        self.estado = EstadoJuego.PAUSA
                    elif self.estado == EstadoJuego.PAUSA:
                        self.estado = EstadoJuego.JUGANDO
                elif evento.key == pygame.K_RETURN and self.estado in (EstadoJuego.VICTORIA, EstadoJuego.DERROTA):
                    self.reiniciar_juego()
                elif self.estado == EstadoJuego.PAUSA:
                    # Atajos en pausa
                    if evento.key == pygame.K_g:
                        self.guardar_juego()
                    elif evento.key == pygame.K_c:
                        self.cargar_juego()
                    elif evento.key == pygame.K_q:
                        return False
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

        # HUD
        texto = self.fuente_pequenia.render(
            f"Puntuación: {self.pacman.puntuacion}   Vidas: {self.pacman.vidas}",
            True, COLOR_TEXTO
        )
        self.pantalla.blit(texto, (20, 10))

        # Mundo y personajes
        self.mapa.dibujar(self.pantalla)
        self.pacman.dibujar(self.pantalla)
        self.pinky.dibujar(self.pantalla)
        self.blinky.dibujar(self.pantalla)
        self.clyde.dibujar(self.pantalla)
        self.inky.dibujar(self.pantalla)

        # Mensajes según estado (no bloqueante)
        if self.estado == EstadoJuego.PREPARADO:
            self.mostrar_mensaje("READY!")
        elif self.estado == EstadoJuego.VICTORIA:
            self.mostrar_mensaje("¡VICTORIA!", -40)
            self.mostrar_mensaje("Presiona ENTER para jugar de nuevo", 40, COLOR_TEXTO)
        elif self.estado == EstadoJuego.DERROTA or self.pacman.vidas <= 0:
            self.estado = EstadoJuego.DERROTA
            self.mostrar_mensaje("¡Has Perdido!", -60, color=(255, 0, 0))
            self.mostrar_mensaje(f"Puntos Obtenidos: {self.pacman.puntuacion}", 0, color=(255, 255, 255))
            self.mostrar_mensaje("ESC: salir   ENTER: reiniciar", 60, color=(255, 255, 255))

        # Overlay de pausa por encima
        if self.estado == EstadoJuego.PAUSA:
            self.dibujar_pausa()

        # Modal no bloqueante
        if self.modal:
            if time.time() < self.modal["hasta"]:
                fondo_modal = pygame.Surface((300, 100))
                fondo_modal.set_alpha(200)
                fondo_modal.fill(self.modal["cfondo"])
                rect_modal = fondo_modal.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))

                texto = self.fuente_pequenia.render(self.modal["msg"], True, self.modal["ctexto"])
                texto_rect = texto.get_rect(center=rect_modal.center)

                self.pantalla.blit(fondo_modal, rect_modal)
                self.pantalla.blit(texto, texto_rect)
            else:
                self.modal = None

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

    # (Ya no se usa una pantalla de derrota bloqueante)
    def mostrar_pantalla_derrota(self):
        pass

    def ejecutar(self):
        jugando = True
        reloj = pygame.time.Clock()

        while jugando:
            jugando = self.manejar_eventos()

            # Verificar derrota
            if self.pacman.vidas <= 0:
                self.estado = EstadoJuego.DERROTA

            movimiento = self.capturar_movimiento()

            if self.estado == EstadoJuego.PREPARADO:
                if time.time() - self.tiempo_inicio >= TIEMPO_INICIO_JUEGO:
                    self.estado = EstadoJuego.JUGANDO

            # Lógica de juego
            if self.estado == EstadoJuego.JUGANDO and movimiento:
                self.pacman.mover(movimiento, self.mapa, self.activar_modo_frightened, self.fantasmas)
                self.puntos_recolectados = self.pacman.puntos_recolectados
                self.actualizar_estado()

            if self.estado == EstadoJuego.JUGANDO:
                self.contador_fruta += 1
                if self.contador_fruta > 300:
                    self.mapa.generar_fruta_aleatoria()
                    self.contador_fruta = 0

                if self.contador_fruta % 2 == 0:
                    self.pinky.mover(self.pacman, self.mapa)
                    self.blinky.mover(self.pacman, self.mapa)
                    self.clyde.mover(self.pacman, self.mapa)
                    self.inky.mover(self.pacman, self.blinky, self.mapa)

                # Actualizaciones de estado
                self.pinky.actualizar_frightened()
                self.blinky.actualizar_frightened()
                self.clyde.actualizar_frightened()
                self.inky.actualizar_frightened()

                # Colisiones
                self.pinky.verificar_colision_con_pacman(self.pacman)
                self.blinky.verificar_colision_con_pacman(self.pacman)
                self.clyde.verificar_colision_con_pacman(self.pacman)
                self.inky.verificar_colision_con_pacman(self.pacman)

            # Dibujar
            self.dibujar_juego()

            # Cuando el jingle termina, arrancar música de fantasmas (sin timer)
            if self.AUDIO_OK and self._wait_channel_end:
                ready = (self._start_ch is None) or (not self._start_ch.get_busy())
                if ready:
                    try:
                        pygame.mixer.music.load(self.sonido_fantasmas)
                        pygame.mixer.music.play(-1)
                    except pygame.error:
                        pass
                    self._wait_channel_end = False

            pygame.display.flip()
            reloj.tick(FPS)

        pygame.quit()


async def main():
    juego = JuegoPacman()
    reloj = pygame.time.Clock()

    while True:
        # Eventos
        if not juego.manejar_eventos():
            break

        # Derrota
        if juego.pacman.vidas <= 0:
            juego.estado = EstadoJuego.DERROTA

        # Movimiento
        movimiento = juego.capturar_movimiento()

        if juego.estado == EstadoJuego.PREPARADO:
            if time.time() - juego.tiempo_inicio >= TIEMPO_INICIO_JUEGO:
                juego.estado = EstadoJuego.JUGANDO

        if juego.estado == EstadoJuego.JUGANDO and movimiento:
            juego.pacman.mover(movimiento, juego.mapa, juego.activar_modo_frightened, juego.fantasmas)
            juego.puntos_recolectados = juego.pacman.puntos_recolectados
            juego.actualizar_estado()

        # Lógica de juego (no bloqueante)
        if juego.estado == EstadoJuego.JUGANDO:
            juego.contador_fruta += 1
            if juego.contador_fruta > 300:
                juego.mapa.generar_fruta_aleatoria()
                juego.contador_fruta = 0

            if juego.contador_fruta % 2 == 0:
                juego.pinky.mover(juego.pacman, juego.mapa)
                juego.blinky.mover(juego.pacman, juego.mapa)
                juego.clyde.mover(juego.pacman, juego.mapa)
                juego.inky.mover(juego.pacman, juego.blinky, juego.mapa)

            for fantasma in juego.fantasmas:
                fantasma.actualizar_frightened()
                fantasma.verificar_colision_con_pacman(juego.pacman)

        # Dibujar
        juego.dibujar_juego()

        # Cuando el jingle termina, arrancar música de fantasmas (sin timer)
        if juego.AUDIO_OK and juego._wait_channel_end:
            ready = (juego._start_ch is None) or (not juego._start_ch.get_busy())
            if ready:
                try:
                    pygame.mixer.music.load(juego.sonido_fantasmas)
                    pygame.mixer.music.play(-1)
                except pygame.error:
                    pass
                juego._wait_channel_end = False

        pygame.display.flip()
        reloj.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
