class Item:
    def __init__(self, name, itemType, stats):
        self.name = name
        self.itemType = itemType
        self.stats = stats

"""
Example: 
Input:
items = [
        [item, quantity],
        [item, quantity],
        [item, quantity]
        ]
Output:
inventory.items = [
                    {
                    "item" : item,
                    "quantity" : quantity 
                    },
                    {
                    "item" : item,
                    "quantity" : quantity 
                    },
                    {
                    "item" : item,
                    "quantity" : quantity 
                    }
]
"""
class Inventory:
    def __init__(self, items):
        if items:
            self.items = list(map(items_with_quantity, items))
        else:
            self.items = []

    def add_item(self, item, quantity):
        if self.find_item(item) == -1:
            self.items.append(items_with_quantity([item, quantity]))
        else:
            self.items[self.find_item(item)]["quantity"] += quantity 

    def remove_item(self, item):
        if self.find_item(item) == -1:
            return
        del self.items[self.find_item(item)]

    def find_item(self, item):
        for index, heldItem in enumerate(self.items):
            if item == heldItem["item"]:
                return index
        return -1

    def display_items(self):
        result = ""
        for item in self.items:
            result += f"{item['item'].name} x{item['quantity']}\n"
        return result
    
def items_with_quantity(item):
    return {
            "item" : item[0],
            "quantity" : item[1]
            }
