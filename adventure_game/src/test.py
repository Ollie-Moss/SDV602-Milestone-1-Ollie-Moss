import inventory as inv 
import monster_fight as mf

sword = inv.Item("sword", "weapon", {"damage" : 100});
helmet = inv.Item("helmet", "armor", {"defense" : 30});
grapes = inv.Item("grape", "food", {"health" : 25});
bread_loaf = inv.Item("bread loaf", "food", {"health" : 100});

playerInv = inv.Inventory([[sword, 1], [helmet, 1], [grapes, 12], [bread_loaf, 3]])
player = mf.entity(100, playerInv)

player.equipItem(sword)

monsterInv = inv.Inventory([[sword, 1]])
monster = mf.entity(100, monsterInv)

print(monster.health)
player.deal_damage(monster)
print(monster.health)
