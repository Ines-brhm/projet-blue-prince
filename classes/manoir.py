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

# --- panneau inventaire (à droite) ---
PANNEAU_LARGEUR = 260
COUL_PANNEAU    = (30, 33, 45)
COUL_TEXTE      = (235, 235, 240)
COUL_TITRE      = (180, 200, 255)

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
        # classes/manoir.py (dans __init__)
        self.font_titre = pygame.font.Font(None, 32)
        self.font_texte = pygame.font.Font(None, 24)


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
    def dessiner_panneau(self, surface: pygame.Surface, inventaire) -> None:
            """
            Dessine le panneau d'inventaire à droite (largeur PANNEAU_LARGEUR).
            `inventaire` doit avoir: steps, gold, gems, keys, dice
            """
            x0 = self.largeur  # le panneau commence juste après la grille
            # fond du panneau
            panneau_rect = pygame.Rect(x0, 0, PANNEAU_LARGEUR, self.hauteur)
            pygame.draw.rect(surface, COUL_PANNEAU, panneau_rect)

            # titre
            titre = self.font_titre.render("Inventaire", True, COUL_TITRE)
            surface.blit(titre, (x0 + 16, 16))

            # lignes de stats
            lignes = [
                f"Steps : {inventaire.steps}",
                f"Gold  : {inventaire.gold}",
                f"Gems  : {inventaire.gems}",
                f"Keys  : {inventaire.keys}",
                f"Dice  : {inventaire.dice}",
            ]
            y = 60
            for li in lignes:
                surf = self.font_texte.render(li, True, COUL_TEXTE)
                surface.blit(surf, (x0 + 16, y))
                y += 28