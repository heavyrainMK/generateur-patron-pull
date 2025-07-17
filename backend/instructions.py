abbreviations = {
    "m" : "maille", 
    "M" : "marqueur",
    "GM" : "glisser le marqueur",
    "aug" : "augmentation",
    "dim" : "diminution",
    "PM" : "placer le marqueur",
    "RM" : "retirer le marqueur"
}
def montage(devant_droit, manche, dos, devant_gauche):
    return (f"Début : monter {devant_droit} m, PM, 1 m, PM, {manche} m, PM, 1 m, PM, "
            f"{dos} m, PM, 1 m, PM, {manche} m, PM, 1 m, PM, {devant_gauche} m.")

def rangsAplat(rangs):
    return (f"Il faut tricoter à plat sur {rangs} rangs pour créer l'encolure en V. "
            f"Augmenter d'une maille au début et à la fin de chaque rang, en plus des augmentations des raglans.")

#comme les manches et le corps n'ont pas forcement le meme nombre d'augmentations dans la section rapide
#il est possible que les augmentations dans la section lente ne tombent pas sur les memes rangs 
#par exemple rangs 14, 17, 20... pour les manches, et rangs 15, 18, 21... pour le corps
#par convention, il est preferable de faire en sorte que les augmentations aient lieu en meme temps 
#dans la mesure du possible, afin de diminuer le risque d'erreur de tricot
def synchronisationDesRangs(liste_1, liste_2):
    if not liste_1 or not liste_2:
        print("synchronisationDesRangs : au moins une des deux listes est vide, aucune synchronisation possible.")
        return []
    if(len(liste_1) < len(liste_2)):
        i = 0
        while (liste_1[0] not in liste_2):
            i+=1
            liste_1[0] += 1
        for n in range (1, len(liste_1)):
            liste_1[n] += i
        print(f"Après modification : {liste_1}, {liste_2}")

    else:
        i = 0
        while (liste_2[0] not in liste_1):
            i+=1
            liste_2[0] += 1
        for n in range (1, len(liste_2)):
            liste_2[n] += i
        print(f"Après modification : {liste_1}, {liste_2}")

def augmentationsCorps(rang):
    return (f"Rang {rang} : Tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, tricoter jusqu'au M suivant, GM, 1 m, GM, 1 aug, "
            f"tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, tricoter jusqu'au M suivant, GM, 1 m, GM, 1 aug, "
            f"tricoter jusqu'à la fin du rang. (4 augmentations)\n")

def augmentationsManches(rang):
    return (f"Rang {rang} : Tricoter jusqu'au premier M, GM, tricoter 1 m, GM, 1 aug, tricoter jusqu'à 1 m avant M, 1 aug, GM, "
            f"tricoter 1 m, GM, tricoter jusqu'au M suivant, GM, tricoter 1 m, GM, 1 aug, tricoter jusqu'à 1 m avant M, "
            f"1 aug, GM, tricoter 1 m, GM, tricoter jusqu'à la fin du rang. (4 augmentations)\n")

def augmentationsCorpsEtManches(rang):
    return (f"Rang {rang} : Tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, 1 aug. "
            f"Répéter jusqu'à la fin du rang. (8 augmentations)\n")

def tricoter(rang):
    return f"Rang {rang} : Tricoter le rang normalement.\n"

def joindre(rang):
    return (f"Rang {rang} : Joindre les deux côtés du tricot pour commencer à tricoter en rond. "
            f"Pour cela, tricoter la dernière maille du rang ensemble à l'endroit avec la première maille du rang. "
            f"Attention de toujours bien joindre sur un rang endroit. "
            f"Si le rang en cours est un rang envers, repartez sur un rang endroit (sans faire les augmentations de l'encolure), puis joignez à la fin de ce rang. "
            f"Le début du rang se trouve à la pointe du V ; vous allez le déplacer jusqu'au premier raglan de la manche droite (après la maille raglan, de sorte à ce qu'elle soit bien comprise dans le corps et non la manche). "
            f"Il suffit de tricoter jusqu'à cet endroit et d'y placer un marqueur différent des autres.\n")

def separationManchesEtCorps(rang, mailles_aisselle, mailles_manches, maille_corps):
    return (f"Rang {rang} : Il faut maintenant séparer les manches et le corps du pull. Les mailles des raglans s'intègrent dans le corps. "
            f"On peut retirer tous les marqueurs sauf celui qui indique le début du rang. "
            f"Placer {mailles_manches} mailles en attente, monter {mailles_aisselle} mailles, RM, tricoter 1 m, RM, tricoter {maille_corps} mailles, "
            f"RM, tricoter 1 m, RM, placer {mailles_manches} mailles en attente, monter {mailles_aisselle} mailles, RM, tricoter 1 m, RM, "
            f"tricoter {maille_corps} mailles, tricoter 1 m.\n")

def diminutionDebutEtFinDeRang(rang):
    return (f"Rang {rang} : Tricoter 1 m, glisser les 2 mailles suivantes à l'envers puis les tricoter ensemble, "
            f"tricoter jusqu'à 3 m de la fin, tricoter 2 m ensemble à l'endroit, tricoter 1 m.\n")