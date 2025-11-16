# classes/ouverture_portes.py
import pygame

def _draw_overlay(fenetre, lines, selected=None):
    """Petit overlay semi-transparent + panneau avec 2–3 lignes."""
    w, h = fenetre.get_size()
    # voile
    voilesurf = pygame.Surface((w, h), pygame.SRCALPHA)
    voilesurf.fill((0, 0, 0, 170))
    fenetre.blit(voilesurf, (0, 0))

    # panneau
    pw, ph = 520, 200
    rect = pygame.Rect((w - pw)//2, (h - ph)//2, pw, ph)
    pygame.draw.rect(fenetre, (35, 38, 52), rect, border_radius=12)
    pygame.draw.rect(fenetre, (200, 205, 220), rect, width=2, border_radius=12)

    font_title = pygame.font.Font(None, 36)
    font_line  = pygame.font.Font(None, 28)

    titre = font_title.render("Porte verrouillée", True, (230, 230, 240))
    fenetre.blit(titre, (rect.x + 20, rect.y + 16))

    y = rect.y + 64
    for i, txt in enumerate(lines):
        surf = font_line.render(txt, True, (235, 235, 240))
        fenetre.blit(surf, (rect.x + 20, y))
        y += 34

    pygame.display.flip()

def demande_ouverture(fenetre, inv, level: int) -> bool:
    """
    Fenêtre bloquante:
      - level 1: [E] Crochetage (-1 lockpick)  |  [R] Clé (-1 key)  |  [T] Annuler
      - level 2: [R] Clé (-1 key)              |  [T] Annuler
    Retourne True si la porte a été ouverte (et l’inventaire débité), False sinon.
    """
    # valeurs d’inventaire (avec fallback si l’attribut n’existe pas)
    keys      = getattr(inv, "keys", 0)
    lockpicks = getattr(inv, "lockpicks", 0)

    # messages d’option
    if level == 1:
        lines = [
            f"[E] Crocheter (-1 pick)  — dispo: {lockpicks}",
            f"[R] Ouvrir avec clé (-1) — dispo: {keys}",
            "[T] Annuler",
        ]
    else:  # level >= 2
        lines = [
            f"[R] Ouvrir avec clé (-1) — dispo: {keys}",
            "[T] Annuler",
        ]

    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        _draw_overlay(fenetre, lines)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                # Niveau 1 : clé ou crochetage
                if level == 1:
                    if event.key == pygame.K_e:
                        # crocheter
                        lockpick_open,data=inv.use_item("lockpick", manoir=None, joueur=None)
                        if lockpick_open :
                            return True
                        else:
                            _draw_overlay(fenetre, lines + ["", "❌ Pas de pick disponible"])
                            pygame.time.delay(900)
                    elif event.key == pygame.K_r:
                        # clé
                        if keys > 0:
                            setattr(inv, "keys", keys - 1)
                            return True
                        else:
                            _draw_overlay(fenetre, lines + ["", "❌ Pas de clé disponible"])
                            pygame.time.delay(900)
                    elif event.key == pygame.K_t:
                        return False

                # Niveau 2 : uniquement clé (ou annuler)
                else:
                    if event.key == pygame.K_r:
                        if keys > 0:
                            setattr(inv, "keys", keys - 1)
                            return True
                        else:
                            _draw_overlay(fenetre, lines + ["", "❌ Pas de clé disponible"])
                            pygame.time.delay(900)
                    elif event.key == pygame.K_t:
                        return False

        clock.tick(60)
