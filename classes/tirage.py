# classes/rooms/tirage.py
import random
from .rooms.purple_rooms import Bedroom
from .rooms.red_rooms import Chapel ,WeightRoom   # adapte le nom si ton fichier s'appelle autrement
from .rooms.blue_rooms import Garage, Vault  
from .rooms.base import Door  # et Dir si besoin ailleurs
from .rooms.green_rooms import Veranda, Terrace
from .rooms.orange_rooms import Hallway, Foyer,WestWingHall,Passageway

def is_border(i: int, j: int, lignes: int, colonnes: int) -> bool:
    """Retourne True si (i, j) est sur la bordure de la grille."""
    return (
        i == 0
        or i == lignes - 1
        or j == 0
        or j == colonnes - 1
    )


# --- Pioche : usines qui créent une NOUVELLE instance à chaque tirage ---
FACTORIES = [
    lambda: Bedroom(),
    lambda: Garage(),
    lambda: Chapel(),
    lambda: WeightRoom(),
    lambda: Vault(),
    lambda: Veranda(),
    lambda: Terrace(),
    lambda: Hallway(),
    lambda: Foyer(),
    lambda: WestWingHall(),
    lambda: Passageway(),
]


all_rooms = [f() for f in FACTORIES]

def piocher_roomss(k: int = 3, i: int = None, j: int = None, manoir=None):
    rooms_possible = [f() for f in FACTORIES]

    

    if i is not None and j is not None and manoir is not None \
   and not is_border(i, j, manoir.lignes, manoir.colonnes):

     rooms_possible = [
        r for r in rooms_possible
        if not getattr(r, "border_only", False)
]


    rooms = random.sample(rooms_possible, k)
    rooms = [randomize_doors_progress(r, i) for r in rooms]
    print("j'ai tiré des chambres :", ", ".join(r.nom for r in rooms))
    return rooms

 

def attend_choix_joueur(manoir, joueur):
    i, j = joueur.i, joueur.j
    if manoir.grille[i][j] is None:
        # 3 rooms tirées pour un draft
        return piocher_roomss(3,i,j,manoir) #on ajoute j et manoir pour les bordures 
    return []


def randomize_doors(room):
    """Randomise uniquement le niveau de verrou des portes déjà définies."""
    portes = getattr(room, "portes", None)
    if portes:  # True si dict non vide
        room.portes = {d: Door(random.randint(0, 2)) for d in portes.keys()}
    return room



def _sample_level(progress: float) -> int:
    """
    Donne un niveau {0,1,2} en fonction de la progression 0..1.
    0 = début de journée (portes ouvertes), 1 = vers le haut (portes dures).
    """
    # barème simple (ajuste si tu veux)
    if progress <= 0.25:
        p0, p1, p2 = 1.00, 0.00, 0.00       # tout ouvert
    elif progress <= 0.50:
        p0, p1, p2 = 0.60, 0.40, 0.00       # un peu de lvl1
    elif progress <= 0.80:
        p0, p1, p2 = 0.30, 0.50, 0.20       # lvl2 commence à apparaître
    else:
        p0, p1, p2 = 0.00, 0.40, 0.60       # surtout lvl2

    r = random.random()
    if r < p0:  return 0
    if r < p0 + p1: return 1
    return 2

def randomize_doors_progress(room, i: int):
    """Randomise les NIVEAUX de verrous selon la rangée i."""
    portes = getattr(room, "portes", None)
    if not portes or getattr(room, "fixed_doors", False):
        return room

    # i == 0 : toutes les portes niveau 2
    if i == 0:
        room.portes = {d: Door(2) for d in portes.keys()}
        return room

    # progression 0..1 (0 = bas/entrée ; 1 = haut)
    progress = (9 - i) / 9      # 0 au départ → 1 en haut

    room.portes = {d: Door(_sample_level(progress)) for d in portes.keys()}
    return room
