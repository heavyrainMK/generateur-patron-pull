# *******************************************************
# Nom ......... : calculs.py
# Rôle ........ : Classe abstraite fournissant des méthodes de calcul communes aux différentes parties du patron de tricot.
# Auteurs ..... : M, L, M
# Version ..... : V1.0.0 du 28/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : Contient la classe Calculs qui encapsule les paramètres et algorithmes pour déterminer les rythmes d'augmentation et de diminution,
#                 calculer le nombre de mailles ou de rangs en fonction d'une densité d'échantillon, et répartir les augmentations de manière équitable.
# Technologies  : Python
# Dépendances . : abc, math
# Usage ....... : Classe parente pour Back, Front, Sleeve et toute autre classe nécessitant des calculs génériques.
# *******************************************************

from abc import ABC
import math

class Calculs(ABC):
    """
    Classe abstraite centralisant les calculs nécessaires à la génération d'un patron.

    Cette classe gère notamment :
      * les rythmes d'augmentation (rapide/lent) et leur nombre,
      * le calcul du nombre de mailles nécessaires à partir d'une densité (mailles par 10 cm) et d'une largeur cible,
      * le calcul du nombre de rangs nécessaires à partir d'une densité (rangs par 10 cm) et d'une longueur cible,
      * la répartition des augmentations ou diminutions de manière homogène,
      * le stockage des rangs sur lesquels des augmentations auront lieu.

    Les classes concrètes (Back, Front, Sleeve) héritent de Calculs pour bénéficier de ces outils.
    """
    def __init__(self):
        self.rythme_rapide = 0
        self.rythme_lent = 0 
        self.augmentations_rapides = 0
        self.augmentations_lentes = 0
        self.numero_rangs_augmentation_rapide = []
        self.numero_rangs_augmentation_lent = []

    def setRythmeRapide(self, frequence):
        """
        Définit la fréquence des rangs sur lesquels les augmentations rapides seront effectuées.

        :param frequence: Intervalle (en nombre de rangs) entre deux augmentations rapides.
        """
        self.rythme_rapide = frequence

    def getRythmeRapide(self):
        """
        Renvoie la fréquence des augmentations rapides.
        :return: Nombre de rangs entre deux augmentations rapides.
        """
        return self.rythme_rapide

    def setRythmeLent(self, frequence):
        """
        Définit la fréquence des rangs sur lesquels les augmentations lentes seront effectuées.

        :param frequence: Intervalle (en nombre de rangs) entre deux augmentations lentes.
        """
        self.rythme_lent = frequence

    def getRythmeLent(self):
        """
        Renvoie la fréquence des augmentations lentes.
        :return: Nombre de rangs entre deux augmentations lentes.
        """
        return self.rythme_lent

    def setAugmentationsRapides(self, nombre):
        """
        Enregistre le nombre d'augmentations à effectuer en rythme rapide.

        :param nombre: Nombre d'augmentations rapides.
        """
        self.augmentations_rapides = nombre

    def getAugmentationsRapides(self):
        """
        Renvoie le nombre d'augmentations rapides.
        :return: Nombre d'augmentations rapides.
        """
        return self.augmentations_rapides

    def setAugmentationsLentes(self, nombre):
        """
        Enregistre le nombre d'augmentations à effectuer en rythme lent.

        :param nombre: Nombre d'augmentations lentes.
        """
        self.augmentations_lentes = nombre

    def getAugmentationsLentes(self):
        """
        Renvoie le nombre d'augmentations lentes.
        :return: Nombre d'augmentations lentes.
        """
        return self.augmentations_lentes

    def setNumeroRangsAugmentationRapide(self, num):
        """
        Ajoute un rang à la liste des rangs où des augmentations rapides doivent être réalisées.

        :param num: Numéro du rang.
        """
        self.numero_rangs_augmentation_rapide.append(num)

    def getNumeroRangsAugmentationRapide(self):
        """
        Renvoie la liste des numéros de rangs avec augmentations rapides.
        :return: Liste de rangs.
        """
        return self.numero_rangs_augmentation_rapide

    def setNumeroRangsAugmentationLent(self, num):
        """
        Ajoute un rang à la liste des rangs où des augmentations lentes doivent être réalisées.

        :param num: Numéro du rang.
        """
        self.numero_rangs_augmentation_lent.append(num)

    def getNumeroRangsAugmentationLent(self):
        """
        Renvoie la liste des numéros de rangs avec augmentations lentes.
        :return: Liste de rangs.
        """
        return self.numero_rangs_augmentation_lent

    def calculStitchesNeeded(self, stitches, width, ease):
        """
        Calcule le nombre de mailles nécessaires en fonction d'une densité et d'une largeur.

        On arrondit toujours à l'entier supérieur et, si nécessaire, au nombre pair supérieur afin de
        faciliter le partage symétrique des mailles lors du montage.

        :param stitches: Nombre de mailles pour 10 cm (densité horizontale).
        :param width: Largeur cible en centimètres.
        :param ease: Aisance en centimètres à ajouter à la largeur.
        :return: Nombre de mailles arrondi à l'entier pair supérieur.
        """
        maille_calculee = math.ceil(stitches / 10 * (width + ease))
        if maille_calculee % 2 == 0:
            return maille_calculee
        else:
            return maille_calculee + 1

    def calculRowsNeeded(self, rows, length):
        """
        Calcule le nombre de rangs nécessaires en fonction d'une densité et d'une longueur.

        :param rows: Nombre de rangs pour 10 cm (densité verticale).
        :param length: Longueur cible en centimètres.
        :return: Nombre de rangs arrondi à l'entier supérieur.
        """
        return math.ceil(rows / 10 * length)

    def calculIncreases(self, nb_mailles_1, nb_mailles_2):
        """
        Calcule le nombre d'augmentations nécessaires pour passer d'un nombre initial de mailles à un nombre final.

        Les augmentations se font par paires, il convient donc de retourner un nombre pair.

        :param nb_mailles_1: Nombre initial de mailles.
        :param nb_mailles_2: Nombre final de mailles désiré.
        :return: Nombre pair d'augmentations nécessaires.
        """
        inc = nb_mailles_2 - nb_mailles_1
        if inc % 2 != 0:
            inc += 1
        return inc

    def calculDecreases(self, nb_mailles_1, nb_mailles_2):
        """
        Calcule le nombre de diminutions nécessaires pour passer d'un nombre initial de mailles à un nombre final.

        Les diminutions se font par paires, il convient donc de retourner un nombre pair.

        :param nb_mailles_1: Nombre initial de mailles.
        :param nb_mailles_2: Nombre final de mailles désiré.
        :return: Nombre pair de diminutions nécessaires.
        """
        dec = nb_mailles_1 - nb_mailles_2
        if dec % 2 != 0:
            dec -= 1
        return dec


    def setAugmentationsRaglan(self, increases, rows):
        """
        Détermine le rythme des augmentations de type raglan en fonction du nombre total d'augmentations
        à réaliser et du nombre de rangs disponibles.

        La méthode remplit les listes `numero_rangs_augmentation_rapide` et `numero_rangs_augmentation_lent` et
        fixe les fréquences rapides et lentes ainsi que le nombre d'augmentations associées. Trois cas sont distingués
        en fonction du rapport entre le nombre d'augmentations et la longueur de la section :
          - si les augmentations sont très rapprochées (increases * 2 > rows),
          - si elles sont moyennement rapprochées (increases * 3 > rows),
          - sinon, elles sont plus espacées.

        :param increases: Nombre total d'augmentations à répartir.
        :param rows: Nombre de rangs disponibles pour réaliser ces augmentations.
        """
        rang_en_cours = 0
        rangs_restants = rows
        augmentations_effectuees = 0
        augmentations_restantes = increases
        # Cas où les augmentations doivent être très fréquentes : toutes les 1 ou 2 rangs.
        if (increases * 2) > rows:
            while (augmentations_restantes * 2) >= rangs_restants:
                rang_en_cours += 1
                rangs_restants -= 1
                augmentations_effectuees += 1
                augmentations_restantes -= 1
                self.setNumeroRangsAugmentationRapide(rang_en_cours)
            self.setRythmeRapide(1)
            self.setRythmeLent(2)
            self.setAugmentationsRapides(augmentations_effectuees)
            self.setAugmentationsLentes(augmentations_restantes)
            rang_en_cours = (self.getAugmentationsRapides() * self.getRythmeRapide()) + 1
            while (
                rang_en_cours
                <= (
                    self.getAugmentationsRapides() * self.getRythmeRapide()
                    + self.getAugmentationsLentes() * self.getRythmeLent()
                )
            ):
                self.setNumeroRangsAugmentationLent(rang_en_cours)
                rang_en_cours += self.getRythmeLent()
            print(
                f"Rythme rapide : {self.getAugmentationsRapides()} augmentations tous les {self.getRythmeRapide()} rangs. "
                f"Rythme lent : {self.getAugmentationsLentes()} augmentations tous les {self.getRythmeLent()} rangs\n"
            )
            print(self.getNumeroRangsAugmentationRapide())
            print(self.getNumeroRangsAugmentationLent())

        # Cas où les augmentations sont légèrement moins fréquentes : toutes les 1 ou 3 rangs.
        elif (increases * 3) > rows:
            while (augmentations_restantes * 3) >= rangs_restants:
                rang_en_cours += 1
                rangs_restants -= 1
                augmentations_effectuees += 1
                augmentations_restantes -= 1
                self.setNumeroRangsAugmentationRapide(rang_en_cours)
            self.setRythmeRapide(1)
            self.setRythmeLent(3)
            self.setAugmentationsRapides(augmentations_effectuees)
            self.setAugmentationsLentes(augmentations_restantes)
            rang_en_cours = (self.getAugmentationsRapides() * self.getRythmeRapide()) + 1
            while (
                rang_en_cours
                <= (
                    self.getAugmentationsRapides() * self.getRythmeRapide()
                    + self.getAugmentationsLentes() * self.getRythmeLent()
                )
            ):
                self.setNumeroRangsAugmentationLent(rang_en_cours)
                rang_en_cours += self.getRythmeLent()
            print(
                f"Rythme rapide : {self.getAugmentationsRapides()} augmentations tous les {self.getRythmeRapide()} rangs. "
                f"Rythme lent : {self.getAugmentationsLentes()} augmentations tous les {self.getRythmeLent()} rangs\n"
            )
            print(self.getNumeroRangsAugmentationRapide())
            print(self.getNumeroRangsAugmentationLent())

        # Cas par défaut : augmentations plus espacées (par exemple toutes les 2 ou 4 rangs).
        else:
            while (augmentations_restantes * 4) >= rangs_restants:
                rang_en_cours += 2
                rangs_restants -= 2
                augmentations_effectuees += 1
                augmentations_restantes -= 1
                self.setNumeroRangsAugmentationRapide(rang_en_cours)
            self.setRythmeRapide(2)
            self.setRythmeLent(4)
            self.setAugmentationsRapides(augmentations_effectuees)
            self.setAugmentationsLentes(augmentations_restantes)
            rang_en_cours = (self.getAugmentationsRapides() * self.getRythmeRapide()) + 1
            while (
                rang_en_cours
                <= (
                    self.getAugmentationsRapides() * self.getRythmeRapide()
                    + self.getAugmentationsLentes() * self.getRythmeLent()
                )
            ):
                self.setNumeroRangsAugmentationLent(rang_en_cours)
                rang_en_cours += self.getRythmeLent()
            print(
                f"Rythme rapide : {self.getAugmentationsRapides()} augmentations tous les {self.getRythmeRapide()} rangs. "
                f"Rythme lent : {self.getAugmentationsLentes()} augmentations tous les {self.getRythmeLent()} rangs\n"
            )
            print(self.getNumeroRangsAugmentationRapide())
            print(self.getNumeroRangsAugmentationLent())

    # pour l'instant on utilisera cette fonction uniquement pour les manches
    # mais à l'avenir il est possible que j'en aie besoin pour le corps également
    # je la mets dans la classe "Calculs" pour que toutes les autres classes y aient accès
    def calculRatio(self, rangs, occurences):
        """
        Calcule le rapport entre un nombre total de rangs et un nombre d'occurrences (augmentations ou diminutions).

        Ce ratio indique la fréquence à laquelle une opération doit être répétée pour répartir uniformément un
        nombre donné d'opérations sur un nombre de rangs.

        :param rangs: Nombre total de rangs disponibles.
        :param occurences: Nombre d'opérations à répartir.
        :return: Entier représentant l'intervalle entre deux opérations.
        """
        return math.ceil(rangs / occurences)