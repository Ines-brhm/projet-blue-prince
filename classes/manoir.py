# classes/manoir.py
import pygame
from .rooms.base import Dir  # ← tu as déjà Dir dans pieces/base.py

# (tes constantes...)

# Table des vecteurs par direction
DIR_VEC = {
    Dir.UP:    (-1, 0),
    Dir.DOWN:  ( 1, 0),
    Dir.LEFT:  ( 0,-1),
    Dir.RIGHT: ( 0, 1),
}

# --------- constantes (grille + couleurs) ----------
LIGNES= 9   
COLONNES =  5
TAILLE_CASE, MARGE = 90, 2

COUL_FOND      = (22, 22, 28)
COUL_CASE_VIDE = (40, 42, 54)
COUL_CASE_VIDE = (0, 0, 0)

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
        
        self._img_cache = {}  # ← servira à ne pas recharger les mêmes images à chaque frame


    def _get_img(self, path: str):
        if not path:
            return None
        if path in self._img_cache:
            return self._img_cache[path]
        try:
            surf = pygame.image.load(path).convert_alpha()
            w = h = self.taille_case - 2 * MARGE
            surf = pygame.transform.smoothscale(surf, (w, h))
            self._img_cache[path] = surf
            return surf
        except Exception as e:
            print("⚠️ load fail:", path, "->", e)   # <-- aide debug
            return None



    def dessiner_grille(self, surface: pygame.Surface):
        """Dessine la grille 5x9 et colore l'Entrance Hall."""
        surface.fill(COUL_FOND)
                
        for i in range(self.lignes):
            for j in range(self.colonnes):
                x = j * self.taille_case + MARGE
                y = i * self.taille_case + MARGE
                w = h = self.taille_case - 2*MARGE
                rect = pygame.Rect(x, y, w, h)

                salle = self.grille[i][j]

                if salle is not None:
                    # 1) Case occupée par une salle → affiche d’abord l’image si présente, sinon couleur par type
                    img = self._get_img(getattr(salle, "image", None))
                    if img:
                        # petit fond discret
                        pygame.draw.rect(surface, COUL_CASE_VIDE, rect, border_radius=10)
                        surface.blit(img, (x, y))
                    else:
                        #couleur = COULEURS_RGB.get(salle.couleur, COUL_CASE_VIDE)
                        pygame.draw.rect(surface, COUL_CASE_VIDE, rect, border_radius=10)
                else:
                    # 3) Case vide standard
                    pygame.draw.rect(surface, COUL_CASE_VIDE, rect, border_radius=10)

                # contour
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
                f"shovel  : {inventaire.shovel}",
            ]
            y = 60
            for li in lignes:
                surf = self.font_texte.render(li, True, COUL_TEXTE)
                surface.blit(surf, (x0 + 16, y))
                y += 28
                
    def in_bounds(self, i:int, j:int) -> bool:
        #Évite les IndexError quand on sort de la grille (ex: i = -1 ou j = COLONNES).
        return 0 <= i < self.lignes and 0 <= j < self.colonnes
    
    def can_move(self, i:int, j:int, d: Dir) -> tuple[bool, tuple[int,int] | None, str]:
        """
        V1 simple : on autorise le déplacement si la SALLE COURANTE a une porte côté d.
        On ne vérifie PAS la case voisine (qu'elle soit vide ou non).
        """
        cur = self.grille[i][j]
        if cur is None:
            return (False, None, "Pas de salle sous le joueur.")
        if not cur.a_porte(d):
            return (False, None, "Pas de porte dans cette direction.")
        di, dj = DIR_VEC[d]
        ni, nj = i + di, j + dj
        if not self.in_bounds(ni, nj):
            return (False, None, "Hors de la grille.")
        return (True, (ni, nj), "")
