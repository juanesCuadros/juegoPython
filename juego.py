import pygame
import random

# Inicializar PyGame
pygame.init()

# Dimensiones de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Recoge las Estrellas")

# Colores
COLOR_FONDO = (0, 0, 30)
COLOR_JUGADOR = (0, 255, 0)
COLOR_ESTRELLA = (255, 215, 0)
COLOR_ENEMIGO = (255, 0, 0)
COLOR_TEXTO = (255, 255, 255)

# Parámetros del jugador
jugador_tamano = 50
jugador_x, jugador_y = ANCHO // 2, ALTO // 2
velocidad_jugador = 10

# Parámetros de la estrella
estrella_tamano = 30

# Parámetros del enemigo
enemigo_tamano = 40
velocidad_enemigo = 3

# Fuente para el texto
fuente = pygame.font.Font(None, 36)

# Funciones del juego
def menu_principal():
    pantalla.fill(COLOR_FONDO)
    texto = fuente.render("Presiona ESPACIO para empezar a jugar", True, COLOR_TEXTO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    pygame.display.flip()
    espera_inicio()

def espera_inicio():
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                esperando = False

def mover_jugador(teclas, x, y):
    if teclas[pygame.K_LEFT] and x > 0:
        x -= velocidad_jugador
    if teclas[pygame.K_RIGHT] and x < ANCHO - jugador_tamano:
        x += velocidad_jugador
    if teclas[pygame.K_UP] and y > 0:
        y -= velocidad_jugador
    if teclas[pygame.K_DOWN] and y < ALTO - jugador_tamano:
        y += velocidad_jugador
    return x, y

def crear_estrella():
    x = random.randint(0, ANCHO - estrella_tamano)
    y = random.randint(0, ALTO - estrella_tamano)
    return pygame.Rect(x, y, estrella_tamano, estrella_tamano)

def crear_enemigo():
    x = random.randint(0, ANCHO - enemigo_tamano)
    y = random.randint(0, ALTO - enemigo_tamano)
    return pygame.Rect(x, y, enemigo_tamano, enemigo_tamano)

def mover_enemigos(enemigos, jugador_rect):
    for enemigo in enemigos:
        if enemigo.x < jugador_rect.x:
            enemigo.x += velocidad_enemigo
        elif enemigo.x > jugador_rect.x:
            enemigo.x -= velocidad_enemigo
        if enemigo.y < jugador_rect.y:
            enemigo.y += velocidad_enemigo
        elif enemigo.y > jugador_rect.y:
            enemigo.y -= velocidad_enemigo

def detectar_colision(jugador, objeto):
    return jugador.colliderect(objeto)

def mostrar_puntaje(puntaje):
    texto = fuente.render(f"Puntaje: {puntaje}", True, COLOR_TEXTO)
    pantalla.blit(texto, (10, 10))

# Loop principal del juego
def juego():
    puntaje = 0
    reloj = pygame.time.Clock()
    enemigos = []
    estrella = crear_estrella()
    
    jugando = True
    while jugando:
        pantalla.fill(COLOR_FONDO)
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Movimiento del jugador
        teclas = pygame.key.get_pressed()
        global jugador_x, jugador_y
        jugador_x, jugador_y = mover_jugador(teclas, jugador_x, jugador_y)
        
        # Crear enemigo nuevo por cada estrella recogida
        jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_tamano, jugador_tamano)
        if detectar_colision(jugador_rect, estrella):
            puntaje += 1
            estrella = crear_estrella()
            enemigos.append(crear_enemigo())
        
        # Mover enemigos hacia el jugador
        mover_enemigos(enemigos, jugador_rect)
        
        # Verificar colisiones con enemigos
        for enemigo in enemigos:
            if detectar_colision(jugador_rect, enemigo):
                jugando = False
        
        # Dibujar jugador, estrella y enemigos
        pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador_rect)
        pygame.draw.rect(pantalla, COLOR_ESTRELLA, estrella)
        for enemigo in enemigos:
            pygame.draw.rect(pantalla, COLOR_ENEMIGO, enemigo)
        
        # Mostrar el puntaje
        mostrar_puntaje(puntaje)
        
        pygame.display.flip()
        reloj.tick(30)
    
    # Fin del juego
    fin_del_juego(puntaje)

def fin_del_juego(puntaje):
    pantalla.fill(COLOR_FONDO)
    texto = fuente.render(f"Fin del Juego - Puntaje: {puntaje}", True, COLOR_TEXTO)
    pantalla.blit(texto, (ANCHO // 2 - texto.get_width() // 2, ALTO // 2))
    texto2 = fuente.render("Presiona R para reiniciar o Q para salir", True, COLOR_TEXTO)
    pantalla.blit(texto2, (ANCHO // 2 - texto2.get_width() // 2, ALTO // 2 + 50))
    pygame.display.flip()
    
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    juego()
                if evento.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Iniciar el juego
menu_principal()
juego()
