import pygame
import os
import json
import time
import configparser
from classes.entities.player import Player
from classes.GUI.inventory import Inventory
from tile_actions import *

pygame.init()

# Variables
width = 1280
height = 720
clock = pygame.time.Clock()
fps = 60
tile_size = 32

# Couleurs
white = (255, 255, 255)
black = (0, 0, 0)

# Créer la fenêtre
icon = pygame.image.load("ressources/GUI/icone.png")
pygame.display.set_caption("Évolife")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode(size=(width, height))

os.system("cls")

# Définition des fonctions
def create_fps_text():
    fps = str(int(clock.get_fps()))
    font = pygame.font.Font(None, 30)
    return font.render(f"FPS: {fps}", True, (255, 255, 255))

def load_config():
    global controls
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    controls = {}
    for key, value in config['KEY'].items():
        controls[key] = getattr(pygame, value)

def reset_var():
    global running, player, mov, key_states, map, inventory, drop_key_pressed, drop_time
    running = True
    drop_time = time.time()
    mov = "idle"
    map = load_map()
    player_data = load_data()
    player = Player(player_data["playerx"], player_data["playery"], tile_size)
    inventory = Inventory()
    drop_key_pressed = False
    key_states = {controls['up']: False, controls['down']: False, controls['left']: False, controls['right']: False}
    
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
        return create_new_map()

def create_new_map():
    new_map = [[0 for _ in range(39)] for _ in range(22)]
    
    with open("save/map.json", "w") as fichier:
        json.dump(new_map, fichier, indent=4)
    
    return new_map

def save_data():
    data = {
        "playerx": player.pos.x,
        "playery": player.pos.y
    }
    with open("save/player.json", "w") as fichier:
        json.dump(data, fichier, indent=4)

def load_data():
    file_path = "save/player.json"
    default_data = {"playerx": width // 2, "playery": height // 2}  # Valeurs par défaut

    if not os.path.exists(file_path):
        print("Fichier de sauvegarde non trouvé. Utilisation des valeurs par défaut.")
        return default_data

    try:
        with open(file_path, "r") as fichier:
            data = json.load(fichier)
        
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        if "playerx" in data and "playery" in data:
            return data
        else:
            return default_data
    except:
        return default_data
            

# Boucle principale du jeu
load_config()
reset_var()
load_data()
load_texture()
while running:
    mouse_pos = pygame.mouse.get_pos()
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_data()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == controls['drop']:
                drop_key_pressed = True
            if event.key in key_states:
                key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key == controls['drop']:
                drop_key_pressed = False
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
                            grass_action(inventory=inventory)
                        case 1:
                            sand_action(inventory=inventory)
                        case 2:
                            stone_action(inventory=inventory)
                        case _:
                            pass

    mov = "idle"
    if key_states[controls['up']] and player.pos.y > 27:
        player.move(0, -1)
        mov = "back"
    if key_states[controls['down']] and player.pos.y < 695:
        player.move(0, 1)
        mov = "front"
    if key_states[controls['left']] and player.pos.x > 33:
        player.move(-1, 0)
        mov = "left"
    if key_states[controls['right']] and player.pos.x < 1247:
        player.move(1, 0)
        mov = "right"
    if drop_key_pressed:
        if drop_time <= time.time():
            inventory.dropitem()
            drop_time = time.time() + 0.2
    
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
    inventory.saveinventory()
    
    fps_text = create_fps_text()
    screen.blit(fps_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()