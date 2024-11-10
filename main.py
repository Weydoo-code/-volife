import pygame
import os
import json
from classes.entities.player import Player
from classes.GUI.inventory import Inventory
from tile_actions import *

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
    global running, player, mov, key_states, map, inventory
    running = True
    mov = "idle"
    map = load_map()
    player = Player(screen.get_width() / 2 - tile_size / 2, 
                    screen.get_height() / 2 - tile_size / 2, 
                    tile_size)
    inventory = Inventory()
    key_states = {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
    
def load_texture():
    global texture_hover, texture_debug, texture_grass, texture_sand, texture_stone
    texture_grass = pygame.image.load("ressources/tiles/grass.png").convert_alpha()
    texture_sand = pygame.image.load("ressources/tiles/sand.png").convert_alpha()
    texture_stone = pygame.image.load("ressources/tiles/stone.png").convert_alpha()
    
    texture_hover = pygame.image.load("ressources/tiles/hover.png").convert_alpha()
    texture_debug = pygame.image.load("ressources/tiles/debug.png").convert_alpha()

def load_map():
    file_path = "save/map.json"
    
    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print(f"Le fichier {file_path} n'existe pas. Création d'une nouvelle carte.")
        return create_new_map()
    
    # Lire le contenu du fichier
    with open(file_path, "r") as fichier:
        content = fichier.read().strip()
    
    # Vérifier si le fichier est vide
    if not content:
        print(f"Le fichier {file_path} est vide. Création d'une nouvelle carte.")
        return create_new_map()
    
    # Essayer de charger le JSON
    try:
        map = json.loads(content)
        return map
    except json.JSONDecodeError:
        print(f"Le fichier {file_path} ne contient pas de JSON valide. Création d'une nouvelle carte.")
        return create_new_map()

def create_new_map():
    # Créer une nouvelle carte (22 lignes x 39 colonnes remplie de zéros)
    new_map = [[0 for _ in range(39)] for _ in range(22)]
    
    # Sauvegarder la nouvelle carte dans le fichier
    with open("save/map.json", "w") as fichier:
        json.dump(new_map, fichier, indent=4)
    
    return new_map

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
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key in key_states:
                key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in key_states:
                key_states[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_x, mouse_y = event.pos
                tile_x = (mouse_x - 16) // tile_size
                tile_y = (mouse_y - 8) // tile_size
                if 0 <= tile_x < 39 and 0 <= tile_y < 22:
                    match map[tile_y][tile_x]:
                        case 0:
                            grass_action()
                        case 1:
                            sand_action()
                        case 2:
                            stone_action()
                        case _:
                            print(f"Type de tile {map[tile_y][tile_x]} non reconu.")

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
            
            match map[y][x]:
                case 0:
                    texture_adapted = texture_grass
                case 1:
                    texture_adapted = texture_sand
                case 2:
                    texture_adapted = texture_stone
                case _:
                    texture_adapted = texture_debug
            
            screen.blit(texture_adapted, (tile_x, tile_y))
            if tile_rect.collidepoint(mouse_pos):
                screen.blit(texture_hover, (tile_x, tile_y))
    
    player.update(current_time, mov)
    player.draw(screen, mov)
    
    inventory.update(screen)
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()