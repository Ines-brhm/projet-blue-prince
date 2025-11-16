from .tirage import attend_choix_joueur
#from .consomable import Dice, RabbitFoot
#from .permanent_items import MetalDetector , Shovel, Lockpick
from .items import MetalDetector , Shovel, Lockpick , Dice, RabbitFoot
class Inventaire:
    def __init__(self):
        """
        Initialise l’inventaire du joueur avec les ressources de base
        et enregistre les objets utilisables (dés, lockpicks, pelles, etc.).
        """
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
        """
        Retire 1 step si disponible. 
        Retourne True si la dépense est possible, sinon False.
        """
        if self.steps <= 0: return False
        self.steps -= 1; return True

    def payer_gemmes(self, n:int) -> bool:
        """
        Tente de payer n gemmes. 
        Retourne True si le joueur a assez de gemmes, sinon False.
        """
        if self.gems >= n:
            self.gems -= n; return True
        return False
    def use_dice(self,manoir,joueur) :
        """
        Utilise un dé si disponible : décrémente la réserve et 
        génère un nouveau tirage de rooms via attend_choix_joueur.
        Retourne (True, rooms) si réussi, sinon (False, []).
        """
        if self.dice >0:
            self.dice-=1
            rooms =attend_choix_joueur(manoir, joueur)
            return True,rooms
        return False , []
    
    def use_item(self, item_id: str, manoir=None, joueur=None) -> bool:
        """
        Utilise un objet de l’inventaire basé sur son identifiant.
        Cherche l’objet dans le registre puis exécute sa logique.
        Retourne le résultat de l’effet appliqué.
        """
        item = self._registry.get(item_id)
        if not item:
            return False,[]
        return item.use(self, manoir, joueur)
        
