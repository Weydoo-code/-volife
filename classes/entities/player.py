import pygame

class Player:
    def __init__(self, x, y, tile_size):
        self.pos = pygame.Vector2(x + tile_size / 2, y)
        self.tile_size = tile_size
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 200
        self.speed = 3
        self.load_textures()

    def load_textures(self):
        directions = ['idle', 'front', 'back', 'left', 'right']
        self.textures = {direction: [
            pygame.image.load(f"ressources/sprite/player/{direction}_{i}.png").convert_alpha()
            for i in range(1, 5)
        ] for direction in directions}

    def move(self, dx, dy):
        self.pos.x += dx * self.speed
        self.pos.y += dy * self.speed

    def update(self, current_time, mov):
        if current_time - self.last_update >= self.animation_cooldown:
            if mov != "idle":
                self.current_frame = (self.current_frame + 1) % len(self.textures[mov])
            else:
                self.current_frame = (self.current_frame + 1) % len(self.textures["idle"])
            self.last_update = current_time

    def draw(self, screen, mov="idle"):
        current_sprite = self.textures[mov][self.current_frame]
        sprite_rect = current_sprite.get_rect(center=self.pos)
        screen.blit(current_sprite, sprite_rect)
    
    def set_speed(self, speed):
        self.speed = speed