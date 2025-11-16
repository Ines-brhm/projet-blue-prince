# classes/tirage.py
import random
from .rooms.base import Dir  

from .rooms.purple_rooms import Bedroom,GuestBedroom,Boudoir,MasterBedroom,ServantsQuarters,Nursery
from .rooms.red_rooms import Chapel ,WeightRoom,Gymnasium,Lavatory
from .rooms.blue_rooms import Garage, Vault,Den,WineCellar,Pantry,TrophyRoom,RumpusRoom,Nook,SpareRoom
from .rooms.base import Door  # et Dir si besoin ailleurs
from .rooms.green_rooms import Veranda, Terrace,Cloister,Courtyard,Patio
from .rooms.orange_rooms import Hallway, Foyer,WestWingHall,Passageway,EastWingHall,Corridor
from .rooms.yellow_rooms import Locksmith, Kitchen

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
    lambda: Gymnasium(),
    lambda: Locksmith(),
    lambda: Kitchen(),
    lambda: EastWingHall(),
    lambda: Corridor(),
    lambda: GuestBedroom(),
    lambda: Boudoir(),
    lambda: MasterBedroom(),
    lambda: ServantsQuarters(),
    lambda: Nursery(),
    lambda: Cloister(),
    lambda: Courtyard(),
    lambda: Patio(),
    lambda: Lavatory(),
    lambda: Den(),
    lambda: WineCellar(),
    lambda: Pantry(),
    lambda: TrophyRoom(),
    lambda: RumpusRoom(),
    lambda: Nook(),
    lambda: SpareRoom(),
]

all_rooms = [f() for f in FACTORIES]

def piocher_roomss(k: int = 3, i: int = None, j: int = None, manoir=None,inv=None):
    rooms_possible = [f() for f in FACTORIES]


    if i is not None and j is not None and manoir is not None \
   and not is_border(i, j, manoir.lignes, manoir.colonnes):

     rooms_possible = [
        r for r in rooms_possible
        if not getattr(r, "border_only", False)
]

     
    bonus_rare = 0.0  # pas du lapin
    if inv is not None and inv.rabbit_foot > 0:
        bonus_rare = 0.10 * inv.rabbit_foot   # +10% par lapin
        inv.rabbit_foot = 0                   # on consomme tous les pas de lapin

    # Détection des rooms rares
    rare_rooms = [r for r in rooms_possible if getattr(r, "rare", False)]

    weighted_list = []
    for r in rooms_possible:
        if getattr(r, "rare", False):
            weighted_list.append(r)
            if random.random() < bonus_rare:
                weighted_list.append(r)     # double apparition = plus de chances
        else:
            weighted_list.append(r)

    # Tirage final
    rooms = random.sample(weighted_list, k)
    rooms = [randomize_doors_progress(r, i) for r in rooms]
    print("j'ai tiré des chambres :", ", ".join(r.nom for r in rooms))
    return rooms

 

def attend_choix_joueur(manoir, joueur):
    i, j = joueur.i, joueur.j
    if manoir.grille[i][j] is None:
        # 3 rooms tirées pour un draft
        return piocher_roomss(3,i,j,manoir,joueur.inv) #on ajoute j et manoir pour les bordures 
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


# --- helpers directions (simples, locaux à tirage) ---
def _opp(d):
    return {Dir.UP:Dir.DOWN, Dir.DOWN:Dir.UP, Dir.LEFT:Dir.RIGHT, Dir.RIGHT:Dir.LEFT}[d]

def _rot90_dir(d):
    return {Dir.UP:Dir.RIGHT, Dir.RIGHT:Dir.DOWN, Dir.DOWN:Dir.LEFT, Dir.LEFT:Dir.UP}[d]

def _door_would_exit(i, j, d,manoir) -> bool:
    return ((i == 0 and d == Dir.UP) or
            (i == manoir.lignes-1 and d == Dir.DOWN) or
            (j == 0 and d == Dir.LEFT) or
            (j == manoir.colonnes-1 and d == Dir.RIGHT))

# 1) Tourner la salle de 90° horaire
def rotate_room_once(room) -> None:
    new_portes = {}
    for d, door in room.portes.items():
        nd =_rot90_dir(d)
        new_portes[nd] = Door(door.level)
    room.portes = new_portes
    room.rot = (room.rot + 1) % 4 


# 2) Tester l’orientation (True/False)
def is_room_orientation_ok(room, i:int, j:int, came_from_dir,manoir) -> bool:
    # a) pas de porte qui sort
    need= None
    for d in room.portes.keys():
        if _door_would_exit(i, j, d, manoir):
            return False, need
    # b) porte retour requise si on connaît la direction d’arrivée
    if came_from_dir is not None:
        need =_opp(came_from_dir)  # ex: si on est venu par RIGHT, il faut LEFT
        if need not in room.portes:
            return False, need
    return True,need


# 3) Essayer jusqu’à 4 rotations puis placer
def place_room_oriented(room, i: int, j: int, came_from_dir,manoir) -> bool:
    """
    Tente de placer `room` à (i,j). On accepte si l'orientation est OK.
    Si OK, on met le niveau de la porte **de la nouvelle room** dans la direction `need` à 0
    (sans toucher aux autres portes de cette room).
    """
    for _ in range(4):
        ok, need = is_room_orientation_ok(room, i, j, came_from_dir,manoir)
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
        rotate_room_once(room)

    return False
