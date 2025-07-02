def montage(devant_droit, manche, dos, devant_gauche):
    instruction = "Debut : monter " + str(devant_droit) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(manche) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(dos) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(manche) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(devant_gauche) + " mailles.\n"

    return instruction

def rangsAplat(rangs):
    instruction = "il faut tricoter a plat pendant " + str(rangs) + " rangs.\n"
    return instruction

#comme les manches et le corps n'ont pas forcement le meme nombre d'augmentations dans la section rapide
#il est possible que les augmentations dans la section lente ne tombent pas sur les memes rangs 
#par exemple rangs 14, 17, 20... pour les manches, et rangs 15, 18, 21... pour le corps
#par convention, il est preferable de faire en sorte que les augmentations aient lieu en meme temps 
#dans la mesure du possible, afin de diminuer le risque d'erreur 
def miseAJourDesRangs(liste_1, liste_2):
    if(len(liste_1) < len(liste_2)):
        i = 0
        while (liste_1[0] not in liste_2):
            i+=1
            liste_1[0] += i
        for n in range (1, len(liste_1)):
            liste_1[n] += i

    else:
        i = 0
        while (liste_2[0] not in liste_1):
            i+=1
            liste_2[0] += i
        for n in range (1, len(liste_2)):
            liste_2[n] += i