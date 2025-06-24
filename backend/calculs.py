from abc import ABC
import math


class Calculs(ABC):
    def __init__(self):
        rythme_rapide = 0
        rythme_lent = 0 
        augmentations_rapides = 0
        augmentations_lentes = 0

    def setRythmeRapide(self, frequence):
        self.rythme_rapide = frequence

    def getRythmeRapide(self):
        return self.rythme_rapide

    def setRythmeLent(self, frequence):
        self.rythme_lent = frequence

    def getRythmeLent(self):
        return self.rythme_lent

    def setAugemntationsRapides(self, nombre):
        self.augmentations_rapides = nombre

    def getAugmentationsRapides(self):
        return self.augmentations_rapides

    def setAugemntationsLentes(self, nombre):
        self.augmentations_lentes = nombre

    def getAugmentationsLentes(self):
        return self.augmentations_lentes

    #don't forget to round up the numbers
    #c'est aussi plus facile de travailler avec des nombres pairs
    def calculStitchesNeeded(self, stitches, width, ease):
        if math.ceil(stitches / 10 * (width + ease)) % 2 == 0:
            return math.ceil(stitches / 10 * (width + ease))
        else:
            return math.ceil(stitches / 10 * (width + ease)) + 1

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


    def setAugmentationsRaglan(self, increases, rows):
        rang_en_cours = 0
        rangs_restants = rows
        augmentations_effectuees = 0
        augmentations_restantes = increases
        if ((increases*2) > rows):
            while ((augmentations_restantes * 2) >= rangs_restants):
                rang_en_cours+=1
                rangs_restants-=1
                augmentations_effectuees+=1
                augmentations_restantes-=1
            self.setRythmeRapide(1) 
            self.setRythmeLent(2)
            self.setAugemntationsRapides(augmentations_effectuees)
            self.setAugemntationsLentes(augmentations_restantes)

        elif ((increases*3) > rows):
            while ((augmentations_restantes * 3) >= rangs_restants):
                rang_en_cours+=1
                rangs_restants-=1
                augmentations_effectuees+=1
                augmentations_restantes-=1
            self.setRythmeRapide(1) 
            self.setRythmeLent(3)
            self.setAugemntationsRapides(augmentations_effectuees)
            self.setAugemntationsLentes(augmentations_restantes)

        else:
            while((augmentations_restantes * 4) >= rangs_restants):
                rang_en_cours+=2
                rangs_restants-=2
                augmentations_effectuees+=2
                augmentations_restantes-=2
            self.setRythmeRapide(2) 
            self.setRythmeLent(4)
            self.setAugemntationsRapides(augmentations_effectuees)
            self.setAugemntationsLentes(augmentations_restantes)

