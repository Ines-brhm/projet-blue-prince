# classes/main.py
import pygame
from .manoir import Manoir
from .joueur import Joueur
from .inventaire import Inventaire
from .rooms.blue_rooms import EntranceHall  # ta room de départ
from .tirage import ensure_room_and_trigger  # <--- AJOUT

PANNEAU_LARGEUR = 260

def main():
    pygame.init()

    inventaire = Inventaire()
    manoir = Manoir()
    joueur = Joueur(pos_depart=manoir.pos_entree)
    joueur.inv=inventaire

    # 1) Créer l'instance de la salle de départ
    start_room = EntranceHall()  

    # 2) Récupérer la case d'entrée
    i, j = manoir.pos_entree  # (ligne, colonne)

    # 3) Poser la salle UNE FOIS sur la case d’entrée
    manoir.grille[i][j] = start_room

    # Fenêtre = grille + panneau à droite
    fenetre = pygame.display.set_mode((manoir.largeur + PANNEAU_LARGEUR, manoir.hauteur))
    pygame.display.set_caption("Blue Prince - Prototype")

    clock = pygame.time.Clock()
    en_cours = True
    while en_cours:
        # --- événements ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    en_cours = False
                # ZQSD → déplacement via can_move (portes)
                elif event.key in (pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d):
                    if joueur.deplacer_key(manoir, event.key):
                        ensure_room_and_trigger(manoir, joueur)  # ← poser si vide + on_enter
                    
        # --- rendu ---
        manoir.dessiner_grille(fenetre)
        manoir.dessiner_panneau(fenetre, inventaire)
        joueur.dessiner(fenetre)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
