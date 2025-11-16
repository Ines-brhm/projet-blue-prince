# classes/main.py
import pygame
from .manoir import Manoir
from .joueur import Joueur
from .inventaire import Inventaire
from .rooms.blue_rooms import EntranceHall
from .tirage import attend_choix_joueur,place_room_oriented
from .end_game import etat_fin_partie
from .depense import payer_room_si_possible , try_open_shop
PANNEAU_LARGEUR = 500

def main():
    pygame.init()

    # État UI du draft
    mode_draft     = False
    draft_choices  = []   # liste de 3 rooms
    draft_selected = 0    # index sélectionné (0..2)

    inv    = Inventaire()
    manoir = Manoir()
    joueur = Joueur(pos_depart=manoir.pos_entree)
    joueur.inv = inv
    manoir.joueur = joueur

    # Salle de départ posée une fois
    i0, j0 = manoir.pos_entree
    manoir.grille[i0][j0] = EntranceHall()

    # Fenêtre
    fen = pygame.display.set_mode((manoir.largeur + PANNEAU_LARGEUR, manoir.hauteur))
    pygame.display.set_caption("Blue Prince - Prototype")
    manoir.fenetre = fen  # <--- AJOUT

    clock = pygame.time.Clock()
    running = True
    while running:
        # ----------------- ÉVÉNEMENTS -----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if event.type == pygame.KEYDOWN:
                # ESC quitte toujours
                if event.key == pygame.K_ESCAPE:
                    running = False
                    continue

                if mode_draft:
                    # -------- Mode draft : SEULES flèches + Enter sont prises en compte --------
                    if event.key == pygame.K_LEFT:
                        draft_selected = (draft_selected - 1) % len(draft_choices)
                    elif event.key == pygame.K_RIGHT:
                        draft_selected = (draft_selected + 1) % len(draft_choices)
                    elif event.key == pygame.K_a:  #utilisation du dés
                        bool_dice_use,dice_rooms=inv.use_item("dice", manoir, joueur)
                        if bool_dice_use:
                            draft_choices=dice_rooms
                            draft_selected = 0
                        else : 
                            manoir.show_message("vous n'avez pas de dés", 1.0) 
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        i, j = joueur.i, joueur.j
                        choix = draft_choices[draft_selected]
                        
                        
                        
                        if place_room_oriented(choix, i, j, getattr(joueur, "last_dir", None),manoir):
                            payee=payer_room_si_possible(choix, inv,manoir)
                            print(payee)
                            if payee:
                                manoir.grille[i][j] = choix
                            
                            # effet d'entrée
                                if hasattr(choix, "on_enter"):
                                    choix.on_enter(joueur, manoir)
                                # sortir du mode draft
                                mode_draft = False
                                draft_choices = []
                                draft_selected = 0
                        else :
                            # RE-TIRAGE 
                            draft_choices = attend_choix_joueur(manoir, joueur) or []
                            draft_selected = 0


                    # TOUTES les autres touches sont ignorées en mode draft
                    continue

                # -------- Mode normal : déplacements (ZQSD + flèches si tu veux) --------
                if event.key in (pygame.K_z, pygame.K_q, pygame.K_s, pygame.K_d,pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT,pygame.K_m,pygame.K_c):
                    if event.key == pygame.K_m:
                        try_open_shop(manoir, joueur, fen, inv)

                    elif event.key == pygame.K_c:
                        #manoir.essayer_creuser()
                        inv.use_item("shovel", manoir, joueur)
                        continue  

                    moved = joueur.deplacer_key(manoir, event.key)
                    etat_fin_partie(manoir, joueur, inv,fen)
                    if moved:
                        # Si la case est vide : proposer 3 rooms
                        choix = attend_choix_joueur(manoir, joueur)
                        if choix:
                            draft_choices  = choix
                            draft_selected = 0
                            mode_draft     = True
                        else:
                            # Case déjà occupée → déclencher l'effet au besoin
                            r = manoir.grille[joueur.i][joueur.j]
                            if hasattr(r, "on_enter"):
                                r.on_enter(joueur, manoir)

        # ----------------- RENDU -----------------
        manoir.dessiner_grille(fen)
        manoir.dessiner_panneau(fen, inv)
        if mode_draft and draft_choices:
            manoir.dessiner_draft_choices(fen, draft_choices, draft_selected)
        joueur.dessiner(fen)
        manoir.draw_message(fen)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
