from sleeve import Sleeve
from front import Front
from back import Back
from swatch import Swatch
import math

#don't forget to round up the numbers
def calculStitchesNeeded(stitches, width, ease):
    return math.ceil(stitches / 10 * (width + ease))

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
    my_front = Front(80, 25, 30)
    my_back = Back(21, 80, 25, 30)
    my_right_sleeve = Sleeve(28, 18.5, 25, 45)
    my_left_sleeve = Sleeve(28, 18.5, 25, 45)

    my_swatch = Swatch(25, 39)
    aisance_corps = 5
    aisance_manches = 2

    #je ne mets pas les mailles d'aisselle dans une classe car elles sont communes a la manches et au corps, reparties sur le devant et le dos
    nb_de_mailles_aisselle = 0
    nb_augmentations_dos = 0
    nb_augmentations_manches = 0

    #calcul des mailles au montage
    my_back.setNeckStitches(calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth(), 0))
    my_right_sleeve.setTopSleeveStitches(calculStitchesNeeded(my_swatch.getStitches(), my_right_sleeve.getTopSleeveWidth(), 0))
    my_left_sleeve.setTopSleeveStitches(calculStitchesNeeded(my_swatch.getStitches(), my_left_sleeve.getTopSleeveWidth(), 0))

    #NE PAS OUBLIER D'ENLEVER AVANT DE RENDRE !!!!!!!
    test = 'devant droit ' + str(my_front.getRightFrontStitches()) + ' mailles, manche droite ' + str(my_right_sleeve.getTopSleeveStitches()) + ' mailles, dos ' + str(my_back.getNeckStitches()) + ' mailles, manche gauche ' + str(my_left_sleeve.getTopSleeveStitches()) + ' mailles, devant gauche ' + str(my_front.getLeftFrontStitches()) + ' mailles'
    print(test)

    #on ajoute 4 mailles pour former les raglan
    total_mailles_debut = my_front.getRightFrontStitches() + my_right_sleeve.getTopSleeveStitches() + my_back.getNeckStitches() + my_left_sleeve.getTopSleeveStitches() + my_front.getLeftFrontStitches() + 4  
    print('total des mailles pour le devant, le dos et les manches, plus 4 pour les raglans : ' + str(total_mailles_debut))

    #calcul des mailles avant separation des manche et du corps
    #bien penser a prendre en compte l'aisance souhaitee
    #on divise la circonference totale par 2 puisqu'elle est repartie sur les mailles du devant et du dos
    my_front.setChestStitches(calculStitchesNeeded(my_swatch.getStitches(), (my_front.getChestWidth() / 2), aisance_corps))
    my_back.setChestStitches(calculStitchesNeeded(my_swatch.getStitches(), (my_back.getChestWidth() / 2), aisance_corps))
    my_right_sleeve.setUpperarmStitches(calculStitchesNeeded(my_swatch.getStitches(), my_right_sleeve.getUpperArmCircumference(), aisance_manches))
    my_left_sleeve.setUpperarmStitches(calculStitchesNeeded(my_swatch.getStitches(), my_left_sleeve.getUpperArmCircumference(), aisance_manches))

    #calcul des augmentations necessaires
    #au moment de la separation des bras et du corps, on monte des mailles supplementaires sour l'aisselle pour ne pas que cela soit trop serre
    #il faut donc bien penser a les soustraire au nombre d'augmentation pour ne pas se retrouver avec des manches/un corps trop large
    #je compte une largeur d'aisselle de 3cm, changerai peut etre plus tard
    nb_de_mailles_aisselle = calculStitchesNeeded(my_swatch.getStitches(), 3, 0)
    print('mailles aisselle : ' + str(nb_de_mailles_aisselle))

    print('apres separation : \ndevant : ' + str(my_front.getChestStitches()) + '\nmanche droite : ' + str(my_right_sleeve.getUpperarmStitches()) + '\ndos : ' + str(my_back.getChestStitches()) + '\nmanche gauche : ' + str(my_left_sleeve.getUpperarmStitches()) + '\nraglan : 4')

    #on fait le meme nombre d'augmentations devant et derriere, donc on ne fait qu'une fois le calcul
    #les augmentation/diminutions vont toujours par paire, une au debut une a la fin
    #on divise donc par 2 pour savoir le nombre de rangs qui contiendront des augmentations
    #il ne faut pas oublier de soustraire les mailles de l'aisselle pour le devant, le dos et les manches, ainsi que les mailles raglan (pour le devant et le dos seulement)
    nb_augmentations_dos = math.ceil((calculIncreases(my_back.getNeckStitches(), my_back.getChestStitches()) - nb_de_mailles_aisselle - 4) / 2)
    #les deux manches sont pareilles, on ne fait qu'une fois le calcul
    nb_augmentations_manches = math.ceil((calculIncreases(my_left_sleeve.getTopSleeveStitches(), my_left_sleeve.getUpperarmStitches()) - nb_de_mailles_aisselle)  / 2)

    print('augmentations pour le corps : ' + str(nb_augmentations_dos))
    print('augmentations pour les manches : ' + str(nb_augmentations_manches))

    #calcul du nombre de rangs pour arriver jusqu'a l'emmanchure
    #la profondeur d'emmanchure est la meeme pour le devant, le dos et les manches, on fait le calcul une seule fois
    my_back.setRowsToUnderarm(calculRowsNeeded(my_swatch.getRows(), my_back.getArmholeDepth()))
    print(str(my_back.getRowsToUnderarm()) + ' rangs avant aisselle')

    #il existe plusieurs schemas d'augmentation en fonction des morphologie
    #on peut combiner des augmentations tous les rangs avec des augmentations tous les 2 rangs
    #ou bien des augmentations tous les 2 puis tous les 4 rangs
    #on peut egalement combiner des augmentations sur le corps et les manches en meme temps, ou bien seulement les manche, ou seulement le corps

    # corps_augmentation_tous_les_rangs
    # corps_augmentation_tous_les_2_rangs
    # corps_augmentation_tous_les_4_rangs
    # manche_augmentation_tous_les_rangs
    # manche_augmentation_tous_les_2_rangs
    # manche_augmentation_tous_les_4_rangs
    if ((my_back.getRowsToUnderarm() / 2) > nb_augmentations_dos or (my_back.getRowsToUnderarm() / 2) > nb_augmentations_manches):
    
        corps_augmentation_tous_les_4_rangs = math.floor(my_back.getRowsToUnderarm() / 4)
        corps_augmentation_tous_les_2_rangs = nb_augmentations_dos - corps_augmentation_tous_les_4_rangs
        corps_augmentation_tous_les_rangs = 0
        manche_augmentation_tous_les_4_rangs = math.floor(my_back.getRowsToUnderarm() / 4)
        manche_augmentation_tous_les_2_rangs = nb_augmentations_manches - manche_augmentation_tous_les_4_rangs
        manche_augmentation_tous_les_rangs = 0

    else:
        corps_augmentation_tous_les_4_rangs = 0
        corps_augmentation_tous_les_2_rangs = math.floor(my_back.getRowsToUnderarm() / 2)
        corps_augmentation_tous_les_rangs = nb_augmentations_dos - corps_augmentation_tous_les_2_rangs
        manche_augmentation_tous_les_4_rangs = 0
        manche_augmentation_tous_les_2_rangs = math.floor(my_back.getRowsToUnderarm() / 2)
        manche_augmentation_tous_les_rangs = nb_augmentations_manches - manche_augmentation_tous_les_2_rangs
    
        

    
    print('corps : ' + str(corps_augmentation_tous_les_4_rangs) + ' augmentations tous les 4 rangs, ' + str(corps_augmentation_tous_les_2_rangs) + ' augmentations tous les 2 rangs et ' + str(corps_augmentation_tous_les_rangs) + ' augmentations tous les rangs\n')


    print('manches : ' + str(manche_augmentation_tous_les_4_rangs) + ' augmentations tous les 4 rangs, ' + str(manche_augmentation_tous_les_2_rangs) + ' augmentations tous les 2 rangs et ' + str(manche_augmentation_tous_les_rangs) + ' augmentations tous les rangs\n')



if __name__ == "__main__":
    main()

    
