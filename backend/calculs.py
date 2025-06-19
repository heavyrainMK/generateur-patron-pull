from abc import ABC
import math


class Calculs(ABC):
    def __init__(self):
        self.augmentations_raglan = {
            'tous_les_4_rangs' : 0,
            'tout_les_3_rangs' : 0,
            'tous_les_2_rangs' : 0,
            'tous_les_rangs' : 0
        }

    #don't forget to round up the numbers
    def calculStitchesNeeded(self, stitches, width, ease):
        return math.ceil(stitches / 10 * (width + ease))

    def calculRowsNeeded(self, rows, length):
        return math.ceil(rows / 10 * length)

#les augmentation/diminutions fonctionnent par paires
    def calculIncreases(self, nb_mailles_1, nb_mailles_2):
        inc = nb_mailles_2 - nb_mailles_1
        if inc % 2 != 0:
            inc = inc + 1
        return inc

    def calculDecreases(self, nb_mailles_1, nb_mailles_2):
        dec = nb_mailles_1 - nb_mailles_2
        if dec % 2 != 0:
            dec = dec -1
        return dec


    def augmentationsRaglan(self, increases, rows):
        rang_en_cours = 0
        rangs_restants = rows
        augmentations_effectuees = 0
        augmentations_restantes = increases
        if (math.floor(rows/2) < increases):
            while (augmentations_restantes > (rangs_restants/2)):
                rang_en_cours = rang_en_cours + 1
                rangs_restants = rangs_restants - 1
                augmentations_effectuees = augmentations_effectuees + 1
                augmentations_restantes = augmentations_restantes - 1
            self.augmentations_raglan['tous_les_rangs'] = augmentations_effectuees
            self.augmentations_raglan['tous_les_2_rangs'] = augmentations_restantes

        elif (math.floor(rows/3) < increases):
            while (augmentations_restantes > (rangs_restants/3)):
                rang_en_cours = rang_en_cours + 1
                rangs_restants = rangs_restants - 1
                augmentations_effectuees = augmentations_effectuees + 1
                augmentations_restantes = augmentations_restantes - 1
            self.augmentations_raglan['tous_les_rangs'] = augmentations_effectuees
            self.augmentations_raglan['tous_les_3_rangs'] = augmentations_restantes

        else:
            while(augmentations_restantes > (rangs_restants/4)):
                rang_en_cours = rang_en_cours + 2
                rangs_restants = rangs_restants - 2
                augmentations_effectuees = augmentations_effectuees + 1
                augmentations_restantes = augmentations_restantes - 1
            self.augmentations_raglan['tous_les_2_rangs'] = augmentations_effectuees
            self.augmentations_raglan['tous_les_4_rangs'] = augmentations_restantes


