# classes/rooms/yellow_rooms.py
from .base import BaseSalle, Dir, Door
import os

# Chemin vers les images jaunes
ASSETS_YELLOW = os.path.join("classes", "rooms", "assets", "yellow")


class Locksmith(BaseSalle):
    """
    Yellow Room — Locksmith.
    - Shop de clés.
    - Portes : 1 porte vers le bas (DOWN).
    - Coût : 1 gemme.
    - Effet : si le joueur a au moins 3 gold, il peut acheter 1 key
      (3 gold -> +1 key) automatiquement à chaque entrée.
      (Version simple du shop 'Keys for Sale' du wiki.)
    """
    def __init__(self):
        super().__init__(
            nom="Locksmith",
            couleur="yellow",
            portes={
                Dir.DOWN: Door(0),
            },
            image=os.path.join(ASSETS_YELLOW, "Locksmith_Icon.png"),
            cout_gemmes=1,
            rarity=1,
        )
        self.draftable = True
        self.fixed_doors = True

    def on_enter(self, joueur, manoir) -> None:
        """
        À l'entrée :
        - si le joueur a >= 3 gold : -3 gold, +1 key
        - sinon : rien 
        """
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        gold = getattr(inv, "gold", 0)
        keys = getattr(inv, "keys", 0)

        if gold >= 3:
            inv.gold = gold - 3
            inv.keys = keys + 1
            print("Locksmith : -3 gold, +1 key")
        else:
            print("Locksmith : pas assez d'or (3 nécessaires)")


class Kitchen(BaseSalle):
    """
    Yellow Room — Kitchen.
    - Food for sale : le joueur peut acheter 10 steps pour 2 gold.
    - Portes : bas et gauche.
    """
    def __init__(self):
        super().__init__(
            nom="Kitchen",
            couleur="yellow",
            portes={Dir.DOWN: Door(0),
                    Dir.LEFT: Door(0)},
            image=os.path.join(ASSETS_YELLOW, "Kitchen_Icon.png"),
            cout_gemmes=1,
            rarity=1,
        )
        self.draftable = True
        self.fixed_doors = True

    def on_enter(self, joueur, manoir) -> None:
        """2 gold -> +10 steps. Sinon rien."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        gold = getattr(inv, "gold", 0)
        steps = getattr(inv, "steps", 0)

        if gold >= 2:
            inv.gold = gold - 2
            inv.steps = steps + 10
            print("Kitchen : -2 gold, +10 steps")
        else:
            print("Kitchen : pas assez d’or (2 nécessaires)")

