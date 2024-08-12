class Item:
    def __init__(self, name, itemType, stats, use = print("No use callback"), equip = print("No equip callback")):
        self.name = name
        self.itemType = itemType
        self.stats = stats
        self.use = use
        self.equip = equip

class InventoryItem(Item):
    def __init__(self, item, quantity):
        super().__init__(item.name, item.itemType, item.stats, item.use, item.equip)
        self.quantity = quantity

class Inventory:
    def __init__(self, items):
        if items:
            self.items = items
        else:
            self.items = []

    def add_item(self, item, quantity):
        if self.find_item(item) == -1:
            self.items.append(InventoryItem(item, quantity))
        else:
            self.items[self.find_item(item)].quantity += quantity 

    def remove_item(self, item):
        if self.find_item(item) == -1:
            return
        del self.items[self.find_item(item)]

    def find_item(self, item):
        for index, heldItem in enumerate(self.items):
            if item == heldItem.name:
                return index
        return -1

    def display_items(self):
        result = ""
        for item in self.items:
            result += f"{item.name} x{item.quantity}\n"
        return result
    
