# classes/rooms/orange_rooms.py
import os
from .base import BaseSalle, Dir, Door

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
