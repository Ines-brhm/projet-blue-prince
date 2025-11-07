# classes/joueur.py
import pygame
from .manoir import LIGNES, COLONNES, TAILLE_CASE  # import relatif

COUL_JOUEUR = (245, 210, 66)

class Joueur:
    """Position + déplacements ZQSD + rendu curseur."""
    def __init__(self, pos_depart=None):
        self.i = LIGNES - 1 if pos_depart is None else pos_depart[0]
        self.j = COLONNES // 2 if pos_depart is None else pos_depart[1]

    def deplacer(self, direction: str):
        if direction == "Z" and self.i > 0:
            self.i -= 1
        elif direction == "S" and self.i < LIGNES - 1:
            self.i += 1
        elif direction == "Q" and self.j > 0:
            self.j -= 1
        elif direction == "D" and self.j < COLONNES - 1:
            self.j += 1

    def dessiner(self, surface: pygame.Surface):
        cx = self.j * TAILLE_CASE + TAILLE_CASE // 2
        cy = self.i * TAILLE_CASE + TAILLE_CASE // 2
        pygame.draw.circle(surface, COUL_JOUEUR, (cx, cy), TAILLE_CASE // 5)
