

# # classes/main.py
import pygame
from .manoir import Manoir
from .joueur import Joueur
from .inventaire import Inventaire


PANNEAU_LARGEUR = 260

def main():
    pygame.init()
    inventaire = Inventaire()
    manoir = Manoir()
    joueur = Joueur(pos_depart=manoir.pos_entree)
    
    
    # largeur totale = largeur grille + panneau

    #fenetre = pygame.display.set_mode((manoir.largeur, manoir.hauteur))
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
                elif event.key == pygame.K_z:
                    joueur.deplacer("Z")
                elif event.key == pygame.K_q:
                    joueur.deplacer("Q")
                elif event.key == pygame.K_s:
                    joueur.deplacer("S")
                elif event.key == pygame.K_d:
                    joueur.deplacer("D")

        # --- rendu ---
        manoir.dessiner_grille(fenetre)
        manoir.dessiner_panneau(fenetre,inventaire)
        joueur.dessiner(fenetre)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
