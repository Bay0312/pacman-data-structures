import os

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_PUNTO = (255, 255, 255)  # Blanco para puntos
COLOR_PILDORA = (255, 255, 255)  # Blanco para píldoras
COLOR_PARED = (0, 0, 255)  # Azul para paredes
COLOR_TEXTO = (255, 247, 0)  # RGB
COLOR_VICTORIA = (255, 255, 0)  # Amarillo para mensaje de victoria
GROSOR_BORDE = 4  # Grosor del borde de las paredes

# Dimensiones de pantalla
ANCHO_VENTANA = 839
ALTO_VENTANA = 641
ESPACIO_HUD = 50

# Tamaño de las celdas en el mapa
TAMANIO_CELDA = 31

# Temporización
TIEMPO_INICIO_JUEGO = 3  # Segundos para el mensaje "Ready"
FPS = 10  # Fotogramas por segundo del juego


# Estados del juego
class EstadoJuego:
    INICIO = "inicio"
    PREPARADO = "preparado"
    JUGANDO = "jugando"
    VICTORIA = "victoria"
    DERROTA = "derrota"
    PAUSA = "pausa"


# Rutas de recursos
RUTA_IMAGEN_CEREZA = os.path.join("img", "Cereza.png")
RUTA_IMAGEN_PACMAN = [os.path.join("img", f"Pacman{i}.png") for i in range(1, 5)]
RUTA_IMAGEN_PINKY = [os.path.join("Fantasmas", "Pinky", f"Pinky{i}.png") for i in range(1, 3)]
RUTA_IMAGEN_CLYDE = [os.path.join("Fantasmas", "Clyde", f"Clyde{i}.png") for i in range(1, 3)]
RUTA_IMAGEN_BLINKY = [os.path.join("Fantasmas", "Blinky", f"Blinky{i}.png") for i in range(1, 3)]
RUTA_IMAGEN_INKY = [os.path.join("Fantasmas", "Inky", f"Inky{i}.png") for i in range(1, 3)]
# RUTA_IMAGEN_ASUSTADO = [os.path.join("Fantasmas", "FantasmaAsustado", f"FantasmaAsustado{i}.png") for i in range(1, 3)]
RUTA_IMAGEN_ASUSTADO = os.path.join("Fantasmas", "FantasmaAsustado", "FantasmaAsustado1.png")
RUTA_SONIDO_INICIO = os.path.join("sonidos", "pacman.ogg")
RUTA_SONIDO_FANTASMAS = os.path.join("sonidos", "fantasmas.ogg")
RUTA_SONIDO_FIN_JUEGO = os.path.join("sonidos", "gameover.ogg")