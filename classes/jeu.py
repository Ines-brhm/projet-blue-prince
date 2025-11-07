
import pygame

def lancer(self):
    fenetre = pygame.display.set_mode((900, 500))
    pygame.display.set_caption("Blue Prince - Version Étudiante")

    en_cours = True
    while en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False

        fenetre.fill((30, 30, 30))  # fond gris foncé
        pygame.display.flip()

