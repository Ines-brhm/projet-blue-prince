# classes/rooms/orange_rooms.py
import os
from .base import BaseSalle, Dir, Door
import random

ASSETS_ORANGE = os.path.join("classes", "rooms", "assets", "orange")


class Hallway(BaseSalle):
    """
    Orange Room — Hallway.
    - 4 portes (UP, DOWN, LEFT, RIGHT) : pièce très connectée.
    - Coût : 1 gemme.
    - Rareté : 1 (très commune).
    - Aucun effet spécial : sert seulement à bien connecter le manoir.
    """
    def __init__(self):
        super().__init__(
            nom="Hallway",
            couleur="orange",
            portes={
                Dir.DOWN:  Door(0),
                Dir.LEFT:  Door(0),
                Dir.RIGHT: Door(0),
            },
            image=os.path.join(ASSETS_ORANGE, "Hallway_Icon.png"),
            cout_gemmes=1,
            rarity=1,
        )
        self.draftable = True

    def on_enter(self, joueur, manoir) -> None:
        """Pas d'effet particulier : simple salle de connexion."""
        return
    
class Foyer(BaseSalle):
    """
    Orange Room — Foyer.
    - 2 portes (UP / DOWN).
    - Coût : 1 gemme.
    - Rareté : 2.
    - Effet (version wiki adaptée) :
      Lors de la première entrée, toutes les salles 'Hallway' déjà posées
      voient leurs portes totalement déverrouillées (niveau 0).
    """
    def __init__(self):
        super().__init__(
            nom="Foyer",
            couleur="orange",
            portes={
                Dir.UP:   Door(0),
                Dir.DOWN: Door(0),
            },
            image=os.path.join(ASSETS_ORANGE, "Foyer_Icon.png"),
            cout_gemmes=1,
            rarity=2,
        )
        self.draftable = True
        self._activated = False  # effet une seule fois
        self.fixed_doors = True


    def on_enter(self, joueur, manoir) -> None:
        """Déverrouille toutes les Hallway déjà posées dans le manoir."""
        if self._activated:
            return

        changed = 0

        # On parcourt toutes les cases de la grille du manoir
        for ligne in manoir.grille:
            for salle in ligne:
                if salle is None:
                    continue

                # On repère les Hallway par leur nom
                if getattr(salle, "nom", "") == "Hallway":
                    portes = getattr(salle, "portes", None)
                    if portes:
                        # On met TOUTES les portes de cette Hallway à niveau 0
                        salle.portes = {d: Door(0) for d in portes.keys()}
                        changed += 1

        self._activated = True

        if changed > 0:
            print(f"Foyer : portes des {changed} Hallway déverrouillées.")
        else:
            print("Foyer : aucune Hallway à déverrouiller pour l’instant.")

class WestWingHall(BaseSalle):
    """
    Orange Room — West Wing Hall.
    - Type : Hallway (couloir).
    - Portes en T (DOWN / LEFT / RIGHT), comme Hallway.
    - Coût : 0 gemme.
    - Rareté : 1 (standard).
    - Effet : petite chance de loot (clé, dé, steps) quand on entre.
    - Inspiré du wiki Blue Prince (West Wing Hall).
    """
    def __init__(self):
        super().__init__(
            nom="West Wing Hall",
            couleur="orange",
            portes={
                Dir.DOWN:  Door(0),
                Dir.LEFT:  Door(0),
                Dir.RIGHT: Door(0),
            },
            image=os.path.join(ASSETS_ORANGE, "West_Wing_Hall_Icon.png"),
            cout_gemmes=0,
            rarity=1,
        )
        self.draftable = True
        self.fixed_doors = True
       

    def on_enter(self, joueur, manoir) -> None:
        """
        Effet léger : petite chance de trouver quelque chose
        sur la table (clé, dé, ou un peu de steps).
        """
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        r = random.random()

        #  +1 key
        if r < 0.30:
            keys = getattr(inv, "keys", 0) + 1
            setattr(inv, "keys", keys)
            print(" West Wing Hall : +1 key")

        #  +1 dice
        elif r < 0.60:
            dice = getattr(inv, "dice", 0) + 1
            setattr(inv, "dice", dice)
            print("West Wing Hall : +1 dice")

        #  +3 steps
        elif r < 0.70:
            steps = getattr(inv, "steps", 0) + 3
            setattr(inv, "steps", steps)
            print(" West Wing Hall : +3 steps")

class Passageway(BaseSalle):
    """
    Orange Room — Passageway.
    - 4 portes (UP / DOWN / LEFT / RIGHT).
    - Coût : 2 gemmes.
    - Rareté : 1 (commune).
    - Effet : couloir rapide -> +1 step à chaque entrée.
      (Inspiré de la description du wiki : rapide pour traverser le manoir.)
    """
    def __init__(self):
        super().__init__(
            nom="Passageway",
            couleur="orange",
            portes={
                Dir.UP:    Door(0),
                Dir.DOWN:  Door(0),
                Dir.LEFT:  Door(0),
                Dir.RIGHT: Door(0),
            },
            image=os.path.join(ASSETS_ORANGE, "Passageway_Icon.png"),
            cout_gemmes=2,
            rarity=1,
        )
        self.draftable = True
        self.fixed_doors = True

    def on_enter(self, joueur, manoir) -> None:
        """Couloir rapide : on gagne +1 step quand on y entre."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        steps = getattr(inv, "steps", 0)
        setattr(inv, "steps", steps + 1)
        print("➡ Passageway : +1 step (couloir rapide)")
           

    
