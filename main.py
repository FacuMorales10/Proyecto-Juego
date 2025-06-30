#main

import pygame
import random
import json
import os

pygame.init()
pygame.mixer.init() # Inicializa el mezclador de sonido de Pygame

# Configurar la pantalla (ALTO/ANCHO)
ANCHO_VENTANA = 800  
ALTO_VENTANA = 600
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Os-Car")

# Rutas a tus carpetas de assets

ASSETS_DIR = os.path.dirname(__file__)
IMAGENES_DIR = os.path.join(ASSETS_DIR, "assets", "images")
SONIDOS_DIR = os.path.join(ASSETS_DIR, "assets", "sounds")
MUSICA_DIR = os.path.join(ASSETS_DIR, "assets", "music")

#imagen del coche del jugador

coche_max_5 = pygame.image.load(os.path.join(IMAGENES_DIR, "Max5.png")).convert_alpha()
coche_max_5 = pygame.transform.scale(coche_max_5, (65, 110 ))

# Colores
COLOR_01 = (0, 0, 0) #NEGRO
COLOR_02 = (255, 255, 255) #BLANCO
COLOR_03 = (255, 0, 0) #ROJO
COLOR_04 = (255, 255, 0) #AMARILLO
COLOR_DEBUG = (0, 255, 0) # VERDE

# Jugador 
jugador = coche_max_5.get_rect()
# Posiciona el jugador:Add commentMore actions
jugador.centerx = ANCHO_VENTANA // 2 
jugador.bottom = ALTO_VENTANA - 10 

# Proyectiles 
proyectiles = []
def crear_proyectil(x, y):
    return {
        "rect": pygame.Rect(x - 2, y, 4, 10),
        "speed": 7
    }

def mover_proyectil(proyectil):
    proyectil["rect"].y -= proyectil["speed"]

def dibujar_proyectil(proyectil):
    pygame.draw.rect(screen, COLOR_04, proyectil["rect"])



# Competidores
competidor_ancho = 50
competidor_alto = 50
competidores = []

# Puntuación 
puntuacion = 0
font = pygame.font.Font(None, 36)  

# Tiempo entre disparos
shoot_delay = 250
last_shot = 0

# Reloj
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    current_time = pygame.time.get_ticks()
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and current_time - last_shot > shoot_delay:
                proyectiles.append(crear_proyectil(jugador.centerx, jugador.top))
                last_shot = current_time

    # Mover jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and jugador.left > 0: 
        jugador.x -= 5 
    if keys[pygame.K_RIGHT] and jugador.right < ANCHO_VENTANA:
        jugador.x += 5  
    if keys[pygame.K_UP] and jugador.top > 0:
        jugador.y -= 5  
    if keys[pygame.K_DOWN] and jugador.bottom < ALTO_VENTANA:  
        jugador.y += 5  
        
    # Rivales 
    if len(competidores) < 5:  
        nuevo_competidor = pygame.Rect(
            random.randint(0, ANCHO_VENTANA - competidor_ancho),
            random.randint(-100, -10),
            competidor_ancho,
            competidor_alto
        )
        competidores.append(nuevo_competidor)
    
    # Mover competidores
    for competidor in competidores[:]:
        competidor.y += random.randint(1, 8) #velocidad
        if competidor.top > ALTO_VENTANA:
            competidores.remove(competidor)
            puntuacion += 1
            
    # Mover y dibujar proyectiles
    for proyectil in proyectiles[:]:
        mover_proyectil(proyectil)
        if proyectil["rect"].bottom < 0:
            proyectiles.remove(proyectil)

    # Colisiones
    for competidor in competidores[:]:
        # Colisión con jugador
        if jugador.colliderect(competidor):
            running = False
            
        # Colisión con proyectiles
        for proyectil in proyectiles[:]:
            if competidor.colliderect(proyectil["rect"]):
                competidores.remove(competidor)
                proyectiles.remove(proyectil)
                puntuacion += 5  # Puntos por eliminar
                break
    
    # Dibujar 
    screen.fill(COLOR_01)
    screen.blit(coche_max_5, jugador)
    pygame.draw.rect(screen, COLOR_DEBUG, jugador, 2)  
    for competidor in competidores:
        pygame.draw.rect(screen, COLOR_03, competidor)
        
    for proyectil in proyectiles:
        dibujar_proyectil(proyectil)
    
    # Mostrar puntuación 
    puntuacion_text = font.render(f"Puntuacion: {puntuacion}", True, COLOR_02)  #parámetros normales
    screen.blit(puntuacion_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()