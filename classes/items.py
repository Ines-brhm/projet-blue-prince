# classes/items/base.py
from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional
import random


class Item(ABC):
    """
    Classe abstraite de base pour tous les objets d'inventaire.
    """
    def __init__(self, item_id: str, label: str, stackable: bool = True):
        self.item_id = item_id
        self.label = label
        self.stackable = stackable  # True => quantité, False => binaire/permanent

    @abstractmethod
    def use(self, inv, manoir=None, joueur=None) -> Tuple[bool, Optional[Any]]:
        """
        Applique l'effet de l'objet. Retourne True si consommé/activé, False sinon.
        """
        ...


# ------------------permanent--------------

class MetalDetector(Item):
    def __init__(self):
        super().__init__("metal_detector", "Metal Detector", stackable=False)

    def use(self, inv, manoir=None, joueur=None) -> bool:
        # permanent => pas de décrément ; activer un flag
        inv.metal_detector = 1
        return (True,0.8)


class Shovel(Item):
    def __init__(self):
        super().__init__("shovel", "Shovel", stackable=False)

    def use(self, inv, manoir=None, joueur=None) -> bool:
        if getattr(inv, "shovel", 0) <= 0:
            return (False,[])
        """Tente de creuser dans la salle actuelle avec une pelle."""
        i, j = joueur.i, joueur.j
        salle = manoir.grille[i][j]
        
        if salle is None or inv is None:
            return (False,[])

        # Vérifier que la salle est une Green Room
        if getattr(salle, "couleur", "") != "green":
            manoir.show_message("On ne peut creuser que dans les pièces vertes.", 1.0)
            return (False,[])

        # Vérifier que le joueur a une pelle
        if getattr(inv, "shovel", 0) <= 0:
            manoir.show_message("Tu n'as pas de pelle…", 1.0)
            return (False,[])

        # Consommer une pelle
        p_tresor = 0.30 # 30% de chance de trouver un trésor

        if inv.metal_detector:
            p_tresor = 1.00  # 70% de cahnce  si détecteur de métaux 
                # Consommer 1 détecteur


        # Loot aléatoire
        r = random.random()
        if r > p_tresor:
            manoir.show_message("Tu ne trouves rien en creusant.", 1.0)
            return (False,[])
        
        loot = random.choice(["gold", "gem", "shovel"])

        if loot == "gold":
            gain = random.randint(3, 8)
            inv.gold += gain
            manoir.show_message(f" Détecteur: +{gain} gold !", 1.5)

        elif loot == "gem":
            gain = 1
            inv.gems += gain
            manoir.show_message(f"Détecteur: +{gain} gemme !", 1.5)

        else:  
            inv.shovel += 1
            manoir.show_message(" Détecteur: +1 shovel !", 1.5)


        return (True,[])
    
    
    
class Lockpick(Item):
    def __init__(self):
        super().__init__("lockpick", "Lockpick", stackable=False)

    def use(self, inv, manoir=None, joueur=None) -> bool:
        if getattr(inv, "lockpicks", 0) <= 0:
            return (False,[])
        return (True,[])
    
    
    
#----------------consomable---------------------

class Dice(Item):
    def __init__(self):
        super().__init__("dice", "Die", stackable=True)

    def use(self, inv, manoir=None, joueur=None) -> bool:
        if getattr(inv, "dice", 0) <= 0:
            return (False,[])
        inv.dice -= 1
        # import local pour éviter les imports circulaires
        from classes.tirage import attend_choix_joueur
        rooms = attend_choix_joueur(manoir, joueur)
        # tu peux stocker la liste tirée quelque part si besoin
        # ou retourner True/False selon un contrat défini
        return (True,rooms)





class RabbitFoot(Item):
    def __init__(self):
        super().__init__("rabbit_foot", "Rabbit Foot", stackable=True)

    def use(self, inv, manoir=None, joueur=None) -> bool:
        if getattr(inv, "rabbit_foot", 0) <= 0:
            return False
        # ton design actuel consomme tous les “pieds de lapin” dans piocher_roomss
        # tu peux au choix consommer ici un seul :
        inv.rabbit_foot -= 1
        # et mettre un flag temporaire sur inv pour booster le tirage :
        inv._rabbit_bonus_once = getattr(inv, "_rabbit_bonus_once", 0) + 1
        return True
