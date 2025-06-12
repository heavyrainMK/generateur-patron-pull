from abc import ABC
import math

class Calculs(ABC):
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