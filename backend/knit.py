
from sleeve import Sleeve
from front import Front
from back import Back
from swatch import Swatch
from calculs import Calculs
from instructions import montage, rangsAplat, synchronisationDesRangs, augmentationsCorps, augmentationsManches, augmentationsCorpsEtManches, tricoterUnRang, tricoterPlusieursRangs, joindre, separationManchesEtCorps, diminutionDebutEtFinDeRang, cotes, maillesDencolure
import math
import io

def main():

    aisance_corps = 5
    aisance_manches = 0
    mailles_dans_10_cm = 28
    rangs_dans_10_cm = 32
    tour_de_poitrine = 92
    largeur_arriere_nuque = 21
    hauteur_emmanchure = 25
    longueur_totale_corps = 30
    longueur_cotes_corps = 5
    longueur_corps = longueur_totale_corps - longueur_cotes_corps
    longueur_totale_manche = 45
    longueur_cotes_manche = 5
    longueur_manche = longueur_totale_manche - longueur_cotes_manche
    tour_de_bras = 31
    tour_de_poignet = 18.5
    cotes_encolure = 5

    fichier_a_telecharger = open("instructions_pull_sur_mesure.txt", "w")
    #il faut construire les objets avec les mesures fournis par l'utilisateur
    my_front = Front(tour_de_poitrine, longueur_corps)
    my_back = Back(largeur_arriere_nuque, tour_de_poitrine, hauteur_emmanchure, longueur_corps)
    my_sleeve = Sleeve(tour_de_bras, tour_de_poignet, longueur_manche)

    my_swatch = Swatch(mailles_dans_10_cm, rangs_dans_10_cm)
    

    #je ne mets pas les mailles d'aisselle dans une classe car elles sont communes a la manches et au corps, reparties sur le devant et le dos
    nb_de_mailles_aisselle = 0
    nb_augmentations_dos = 0
    nb_augmentations_manches = 0

    #calcul des mailles au montage
    my_back.setNeckStitches(my_back.calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth(), 0))
    my_sleeve.setTopSleeveStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getTopSleeveWidth(), 0))

    
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

    rangs_a_plat = 1
    x = my_front.getRightFrontStitches() + my_front.getLeftFrontStitches() 
    y = my_back.getNeckStitches()
    while (x <= y):
        if (rangs_a_plat <= ((my_back.getAugmentationsRapides() * my_back.getRythmeRapide()) + 1)):
            if ((rangs_a_plat - 1) % my_back.getRythmeRapide() == 0):
                x+=4
                y+=2
                rangs_a_plat+=1
            else:
                x+=2
                rangs_a_plat+=1
        else:
            if ((rangs_a_plat - (my_back.getAugmentationsRapides() * my_back.getRythmeRapide()) - 1) % my_back.getRythmeLent() == 0):
                x+=4
                y+=2
                rangs_a_plat+=1
            else:
                x+=2
                rangs_a_plat+=1

    #on synchronise uniquement si les augmentations se font au meme rythme
    if my_back.getRythmeLent() == my_sleeve.getRythmeLent():
        synchronisationDesRangs(my_back.getNumeroRangsAugmentationLent(), my_sleeve.getNumeroRangsAugmentationLent())

    print('Montage : \n')
    fichier_a_telecharger.write('Montage : \n')
    impression = montage(my_front.getRightFrontStitches(), my_sleeve.getTopSleeveStitches(), my_back.getNeckStitches(), my_front.getLeftFrontStitches())
    print(impression)
    fichier_a_telecharger.write(impression)
    impression = rangsAplat(rangs_a_plat)
    print(impression)
    fichier_a_telecharger.write(impression)

    print()
    for rang_en_cours in range (1, my_back.getRowsToUnderarm()):
        if rang_en_cours == rangs_a_plat + 1:
            impression = joindre(rang_en_cours)
            print(impression)
            fichier_a_telecharger.write(impression)

        if (rang_en_cours in my_back.getNumeroRangsAugmentationRapide() and rang_en_cours in my_sleeve.getNumeroRangsAugmentationRapide()) or (rang_en_cours in my_back.getNumeroRangsAugmentationRapide() and rang_en_cours in my_sleeve.getNumeroRangsAugmentationLent()) or (rang_en_cours in my_back.getNumeroRangsAugmentationLent() and rang_en_cours in my_sleeve.getNumeroRangsAugmentationRapide()) or (rang_en_cours in my_back.getNumeroRangsAugmentationLent() and my_sleeve.getNumeroRangsAugmentationLent()):
            impression = augmentationsCorpsEtManches(rang_en_cours)
            print(impression)
            fichier_a_telecharger.write(impression)

        elif rang_en_cours in my_back.getNumeroRangsAugmentationRapide() or rang_en_cours in my_back.getNumeroRangsAugmentationLent():
            impression = augmentationsCorps(rang_en_cours)
            print(impression)
            fichier_a_telecharger.write(impression)

        elif rang_en_cours in my_sleeve.getNumeroRangsAugmentationRapide() or rang_en_cours in my_sleeve.getNumeroRangsAugmentationLent():
            impression = augmentationsManches(rang_en_cours)
            print(impression)
            fichier_a_telecharger.write(impression)

        else:
            impression = tricoterUnRang(rang_en_cours)
            print(impression)
            fichier_a_telecharger.write(impression)

    impression = separationManchesEtCorps(rang_en_cours + 1, nb_de_mailles_aisselle, my_sleeve.getUpperarmStitches(), my_back.getChestStitches())
    print(impression)
    fichier_a_telecharger.write(impression)

    my_back.setRowsToHem(my_back.calculRowsNeeded(my_swatch.getRows(), my_back.getUnderArmToHemLength()))
    print('Le corps : \n')
    fichier_a_telecharger.write('Le corps : \n')
    impression = tricoterPlusieursRangs(1, my_back.getRowsToHem())
    print(impression)
    fichier_a_telecharger.write(impression)
    impression = cotes(longueur_cotes_corps)
    print(impression)
    fichier_a_telecharger.write(impression)


    #calcul et repartition des diminutions de la manche jusqu'au poignet
    #ne pas oublier de soustraire les cotes, j'ai mis 5cm pour l'instant
    my_sleeve.setRowsToWrist(my_sleeve.calculRowsNeeded(my_swatch.getRows(), my_sleeve.getUnderArmToHemLength()))
    my_sleeve.setWristStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getWristCircumference(), 0))

    #ne pas oublier de compter les mailles de l'aisselle
    #on divise le resultat par 2 puisque les diminutions vont par paire, comme les augmentations
    nb_diminutions_manches = my_sleeve.calculDecreases(my_sleeve.getUpperarmStitches() + nb_de_mailles_aisselle, my_sleeve.getWristStitches()) / 2
    ratio_diminution_manche = my_sleeve.calculRatio(my_sleeve.getRowsToWrist(), nb_diminutions_manches)

    print('La manche :\n')
    fichier_a_telecharger.write('La manche :\n')

    impression = diminutionDebutEtFinDeRang(1)
    print(impression)
    fichier_a_telecharger.write(impression)
    impression = tricoterPlusieursRangs(2, ratio_diminution_manche)
    print(impression)
    fichier_a_telecharger.write(impression)
    print(f"Repeter les {math.trunc(ratio_diminution_manche)} rangs precedents {int(nb_diminutions_manches)} fois\n")
    fichier_a_telecharger.write((f"Repeter les {math.trunc(ratio_diminution_manche)} rangs precedents {int(nb_diminutions_manches)} fois\n"))
    impression = cotes(longueur_cotes_manche)
    fichier_a_telecharger.write(impression)
    
    mailles_encolure = math.floor(rangs_a_plat / 3 * 2)

    print("L'encolure :\n")
    fichier_a_telecharger.write("L'encolure :\n")
    print(f"Avec les petites aiguilles, relever les mailles de l'encolure de la facon suivante : {my_sleeve.getTopSleeveStitches()} mailles le long de la manche droite, {my_back.getNeckStitches()} mailles le long du dos, {my_sleeve.getTopSleeveStitches()} mailles le long de la manche gauche, {mailles_encolure} mailles de chaque cote de l'encolure (relever 2 mailles tous les 3 rangs).\nTricoter en cotes sur {cotes_encolure}cm.\nRabattre en utilisant un rabat elastique.\n")
    fichier_a_telecharger.write(f"Avec les petites aiguilles, relever les mailles de l'encolure de la facon suivante : {my_sleeve.getTopSleeveStitches()} mailles le long de la manche droite, {my_back.getNeckStitches()} mailles le long du dos, {my_sleeve.getTopSleeveStitches()} mailles le long de la manche gauche, {mailles_encolure} mailles de chaque cote de l'encolure (relever 2 mailles tous les 3 rangs).\nTricoter en cotes sur {cotes_encolure}cm en effectuant une double diminution centrale ) la pointe du V.\nRabattre en utilisant un rabat elastique.\n")
    
    fichier_a_telecharger.close()


if __name__ == "__main__":
    main()

    
