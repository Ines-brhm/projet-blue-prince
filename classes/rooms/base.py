# classes/pieces/base.py
from enum import Enum
from dataclasses import dataclass

class Dir(Enum):
    UP="U"; DOWN="D"; LEFT="L"; RIGHT="R"

@dataclass(frozen=True)
class Door:
    level: int = 0  # 0=ouverte, 1=verrou, 2=double-verrou

class BaseSalle:
    """
    Classe de base : ce que TOUTES les salles partagent.
    """
    def __init__(
        self,
        nom: str,
        couleur: str,
        portes: dict,
        image: str,
        cout_gemmes: int = 0,
        rarity: int = 0,
    ):
        self.nom = nom
        self.couleur = couleur
        self.portes = portes
        self.cout_gemmes = cout_gemmes
        self.image = image
        self.rot = 0 
        # Sécurise la valeur dans [0..3]
        self.rarity = max(0, min(3, int(rarity)))

    # Hooks (comportements)
    def on_enter(self, joueur, manoir) -> None:
        pass

    def on_visit(self, joueur, manoir) -> None:
        pass

    # Utilitaire
    def a_porte(self, d: Dir) -> bool:
        return d in self.portes
