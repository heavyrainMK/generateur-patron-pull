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
    return f"Debut : monter {devant_droit}m, PM, 1m, PM, {manche}m, PM, 1m, PM, {dos}m, PM, 1m, PM, {manche}m, PM, 1m, PM, {devant_gauche}m."

def rangsAplat(rangs):
    return f"Il faut tricoter a plat sur {rangs} rangs pour creer l'encolure en V. Augmenter d'une maille au debut et a la fin de chaque rang en plus des augmentations des raglans"

#comme les manches et le corps n'ont pas forcement le meme nombre d'augmentations dans la section rapide
#il est possible que les augmentations dans la section lente ne tombent pas sur les memes rangs 
#par exemple rangs 14, 17, 20... pour les manches, et rangs 15, 18, 21... pour le corps
#par convention, il est preferable de faire en sorte que les augmentations aient lieu en meme temps 
#dans la mesure du possible, afin de diminuer le risque d'erreur de tricot
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
    return f"Rang {rang} : tricoter jusqu'a 1m avant M, 1aug, GM, 1m, GM, tricoter jusqu'au M suivant, GM, 1m, GM, 1aug, tricoter jusqu'a 1m avant M, 1aug, GM, 1m, GM, tricoter jusqu'au M suivant, GM, 1m, GM, 1aug, tricoter jusqu'a la fin du rang. (4 augmentations)\n"

def augmentationsManches(rang):
    return f"Rang {rang} : Tricoter jusqu'au premier M, GM, tricoter 1m, GM, 1aug, tricoter jusqu'a 1m avant M, 1aug, GM, tricoter 1m, GM, tricoter jusqu'au M suivant, GM, tricoter 1m, GM, 1aug, tricoter jusqu'a 1m avant M, 1aug, GM, tricoter 1m, GM, tricoter jusqu'a la fin du rang. (4 augmentations)\n"

def augmentationsCorpsEtManches(rang):
    return f"Rang {rang} : Tricoter jusqu'a 1m avant M, 1aug, GM, 1m, GM, 1aug. Repeter jusqu'a la fin du rang. (8 augmentations)\n"

def tricoter(rang):
    return f"Rang {rang} : Tricoter le rang normalement.\n"

def joindre(rang):
    return f"Rang {rang} : Joindre les deux cotes du tricot pour commencer a tricoter en rond. Pour se faire, tricoter la derniere maille du rang ensemble a l'endroit avec la premiere maille du rang. Attention de toujours bien joindre sur un rang endroit. Si le rang en cours est un rang envers, repartez sur un rang endroit (sans faire les augmentations de l'encolure) puis joindre a la fin de ce rang. Le debut du rang se trouve a la point du V, vous allez le deplacer jusqu'au premier raglan de la manche droite (apres la maille raglan, de sorte a ce qu'elle soit bien comprise dans le corps et non la manche). Il suffit de tricoter jusqu'a cet endroit et y placer un marqueur different des autres.\n"

def separationManchesEtCorps(rang, mailles_aisselle, mailles_manches, maille_corps):
    return f"Rang {rang} : Il faut maintenant separer les manches et le corps du pull. Les mailles des raglans s'integrent dans le corps. On peut retirer tous les marqueurs sauf celui qui indique le debut du rang.  Placer {mailles_manches} mailles en attente, monter {mailles_aisselle} mailles, RM, tricoter 1m, RM, tricoter {maille_corps} mailles, RM, tricoter 1m, RM, placer {mailles_manches} mailles en attente, monter {mailles_aisselle} mailles, RM, tricoter 1m, RM, tricoter {maille_corps} mailles, tricoter 1m.\n"

def diminutionDebutEtFinDeRang(rang):
    return f"Rang {rang} : Tricoter 1m, glisser les 2 mailles suivantes a l'envers puis les tricoter ensemble, tricoter jusqu'a 3m de la fin, tricoter 2m ensemble a l'endroit, tricoter 1m.\n"