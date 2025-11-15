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
        elif r < 0.8:
            inv.gold += 10
        else:
            if getattr(inv, "shovel", 0) == 0:
                inv.shovel = 1
            else:
                inv.gold += 5


    


class Terrace(BaseSalle):
    """
    Green Room — Terrace.
    - 1 porte .
    - Coût : 0 gemme.
    - Rareté : 1.
    - Room de bordure uniquement.
    - Effet : active un flag qui rend les green rooms gratuites.
    """
    def __init__(self):
        super().__init__(
            nom="Terrace",
            couleur="green",
            portes={ 
                Dir.DOWN: Door(0),    # 1 seule porte en bas
            },
            image=os.path.join(ASSETS_GREEN, "Terrace_Icon.png"),
            cout_gemmes=0,
            rarity=1,
        )
        self.draftable = True
        self.border_only = True
        self._activated = False   # effet à usage unique

    def on_enter(self, joueur, manoir):
        """Effet : green rooms deviennent gratuites."""
        if self._activated:
            return

        setattr(manoir, "green_rooms_free", True)
        self._activated = True
        print("Terrace : les Green Rooms ne coûtent plus de gemmes à drafter !")

