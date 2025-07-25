from abc import ABC
import math


class Calculs(ABC):
    def __init__(self):
        self.rythme_rapide = 0
        self.rythme_lent = 0 
        self.augmentations_rapides = 0
        self.augmentations_lentes = 0
        self.numero_rangs_augmentation_rapide = []
        self.numero_rangs_augmentation_lent = []

    def setRythmeRapide(self, frequence):
        self.rythme_rapide = frequence

    def getRythmeRapide(self):
        return self.rythme_rapide

    def setRythmeLent(self, frequence):
        self.rythme_lent = frequence

    def getRythmeLent(self):
        return self.rythme_lent

    def setAugmentationsRapides(self, nombre):
        self.augmentations_rapides = nombre

    def getAugmentationsRapides(self):
        return self.augmentations_rapides

    def setAugmentationsLentes(self, nombre):
        self.augmentations_lentes = nombre

    def getAugmentationsLentes(self):
        return self.augmentations_lentes

    def setNumeroRangsAugmentationRapide(self, num):
        self.numero_rangs_augmentation_rapide.append(num)

    def getNumeroRangsAugmentationRapide(self):
        return self.numero_rangs_augmentation_rapide

    def setNumeroRangsAugmentationLent(self, num):
        self.numero_rangs_augmentation_lent.append(num)

    def getNumeroRangsAugmentationLent(self):
        return self.numero_rangs_augmentation_lent

    #don't forget to round up the numbers
    #c'est aussi plus facile de travailler avec des nombres pairs
    def calculStitchesNeeded(self, stitches, width, ease):
        if math.ceil(stitches / 10 * (width + ease)) % 2 == 0:
            return math.ceil(stitches / 10 * (width + ease))
        else:
            return math.ceil(stitches / 10 * (width + ease)) + 1

    def calculRowsNeeded(self, rows, length):
        return math.ceil(rows / 10 * length)

#les augmentation/diminutions fonctionnent par paires, il faut donc un nombre pair
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
                self.setNumeroRangsAugmentationRapide(rang_en_cours)
            self.setRythmeRapide(1) 
            self.setRythmeLent(2)
            self.setAugmentationsRapides(augmentations_effectuees)
            self.setAugmentationsLentes(augmentations_restantes)
            rang_en_cours = (self.getAugmentationsRapides() * self.getRythmeRapide()) + 1
            while (rang_en_cours <= (self.getAugmentationsRapides() * self.getRythmeRapide() + self.getAugmentationsLentes() * self.getRythmeLent())):
                self.setNumeroRangsAugmentationLent(rang_en_cours)
                rang_en_cours+= self.getRythmeLent()
            print(f"Rythme rapide : {self.getAugmentationsRapides()} augmentations tous les {self.getRythmeRapide()} rangs. Rythme lent : {self.getAugmentationsLentes()} augmentations tous les {self.getRythmeLent()} rangs\n")
            print(self.getNumeroRangsAugmentationRapide())
            print(self.getNumeroRangsAugmentationLent())

        elif ((increases*3) > rows):
            while ((augmentations_restantes * 3) >= rangs_restants):
                rang_en_cours+=1
                rangs_restants-=1
                augmentations_effectuees+=1
                augmentations_restantes-=1
                self.setNumeroRangsAugmentationRapide(rang_en_cours)
            self.setRythmeRapide(1) 
            self.setRythmeLent(3)
            self.setAugmentationsRapides(augmentations_effectuees)
            self.setAugmentationsLentes(augmentations_restantes)
            rang_en_cours = (self.getAugmentationsRapides() * self.getRythmeRapide()) + 1
            while (rang_en_cours <= (self.getAugmentationsRapides() * self.getRythmeRapide() + self.getAugmentationsLentes() * self.getRythmeLent())):
                self.setNumeroRangsAugmentationLent(rang_en_cours)
                rang_en_cours+= self.getRythmeLent()
            print(f"Rythme rapide : {self.getAugmentationsRapides()} augmentations tous les {self.getRythmeRapide()} rangs. Rythme lent : {self.getAugmentationsLentes()} augmentations tous les {self.getRythmeLent()} rangs\n")
            print(self.getNumeroRangsAugmentationRapide())
            print(self.getNumeroRangsAugmentationLent())


        else:
            while((augmentations_restantes * 4) >= rangs_restants):
                rang_en_cours+=2
                rangs_restants-=2
                augmentations_effectuees+=1
                augmentations_restantes-=1
                self.setNumeroRangsAugmentationRapide(rang_en_cours)
            self.setRythmeRapide(2) 
            self.setRythmeLent(4)
            self.setAugmentationsRapides(augmentations_effectuees)
            self.setAugmentationsLentes(augmentations_restantes)
            rang_en_cours = (self.getAugmentationsRapides() * self.getRythmeRapide()) + 1
            while (rang_en_cours <= (self.getAugmentationsRapides() * self.getRythmeRapide() + self.getAugmentationsLentes() * self.getRythmeLent())):
                self.setNumeroRangsAugmentationLent(rang_en_cours)
                rang_en_cours+= self.getRythmeLent()
            print(f"Rythme rapide : {self.getAugmentationsRapides()} augmentations tous les {self.getRythmeRapide()} rangs. Rythme lent : {self.getAugmentationsLentes()} augmentations tous les {self.getRythmeLent()} rangs\n")
            print(self.getNumeroRangsAugmentationRapide())
            print(self.getNumeroRangsAugmentationLent())

    # pour l'instant on utilisera cette fonction uniquement pour les manches
    # mais a l'avenir il est possible que j'en aie besoin pour le corps egalement
    # je la mets dans la classe "calculs" pour que toutes les autres classes y aient acces
    def calculRatio(self, rangs, occurences):
        return math.ceil(rangs / occurences)


            

