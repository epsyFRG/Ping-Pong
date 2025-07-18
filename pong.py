# Importo le librerie
import pygame # Libreria per creare giochi 2D
import sys # Libreria standard di Python (es. Chiudere il programma)
import random # Libreria per scegliere casualmeente tra una lista di valori

# Inizializzo le funzioni
pygame.init() # Attiva tutte le funzioni pygame
pygame.mixer.init() # Attiva il modulo audio di pygame
pygame.mixer.music.load("assets/sounds/background.mp3") # Carica la musica di sottofondo
pygame.mixer.music.set_volume(0.2) # Imposta il volume del backgroun
pygame.mixer.music.play(-1) # Loop infinito della musica

# Definisco alcune variabili
WIDTH, HEIGHT = 1024, 768 # Dimensione della finestra del gioco
WHITE = (255, 255, 255) # Colori utilizzati nel gioco
BLACK = (0, 0, 0) # Colori utilizzati nel gioco x2
BALL_SPEED = 5 # Velocità della pallina
COBALT_BLUE = (0, 71, 171) # Colori utilizzati nel gioco x3
GOLD = (255, 215, 0) # Colori utilizzati nel gioco x4
RED = (255, 0, 0) # Colore rosso per collisione

# Creazione della finestra del gioco + Titolo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Epsy Pong Game")

# Inizializzazione delle posizioni e velocità
ball_x, ball_y = WIDTH // 2, HEIGHT // 2 # Posizione iniziale della pallina (al centro)
ball_speed_x, ball_speed_y = BALL_SPEED, BALL_SPEED # Velocità iniziali della pallina
paddle_width, paddle_height = 15, 60 # Dimensioni delle racchette
left_paddle_x, right_paddle_x = 10, WIDTH - 25 # Posizione orizzontale delle racchette
left_paddle_y = HEIGHT // 2 - paddle_height // 2  # Posizione verticale delle racchette
right_paddle_y = HEIGHT // 2 - paddle_height // 2
paddle_speed = 7 # Velocità delle racchette
score_left, score_right = 0, 0 # Punteggio

# Font per mostrare lo score
font = pygame.font.Font(None, 36)   

# Caricamento della pallina come immagine
ball_image = pygame.image.load("assets/images/ball.png").convert_alpha()
ball_image = pygame.transform.scale(ball_image, (64, 64))

# Caricamento dei suoni per lo score
score_sounds = [
    pygame.mixer.Sound("assets/sounds/score1.mp3"),
    pygame.mixer.Sound("assets/sounds/score2.mp3")
]

# Funzione per reimpostare la pallina dopo un punto
def reset_ball():
    return WIDTH // 2, HEIGHT // 2, BALL_SPEED, BALL_SPEED

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Gestione dei tasti per muovere le racchette
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= paddle_speed
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - paddle_height:
        left_paddle_y += paddle_speed
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - paddle_height:
        right_paddle_y += paddle_speed

# Aggiorna la posizione della pallina   
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collisione con le racchette
    if (
        left_paddle_x < ball_x < left_paddle_x + paddle_width
        and left_paddle_y < ball_y < left_paddle_y + paddle_height
    ) or (
        right_paddle_x < ball_x < right_paddle_x + paddle_width
        and right_paddle_y < ball_y < right_paddle_y + paddle_height
    ):
        ball_speed_x = -ball_speed_x

    # Collisione con i bordi superiore e inferiore
    if ball_y <= 0 or ball_y >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Punto peer il giocatore destro
    if ball_x <= 0:
        score_right += 1
        random.choice(score_sounds).play()
        ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()

    # Punto peer il giocatore sinistro
    if ball_x >= WIDTH:
        score_left += 1
        random.choice(score_sounds).play()
        ball_x, ball_y, ball_speed_x, ball_speed_y = reset_ball()

    # Disegno tutti gli elementi ad ogni frame
    screen.fill(COBALT_BLUE) # Sfondo blu cobalto
    pygame.draw.rect(screen, GOLD, (left_paddle_x, left_paddle_y, paddle_width, paddle_height)) # Disegna la racchetta sinistra
    pygame.draw.rect(screen, RED, (right_paddle_x, right_paddle_y, paddle_width, paddle_height)) # Disegna la racchetta destra
    screen.blit(ball_image, (ball_x - ball_image.get_width() // 2, ball_y - ball_image.get_height() // 2)) # Disegna la pallina
    score_display = font.render(f"{score_left} : {score_right}", True, WHITE) # Crea lo score
    screen.blit(score_display, (WIDTH // 2 - 40, 10)) # Disegna lo score a schermo

    pygame.display.flip() # Aggiorna la schermata per mostrare tutto a schermo
    pygame.time.Clock().tick(60) # Limita il framerate a 60 FPS