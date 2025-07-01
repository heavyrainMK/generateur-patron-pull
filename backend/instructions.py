def montage(devant_droit, manche, dos, devant_gauche):
    instruction = "Debut : monter " + str(devant_droit) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(manche) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(dos) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(manche) + " mailles, placer un marqueur, 1 maille, placer un marqueur, " + str(devant_gauche) + " mailles.\n"

    return instruction

def rangsAplat(rangs):
    instruction = "il faut tricoter a plat pendant " + str(rangs) + " rangs.\n"
    return instruction

def miseAJourDesRangs(liste_1, liste_2):
    if(len(liste_1) < len(liste_2)):
        i = 0
        while (liste_1[0] not in liste_2):
            i+=1
            liste_1[0] += i
        for n in range (1, len(liste_1)):
            liste_1[n] += i
        return liste_1

    else:
        i = 0
        while (liste_2[0] not in liste_1):
            i+=1
            liste_2[0] += i
        for n in range (1, len(liste_2)):
            liste_2[n] += i
        return liste_2