import pygame

def afficher_ecran_fin(fenetre, titre="GAME OVER", sous_titre="Appuie sur ESC ou ferme la fenêtre"):
    w, h = fenetre.get_size()
    # voile sombre
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    fenetre.blit(overlay, (0, 0))

    # panneau
    rect = pygame.Rect(0, 0, min(600, w - 80), 220)
    rect.center = (w // 2, h // 2)
    pygame.draw.rect(fenetre, (35, 38, 52), rect, border_radius=14)
    pygame.draw.rect(fenetre, (210, 215, 230), rect, width=2, border_radius=14)

    font_title = pygame.font.Font(None, 64)
    font_sub   = pygame.font.Font(None, 32)
    surf_t = font_title.render(titre, True, (240, 240, 250))
    surf_s = font_sub.render(sous_titre, True, (220, 220, 230))

    fenetre.blit(surf_t, (rect.centerx - surf_t.get_width()//2, rect.y + 36))
    fenetre.blit(surf_s, (rect.centerx - surf_s.get_width()//2, rect.y + 120))
    pygame.display.flip()

    # boucle bloquante jusqu'à fermeture/ESC
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        clock.tick(60)


# classes/fin_partie.py
def etat_fin_partie(manoir, joueur, inv,fenetre):
    """
    Retourne:
      - "win"  si le joueur est arrivé en (0, milieu)
      - "lose" si inv.steps <= 0
      - None   sinon
    """
    if inv is None:
        return None
    # défaite : plus de pas
    if getattr(inv, "steps", 0) <= 0:
        afficher_ecran_fin(fenetre,"GAME OVER","Appuie sur ESC ou ferme la fenêtre")
        return "lose"
    # victoire : haut / milieu
    i, j = joueur.i, joueur.j
    if i == 0 and j == (manoir.colonnes // 2):
        afficher_ecran_fin(fenetre," VICTORY","Appuie sur ESC ou ferme la fenêtre")
        return "win"
    return None
