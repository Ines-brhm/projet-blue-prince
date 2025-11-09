# classes/joueur.py
import pygame
from .manoir import TAILLE_CASE
from .rooms.base import Dir

COUL_JOUEUR = (245, 210, 66)

KEY_TO_DIR = {
    pygame.K_z: Dir.UP,
    pygame.K_s: Dir.DOWN,
    pygame.K_q: Dir.LEFT,
    pygame.K_d: Dir.RIGHT,
}

class Joueur:
    def __init__(self, pos_depart=None):
        self.i, self.j = pos_depart if pos_depart is not None else (0, 0)

    def deplacer_dir(self, manoir, d: Dir) -> bool:
        if d is None:
            return False

        ok, dest, _ = manoir.can_move(self.i, self.j, d)
        if not ok:
            return False

        # --- consommer 1 pas AVANT de se déplacer ---
        inv = getattr(self, "inv", None)
        if inv is None:
            # si jamais l'inventaire n'est pas attaché, on refuse (sécurité)
            return False

        if getattr(inv, "steps", 0) <= 0:
            return False  # plus de pas => pas de déplacement

        inv.steps -= 1  # OK on consomme 1 pas

        # déplacer le joueur
        self.i, self.j = dest
        return True


    def deplacer_key(self, manoir, key) -> bool:
        return self.deplacer_dir(manoir, KEY_TO_DIR.get(key))

    def dessiner(self, surface: pygame.Surface):
        cx = self.j * TAILLE_CASE + TAILLE_CASE // 2
        cy = self.i * TAILLE_CASE + TAILLE_CASE // 2
        pygame.draw.circle(surface, COUL_JOUEUR, (cx, cy), TAILLE_CASE // 5)
