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






class Cloister(BaseSalle):
    """
    Green Room — Cloister.
    - 4 portes (UP / DOWN / LEFT / RIGHT).
    - Coût : 3 gemmes.
    - Effet unique : la 1ère fois que le joueur entre ici, il gagne
      → +1 dé et +5 or, puis plus rien.
    """
    def __init__(self):
        super().__init__(
            nom="Cloister",
            couleur="green",
            portes={
                Dir.UP:    Door(0),
                Dir.DOWN:  Door(0),
                Dir.LEFT:  Door(0),
                Dir.RIGHT: Door(0),
            },
            image=os.path.join(ASSETS_GREEN, "Cloister_Icon.png"),
            cout_gemmes=3,
            rarity=3,
        )
        self.draftable = True
        self.border_only = True
        self._reward_done = False    # pour que l'effet ne se fasse qu'une fois

    def on_enter(self, joueur, manoir) -> None:
        """Récompense unique à la première entrée."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        if self._reward_done:
            return

        # Récompense : +1 dé, +5 or
        inv.dice = getattr(inv, "dice", 0) + 1
        inv.gold = getattr(inv, "gold", 0) + 5
        self._reward_done = True

        print("🌿 Cloister : +1 Dice, +5 Gold (jardin découvert)")



# classes/rooms/green_rooms.py
from .base import BaseSalle, Dir, Door
import os
import random

ASSETS_GREEN = os.path.join("classes", "rooms", "assets", "green")


class Courtyard(BaseSalle):
    """
    Green Room — Courtyard.
    - 3 portes (UP / LEFT / RIGHT).
    - Coût : 1 gemme.
    - Loot fréquent : pelle, gemmes ou or.
    """

    def __init__(self):
        super().__init__(
            nom="Courtyard",
            couleur="green",
            portes={
                Dir.DOWN:   Door(0),
                Dir.LEFT: Door(0),
                Dir.RIGHT: Door(0),
            },
            image=os.path.join(ASSETS_GREEN, "Courtyard_Icon.png"),
            cout_gemmes=1,
            rarity=1,      # standard
        )
        self.draftable    = True
        self.border_only  = True
        self._loot_chance = 0.75   # 75% de chance de loot

    def on_enter(self, joueur, manoir) -> None:
        """Loot fréquent : pelle, gemme ou or."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        # parfois rien
        if random.random() > self._loot_chance:
            return

        # priorité : donner une pelle si le joueur n'en a pas
        if getattr(inv, "shovel", 0) == 0:
            inv.shovel = 1
            print(" Courtyard : vous trouvez une pelle.")
            return

        # sinon, soit une gemme soit de l’or
        if random.random() < 0.5:
            inv.gems = getattr(inv, "gems", 0) + 1
            print(" Courtyard : +1 gemme")
        else:
            inv.gold = getattr(inv, "gold", 0) + 8
            print("Courtyard : +8 or")




class Patio(BaseSalle):
    """
    Green Room — Patio.
    - 2 portes  (LEFT / DOWN).
    - Coût : 2 gemmes.
    - Effet (1 seule fois) : +1 gemme pour CHAQUE Green Room déjà construite.
    """

    def __init__(self):
        super().__init__(
            nom="Patio",
            couleur="green",
            portes={
                Dir.LEFT:   Door(0),
                Dir.DOWN: Door(0),
            },
            image=os.path.join(ASSETS_GREEN, "Patio_Icon.png"),
            cout_gemmes=2,
            rarity=2,
        )
        self.draftable  = True
        self.border_only = True
        self._activated = False   # effet une seule fois

    def on_enter(self, joueur, manoir) -> None:
        """La première entrée : +1 gemme par Green Room déjà posée."""
        if self._activated:
            return

        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        nb_green = 0
        for ligne in manoir.grille:
            for salle in ligne:
                if salle is None:
                    continue
                if getattr(salle, "couleur", "") == "green":
                    nb_green += 1

        if nb_green <= 0:
            return

        inv.gems = getattr(inv, "gems", 0) + nb_green
        self._activated = True
        print(f"🌿 Patio : +{nb_green} gemmes (1 par Green Room).")