import inventory as inv


class entity:
    def __init__(self, health, inventory, name=None):
        self.stats = {
            "health": health
        }
        self.heldItem = None
        self.inventory = inventory
        self.name = name

    def take_damage(self, dmg):
        damage = dmg - self.stats["dmg"]
        damage = damage if damage > 0 else 0
        self.stats["health"] -= damage 
        return damage

    def deal_damage(self, target):
        if type(target) == entity:
            target.take_damage(self.stats["damage"])
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
