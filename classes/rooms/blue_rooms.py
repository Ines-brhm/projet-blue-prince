# classes/pieces/bleues.py
from .base import BaseSalle, Dir, Door
import os

ASSETS_BLUE = os.path.join("classes","rooms","assets", "blue")

class EntranceHall(BaseSalle):
    """
    Salle permanente de départ (non draftable).
    - Toujours placée au centre de la rangée du bas.
    - Sert de hub ; on autorise UP/LEFT/RIGHT (pas DOWN pour éviter de sortir de la grille).
    - Peut, si tu l'actives, donner le 'blueprint' au Day One via on_enter(...).
    """
    def __init__(self):
        super().__init__(
            nom="Entrance Hall",
            couleur="blue",
            # tu peux ajuster les portes : ici UP/LEFT/RIGHT
            portes={Dir.UP: Door(0), Dir.LEFT: Door(0), Dir.RIGHT: Door(0)},
            image=os.path.join(ASSETS_BLUE, "Entrance_Hall_Icon.png"),
            cout_gemmes=0,
            rarity=0,
        )
        # indicateur simple pour ne JAMAIS la proposer au draft
        self.draftable = False

        # Si tu veux tracer un état interne minimal (ex: lettre/blueprint pris)
        self._blueprint_donne = False

    """# --- optionnel: activer si tu veux donner le 'blueprint' à la 1re visite ---
    def on_enter(self, joueur, manoir) -> None:
        
        Exemple minimal : donner le 'blueprint' la 1ère fois.
        Tu peux commenter ce bloc tant que tu n'as pas ces champs dans Joueur/Inventaire.
        
        if getattr(joueur, "has_blueprint", None) is None:
            # ajoute un champ dynamique si absent
            joueur.has_blueprint = False

        if not self._blueprint_donne and not joueur.has_blueprint:
            joueur.has_blueprint = True
            self._blueprint_donne = True
            # Affichage console (en attendant un UI/HUD)
            print("📜 Blueprint obtenu : vous pouvez drafter des rooms.")"""
