from sleeve import Sleeve
from front import Front
from back import Back
from swatch import Swatch
from calculs import Calculs
from instructions import montage, rangsAplat
import math
import io

def main():

    fichier_a_telecharger = open("instructions_pull_sur_mesure.txt", "a")
    #il faut construire les objets avec les mesures fournis par l'utilisateur
    my_front = Front(92, 30)
    my_back = Back(21, 92, 25, 30)
    my_sleeve = Sleeve(28, 18.5, 45)

    my_swatch = Swatch(28, 32)
    aisance_corps = 5
    aisance_manches = 2

    #je ne mets pas les mailles d'aisselle dans une classe car elles sont communes a la manches et au corps, reparties sur le devant et le dos
    nb_de_mailles_aisselle = 0
    nb_augmentations_dos = 0
    nb_augmentations_manches = 0

    #calcul des mailles au montage
    my_back.setNeckStitches(my_back.calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth(), 0))
    my_sleeve.setTopSleeveStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getTopSleeveWidth(), 0))

    
    debut = montage(my_front.getRightFrontStitches(), my_sleeve.getTopSleeveStitches(), my_back.getNeckStitches(), my_front.getLeftFrontStitches())
    print(debut)
    fichier_a_telecharger.write(debut)
    
    #calcul des mailles avant separation des manche et du corps
    #bien penser a prendre en compte l'aisance souhaitee
    #on divise la circonference totale par 2 puisqu'elle est repartie sur les mailles du devant et du dos
    my_front.setChestStitches(my_front.calculStitchesNeeded(my_swatch.getStitches(), (my_front.getChestWidth() / 2), aisance_corps))
    my_back.setChestStitches(my_back.calculStitchesNeeded(my_swatch.getStitches(), (my_back.getChestWidth() / 2), aisance_corps))
    my_sleeve.setUpperarmStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getUpperArmCircumference(), aisance_manches))
    

    #calcul des augmentations necessaires
    #au moment de la separation des bras et du corps, on monte des mailles supplementaires sour l'aisselle pour ne pas que cela soit trop serre
    #il faut donc bien penser a les soustraire au nombre d'augmentation pour ne pas se retrouver avec des manches/un corps trop large
    #je compte une largeur d'aisselle de 3cm, changerai peut etre plus tard
    #je fais le calcul seulement une fois puisque c'est pareil a droite et a gauche
    nb_de_mailles_aisselle = my_back.calculStitchesNeeded(my_swatch.getStitches(), 3, 0)

    #on fait le meme nombre d'augmentations devant et derriere, donc on ne fait qu'une fois le calcul
    #les augmentation/diminutions vont toujours par paire, une au debut une a la fin
    #on divise donc par 2 pour savoir le nombre de rangs qui contiendront des augmentations
    #il ne faut pas oublier de soustraire les mailles de l'aisselle pour le devant, le dos et les manches, ainsi que les mailles raglan (pour le devant et le dos seulement)
    nb_augmentations_dos = math.ceil((my_back.calculIncreases(my_back.getNeckStitches(), my_back.getChestStitches()) - nb_de_mailles_aisselle - 2) / 2)
    #actualiser le nombre de mailles dos et devant apres avoir calculer les augmentations
    my_back.setChestStitches(my_back.getNeckStitches() + nb_augmentations_dos * 2 + 2 + nb_de_mailles_aisselle)
    my_front.setChestStitches(my_back.getChestStitches())
    #les deux manches sont pareilles, on ne fait qu'une fois le calcul
    nb_augmentations_manches = math.ceil((my_sleeve.calculIncreases(my_sleeve.getTopSleeveStitches(), my_sleeve.getUpperarmStitches()) - nb_de_mailles_aisselle)  / 2)
    #on actualise le nombre de mailles manche apres avoir calcule les augmentations
    my_sleeve.setUpperarmStitches(my_sleeve.getTopSleeveStitches() + nb_augmentations_manches * 2 + nb_de_mailles_aisselle)


    #calcul du nombre de rangs pour arriver jusqu'a l'emmanchure
    #la profondeur d'emmanchure est la meme pour le devant, le dos et les manches, on fait le calcul une seule fois
    my_back.setRowsToUnderarm(my_back.calculRowsNeeded(my_swatch.getRows(), my_back.getArmholeDepth()))

    my_back.setAugmentationsRaglan(nb_augmentations_dos, my_back.getRowsToUnderarm())

    my_sleeve.setAugmentationsRaglan(nb_augmentations_manches, my_back.getRowsToUnderarm())

    rangs_a_plat = 0
    x = my_front.getRightFrontStitches() + my_front.getLeftFrontStitches()
    y = my_back.getNeckStitches()
    while (x != y):
        while (rangs_a_plat <= my_back.getAugmentationsRapides()):
            rangs_a_plat+= my_back.getRythmeRapide()
            x+=4
            y+=2
        rangs_a_plat+= my_back.getRythmeLent()
        x+=4
        y+=2
    
    a_plat = rangsAplat(rangs_a_plat)
    print(a_plat)
    fichier_a_telecharger.write(a_plat)


    #separation du corps et des

    fichier_a_telecharger.close()


if __name__ == "__main__":
    main()

    
