from .tirage import attend_choix_joueur
#from .consomable import Dice, RabbitFoot
#from .permanent_items import MetalDetector , Shovel, Lockpick
from .items import MetalDetector , Shovel, Lockpick , Dice, RabbitFoot
class Inventaire:
    def __init__(self):
        self.steps = 700
        self.gold = 10
        self.gems = 100
        self.keys = 10
        self.dice = 10
        self.shovel=1
        self.lockpicks=1
        self.metal_detector=0
        self.rabbit_foot=0
        self._registry = {
            "dice": Dice(),
            "lockpick": Lockpick(),
            "shovel": Shovel(),
            "rabbit_foot": RabbitFoot(),
            "metal_detector": MetalDetector(),
        }

    def depenser_step(self) -> bool:
        if self.steps <= 0: return False
        self.steps -= 1; return True

    def payer_gemmes(self, n:int) -> bool:
        if self.gems >= n:
            self.gems -= n; return True
        return False
    def use_dice(self,manoir,joueur) :
        if self.dice >0:
            self.dice-=1
            rooms =attend_choix_joueur(manoir, joueur)
            return True,rooms
        return False , []
    
    def use_item(self, item_id: str, manoir=None, joueur=None) -> bool:
        item = self._registry.get(item_id)
        if not item:
            return False,[]
        return item.use(self, manoir, joueur)
        
