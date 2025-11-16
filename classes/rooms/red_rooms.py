# classes/pieces/rouges.py
from .base import BaseSalle, Dir, Door
import os
import random

ASSETS_RED = os.path.join("classes","rooms","assets", "red")

class Chapel(BaseSalle):
    """
    Salle rouge 'Chapel' :
    - Malus : à CHAQUE entrée, perdre 1 or si possible.
    - Butin occasionnel : parfois 1–2 gemmes, ou un tas d'or (2..12 ou 14 ; jamais 13).
    - Portes : une seule (UP) par défaut (tu peux ajuster).
    """
    def __init__(self):
        super().__init__(
            nom="Chapel",
            couleur="red",
            portes={Dir.RIGHT: Door(0), Dir.LEFT: Door(0),Dir.DOWN: Door(0)},                 # ajustable : {Dir.UP:Door(0), Dir.LEFT:Door(0)}...
            image=os.path.join(ASSETS_RED, "Chapel_Icon.png"),
            cout_gemmes=0,
            rarity=0,
        )
        self.draftable = True  # incluse dans le tirage

        # tuning loot simple
        self._loot_chance = 0.25  # 25% de chances d'un butin par entrée

        # valeurs d'or possibles (pas 13)
        self._gold_piles = [v for v in range(2, 13)] + [14]

    def on_enter(self, joueur, manoir) -> None:
        """
        - Perdre 1 or si le joueur en a.
        - Avec une proba _loot_chance, donner soit 1–2 gemmes, soit un tas d'or admissible.
        """
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return  # pas d'inventaire -> rien à faire (sécurité)

        # Malus or : -1 si possible
        if getattr(inv, "gold", 0) > 0:
            inv.gold -= 1

        # Loot occasionnel
        if random.random() < self._loot_chance:
            if random.random() < 0.5:
                # gemmes 1–2
                gain = random.randint(1, 2)
                inv.gems = getattr(inv, "gems", 0) + gain
                print(f"💎 Chapel: +{gain} gem(s)")
            else:
                # or parmi {2..12, 14}
                gain = random.choice(self._gold_piles)
                inv.gold = getattr(inv, "gold", 0) + gain
                print(f"🪙 Chapel: +{gain} or")


class WeightRoom(BaseSalle):
    """
    Red Room — Steps perdus au DRAFT (pas à l'entrée) :
    - Au moment où la salle est draftée/placée, on retire floor(steps/2).
    - Loot occasionnel : +3 Gold.
    """
    def __init__(self):
        super().__init__(
            nom="Weight Room",
            couleur="red",
            portes={Dir.UP: Door(0),Dir.LEFT: Door(0),Dir.RIGHT: Door(0),Dir.DOWN: Door(0)},  # ajuste si besoin
            image=os.path.join(ASSETS_RED, "Weight_Room_Icon.png"),
            cout_gemmes=0,
            rarity=0,
        )
        self.draftable = True
        self._loot_chance = 0.25  # 25% ≈ tu peux changer

    # ---- Spécifique : effet au DRAFT (pas à l'entrée) ----
    def on_enter(self, joueur, manoir):
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        cur = getattr(inv, "steps", 0)
        perte = cur // 2  # floor
        inv.steps = max(0, cur - perte)

        # loot occasionnel : +3 gold
        if random.random() < self._loot_chance:
            inv.gold = getattr(inv, "gold", 0) + 3
            print("🏋️ Weight Room: +3 Gold (draft loot)")
            
class Gymnasium(BaseSalle):
    """
    Red Room — Gymnasium.
    - À CHAQUE entrée : le joueur perd 2 steps (si possible).
    - Salle fatigante (on fait du sport -> on se fatigue).
    - Portes : 4 directions (UP / DOWN / LEFT / RIGHT).
    """
    def __init__(self):
        super().__init__(
            nom="Gymnasium",
            couleur="red",
            portes={
                Dir.DOWN:  Door(0),
                Dir.LEFT:  Door(0),
                Dir.RIGHT: Door(0),
            },
            image=os.path.join(ASSETS_RED, "Gymnasium_Icon.png"),
            cout_gemmes=0,   # tu peux mettre 1 si tu veux la rendre plus chère
            rarity=1,        # fréquence moyenne
        )
        self.draftable = True
        self.fixed_doors = True

    def on_enter(self, joueur, manoir) -> None:
        """À chaque entrée : perdre 2 steps (sans aller en dessous de 0)."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        cur = getattr(inv, "steps", 0)
        perte = min(2, cur)      # on ne peut pas perdre plus que ce qu'on a
        inv.steps = cur - perte

        if perte > 0:
            print(f"Gymnasium : -{perte} steps (séance de sport)")


# classes/rooms/red_rooms.py
from .base import BaseSalle, Dir, Door
import os
import random

ASSETS_RED = os.path.join("classes", "rooms", "assets", "red")

# ... Chapel, WeightRoom, Gymnasium, etc. ...


class Lavatory(BaseSalle):
    """
    Red Room — Lavatory.
    - 1 porte (DOWN).
    - À chaque entrée : tu perds 2 steps.
    - Petite chance de trouver une clé oubliée.
    """

    def __init__(self):
        super().__init__(
            nom="Lavatory",
            couleur="red",
            portes={
                Dir.DOWN: Door(0),
            },
            image=os.path.join(ASSETS_RED, "Lavatory_Icon.png"),
            cout_gemmes=0,
            rarity=1,   # standard
        )
        self.draftable = True
        self._key_chance = 0.30   # 30% de chance de trouver une clé

    def on_enter(self, joueur, manoir) -> None:
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        # malus principal : -2 steps si possible
        cur = getattr(inv, "steps", 0)
        if cur > 0:
            perte = min(2, cur)
            inv.steps = cur - perte
            print(f" Lavatory : tu perds {perte} steps.")

        # petite chance de trouver une clé
        if random.random() < self._key_chance:
            inv.keys = getattr(inv, "keys", 0) + 1
            print("Lavatory : tu trouves une clé oubliée.")