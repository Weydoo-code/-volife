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
        self.item = self.inventory[0]
        match self.item["type"]:
            case -1:
                return f"Vide"
            case 0:
                return f"Terre: {self.item['quantity']}"
            case 1:
                return f"Sable: {self.item['quantity']}"
            case 2:
                return f"Pierre: {self.item['quantity']}"
            case _:
                return f"Non reconnu: {self.item['quantity']}"

    def update(self, screen):
        inventory_decoded = self.decode_inventory()
        text = self.font.render(inventory_decoded, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (1280 // 2, 36)
        screen.blit(text, text_rect)
        
    def additem(self, quantity=1, type=None):
        match self.item['type']:
            case -1:
                self.weight = 0
                self.item_weight = 0
                self.item_type = self.item['type']                
            case 0:
                self.weight = 1 * self.item['quantity']
                self.item_weight = 1
                self.item_type = self.item['type']
            case 1:
                self.weight = 1.5 * self.item['quantity']
                self.item_weight = 1.5
                self.item_type = self.item['type']
            case 2:
                self.weight = 4 * self.item['quantity']
                self.item_weight = 4
                self.item_type = self.item['type']
            case _:
                return False
        if self.weight < self.player_capacity and (self.weight + self.item_weight) <= self.player_capacity and (type == self.item_type or self.item_type == -1):
            self.item['quantity'] += quantity
            self.item['type'] = type
            return True
        else:
            return False
        
    def dropitem(self, quantity=1):
        if self.item['quantity'] >= 1:
            self.item['quantity'] -= quantity
            if self.item['quantity'] == 0:
                self.item['type'] = -1
    
    def saveinventory(self):
        with open("save/inventory.json", "w") as f:
            json.dump(self.inventory, f, indent=4)