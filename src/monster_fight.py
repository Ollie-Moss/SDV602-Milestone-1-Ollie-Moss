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
        self.stats["health"] -= dmg

    def deal_damage(self, target):
        if self.heldItem and type(target) == entity:
            target.take_damage(self.heldItem.stats["damage"])
        else:
            # Error Message!
            print(
                f"Could not deal damage\nHeld Item: {self.heldItem}")

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
