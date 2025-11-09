# classes/rooms/purple_rooms.py
from .base import BaseSalle, Dir, Door
import os
import random

ASSETS_PURPLE = os.path.join("classes","rooms","assets", "purple")

class Bedroom(BaseSalle):
    """
    Common Purple Room:
    - Effet: +2 Steps à chaque entrée.
    - Possible loot (aléatoire, faible chance).
    - Portes: par défaut UP (à ajuster si besoin).
    """
    def __init__(self):
        super().__init__(
            nom="Bedroom",
            couleur="violet",
            portes={Dir.UP: Door(0),Dir.DOWN: Door(0)},  # ajoute LEFT/RIGHT si tu veux
            image=os.path.join(ASSETS_PURPLE, "Bedroom_Icon.png"),
            cout_gemmes=0,
            rarity=0,
        )
        self.draftable = True
        self._loot_chance = 0.30  # ~30% d’avoir un objet

        # table de loot simple, inspirée de ta description
        self._drops = [
            "apple",             # Apple
            "die",               # 1 Die
            "key",               # 1x Key
            "gem",               # 1 Gem
            "gold3",             # 3 Gold
            "car_keys",          # Car Keys
            "coin_purse",        # Coin Purse
            "locked_trunk",      # Locked Trunk
            "sleeping_mask",     # Sleeping Mask
        ]

    def on_enter(self, joueur, manoir) -> None:
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        # Effet principal : +2 steps à l’entrée
        inv.steps = getattr(inv, "steps", 0) + 2

        # Loot occasionnel
        if random.random() < self._loot_chance:
            drop = random.choice(self._drops)
            if drop == "die":
                inv.dice = getattr(inv, "dice", 0) + 1
                print("🎲 Bedroom: +1 Die")
            elif drop == "key":
                inv.keys = getattr(inv, "keys", 0) + 1
                print("🗝️ Bedroom: +1 Key")
            elif drop == "gem":
                inv.gems = getattr(inv, "gems", 0) + 1
                print("💎 Bedroom: +1 Gem")
            elif drop == "gold3":
                inv.gold = getattr(inv, "gold", 0) + 3
                print("🪙 Bedroom: +3 Gold")
            else:
                # objets “lore” → on les range côté joueur (liste simple)
                bag = getattr(joueur, "items", None)
                if bag is None:
                    joueur.items = []
                    bag = joueur.items
                bag.append(drop)
                # log léger pour debug
                print(f"🛏️ Bedroom: found {drop.replace('_',' ')}")
