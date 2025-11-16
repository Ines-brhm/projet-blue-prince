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
            portes={Dir.LEFT: Door(0),Dir.DOWN: Door(0)},  # ajoute LEFT/RIGHT si tu veux
            image=os.path.join(ASSETS_PURPLE, "Bedroom_Icon.png"),
            cout_gemmes=0,
            rarity=0,
        )
        self.draftable = True
        self._loot_chance = 0.3 # ~30% d’avoir un objet

        # table de loot simple, inspirée de ta description
        self._drops = [
            #"apple",             # Apple
            "die",               # 1 Die
            "key",               # 1x Key
            "gem",               # 1 Gem
            "gold3",             # 3 Gold
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
                manoir.show_message(" Bedroom: +1 Dice",1.0)
                
            elif drop == "key":
                inv.keys = getattr(inv, "keys", 0) + 1
                manoir.show_message( " Bedroom: +1 Key",1.0)
                print("Bedroom: +1 Key")
            elif drop == "gem":
                inv.gems = getattr(inv,"gems", 0) + 1
                manoir.show_message(" Bedroom: +1 Gem",1.0)
                print(" Bedroom: +1 Gem")
            elif drop == "gold3":
                inv.gold = getattr(inv,"gold", 0) + 3
                manoir.show_message(" Bedroom: +3 Gold",1.0)
                print(" Bedroom: +3 Gold")
            else:
                # objets “lore” → on les range côté joueur (liste simple)
                bag = getattr(joueur, "items", None)
                if bag is None:
                    joueur.items = []
                    bag = joueur.items
                bag.append(drop)
                # log léger pour debug
                print(f"🛏️ Bedroom: found {drop.replace('_',' ')}")


class GuestBedroom(BaseSalle):
    """
    Purple Room — Guest Bedroom.
    - Dead end (1 porte DOWN)
    - Effet : +10 steps à chaque entrée
    """
    def __init__(self):
        super().__init__(
            nom="Guest Bedroom",
            couleur="purple",
            portes={
                Dir.DOWN: Door(0),    # cul-de-sac
            },
            image=os.path.join(ASSETS_PURPLE, "Guest_Bedroom_Icon.png"),
            cout_gemmes=0,
            rarity=1,
        )

        self.draftable = True

    def on_enter(self, joueur, manoir):
        """+10 steps à chaque entrée."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        inv.steps += 10
        print("Guest Bedroom : +10 steps")


class Boudoir(BaseSalle):
    """
    Purple Room — Boudoir.
    - Dead end (1 porte DOWN)
    - Aucun effet particulier.
    """
    def __init__(self):
        super().__init__(
            nom="Boudoir",
            couleur="purple",
            portes={
                Dir.DOWN: Door(0),
                Dir.LEFT: Door(0)  
            },
            image=os.path.join(ASSETS_PURPLE, "Boudoir_Icon.png"),
            cout_gemmes=0,
            rarity=1,
        )
        self.draftable = True
        self.rare = True

class MasterBedroom(BaseSalle):
    """
    Purple Room — Master Bedroom
    Effet : +1 step pour CHAQUE salle déjà placée dans le manoir.
    """
    def __init__(self):
        super().__init__(
            nom="Master Bedroom",
            couleur="purple",
            portes={Dir.DOWN: Door(0)},   
            image=os.path.join(ASSETS_PURPLE, "Master_Bedroom_Icon.png"),
            cout_gemmes=0,
            rarity=0,
        )
        self.draftable = True
        self.rare = True

    def on_enter(self, joueur, manoir) -> None:
        """
        Effet : +1 step pour chaque salle déjà posée dans le manoir.
        """
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return
        # compter les salles déjà placées
        nb = 0
        for ligne in manoir.grille:
            for salle in ligne:
                if salle is not None:
                    nb += 1
        # ajouter les steps
        inv.steps = getattr(inv, "steps", 0) + nb



class ServantsQuarters(BaseSalle):
    """
    Purple Room — Servant's Quarters
    Effet : +1 key pour CHAQUE chambre de type Bedroom déjà dans le manoir.
    """
    def __init__(self):
        super().__init__(
            nom="Servant's Quarters",
            couleur="purple",
            portes={Dir.DOWN: Door(0)},   # une seule porte en bas
            image=os.path.join(ASSETS_PURPLE, "Servants_Quarters_Icon.png"),
            cout_gemmes=0,
            rarity=1,
        )
        self.draftable = True
        self.rare = True

    def on_enter(self, joueur, manoir) -> None:
        """+1 key pour chaque Bedroom déjà posée dans le manoir."""
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        # Noms des chambres "Bedroom"
        bedroom_names = {
            "Bedroom",
            "Guest Bedroom",
            "Boudoir",
            "Master Bedroom",
            "Servant's Quarters",
        }

        nb_bedrooms = 0
        for ligne in manoir.grille:
            for salle in ligne:
                if salle is not None and getattr(salle, "nom", "") in bedroom_names:
                    nb_bedrooms += 1

        if nb_bedrooms > 0:
            inv.keys = getattr(inv, "keys", 0) + nb_bedrooms
            print(f" Servant's Quarters : +{nb_bedrooms} keys (pour {nb_bedrooms} Bedrooms)")
        else:
            print(" Servant's Quarters : aucune Bedroom dans le manoir pour l’instant.")

class Nursery(BaseSalle):
    """
    Purple Room — Nursery.
    Effet : Quand vous DRAFTEZ une chambre de type Bedroom, gagnez +5 steps.
    """
    def __init__(self):
        super().__init__(
            nom="Nursery",
            couleur="purple",
            portes={Dir.DOWN: Door(0)},
            image=os.path.join(ASSETS_PURPLE, "Nursery_Icon.png"),
            cout_gemmes=0,
            rarity=1,
        )
        self.draftable = True
        self.rare = True

    #  quand une autre salle est draftée
    def on_draft_other_room(self, joueur, room_draftee, manoir):
        """
        Appelé lorsqu'une AUTRE salle a été posée sur le manoir.
        Si cette salle est un Bedroom => +5 steps au joueur.
        """
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        if getattr(room_draftee, "nom", "") in {
            "Bedroom",
            "Guest Bedroom",
            "Boudoir",
            "Master Bedroom",
            "Servant's Quarters",
        }:
            inv.steps = getattr(inv, "steps", 0) + 5
            print("Nursery : +5 steps (nouvelle Bedroom posée !)")