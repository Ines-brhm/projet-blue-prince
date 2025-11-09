# classes/pieces/bleues.py
from .base import BaseSalle, Dir, Door


class SalleBleueCommune(BaseSalle):
    def __init__(self):
        super().__init__(
            nom="Common Room",
            couleur="bleu",
            portes={Dir.UP: Door(0)},
            cout_gemmes=0,
            image=f"classes/rooms/assets/blue/Entrance_Hall_Icon.png", 
            rarity=0,  # commun
        )