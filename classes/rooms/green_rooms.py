# classes/rooms/green_rooms.py
import os
import random
from .base import BaseSalle, Dir, Door

ASSETS_GREEN = os.path.join("classes", "rooms", "assets", "green")



class Veranda(BaseSalle):
    """
    Green Room — Veranda.
    - 2 portes verticales (UP / DOWN).
    - Coût : 2 gemmes.
    - Rareté : 2.
    - Room de bordure uniquement.
    - Forte chance de loot (gems, gold, shovel).
    """
    def __init__(self):
        super().__init__(
            nom="Veranda",
            couleur="green",
            portes={
                Dir.UP:   Door(0),
                Dir.DOWN: Door(0),
            },
            image=os.path.join(ASSETS_GREEN, "Veranda_Icon.png"),
            cout_gemmes=2,
            rarity=2,
        )
        self.draftable = True
        self.border_only = True   # utilisé par piocher_roomss pour la bordure

    def on_enter(self, joueur, manoir) -> None:
        """Effet simple : forte chance de loot."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        r = random.random()

        if r < 0.5:
            inv.gems += 1
            print("💎 Veranda : +1 gemme")
        elif r < 0.8:
            inv.gold += 10
            print("🪙 Veranda : +10 gold")
        else:
            if getattr(inv, "shovel", 0) == 0:
                inv.shovel = 1
                print("🛠️ Veranda : +1 shovel")
            else:
                inv.gold += 5
                print("🪙 Veranda : +5 gold")
