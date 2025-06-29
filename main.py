#main

import pygame
import random

pygame.init()

# Configurar la pantalla (ALTO/ANCHO)
ANCHO_VENTANA = 800  
ALTO_VENTANA = 600
screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Os-Car")

# Colores
COLOR_01 = (0, 0, 0) #NEGRO
COLOR_02 = (255, 255, 255) #BLANCO
COLOR_03 = (255, 0, 0) #ROJO

# Jugador 
jugador_ancho = 50
jugador_alto = 50
jugador = pygame.Rect(
    (ANCHO_VENTANA // 2) - (jugador_ancho // 2),
    ALTO_VENTANA - (jugador_alto + 10),  
    jugador_ancho,
    jugador_alto
)

# Competidores
competidor_ancho = 50
competidor_alto = 50
competidores = []

# Puntuación 
puntuacion = 0
font = pygame.font.Font(None, 36)  

# Reloj
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
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
            
    # Colisiones
    for competidor in competidores:
        if jugador.colliderect(competidor):
            running = False
    
    # Dibujar 
    screen.fill(COLOR_01)
    pygame.draw.rect(screen, COLOR_02, jugador)
    for competidor in competidores:
        pygame.draw.rect(screen, COLOR_03, competidor)
    
    # Mostrar puntuación 
    puntuacion_text = font.render(f"Puntuacion: {puntuacion}", True, COLOR_02)  #parámetros normales
    screen.blit(puntuacion_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()