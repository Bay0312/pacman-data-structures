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
        # Mixer con buffer más amplio (reduce stutter en web)
        try:
            pygame.mixer.pre_init(44100, -16, 2, 1024)
        except Exception:
            pass

        pygame.init()
        pygame.font.init()

        # Plataforma
        self.IS_WEB = (sys.platform == "emscripten")

        # UI/estado
        self.modal = None

        # AUDIO
        self.AUDIO_OK = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.AUDIO_OK = True
        except pygame.error:
            self.AUDIO_OK = False

        # Evento personalizado de fin de pista (music)
        self._EVT_JINGLE_DONE = pygame.USEREVENT + 1

        # Fases de audio: 'idle' | 'jingle' | 'ghost'
        self._audio_phase = 'idle'
        self._needs_engagement = self.IS_WEB   # en web se requiere primer gesto
        self._user_engaged = False
        self._music_fallback_at = None         # timestamp para fallback del jingle
        self._jingle_len_hint = 3.5            # valor por defecto si no podemos medir

        # Pantalla
        flags = 0
        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), flags)
        pygame.display.set_caption("Pacman")

        # Fuentes
        self.fuente_grande = pygame.font.Font(None, 74)
        self.fuente_pequenia = pygame.font.Font(None, 36)

        # Rutas y recursos de audio
        self.sonido_inicio_path = RUTA_SONIDO_INICIO
        self.sonido_fantasmas_path = RUTA_SONIDO_FANTASMAS
        self.sfx_gameover = None

        if self.AUDIO_OK:
            # Cargar SFX de game over como Sound (corto). Música/jingle se manejan con mixer.music
            try:
                self.sfx_gameover = pygame.mixer.Sound(RUTA_SONIDO_FIN_JUEGO)
            except pygame.error:
                self.sfx_gameover = None

            # Intentar medir duración del jingle usando Sound (solo para length)
            try:
                _s = pygame.mixer.Sound(self.sonido_inicio_path)
                self._jingle_len_hint = max(1.0, min(8.0, _s.get_length()))
                del _s
            except pygame.error:
                pass

        # Estado inicial del juego
        self.reiniciar_juego(first_time=True)

    # -------------------------
    # Utilidades de UI (modal)
    # -------------------------
    def programar_modal(self, mensaje, duracion=2.0, color_fondo=(50, 50, 50), color_texto=(255, 255, 255)):
        self.modal = {
            "msg": mensaje,
            "hasta": time.time() + duracion,
            "cfondo": color_fondo,
            "ctexto": color_texto,
        }

    # -------------------------
    # Audio helpers
    # -------------------------
    def _play_jingle_music(self):
        """Reproduce pacman.ogg con mixer.music (streaming), y al terminar arranca la música de fantasmas.
        Incluye fallback temporal por si no llega el endevent en WASM.
        """
        if not self.AUDIO_OK or not self.sonido_inicio_path:
            return

        # Detener cualquier música previa
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

        # Configurar evento al terminar pista
        try:
            pygame.mixer.music.set_endevent(self._EVT_JINGLE_DONE)
        except pygame.error:
            pass

        # Reproducir jingle con pequeño fade-in
        try:
            pygame.mixer.music.load(self.sonido_inicio_path)
            pygame.mixer.music.play(loops=0, fade_ms=120)
            self._audio_phase = 'jingle'
            # Fallback: un pequeño margen sobre la duración estimada del jingle
            self._music_fallback_at = time.time() + self._jingle_len_hint + 0.6
        except pygame.error:
            # Si falla el jingle, arrancar directamente la música de fantasmas
            self._start_ghost_music()

    def _start_ghost_music(self):
        """Arranca/loopea fantasmas.ogg con fade-in suave."""
        if not self.AUDIO_OK or not self.sonido_fantasmas_path:
            self._audio_phase = 'idle'
            self._music_fallback_at = None
            return

        try:
            # Cancelar eventos de fin de pista para la música en loop
            pygame.mixer.music.set_endevent(0)
        except pygame.error:
            pass

        try:
            pygame.mixer.music.load(self.sonido_fantasmas_path)
            pygame.mixer.music.play(loops=-1, fade_ms=250)
            self._audio_phase = 'ghost'
        except pygame.error:
            self._audio_phase = 'idle'
        finally:
            self._music_fallback_at = None

    def _stop_music(self):
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass
        self._audio_phase = 'idle'
        self._music_fallback_at = None

    # -------------------------
    # Ciclo de vida del juego
    # -------------------------
    def reiniciar_juego(self, first_time=False):
        self.mapa = Mapa()
        self.TAMANIO_CELDA = TAMANIO_CELDA
        self.pacman = PacMan(posicion=(1, 1), tamanio_celda=self.TAMANIO_CELDA)

        # Crear fantasmas
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

        # Alternancia scatter/chase
        self.tiempo_modo = 0
        self.intervalos_modos = [7, 20, 7, 20, 5, 20, 5, 20]
        self.indice_modo = 0
        self.modo_actual = 'scatter'

        # Audio de inicio:
        if self.AUDIO_OK:
            if (not self.IS_WEB) or self._user_engaged:
                self._play_jingle_music()
            else:
                # En web, esperar el primer gesto
                self._audio_phase = 'idle'
                self._music_fallback_at = None

    # -------------------------
    # Persistencia
    # -------------------------
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

        # Aviso visual
        self.programar_modal("Guardado exitoso ✓", duracion=2.5, color_fondo=(30, 120, 30), color_texto=(255, 255, 255))
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

            self.programar_modal("Partida cargada ✓", duracion=2.5, color_fondo=(30, 30, 120), color_texto=(255, 255, 255))
            print("Partida cargada.")
            return True
        except FileNotFoundError:
            self.programar_modal("No hay partida guardada", duracion=2.5, color_fondo=(120, 30, 30), color_texto=(255, 255, 255))
            print("No se encontró ninguna partida guardada.")
            return False

    # -------------------------
    # Render y lógica
    # -------------------------
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
                self._stop_music()
                try:
                    if self.sfx_gameover is not None:
                        self.sfx_gameover.play()
                except pygame.error:
                    pass

        if self.pacman.vidas == 0:
            self.estado = EstadoJuego.DERROTA
            if self.AUDIO_OK:
                self._stop_music()
                try:
                    if self.sfx_gameover is not None:
                        self.sfx_gameover.play()
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

            # Fin del jingle -> arrancar música de fantasmas
            if self.AUDIO_OK and evento.type == self._EVT_JINGLE_DONE:
                if self._audio_phase == 'jingle':
                    self._start_ghost_music()

            # Primer gesto del usuario (solo web) -> desbloquear audio y tocar jingle
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if not self._user_engaged:
                    self._user_engaged = True
                if self._needs_engagement and self.AUDIO_OK:
                    self._needs_engagement = False
                    if self._audio_phase != 'jingle':
                        self._play_jingle_music()

            # Teclas de control
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.estado in (EstadoJuego.JUGANDO, EstadoJuego.PREPARADO):
                        self.estado = EstadoJuego.PAUSA
                    elif self.estado == EstadoJuego.PAUSA:
                        self.estado = EstadoJuego.JUGANDO
                elif evento.key == pygame.K_RETURN and self.estado in (EstadoJuego.VICTORIA, EstadoJuego.DERROTA):
                    self.reiniciar_juego()
                elif self.estado == EstadoJuego.PAUSA:
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

    def dibujar_pausa(self):
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

        # Mensajes según estado
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

        if self.estado == EstadoJuego.PAUSA:
            self.dibujar_pausa()

        # Modal no bloqueante
        if self.modal:
            if time.time() < self.modal["hasta"]:
                fondo_modal = pygame.Surface((320, 110))
                fondo_modal.set_alpha(220)
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

    def _tick_audio_fallback(self):
        """Si no llega endevent del jingle (WASM), arrancar fantasmas tras la duración estimada."""
        if not self.AUDIO_OK:
            return
        if self._audio_phase == 'jingle' and self._music_fallback_at is not None:
            if time.time() >= self._music_fallback_at:
                # Solo si la música ya no está ocupada o si estamos muy pasados de tiempo
                try:
                    busy = pygame.mixer.music.get_busy()
                except pygame.error:
                    busy = False
                if (not busy) or (time.time() - self._music_fallback_at > 0.5):
                    self._start_ghost_music()

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

                self.pinky.actualizar_frightened()
                self.blinky.actualizar_frightened()
                self.clyde.actualizar_frightened()
                self.inky.actualizar_frightened()

                self.pinky.verificar_colision_con_pacman(self.pacman)
                self.blinky.verificar_colision_con_pacman(self.pacman)
                self.clyde.verificar_colision_con_pacman(self.pacman)
                self.inky.verificar_colision_con_pacman(self.pacman)

            self.dibujar_juego()

            # Fallback de audio si hiciera falta
            self._tick_audio_fallback()

            pygame.display.flip()
            reloj.tick(FPS)

        pygame.quit()


async def main():
    juego = JuegoPacman()
    reloj = pygame.time.Clock()

    while True:
        if not juego.manejar_eventos():
            break

        if juego.pacman.vidas <= 0:
            juego.estado = EstadoJuego.DERROTA

        movimiento = juego.capturar_movimiento()

        if juego.estado == EstadoJuego.PREPARADO:
            if time.time() - juego.tiempo_inicio >= TIEMPO_INICIO_JUEGO:
                juego.estado = EstadoJuego.JUGANDO

        if juego.estado == EstadoJuego.JUGANDO and movimiento:
            juego.pacman.mover(movimiento, juego.mapa, juego.activar_modo_frightened, juego.fantasmas)
            juego.puntos_recolectados = juego.pacman.puntos_recolectados
            juego.actualizar_estado()

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

        juego.dibujar_juego()
        juego._tick_audio_fallback()

        pygame.display.flip()
        reloj.tick(FPS)
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
