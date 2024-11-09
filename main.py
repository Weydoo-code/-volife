import pygame
import os
from classes.entities.player import Player

pygame.init()

# Variables
width = 1280
height = 720
clock = pygame.time.Clock()
fps = 25
tile_size = 32

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)

# Créer la fenêtre
screen = pygame.display.set_mode(size=(width, height))
pygame.display.set_caption("Évolife")

os.system("cls")

# Définition des fonctions
def reset_var():
    global running, player, mov, key_states
    running = True
    mov = "idle"
    player = Player(screen.get_width() / 2 - tile_size / 2, 
                    screen.get_height() / 2 - tile_size / 2, 
                    tile_size)
    key_states = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    
def load_texture():
    global texture_sol, texture_hover
    texture_sol = pygame.image.load("ressources/tiles/grass.png").convert_alpha()
    texture_hover = pygame.image.load("ressources/tiles/hover.png").convert_alpha()

# Boucle principale du jeu
reset_var()
load_texture()
while running:
    mouse_pos = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # if event.key == pygame.K_ESCAPE:
            #     running = False
            if event.key in key_states:
                key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in key_states:
                key_states[event.key] = False

    mov = "idle"
    if key_states[pygame.K_UP] and player.pos.y > 27:
        player.move(0, -1)
        mov = "back"
    if key_states[pygame.K_DOWN] and player.pos.y < 695:
        player.move(0, 1)
        mov = "front"
    if key_states[pygame.K_LEFT] and player.pos.x > 33:
        player.move(-1, 0)
        mov = "left"
    if key_states[pygame.K_RIGHT] and player.pos.x < 1247:
        player.move(1, 0)
        mov = "right"

    screen.fill(black)
    for x in range(39):
        for y in range(22):
            tile_x = x * tile_size + 16
            tile_y = y * tile_size + 8
            tile_rect = pygame.Rect(tile_x, tile_y, tile_size, tile_size)
            
            if tile_rect.collidepoint(mouse_pos):
                screen.blit(texture_sol, (tile_x, tile_y))
                screen.blit(texture_hover, (tile_x, tile_y))
            else:
                screen.blit(texture_sol, (tile_x, tile_y))
    
    player.update(current_time, mov)
    player.draw(screen, mov)
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()