# classes/manoir.py
import pygame
from .rooms.base import Dir  
from .rooms.base import Door  
from.ouverture_porte import demande_ouverture
import random
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


# --- zone "draft" en bas du panneau inventaire ---
CHOIX_TAILLE   = 110      # taille de la vignette (carré)
CHOIX_ESPACE   = 18       # espace horizontal entre cartes
DRAFT_MARGE    = 16       # marge intérieure du panneau
DRAFT_TITRE_H  = 28       # hauteur pour le titre "Choose a room"

class Manoir:
    """Grille 5x9 du manoir + entrée en bas-centre + dessin Pygame."""
    def __init__(self):
        self.lignes, self.colonnes = LIGNES, COLONNES
        self.taille_case = TAILLE_CASE

        self.largeur = self.colonnes * self.taille_case
        self.hauteur = self.lignes   * self.taille_case
        self.joueur = None  

        # entrée (bas-centre)
        self.pos_entree = (self.lignes - 1, self.colonnes // 2)
        
        #font pour affichage des message
        self._msg_text = None
        self._msg_until = 0
        self.font_msg  = pygame.font.Font(None, 36)
        
        # grille logique (pour plus tard)
        self.grille = [[None for _ in range(self.colonnes)] for _ in range(self.lignes)]
        # classes/manoir.py (dans __init__)
        self.font_titre = pygame.font.Font(None, 32)
        self.font_texte = pygame.font.Font(None, 24)
        
        self._img_cache = {}  # ← servira à ne pas recharger les mêmes images à chaque frame
        
        self.fenetre=0

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
                    rot = getattr(salle, "rot", 0)
                    if img and rot:
                        # rotation horaire 90° => angle négatif en pygame.rotate
                        img = pygame.transform.rotate(img, -90 * rot)
                        # on rescale pour rentrer proprement dans la case
                        img = pygame.transform.smoothscale(img, (w, h))
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
    

    
    def can_move(self, i:int, j:int, d:Dir, inv=None):
        cur = self.grille[i][j]
        if cur is None:
            return (False, None, "Pas de salle sous le joueur.")
        if not cur.a_porte(d):
            return (False, None, "Pas de porte dans cette direction.")

        door = cur.portes.get(d)
        level = door.level if door else 0

        if level >= 1:
            if self.fenetre is None or inv is None:
                return (False, None, "Porte verrouillée.")
            ok = demande_ouverture(self.fenetre, inv, level)  # <-- utilise la même fen
            if not ok:
                return (False, None, "Ouverture annulée.")
            cur.portes[d] = Door(0)
        di, dj = DIR_VEC[d]
        ni, nj = i + di, j + dj
        print("les porte de cette chambre ",cur.nom ,cur.portes)
        if not self.in_bounds(ni, nj):
            return (False, None, "Hors de la grille.")
        return (True, (ni, nj), "")
    


    ############### Actions spéciales avec la pelle ###############
    
    def essayer_creuser(self):
        """Tente de creuser dans la salle actuelle avec une pelle."""
        i, j = self.joueur.i, self.joueur.j
        salle = self.grille[i][j]
        inv = getattr(self.joueur, "inv", None)

        if salle is None or inv is None:
            return

        # Vérifier que la salle est une Green Room
        if getattr(salle, "couleur", "") != "green":
            self.show_message("On ne peut creuser que dans les pièces vertes.", 1.0)
            return

        # Vérifier que le joueur a une pelle
        if getattr(inv, "shovel", 0) <= 0:
            self.show_message("Tu n'as pas de pelle…", 1.0)
            return

        # Consommer une pelle
        inv.shovel -= 1

        # Loot aléatoire
        r = random.random()
        if r < 0.40:
            gain = random.randint(3, 8)
            inv.gold += gain
            self.show_message(f"Tu déterres {gain} or !", 1.0)

        elif r < 0.70:
            inv.gems += 1
            self.show_message("Tu trouves 1 gemme enfouie !", 1.0)

        elif r < 0.85:
            inv.lockpicks += 1
            self.show_message("Tu trouves un vieux crochet de serrure (+1 pick).", 1.0)

        else:
            inv.shovel += 1
            self.show_message("Incroyable… une autre pelle !", 1.0)








    def _get_thumb(self, path: str, size: int = CHOIX_TAILLE):
        """Charge une image et la met au format vignette."""
        if not path:
            return None
    # on réutilise le cache de _get_img mais on rescale si besoin
        surf = self._get_img(path)
        if surf is None: 
            return None
        if surf.get_width() != size or surf.get_height() != size:
            surf = pygame.transform.smoothscale(surf, (size, size))
        return surf
    
    def dessiner_draft_choices(self, surface: pygame.Surface, rooms: list, selected_idx: int = 0):
        """
        Affiche 3 rooms (tirées) en bas du panneau inventaire, avec un surlignage
        pour l’élément sélectionné. Retourne la liste des pygame.Rect des cartes.
        """
        # géométrie de la zone "draft" (dans le panneau à droite)
        x_pan = self.largeur +100
        y_zone = self.hauteur - (DRAFT_MARGE + CHOIX_TAILLE + DRAFT_TITRE_H +100)
        w_zone = PANNEAU_LARGEUR
        h_zone = DRAFT_MARGE + CHOIX_TAILLE + DRAFT_TITRE_H + 100

        # fond léger de la zone
        zone_rect = pygame.Rect(x_pan, y_zone, w_zone, h_zone)
        pygame.draw.rect(surface, (25, 27, 37), zone_rect)

        # titre
        titre = self.font_texte.render("Choose a room to draft", True, COUL_TITRE)
        surface.blit(titre, (x_pan + DRAFT_MARGE, y_zone + 6))

        # positionnement des 3 vignettes
        n = min(3, len(rooms))
        if n == 0:
            return []

        total_w = n * CHOIX_TAILLE + (n - 1) * CHOIX_ESPACE
        x0 = x_pan + (w_zone - total_w) // 2
        y0 = y_zone + DRAFT_TITRE_H + 10

        card_rects = []
        for i in range(n):
            room = rooms[i]
            rx = x0 + i * (CHOIX_TAILLE + CHOIX_ESPACE)
            ry = y0
            card = pygame.Rect(rx, ry, CHOIX_TAILLE, CHOIX_TAILLE)
            card_rects.append(card)

            # cadre (surlignage si sélectionné)
            border = 4 if i == selected_idx else 1
            border_color = (235, 235, 240) if i == selected_idx else COUL_GRILLE
            pygame.draw.rect(surface, COUL_CASE_VIDE, card, border_radius=10)
            pygame.draw.rect(surface, border_color, card, width=border, border_radius=10)

            # image
            img = self._get_thumb(getattr(room, "image", None), CHOIX_TAILLE - 8)
            if img:
                # centre l’image dans la carte
                ix = rx + (CHOIX_TAILLE - img.get_width()) // 2
                iy = ry + (CHOIX_TAILLE - img.get_height()) // 2
                surface.blit(img, (ix, iy))
            else:
                # fallback : badge couleur + nom
                pygame.draw.rect(surface, (60, 62, 74), card.inflate(-12, -12), border_radius=8)
                nom = getattr(room, "nom", "Room")
                txt = self.font_texte.render(nom, True, COUL_TEXTE)
                tx = rx + (CHOIX_TAILLE - txt.get_width()) // 2
                ty = ry + (CHOIX_TAILLE - txt.get_height()) // 2
                surface.blit(txt, (tx, ty))

        return card_rects


    # --- helpers directions (simples, locaux à Manoir) ---
    def _opp(self, d):
        return {Dir.UP:Dir.DOWN, Dir.DOWN:Dir.UP, Dir.LEFT:Dir.RIGHT, Dir.RIGHT:Dir.LEFT}[d]

    def _rot90_dir(self, d):
        return {Dir.UP:Dir.RIGHT, Dir.RIGHT:Dir.DOWN, Dir.DOWN:Dir.LEFT, Dir.LEFT:Dir.UP}[d]

    def _door_would_exit(self, i, j, d) -> bool:
        return ((i == 0 and d == Dir.UP) or
                (i == self.lignes-1 and d == Dir.DOWN) or
                (j == 0 and d == Dir.LEFT) or
                (j == self.colonnes-1 and d == Dir.RIGHT))

    # 1) Tourner la salle de 90° horaire
    def rotate_room_once(self, room) -> None:
        from .rooms.base import Door
        new_portes = {}
        for d, door in room.portes.items():
            nd = self._rot90_dir(d)
            new_portes[nd] = Door(door.level)
        room.portes = new_portes
        room.rot = (room.rot + 1) % 4 

    # 2) Tester l’orientation (True/False)
    def is_room_orientation_ok(self, room, i:int, j:int, came_from_dir) -> bool:
        # a) pas de porte qui sort
        need= None
        for d in room.portes.keys():
            if self._door_would_exit(i, j, d):
                return False, need
        # b) porte retour requise si on connaît la direction d’arrivée
        if came_from_dir is not None:
            need = self._opp(came_from_dir)  # ex: si on est venu par RIGHT, il faut LEFT
            if need not in room.portes:
                return False, need
        return True,need

    # 3) Essayer jusqu’à 4 rotations puis placer
    def place_room_oriented(self, room, i: int, j: int, came_from_dir) -> bool:
        """
        Tente de placer `room` à (i,j). On accepte si l'orientation est OK.
        Si OK, on met le niveau de la porte **de la nouvelle room** dans la direction `need` à 0
        (sans toucher aux autres portes de cette room).
        """
        for _ in range(4):
            ok, need = self.is_room_orientation_ok(room, i, j, came_from_dir)
            if ok:
                # -- Déverrouille uniquement la porte de la nouvelle salle côté `need`
                if need is not None:
                    current = room.portes.get(need)
                    # Si la room a déjà une porte côté `need`, remplace par Door(0) ;
                    if isinstance(current, Door):
                        if current.level != 0:
                            room.portes[need] = Door(0)


                # Place la room ; on ne touche pas aux autres directions/levels
                return True

            # orientation pas bonne -> on tourne la salle de 90°
            self.rotate_room_once(room)

        return False


    def show_message(self, text: str, seconds: float = 3.0) -> None:
        """Active un message non-bloquant pendant `seconds`."""
        self._msg_text = str(text)
        now = pygame.time.get_ticks()
        self._msg_until = now + int(seconds * 1000)

    def draw_message(self, surface: pygame.Surface) -> None:
        """A appeler à CHAQUE frame (si message actif, on le rend en overlay)."""
        if not self._msg_text:
            return
        if pygame.time.get_ticks() > self._msg_until:
            # message expiré
            self._msg_text = None
            return

        W, H = surface.get_width(), surface.get_height()
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))  # voile semi-transparent
        surface.blit(overlay, (0, 0))

        # boîte centrale
        pad_x, pad_y = 24, 16
        txt = self._msg_text
        surf = self.font_msg.render(txt, True, (235, 235, 240))
        box_w = min(max(320, surf.get_width() + 2*pad_x), W - 40)
        box_h = surf.get_height() + 2*pad_y
        box_x = (W - box_w)//2
        box_y = (H - box_h)//2

        rect = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(surface, (30, 33, 45), rect, border_radius=12)
        pygame.draw.rect(surface, (180, 200, 255), rect, width=2, border_radius=12)

        x = box_x + (box_w - surf.get_width())//2
        y = box_y + (box_h - surf.get_height())//2
        surface.blit(surf, (x, y))
