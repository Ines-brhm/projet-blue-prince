# classes/rooms/tirage.py
import random
from .rooms.purple_rooms import Bedroom
from .rooms.red_rooms import Chapel  # adapte le nom si ton fichier s'appelle autrement
from .rooms.blue_rooms import Garage
# --- Pioche : usines qui créent une NOUVELLE instance à chaque tirage ---
FACTORIES = [
    lambda: Bedroom(),
    lambda: Garage(),
]

def piocher_room():
    """Retourne une nouvelle instance tirée au hasard depuis la pioche."""
    return random.choice(FACTORIES)()

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
