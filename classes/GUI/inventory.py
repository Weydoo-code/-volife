import json
import pygame

class Inventory:
    def __init__(self):
        self.player_capacity = 10  # Kg (corrigé l'orthographe)
        self.inventory = self.load_inventory()  # Appel de la méthode avec parenthèses
        self.font = pygame.font.Font(None, 36)
    
    def load_inventory(self):
        try:
            with open("save/inventory.json", "r") as f:
                return json.load(f)
        except:
            default_inventory = [{"type": 0, "quantity": 0}]
            self.save_inventory(default_inventory)
            return default_inventory
    
    def save_inventory(self, inventory=None):
        if inventory is None:
            inventory = self.inventory
        with open("save/inventory.json", "w") as f:
            json.dump(inventory, f, indent=4)
            
    def decode_inventory(self):
        if not self.inventory:
            return "Inventaire vide"
        item = self.inventory[0]
        match item["type"]:
            case 0:
                return f"Terre: {item['quantity']}"
            case 1:
                return f"Sable: {item['quantity']}"
            case 2:
                return f"Pierre: {item['quantity']}"
            case _:
                return f"Non reconnu: {item['quantity']}"

    def update(self, screen):
        inventory_decoded = self.decode_inventory()
        text = self.font.render(inventory_decoded, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (1280 // 2, 36)
        screen.blit(text, text_rect)