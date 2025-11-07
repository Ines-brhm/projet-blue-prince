# classes/manoir.py
import pygame

# --------- constantes (grille + couleurs) ----------
LIGNES= 9   
COLONNES =  5
TAILLE_CASE, MARGE = 90, 2

COUL_FOND      = (22, 22, 28)
COUL_CASE_VIDE = (40, 42, 54)
COUL_GRILLE    = (70, 70, 80)
COUL_ENTREE    = (66, 135, 245)  # Entrance Hall

class Manoir:
    """Grille 5x9 du manoir + entrée en bas-centre + dessin Pygame."""
    def __init__(self):
        self.lignes, self.colonnes = LIGNES, COLONNES
        self.taille_case = TAILLE_CASE

        self.largeur = self.colonnes * self.taille_case
        self.hauteur = self.lignes   * self.taille_case

        # entrée (bas-centre)
        self.pos_entree = (self.lignes - 1, self.colonnes // 2)

        # grille logique (pour plus tard)
        self.grille = [[None for _ in range(self.colonnes)] for _ in range(self.lignes)]

    def dessiner_grille(self, surface: pygame.Surface):
        """Dessine la grille 5x9 et colore l'Entrance Hall."""
        surface.fill(COUL_FOND)

        for i in range(self.lignes):
            for j in range(self.colonnes):
                x = j * self.taille_case
                y = i * self.taille_case
                rect = pygame.Rect(
                    x + MARGE, y + MARGE,
                    self.taille_case - 2*MARGE, self.taille_case - 2*MARGE
                )

                couleur = COUL_CASE_VIDE
                if (i, j) == self.pos_entree:
                    couleur = COUL_ENTREE

                pygame.draw.rect(surface, couleur, rect, border_radius=10)
                pygame.draw.rect(surface, COUL_GRILLE, rect, width=1, border_radius=10)
