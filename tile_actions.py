from classes.GUI.inventory import Inventory


def grass_action(inventory):
    inventory.additem(type=0)

def sand_action(inventory):
    inventory.additem(type=1)

def stone_action(inventory):
    inventory.additem(type=2)