import inventory as inv

class entity:
    def __init__(self, health, inventory):
        self.health = health
        self.heldItem = None
        self.inventory = inventory
        self.x = 0
        self.y = 0

    def take_damage(self, dmg):
        self.health -= dmg

    def deal_damage(self, target):
        if self.heldItem and type(target) == entity:
            target.take_damage(self.heldItem.stats["damage"])
        else:
            # Error Message!
            print(f"Could not deal damage\nHeld Item: {self.heldItem}\nIs Player an entity: {type(player) == entity}")

    def equipItem(self, item):
        item = self.inventory.items[self.inventory.find_item(item)]
        item.equip(item, self)
        

    def move(self, direction = [0, 0], step = 1):
        self.x += direction[0] * step
        self.y += direction[1] * step


