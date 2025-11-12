# classes/main.py
import pygame
from .manoir import Manoir
from .joueur import Joueur
from .inventaire import Inventaire
from .rooms.blue_rooms import EntranceHall  # ta room de départ
from .tirage import ensure_room_and_trigger ,attend_choix_joueur # <--- AJOUT

PANNEAU_LARGEUR = 500

def main():
    pygame.init()

    # état global
    mode_draft = False
    draft_choices = []
    draft_selected = 0
    
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
                    # après un déplacement réussi :
                    if joueur.deplacer_key(manoir, event.key):
                        choix = attend_choix_joueur(manoir, joueur)
                        if choix:                    # case vide -> on propose 3 rooms
                            draft_choices = choix
                            draft_selected = 0
                            mode_draft = True
                        else:
                            # case déjà occupée -> on_enter si tu veux
                            room = manoir.grille[joueur.i][joueur.j]
                            if hasattr(room, "on_enter"): room.on_enter(joueur, manoir)

                    # gestion des touches en mode draft
                    elif event.type == pygame.KEYDOWN and mode_draft:
                        if event.key == pygame.K_q:
                            draft_selected = (draft_selected - 1) % len(draft_choices)
                        elif event.key == pygame.K_d:
                            draft_selected = (draft_selected + 1) % len(draft_choices)
                        elif event.key in (pygame.K_s, pygame.K_KP_ENTER): 
                            i, j = joueur.i, joueur.j
                            choix = draft_choices[draft_selected]
                            print(choix.portes) # ligne pour verifier si les porte sont bien prise en compte
                            if hasattr(choix, "on_draft"): choix.on_draft(joueur, manoir)
                            manoir.grille[i][j] = choix
                            if hasattr(choix, "on_enter"): choix.on_enter(joueur, manoir)
                            mode_draft = False
                            draft_choices = []
        # --- rendu ---
        manoir.dessiner_grille(fenetre)
        manoir.dessiner_panneau(fenetre, inventaire)
        if mode_draft and draft_choices:
            manoir.dessiner_draft_choices(fenetre, draft_choices, draft_selected)
        joueur.dessiner(fenetre)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
