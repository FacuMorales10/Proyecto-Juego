import pygame
import random
import os

class Juego:
    def __init__(self, screen, imagenes_dir):
        self.screen = screen
        self.ANCHO_VENTANA = screen.get_width()
        self.ALTO_VENTANA = screen.get_height()
        self.imagenes_dir = imagenes_dir

        # Colores
        self.COLOR_01 = (0, 0, 0) # NEGRO
        self.COLOR_02 = (255, 255, 255) # BLANCO
        self.COLOR_03 = (255, 0, 0) # ROJO
        self.COLOR_DEBUG = (0, 255, 0) # VERDE

        # Imagen del coche del jugador
        self.coche_max_5 = pygame.image.load(os.path.join(self.imagenes_dir, "Max5.png")).convert_alpha()
        self.coche_max_5 = pygame.transform.scale(self.coche_max_5, (65, 110))

        # Jugador
        self.jugador = self.coche_max_5.get_rect()
        self.jugador.centerx = self.ANCHO_VENTANA // 2
        self.jugador.bottom = self.ALTO_VENTANA - 10

        # Competidores
        self.competidor_ancho = 50
        self.competidor_alto = 50
        self.competidores = []

        # Puntuación
        self.puntuacion = 0
        self.font = pygame.font.Font(None, 36)

        # Reloj
        self.clock = pygame.time.Clock()

    def ejecutar(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Mover jugador
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.jugador.left > 0:
                self.jugador.x -= 5
            if keys[pygame.K_RIGHT] and self.jugador.right < self.ANCHO_VENTANA:
                self.jugador.x += 5
            if keys[pygame.K_UP] and self.jugador.top > 0:
                self.jugador.y -= 5
            if keys[pygame.K_DOWN] and self.jugador.bottom < self.ALTO_VENTANA:
                self.jugador.y += 5

            # Rivales
            if len(self.competidores) < 5:
                nuevo_competidor = pygame.Rect(
                    random.randint(0, self.ANCHO_VENTANA - self.competidor_ancho),
                    random.randint(-100, -10),
                    self.competidor_ancho,
                    self.competidor_alto
                )
                self.competidores.append(nuevo_competidor)

            # Mover competidores
            for competidor in self.competidores[:]:
                competidor.y += random.randint(1, 8)
                if competidor.top > self.ALTO_VENTANA:
                    self.competidores.remove(competidor)
                    self.puntuacion += 1

            # Colisiones
            for competidor in self.competidores:
                if self.jugador.colliderect(competidor):
                    running = False

            # Dibujar
            self.screen.fill(self.COLOR_01)
            self.screen.blit(self.coche_max_5, self.jugador)
            pygame.draw.rect(self.screen, self.COLOR_DEBUG, self.jugador, 2)
            for competidor in self.competidores:
                pygame.draw.rect(self.screen, self.COLOR_03, competidor)

            # Mostrar puntuación
            puntuacion_text = self.font.render(f"Puntuacion: {self.puntuacion}", True, self.COLOR_02)
            self.screen.blit(puntuacion_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(60)
