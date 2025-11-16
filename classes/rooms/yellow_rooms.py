# classes/rooms/yellow_rooms.py
from .base import BaseSalle, Dir, Door
import os

# Chemin vers les images jaunes
ASSETS_YELLOW = os.path.join("classes", "rooms", "assets", "yellow")


class Locksmith(BaseSalle):
    """
    Yellow Room — Locksmith.
    - Shop.
    - Portes : 1 porte vers le bas (DOWN).
    - Coût : 1 gemme.
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



