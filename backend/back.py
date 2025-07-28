# *******************************************************
# Nom ......... : back.py
# Rôle ........ : Définition de la classe Back représentant le dos du pull et encapsulant ses mesures et calculs spécifiques.
# Auteurs ..... : M, L, M
# Version ..... : V1.0.0 du 28/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : Classe héritant de Calculs pour modéliser le dos d'un pull. Elle stocke la largeur de nuque, la largeur de poitrine,
#                 la profondeur d'emmanchure et la longueur entre l'aisselle et l'ourlet. La classe fournit des accesseurs et mutateurs
#                 pour les nombres de mailles et de rangs calculés et délègue le calcul du rythme des augmentations raglan à la classe parente.
# Technologies  : Python
# Dépendances . : calculs (classe Calculs)
# Usage ....... : Instanciée dans app.py pour représenter la partie arrière du pull.
# *******************************************************

from calculs import Calculs

class Back(Calculs):
    """
    Représente la partie arrière (dos) d'un pull top-down.

    Le dos est défini par :
      * la largeur de nuque (neck_width) en centimètres ;
      * la largeur de poitrine (chest_width) en centimètres ;
      * la profondeur d'emmanchure (armhole_depth) en centimètres ;
      * la longueur entre l'aisselle et l'ourlet (underarm_to_hem_length) en centimètres.

    La classe fournit des accesseurs et mutateurs pour les mailles et rangs calculés et délègue au parent
    le calcul du rythme des augmentations raglan.
    """

    def __init__(self, neck_width: float, chest_width: float, armhole_depth: float, underarm_to_hem_length: float) -> None:
        """
        Initialise une instance de Back avec les mesures fournies.

        :param neck_width: Largeur de l'encolure au niveau de la nuque (en centimètres).
        :param chest_width: Largeur de poitrine en centimètres.
        :param armhole_depth: Profondeur d'emmanchure en centimètres (distance verticale de l'encolure à l'aisselle).
        :param underarm_to_hem_length: Longueur entre l'aisselle et l'ourlet en centimètres.
        """
        super().__init__()
        self.neck_width = neck_width
        self.chest_width = chest_width
        self.armhole_depth = armhole_depth
        self.underarm_to_hem_length = underarm_to_hem_length
        self.neck_stitches = 0
        self.chest_stitches = 0
        self.rows_to_underarm = 0
        self.rows_to_hem = 0

    def getNeckWidth(self) -> float:
        """Renvoie la largeur de l'encolure au niveau de la nuque (en centimètres)."""
        return self.neck_width

    def getChestWidth(self) -> float:
        """Renvoie la largeur de la poitrine (en centimètres)."""
        return self.chest_width

    def getArmholeDepth(self) -> float:
        """Renvoie la profondeur d'emmanchure (en centimètres)."""
        return self.armhole_depth

    def getUnderArmToHemLength(self) -> float:
        """Renvoie la longueur entre l'aisselle et l'ourlet (en centimètres)."""
        return self.underarm_to_hem_length

    def setNeckStitches(self, nb_of_stitches: int) -> None:
        """Enregistre le nombre de mailles à monter pour l'encolure du dos."""
        self.neck_stitches = nb_of_stitches

    def getNeckStitches(self) -> int:
        """Renvoie le nombre de mailles de l'encolure du dos."""
        return self.neck_stitches

    def setChestStitches(self, nb_of_stitches: int) -> None:
        """Enregistre le nombre de mailles pour la largeur du dos au niveau de la poitrine."""
        self.chest_stitches = nb_of_stitches

    def getChestStitches(self) -> int:
        """Renvoie le nombre de mailles pour la largeur du dos au niveau de la poitrine."""
        return self.chest_stitches

    def setRowsToUnderarm(self, nb_of_rows: int) -> None:
        """Enregistre le nombre de rangs nécessaires pour atteindre l'aisselle à partir de l'encolure."""
        self.rows_to_underarm = nb_of_rows

    def getRowsToUnderarm(self) -> int:
        """Renvoie le nombre de rangs nécessaires pour atteindre l'aisselle."""
        return self.rows_to_underarm

    def setRowsToHem(self, nb_of_rows: int) -> None:
        """Enregistre le nombre de rangs nécessaires pour atteindre l'ourlet à partir de l'aisselle."""
        self.rows_to_hem = nb_of_rows

    def getRowsToHem(self) -> int:
        """Renvoie le nombre de rangs nécessaires pour atteindre l'ourlet."""
        return self.rows_to_hem

    def setAugmentationsRaglan(self, increases: int, rows: int) -> None:
        """
        Délègue à la classe parente le calcul du rythme des augmentations raglan pour le dos.

        Un message est imprimé pour indiquer que le calcul concerne le corps du pull.

        :param increases: Nombre d'augmentations raglan à répartir.
        :param rows: Nombre de rangs disponibles pour ces augmentations.
        """
        print("le corps")
        super().setAugmentationsRaglan(increases, rows)

    def __str__(self) -> str:
        """Renvoie une description textuelle des mesures du dos."""
        return (
            f"Le dos mesure {self.armhole_depth}CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle "
            f"jusqu'a l'ourlet. Le tour de poitrine est {self.chest_width}"
        )