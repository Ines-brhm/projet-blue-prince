from .tirage import attend_choix_joueur
class Inventaire:
    def __init__(self):
        self.steps = 700
        self.gold = 10
        self.gems = 100
        self.keys = 10
        self.dice = 10
        self.shovel=0
        self.lockpicks=1
        self.metal_detector=0

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
        
