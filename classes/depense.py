
# classes/depense.py
import pygame

def payer_room_si_possible(room, inventaire,manoir):
    """
    Tente de payer le coût en gemmes de `room` avec `inventaire`.
    - Si la salle ne coûte rien (cout_gemmes <= 0) -> retourne `room`.
    - Si elle coûte > 0 :
        * essaie d'appeler une méthode de paiement si elle existe
          (payer_gemmes ou payer_gemme),
        * sinon, vérifie inventaire.gems et décrémente.
      Retourne `room` si le paiement est possible/effecuté, sinon `None`.
    """
    cout = getattr(room, "cout_gemmes", 0) or 0

    # Pas de coût -> OK
    if cout <= 0:
        return True

    # Essayer une méthode officielle si elle existe
    if hasattr(inventaire, "payer_gemmes"):
        ok = inventaire.payer_gemmes(cout)
        if ok:
            manoir.show_message( "vous avez payer des gemmes",1.0) 
            return True
        else:
            # Pas assez de gemmes
            manoir.show_message( "vous n'avez pas assez de gemmes",1.0) 
            return False




# ---- Catalogue (modifiable facilement) ----
PRODUCTS = [
    {"id":"apple",    "label":"Pomme",    "steps": 2,  "price": 2},
    {"id":"banana",   "label":"Banane",   "steps": 3,  "price": 3},
    {"id":"cake",     "label":"Gâteau",   "steps":10,  "price": 7},
    {"id":"sandwich", "label":"Sandwich", "steps":15,  "price":10},
    {"id":"meal",     "label":"Repas",   "steps":25,  "price":15},
    {"id":"detector", "label":"Détecteur de métaux", "steps": 0, "price":5},
    {"id":"rabbit_foot", "label":"Patte de lapin", "steps": 0, "price":8}
]

# ---------- AFFICHAGE (overlay bloquant) ----------
def _draw_shop_overlay(fenetre, products, selected_idx, gold):
    w, h = fenetre.get_size()
    voile = pygame.Surface((w, h), pygame.SRCALPHA)
    voile.fill((0, 0, 0, 180))
    fenetre.blit(voile, (0, 0))

    panel_w, panel_h = 520, 360
    rect = pygame.Rect((w - panel_w)//2, (h - panel_h)//2, panel_w, panel_h)
    pygame.draw.rect(fenetre, (35, 38, 52), rect, border_radius=12)
    pygame.draw.rect(fenetre, (200, 205, 220), rect, width=2, border_radius=12)

    font_title = pygame.font.Font(None, 40)
    font_line  = pygame.font.Font(None, 28)
    title = font_title.render("Magasin (M pour fermer)", True, (235,235,240))
    fenetre.blit(title, (rect.x + 16, rect.y + 12))

    gold_txt = font_line.render(f"Or: {gold}", True, (255, 230, 120))
    fenetre.blit(gold_txt, (rect.right - gold_txt.get_width() - 16, rect.y + 18))

    y = rect.y + 70
    for i, p in enumerate(products):
        if p["id"] == "detector":
          line = f"{p['label']}  —  +{p['steps']} pas   |   {p['price']} or"
        elif p["id"] == "rabbit_foot":
            line = f"{p['label']}  —  +{p['steps']} pas |   {p['price']} or"
        else:
            line = f"{p['label']}  —  +{p['steps']} pas   |   {p['price']} or"
        color = (235,235,240) if i != selected_idx else (120, 200, 255)
        surf = font_line.render(line, True, color)
        fenetre.blit(surf, (rect.x + 16, y))
        y += 40

    hint = pygame.font.Font(None, 24).render("←/→ pour choisir • Enter pour acheter • M/Echap pour quitter", True, (200,200,210))
    fenetre.blit(hint, (rect.x + 16, rect.bottom - 36))

    pygame.display.flip()

def _flash_msg(fenetre, text, color=(255,120,120), ms=900):
    """Petit message d’erreur/succès dans le bas du panneau."""
    w, h = fenetre.get_size()
    font = pygame.font.Font(None, 30)
    surf = font.render(text, True, color)
    x = (w - surf.get_width()) // 2
    y = h - surf.get_height() - 20
    bg  = pygame.Surface((surf.get_width()+20, surf.get_height()+12), pygame.SRCALPHA)
    bg.fill((0,0,0,160))
    fenetre.blit(bg, (x-10, y-6))
    fenetre.blit(surf, (x, y))
    pygame.display.flip()
    pygame.time.delay(ms)

# ---------- LOGIQUE (boucle bloquante) ----------
def open_shop_blocking(fenetre, inv):
    """
    Ouvre le magasin en mode bloquant.
    - Flèches gauche/droite pour naviguer
    - Enter pour acheter (si assez d’or)
    - M / Esc pour fermer
    Retourne True si un achat a été effectué, sinon False.
    """
    selected = 0
    clock = pygame.time.Clock()
    bought_any = False

    while True:
        _draw_shop_overlay(fenetre, PRODUCTS, selected, getattr(inv, "gold", 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return bought_any
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_m):
                    return bought_any
                elif event.key in (pygame.K_LEFT, pygame.K_q):
                    selected = (selected - 1) % len(PRODUCTS)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    selected = (selected + 1) % len(PRODUCTS)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    item = PRODUCTS[selected]
                    price = item["price"]
                    gold  = getattr(inv, "gold", 0)

                    #  si c'est le détecteur et qu'on en a déjà un
                    if item["id"] == "detector" and inv.metal_detector>=1:
                        _flash_msg(fenetre, "Tu as déjà un détecteur.", (255,120,120))
                        continue
                    if item["id"] == "rabbit_foot" and inv.rabbit_foot>=1:
                        _flash_msg(fenetre, "Tu as déjà un pas de lapin.", (255,120,120))
                        continue

                    if gold < price:
                        _flash_msg(fenetre, " Or insuffisant", (255,120,120))
                    else:
                        setattr(inv, "gold", gold - price)

                        if item["id"] == "detector":
                            # achat du détecteur : on n'ajoute PAS de steps
                            setattr(inv, "metal_detector", 1)
                            _flash_msg(fenetre, "Détecteur acheté !", (120,255,160))

                        elif item["id"] == "rabbit_foot":
                            setattr(inv, "rabbit_foot",inv.rabbit_foot + 1)
                            _flash_msg(fenetre, "Pas de lapin acheté !", (120,255,160))

   
                        else:
                            # achat normal de nourriture = des pas
                            steps = item["steps"]
                            setattr(inv, "steps", getattr(inv, "steps", 0) + steps)
                            _flash_msg(
                                fenetre,
                                f" +{steps} pas (-{price} or)",
                                (120,255,160),
                            )

                        bought_any = True
        clock.tick(60)


# ---------- Garde-fou côté gameplay ----------
def try_open_shop(manoir, joueur, fenetre, inv):
    """
    Ouvre le shop SEULEMENT si la salle courante est un magasin.
    Convention simple : room.couleur == 'yellow'  OU room.is_shop == True
    """
    room = manoir.grille[joueur.i][joueur.j]
    is_shop = room and (getattr(room, "couleur", None) == "yellow")
    if not is_shop:
        manoir.show_message("Ici, il n'y a pas de magasin.", 1.0)
        return False
    return open_shop_blocking(fenetre, inv)
