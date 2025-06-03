from sleeve import Sleeve
from front import Front
from back import Back
from swatch import Swatch
import math

#don't forget to round up the numbers
def calculStitchesNeeded(stitches, width):
        return math.ceil(stitches / 10 * width)

def calculRowsNeeded(rows, length):
        return math.ceil(rows / 10 * length)

def calculIncreases(width_1, width_2):
        return width_2 - width_1

def calculDecreases(width_1, width_2):
        return width_1 - width_2


def main():
    #il faut construire les objets avec les mesures fournis par l'utilisateur
    my_front = Front(tour_de_poitrine, longueur_aisselle, longueur_bas)
    my_back = Back(largeur_encolure, tour_de_poitrine, longueur_aisselle, longueur_bas)
    my_right_sleeve = Sleeve(tour_de_bras, tour_de_poignet, longueur_aisselle, longueur_poignet)
    my_left_sleeve = Sleeve(tour_de_bras, tour_de_poignet, longueur_aisselle, longueur_poignet)

    my_swatch = Swatch(mailles, rangs)

    #calcul des mailles au montage
    my_back.setNeckStitches(calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth()))
    my_right_sleeve.setTopSleeveStitches(calculStitchesNeeded(my_swatch.getStitches(), my_right_sleeve.getTopSleeveWidth()))
    my_left_sleeve.setTopSleeveStitches(calculStitchesNeeded(my_swatch.getStitches(), my_left_sleeve.getTopSleeveWidth()))



    if __name__ == "__main__":
        main()

    
