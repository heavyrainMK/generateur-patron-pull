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

#les augmentation/diminutions fonctionnent par paires
def calculIncreases(nb_mailles_1, nb_mailles_2):
    inc = nb_mailles_2 - nb_mailles_1
    if inc % 2 != 0:
        inc = inc + 1
    return inc

def calculDecreases(nb_mailles_1, nb_mailles_2):
    dec = nb_mailles_1 - nb_mailles_2
    if dec % 2 != 0:
        dec = dec -1
    return dec

def main():
    #il faut construire les objets avec les mesures fournis par l'utilisateur
    my_front = Front(tour_de_poitrine, longueur_aisselle, longueur_bas)
    my_back = Back(largeur_encolure, tour_de_poitrine, longueur_aisselle, longueur_bas)
    my_right_sleeve = Sleeve(tour_de_bras, tour_de_poignet, longueur_aisselle, longueur_poignet)
    my_left_sleeve = Sleeve(tour_de_bras, tour_de_poignet, longueur_aisselle, longueur_poignet)

    my_swatch = Swatch(mailles, rangs)

    #je ne mets pas les mailles d'aisselle dans une classe car elles sont communes a la manches et au corps, reparties sur le devant et le dos
    nb_de_mailles_aisselle = 0
    nb_augmentations_dos = 0
    nb_augmentations_manches = 0

    #calcul des mailles au montage
    my_back.setNeckStitches(calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth()))
    my_right_sleeve.setTopSleeveStitches(calculStitchesNeeded(my_swatch.getStitches(), my_right_sleeve.getTopSleeveWidth()))
    my_left_sleeve.setTopSleeveStitches(calculStitchesNeeded(my_swatch.getStitches(), my_left_sleeve.getTopSleeveWidth()))

    #on ajoute 4 mailles pour former les raglan
    total_mailles_debut = my_front.getRightFrontStitches() + my_right_sleeve.getTopSleeveStitches() + my_back.getNeckStitches() + my_left_sleeve.getTopSleeveStitches() + my_front.getLeftFrontStitches() + 4  

    #calcul des mailles avant separation des manche et du corps
    #bien penser a prendre en compte l'aisance souhaitee
    #on divise la circonference totale par 2 puisqu'elle est repartie sur les mailles du devant et du dos
    my_front.setChestStitches(calculStitchesNeeded(my_swatch.getStitches(), (my_front.getChestWidth() / 2) + aisance))
    my_back.setChestStitches(calculStitchesNeeded(my_swatch.getStitches(), (my_back.getChestWidth() / 2) + aisance))
    my_right_sleeve.setUpperarmStitches(calculStitchesNeeded(my_swatch.getStitches(), my_right_sleeve.getUpperArmCircumference() + aisance))
    my_left_sleeve.setUpperarmStitches(calculStitchesNeeded(my_swatch.getStitches(), my_left_sleeve.getUpperArmCircumference() + aisance))

    #calcul des augmentations necessaires
    #au moment de la separation des bras et du corps, on monte des mailles supplementaires sour l'aisselle pour ne pas que cela soit trop serre
    #il faut donc bien penser a les soustraire au nombre d'augmentation pour ne pas se retrouver avec des manches/un corps trop large
    #je compte une largeur d'aisselle de 4m, 3cm, changerai peut etre plus tard
    nb_de_mailles_aisselle = calculStitchesNeeded(my_swatch.getStitches(), 3)

    #on fait le meme nombre d'augmentations devant et derriere, donc on ne fait qu'une fois le calcul
    #les augmentation/diminutions vont toujours par paire, une au debut une a la fin
    #on divise donc par 2 pour savoir le nombre de rangs qui contiendront des augmentations
    nb_augmentations_dos = (calculIncreases(my_back.getChestStitches(), my_back.getNeckStitches()) - nb_de_mailles_aisselle) / 2
    #les deux manches sont pareilles, on ne fait qu'une fois le calcul
    nb_augmentations_manches = (calculIncreases(my_left_sleeve.getTopSleeveStitches(), my_left_sleeve.getUpperarmStitches()) - nb_de_mailles_aisselle) / 2

    #calcul du nombre de rangs pour arriver jusqu'a l'emmenchure




    




    if __name__ == "__main__":
        main()

    
