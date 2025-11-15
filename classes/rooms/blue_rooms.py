# classes/pieces/bleues.py
from .base import BaseSalle, Dir, Door
import os
import random

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
            
            
class Garage(BaseSalle):
    """
    Blue Room — Dead End (cul-de-sac).
    - 1 seule porte (par ex. UP).
    - 1ère entrée: +3 Keys (porte-clés près de l'entrée).
    - Loot occasionnel: Shovel (pelle).
    """
    def __init__(self):
        super().__init__(
            nom="Garage",
            couleur="blue",
            portes={Dir.DOWN: Door(0)},                 # cul-de-sac : une seule sortie ; change UP si besoin
            image=os.path.join(ASSETS_BLUE, "Garage_Icon.png"),
            cout_gemmes=0,
            rarity=0,
        )
        self.draftable = True
        self._keys_given = False
        self._loot_chance = 0.25  # ~25% de chance d'obtenir la pelle

    def on_enter(self, joueur, manoir) -> None:
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        # 3 clés une seule fois (à la 1ère entrée)
        if not self._keys_given:
            inv.keys = getattr(inv, "keys", 0) + 3
            self._keys_given = True
            print("🔑 Garage: +3 Keys")

        # Loot occasionnel : Shovel
        if random.random() < self._loot_chance:
            if not getattr(inv,"shovel",0):
                inv.shovel = getattr(inv, "shovel", 0) + 1
                print(" Garage: found Shovel")
class Vault(BaseSalle): 
    """
    Blue Room — Vault.
    - 1 seule porte (cul-de-sac).
    - Contient 40 gold.
    - Première entrée : +40 gold.
    - Aucun effet après la récupération du trésor.
    """
    def __init__(self):
        super().__init__(
            nom="Vault",
            couleur="blue",
            portes={Dir.DOWN: Door(0)},
            image=os.path.join(ASSETS_BLUE, "Vault_Icon.png"),
            cout_gemmes=3,
            rarity=3,
        )
        self.draftable   = True
        self._gold_taken = False
        self.gold_amount = 40

    def on_enter(self, joueur, manoir) -> None:
        inv = getattr(joueur, "inv", None)
        if inv is None:
            return

        if not self._gold_taken:
            inv.gold = getattr(inv, "gold", 0) + self.gold_amount
            self._gold_taken = True
            print(f"Vault: +{self.gold_amount} gold")
