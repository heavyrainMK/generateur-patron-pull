from abc import ABC
import math


class Calculs(ABC):
    def __init__(self):
        self.augmentations_raglan = {
            'tous_les_4_rangs' : 0,
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
        if ((rows / 2) > increases):
            self.augmentations_raglan['tous_les_4_rangs'] = math.ceil(rows / 4)
            self.augmentations_raglan['tous_les_2_rangs'] = increases - self.augmentations_raglan['tous_les_4_rangs']

        else:
            self.augmentations_raglan['tous_les_2_rangs'] = math.ceil(rows / 2)
            self.augmentations_raglan['tous_les_rangs'] = increases - self.augmentations_raglan['tous_les_2_rangs']

