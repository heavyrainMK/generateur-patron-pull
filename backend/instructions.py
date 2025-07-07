abbreviations = {
    "m" : "maille", 
    "M" : "marqueur",
    "GM" : "glisser le marqueur",
    "aug" : "augmentation",
    "dim" : "diminution",
    "PM" : "placer marqueur"
}
def montage(devant_droit, manche, dos, devant_gauche):
    return f"Debut : monter {devant_droit}m, PM, 1m, PM, {manche}m, PM, 1m, PM, {dos}m, PM, 1m, PM, {manche}m, PM, 1m, PM, {devant_gauche}m."

def rangsAplat(rangs):
    return f"Il faut tricoter a plat sur {rangs} rangs pour creer l'encolure en V. Augmenter d'une maille au debut et a la fin de chaque rang"

#comme les manches et le corps n'ont pas forcement le meme nombre d'augmentations dans la section rapide
#il est possible que les augmentations dans la section lente ne tombent pas sur les memes rangs 
#par exemple rangs 14, 17, 20... pour les manches, et rangs 15, 18, 21... pour le corps
#par convention, il est preferable de faire en sorte que les augmentations aient lieu en meme temps 
#dans la mesure du possible, afin de diminuer le risque d'erreur 
def synchronisationDesRangs(liste_1, liste_2):
    if(len(liste_1) < len(liste_2)):
        i = 0
        while (liste_1[0] not in liste_2):
            i+=1
            liste_1[0] += 1
        for n in range (1, len(liste_1)):
            liste_1[n] += i
        print(f"apres modification : {liste_1}, {liste_2}")

    else:
        i = 0
        while (liste_2[0] not in liste_1):
            i+=1
            liste_2[0] += 1
        for n in range (1, len(liste_2)):
            liste_2[n] += i
        print(f"apres modification : {liste_1}, {liste_2}")

def augmentationsCorps(rang):
    return f"Rang {rang} : tricoter jusqu'a 1m avant M, 1aug, GM, 1m, GM, tricoter jusqu'au M suivant, GM, 1m, GM, 1aug, tricoter jusqu'a 1m avant M, 1aug, GM, 1m, GM, tricoter jusqu'au M suivant, GM, 1m, GM, 1aug, tricoter jusqu'a la fin du rang. (4 augmentations)"

def augmentationsManches(rang):
    return f"Rang {rang} : Tricoter jusqu'au premier M, GM, tricoter 1m, GM, 1aug, tricoter jusqu'a 1m avant M, 1aug, GM, tricoter 1m, GM, tricoter jusqu'au M suivant, GM, tricoter 1m, GM, 1aug, tricoter jusqu'a 1m avant M, 1aug, GM, tricoter 1m, GM, tricoter jusqu'a la fin du rang. (4 augmentations)"

def augmentationsCorpsEtManches(rang):
    return f"Rang {rang} : Tricoter jusqu'a 1m avant M, 1aug, GM, 1m, GM, 1aug. Repeter jusqu'a la fin du rang. (8 augmentations)"

def tricoter(rang):
    return f"Rang {rang} : Tricoter le rang normalement."