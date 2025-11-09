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
            portes={Dir.UP: Door(0),Dir.DOWN: Door(0)},                 # ajustable : {Dir.UP:Door(0), Dir.LEFT:Door(0)}...
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
