#main

import pygame
import os
from juego import Juego

def main():
    pygame.init()
    pygame.mixer.init()

    ANCHO_VENTANA = 800
    ALTO_VENTANA = 600
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Os-Car")

    # Puedes pasar screen y rutas a la clase Juego
    assets_dir = os.path.dirname(__file__)
    imagenes_dir = os.path.join(assets_dir, "assets", "images")

    juego = Juego(screen, imagenes_dir)
    juego.ejecutar()

    pygame.quit()

if __name__ == "__main__":
    main()