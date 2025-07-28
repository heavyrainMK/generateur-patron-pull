# *******************************************************
# Nom ......... : front.py
# Rôle ........ : Définition de la classe Front représentant le devant du pull et encapsulant ses mesures et calculs spécifiques.
# Auteurs ..... : M, L, M
# Version ..... : V1.0.0 du 28/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : Classe héritant de Calculs pour modéliser le devant d'un pull. Elle stocke la largeur de poitrine et la longueur
#                 depuis l'aisselle jusqu'à l'ourlet, ainsi que les mailles du devant (incluant une séparation pour l'encolure en V).
# Technologies  : Python
# Dépendances . : calculs (classe Calculs)
# Usage ....... : Instanciée dans app.py pour représenter la partie avant du pull.
# *******************************************************

from calculs import Calculs

class Front(Calculs):
    """
    Représente la partie avant (devant) d'un pull top-down.

    Le devant est défini par :
      * la largeur de poitrine (chest_width) exprimée en centimètres ;
      * la longueur entre l'aisselle et l'ourlet (underarm_to_hem_length) en centimètres.

    Pour réaliser une encolure en V, on ne monte pas toutes les mailles du devant immédiatement :
    seules deux mailles sont montées de chaque côté (right_front_stitches et left_front_stitches) et les
    mailles manquantes seront ajoutées au fur et à mesure des augmentations.
    """

    def __init__(self, chest_width: float, underarm_to_hem_length: float) -> None:
        """
        Initialise une instance de Front avec les mesures fournies.

        :param chest_width: Largeur de la poitrine en centimètres.
        :param underarm_to_hem_length: Longueur entre l'aisselle et l'ourlet en centimètres.
        """
        super().__init__()
        self.chest_width = chest_width
        self.underarm_to_hem_length = underarm_to_hem_length
        self.chest_stitches = 0
        self.rows_to_hem = 0
        # Pour obtenir une encolure en V, on monte seulement deux mailles de chaque côté du devant,
        # le reste des mailles étant ajouté au fur et à mesure des augmentations.
        self.right_front_stitches = 2
        self.left_front_stitches = 2

    def getChestWidth(self) -> float:
        """Renvoie la largeur de la poitrine (en centimètres)."""
        return self.chest_width

    def getUnderArmToHemLength(self) -> float:
        """Renvoie la longueur entre l'aisselle et l'ourlet (en centimètres)."""
        return self.underarm_to_hem_length

    def setChestStitches(self, nb_of_stitches: int) -> None:
        """Enregistre le nombre total de mailles du devant après calcul."""
        self.chest_stitches = nb_of_stitches

    def getChestStitches(self) -> int:
        """Renvoie le nombre total de mailles du devant."""
        return self.chest_stitches

    def setRowsToHem(self, nb_of_rows: int) -> None:
        """Enregistre le nombre de rangs nécessaires pour atteindre l'ourlet."""
        self.rows_to_hem = nb_of_rows

    def getRowsToHem(self) -> int:
        """Renvoie le nombre de rangs nécessaires pour atteindre l'ourlet."""
        return self.rows_to_hem

    def getRightFrontStitches(self) -> int:
        """Renvoie le nombre de mailles montées initialement pour le devant droit."""
        return self.right_front_stitches

    def getLeftFrontStitches(self) -> int:
        """Renvoie le nombre de mailles montées initialement pour le devant gauche."""
        return self.left_front_stitches

    def __str__(self) -> str:
        """Renvoie une description textuelle des mesures du devant."""
        return (
            f"Le devant mesure CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle "
            f"jusqu'a l'ourlet. Le tour de poitrine est {self.chest_width}"
        )