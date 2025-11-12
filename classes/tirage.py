# classes/rooms/tirage.py
import random
from .rooms.purple_rooms import Bedroom
from .rooms.red_rooms import Chapel ,WeightRoom   # adapte le nom si ton fichier s'appelle autrement
from .rooms.blue_rooms import Garage
# --- Pioche : usines qui créent une NOUVELLE instance à chaque tirage ---
FACTORIES = [
    lambda: Bedroom(),
    lambda: Garage(),
    lambda: Chapel(),
    lambda: WeightRoom(),
]

def piocher_room():
    """Retourne une nouvelle instance tirée au hasard depuis la pioche."""
    return random.choice(FACTORIES)()

def piocher_rooms(k: int = 3, replace: bool = False):
    """
    Tire k rooms et retourne une liste d'**instances**.
    - replace=False (défaut) : tirage **sans remise** (si k <= nb de FACTORIES).
    - replace=True  : tirage **avec remise** (autorise des doublons).
    """
    if replace or k > len(FACTORIES):
        # avec remise
        return [random.choice(FACTORIES)() for _ in range(k)]
    # sans remise
    return [f() for f in random.sample(FACTORIES, k)]

def placer_si_vide(manoir, i: int, j: int):
    """
    Si la case (i,j) est vide, on pioche et on place une room.
    Retourne la room placée, sinon None si déjà occupée.
    """
    if manoir.grille[i][j] is None:
        room = piocher_room()
        manoir.grille[i][j] = room
        return room
    return None

def ensure_room_and_trigger(manoir, joueur):
    """
    À appeler quand le joueur arrive sur une case.
    - Si la case est vide: on pioche et on place.
    - On déclenche l'effet de la room: on_enter(joueur, manoir).
    Retourne la room présente (placée ou existante).
    """
    i, j = joueur.i, joueur.j
    room = manoir.grille[i][j]
    if room is None:
        room = piocher_room()
        manoir.grille[i][j] = room
    # appliquer l'effet d'entrée
    if hasattr(room, "on_enter"):
        room.on_enter(joueur, manoir)
    return room


def attend_choix_joueur(manoir, joueur):
    i, j = joueur.i, joueur.j
    if manoir.grille[i][j] is None:
        # 3 rooms tirées pour un draft
        return piocher_rooms(3, replace=False)  # sans doublons si possible
    return []