import inventory as inv


class entity:
    def __init__(self, health, inventory, name=None, defense=0, damage=10, drops=[]):
        self.stats = {
            "health": health,
            "defense": defense,
            "damage": damage
        }
        self.heldItem = None
        self.inventory = inventory
        self.name = name
        self.drops = drops

    def take_damage(self, dmg):
        damage = dmg - self.stats["defense"]
        damage = damage if damage > 0 else 0
        self.stats["health"] -= damage 
        return damage

    def deal_damage(self, target):
        if type(target) == entity:
            return target.take_damage(self.stats["damage"])
        else:
            print(
                f"Could not deal damage")

    def equipItem(self, item):
        itemIndex = self.inventory.find_item(item)
        if itemIndex == -1:
            return f"You do not have {item} in your inventory!"

        item = self.inventory.items[itemIndex]
        return item.equip(item, self)

    def useItem(self, item):
        itemIndex = self.inventory.find_item(item)
        if itemIndex == -1:
            return f"You do not have {item} in your inventory!"

        item = self.inventory.items[itemIndex]
        return item.use(item, self)
