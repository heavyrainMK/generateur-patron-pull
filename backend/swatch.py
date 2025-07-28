# *******************************************************
# Nom ......... : swatch.py
# Rôle ........ : Classe utilitaire représentant un échantillon de tricot (swatch).
# Auteurs ..... : M, L, M
# Version ..... : V1.0.0 du 28/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : Ce module définit la classe Swatch, qui stocke les densités en mailles et en rangs pour un carré de 10 cm.
#                 Ces valeurs sont utilisées pour convertir des mesures physiques en nombre de mailles et de rangs.
# Technologies  : Python
# Dépendances . : Aucune
# Usage ....... : Instanciée dans app.py pour fournir les densités de mailles et de rangs aux calculs.
# *******************************************************

class Swatch:
    """
    Représente un échantillon de tricot et stocke la densité de mailles et de rangs pour 10 cm.

    Un échantillon (ou swatch) est un carré de tricot mesurant typiquement 10 cm de côté.
    Il permet de déterminer combien de mailles et de rangs sont nécessaires pour atteindre une
    dimension donnée lorsque l'on calcule un patron.
    """

    def __init__(self, stitches: float, rows: float) -> None:
        """
        Initialise un échantillon avec un nombre de mailles et de rangs mesurés sur 10 cm.

        :param stitches: Nombre de mailles pour 10 cm.
        :param rows: Nombre de rangs pour 10 cm.
        """
        self.stitches = stitches
        self.rows = rows

    def getStitches(self) -> float:
        """Renvoie le nombre de mailles pour 10 cm."""
        return self.stitches

    def getRows(self) -> float:
        """Renvoie le nombre de rangs pour 10 cm."""
        return self.rows

    def __str__(self) -> str:
        """Renvoie une description textuelle de l'échantillon."""
        return (
            f"the swatch is {self.stitches} stitches and {self.rows} rows for a 10cm square"
        )