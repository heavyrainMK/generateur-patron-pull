# *******************************************************
# Nom ......... : sleeve.py
# Rôle ........ : Définition de la classe Sleeve représentant une manche du pull et encapsulant ses mesures et calculs spécifiques.
# Auteurs ..... : M, L, M
# Version ..... : V1.0.0 du 28/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : Classe concrète héritant de Calculs. Elle stocke les mesures de la manche (circonférence du haut du bras,
#                 circonférence du poignet, longueur de l'aisselle jusqu'à l'ourlet) et fournit des accesseurs et mutateurs
#                 pour les nombres de mailles et de rangs calculés. La classe gère également le rythme d'augmentation raglan
#                 spécifique à la manche.
# Technologies  : Python
# Dépendances . : calculs (classe Calculs)
# Usage ....... : Instanciée dans app.py pour représenter les manches du pull et en calculer les paramètres.
# *******************************************************

from calculs import Calculs

class Sleeve(Calculs):
    """
    Représente une manche d'un pull top-down et encapsule ses mesures et ses calculs.

    Une manche est définie par :
      * la circonférence du haut du bras (upperarm_circumference) ;
      * la circonférence du poignet (wrist_circumference) ;
      * la longueur entre l'aisselle et l'ourlet (underarm_to_hem_length).

    La classe fournit des accesseurs pour ces mesures et des mutateurs pour stocker les résultats des calculs
    (nombre de mailles et nombre de rangs). Elle hérite des méthodes génériques de Calculs pour déterminer
    le rythme des augmentations et calcule également la largeur du haut de manche (top_sleeve_width), par défaut
    fixée à 3 cm d'après un échantillon personnel.
    """

    def __init__(self, upperarm_circumference, wrist_circumference, underarm_to_hem_length) -> None:
        """
        Initialise une instance de Sleeve avec les mesures fournies.

        :param upperarm_circumference: Circonférence du bras au niveau du biceps en centimètres.
        :param wrist_circumference: Circonférence du poignet en centimètres.
        :param underarm_to_hem_length: Longueur de la manche depuis l'aisselle jusqu'à l'ourlet en centimètres.
        """
        super().__init__()
        self.upperarm_circumference = upperarm_circumference
        self.wrist_circumference = wrist_circumference
        self.underarm_to_hem_length = underarm_to_hem_length
        # Largeur du haut de manche en centimètres. Une valeur par défaut de 3 cm est utilisée.
        self.top_sleeve_width = 3
        self.top_sleeve_stitches = 0
        self.upperarm_stitches = 0
        self.wrist_stitches = 0
        self.rows_to_wrist = 0

    def getTopSleeveWidth(self) -> float:
        """Renvoie la largeur du haut de manche (en centimètres)."""
        return self.top_sleeve_width

    def getUpperArmCircumference(self) -> float:
        """Renvoie la circonférence du bras au niveau du biceps (en centimètres)."""
        return self.upperarm_circumference

    def getWristCircumference(self) -> float:
        """Renvoie la circonférence du poignet (en centimètres)."""
        return self.wrist_circumference

    def getUnderArmToHemLength(self) -> float:
        """Renvoie la longueur de manche entre l'aisselle et l'ourlet (en centimètres)."""
        return self.underarm_to_hem_length

    def setTopSleeveStitches(self, nb_of_stitches: int) -> None:
        """Enregistre le nombre de mailles du haut de manche obtenu après calcul."""
        self.top_sleeve_stitches = nb_of_stitches

    def getTopSleeveStitches(self) -> int:
        """Renvoie le nombre de mailles du haut de manche."""
        return self.top_sleeve_stitches

    def setUpperarmStitches(self, nb_of_stitches: int) -> None:
        """Enregistre le nombre de mailles au niveau du haut du bras (après augmentations)."""
        self.upperarm_stitches = nb_of_stitches

    def getUpperarmStitches(self) -> int:
        """Renvoie le nombre de mailles au niveau du haut du bras."""
        return self.upperarm_stitches

    def setWristStitches(self, nb_of_stitches: int) -> None:
        """Enregistre le nombre de mailles au niveau du poignet."""
        self.wrist_stitches = nb_of_stitches

    def getWristStitches(self) -> int:
        """Renvoie le nombre de mailles au niveau du poignet."""
        return self.wrist_stitches

    def setRowsToWrist(self, nb_of_rows: int) -> None:
        """Enregistre le nombre de rangs nécessaires pour atteindre le poignet à partir de l'aisselle."""
        self.rows_to_wrist = nb_of_rows

    def getRowsToWrist(self) -> int:
        """Renvoie le nombre de rangs nécessaires pour atteindre le poignet."""
        return self.rows_to_wrist

    def setAugmentationsRaglan(self, increases: int, rows: int) -> None:
        """
        Appelle la méthode de la classe parente pour déterminer le rythme des augmentations raglan pour la manche.

        Un message est imprimé pour indiquer que le calcul concerne la manche.

        :param increases: Nombre d'augmentations raglan à répartir.
        :param rows: Nombre de rangs disponibles pour ces augmentations.
        """
        print("la manche")
        super().setAugmentationsRaglan(increases, rows)

    def __str__(self) -> str:
        """Renvoie une description textuelle des mesures de la manche."""
        return (
            f"La manche mesure CM depuis l'encolure jusqu'a l'aisselle et {self.underarm_to_hem_length}CM de l'aisselle "
            f"jusqu'a l'ourlet. Le bras a une circonference de {self.upperarm_circumference}CM au biceps et "
            f"{self.wrist_circumference}CM au poignet."
        )