# config.py
import os

# Colores
COLOR_FONDO = (0, 0, 0)
COLOR_PUNTO = (255, 255, 255)  # Blanco para puntos
COLOR_PILDORA = (255, 255, 255)  # Blanco para píldoras
COLOR_PARED = (0, 0, 255)  # Azul para paredes
COLOR_TEXTO = (255, 255, 255)  # Blanco para textos
COLOR_VICTORIA = (255, 255, 0)  # Amarillo para mensaje de victoria

# Dimensiones de pantalla
ANCHO_VENTANA = 839
ALTO_VENTANA = 641
ESPACIO_HUD = 50

# Tamaño de las celdas en el mapa
TAMAÑO_CELDA = 31

# Temporización
TIEMPO_INICIO_JUEGO = 3  # Segundos para el mensaje "Ready"
FPS = 10  # Fotogramas por segundo del juego


# Estados del juego
class EstadoJuego:
    INICIO = "inicio"
    PREPARADO = "preparado"
    JUGANDO = "jugando"
    VICTORIA = "victoria"


# Rutas de recursos
RUTA_IMAGEN_CEREZA = os.path.join("img", "Cereza.png")
RUTA_IMAGEN_PACMAN = [os.path.join("img", f"Pacman{i}.png") for i in range(1, 5)]
