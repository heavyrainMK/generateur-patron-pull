# *******************************************************
# Nom ......... : instructions.py
# Rôle ........ : Définition des fonctions générant les instructions textuelles du patron de tricot (montage, augmentations, séparations, etc.).
# Auteurs ..... : M, L, M
# Version ..... : V1.0.0 du 28/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : Contient les différentes fonctions permettant de générer les sections du patron de tricot (montage, rangs à plat,
#                 synchronisation des rangs d'augmentation, augmentations pour le corps et les manches, diminutions, côtes, séparation des manches et du corps)
#                 ainsi que le dictionnaire d'abréviations utilisées dans les instructions.
# Technologies  : Python
# Dépendances . : math
# Usage ....... : Importé par app.py pour composer le patron final sous forme de texte.
# *******************************************************

import math

# Dictionnaire des abréviations utilisées dans les instructions.
abbreviations = {
    "m": "maille",
    "M": "marqueur",
    "GM": "glisser le marqueur",
    "aug": "augmentation",
    "dim": "diminution",
    "PM": "placer le marqueur",
    "RM": "retirer le marqueur",
    "DDMC": "diminution double à maille centrée",
}

def montage(devant_droit, manche, dos, devant_gauche):
    """
    Construit une phrase décrivant le montage initial des mailles pour un pull raglan.

    Chaque section (devant droit, manche, dos, manche, devant gauche) est séparée par un marqueur et
    encadrée de mailles de raglan.

    :param devant_droit: Nombre de mailles à monter pour le devant droit.
    :param manche: Nombre de mailles à monter pour chacune des manches.
    :param dos: Nombre de mailles à monter pour le dos.
    :param devant_gauche: Nombre de mailles à monter pour le devant gauche.
    :return: Une chaîne de caractères décrivant le montage des mailles avec les marqueurs.
    """
    return (
        f"Début : monter {devant_droit} m, PM, 1 m, PM, {manche} m, PM, 1 m, PM, "
        f"{dos} m, PM, 1 m, PM, {manche} m, PM, 1 m, PM, {devant_gauche} m."
    )

def rangsAplat(rangs):
    """
    Génère une instruction expliquant combien de rangs doivent être tricotés à plat pour former l'encolure en V.

    Lorsque l'on tricote à plat au début d'un pull top-down, on augmente une maille au début et à la fin
    de chaque rang pour former l'encolure, en plus des augmentations des raglans.

    :param rangs: Nombre de rangs à tricoter à plat.
    :return: Une chaîne de caractères expliquant la formation de l'encolure en V sur le nombre de rangs spécifié.
    """
    return (
        f"Il faut tricoter à plat sur {rangs} rangs pour créer l'encolure en V. "
        f"Augmenter d'une maille au début et à la fin de chaque rang, en plus des augmentations des raglans."
    )

def synchronisationDesRangs(liste_1, liste_2):
    """
    Synchronise deux listes de numéros de rangs afin que les augmentations lentement espacées
    aient lieu aux mêmes rangs pour le corps et les manches.

    Lorsque le nombre d'augmentations dans la section rapide diffère entre le corps et les manches,
    les augmentations dans la section lente risquent de ne pas tomber sur les mêmes rangs (par exemple 14, 17, 20
    pour les manches et 15, 18, 21 pour le corps). Par convention, il est préférable que les augmentations
    aient lieu en même temps pour diminuer le risque d'erreur.

    :param liste_1: Liste de rangs pour les augmentations d'un premier élément (corps ou manche).
    :param liste_2: Liste de rangs pour les augmentations d'un second élément (corps ou manche).
    :return: La liste modifiée permettant la synchronisation (la fonction agit par effet de bord sur les listes).
    """
    if not liste_1 or not liste_2:
        print(
            "synchronisationDesRangs : au moins une des deux listes est vide, aucune synchronisation possible."
        )
        return []
    # Identifie quelle liste a le moins d'éléments et décale ses rangs pour aligner les débuts.
    if len(liste_1) < len(liste_2):
        i = 0
        while (liste_1[0] not in liste_2):
            i += 1
            liste_1[0] += 1
        for n in range(1, len(liste_1)):
            liste_1[n] += i
        print(f"Après modification : {liste_1}, {liste_2}")
    else:
        i = 0
        while (liste_2[0] not in liste_1):
            i += 1
            liste_2[0] += 1
        for n in range(1, len(liste_2)):
            liste_2[n] += i
        print(f"Après modification : {liste_1}, {liste_2}")
    return liste_1 if len(liste_1) < len(liste_2) else liste_2

def augmentationsCorps(rang):
    """
    Génère une instruction pour effectuer des augmentations uniquement sur le corps lors d'un rang donné.

    L'algorithme décrit les quatre augmentations à répartir de manière symétrique autour des marqueurs.

    :param rang: Numéro du rang en cours.
    :return: Chaîne de caractères décrivant les actions à réaliser pour le corps sur ce rang.
    """
    return (
        f"Rang {rang} : Tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, tricoter jusqu'au M suivant, GM, 1 m, GM, 1 aug, "
        f"tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, tricoter jusqu'au M suivant, GM, 1 m, GM, 1 aug, "
        f"tricoter jusqu'à la fin du rang. (4 augmentations)\n"
    )

def augmentationsManches(rang):
    """
    Génère une instruction pour effectuer des augmentations uniquement sur les manches lors d'un rang donné.

    Les augmentations sont disposées de part et d'autre des marqueurs qui délimitent les manches.

    :param rang: Numéro du rang en cours.
    :return: Chaîne de caractères décrivant les actions à réaliser pour les manches sur ce rang.
    """
    return (
        f"Rang {rang} : Tricoter jusqu'au premier M, GM, tricoter 1 m, GM, 1 aug, tricoter jusqu'à 1 m avant M, 1 aug, GM, "
        f"tricoter 1 m, GM, tricoter jusqu'au M suivant, GM, tricoter 1 m, GM, 1 aug, tricoter jusqu'à 1 m avant M, "
        f"1 aug, GM, tricoter 1 m, GM, tricoter jusqu'à la fin du rang. (4 augmentations)\n"
    )

def augmentationsCorpsEtManches(rang):
    """
    Génère une instruction pour effectuer des augmentations simultanément sur le corps et les manches.

    Dans ce cas, on réalise huit augmentations réparties aux quatre raglans afin d'augmenter à la fois
    le corps et les manches.

    :param rang: Numéro du rang en cours.
    :return: Chaîne de caractères décrivant les actions à réaliser pour le corps et les manches sur ce rang.
    """
    return (
        f"Rang {rang} : Tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, 1 aug. "
        f"Répéter jusqu'à la fin du rang. (8 augmentations)\n"
    )

def tricoterUnRang(rang):
    """
    Génère une instruction pour tricoter un rang sans aucune augmentation ni diminution.

    :param rang: Numéro du rang.
    :return: Chaîne de caractères indiquant simplement de tricoter le rang normalement.
    """
    return f"Rang {rang} : Tricoter le rang normalement.\n"

def tricoterPlusieursRangs(rang_debut, rang_fin):
    """
    Génère une instruction pour tricoter plusieurs rangs consécutifs sans augmentation.

    :param rang_debut: Numéro du premier rang de la séquence.
    :param rang_fin: Numéro du dernier rang de la séquence.
    :return: Chaîne de caractères indiquant la plage de rangs à tricoter normalement.
    """
    return f"Rang {rang_debut} a {rang_fin} : tricoter normalement.\n"


def joindre(rang):
    """
    Génère les instructions permettant de joindre les deux côtés du tricot afin de poursuivre en rond.

    Il est important de joindre sur un rang endroit et d'utiliser un marqueur distinct pour repérer
    le début du rang, déplacé après la maille raglan de la manche droite.

    :param rang: Numéro du rang où la jointure doit être réalisée.
    :return: Chaîne de caractères décrivant la procédure de jointure.
    """
    return (
        f"Rang {rang} : Joindre les deux côtés du tricot pour commencer à tricoter en rond. "
        f"Pour cela, tricoter la dernière maille du rang ensemble à l'endroit avec la première maille du rang. "
        f"Attention de toujours bien joindre sur un rang endroit. "
        f"Si le rang en cours est un rang envers, repartez sur un rang endroit (sans faire les augmentations de l'encolure), puis joignez à la fin de ce rang. "
        f"Le début du rang se trouve à la pointe du V ; vous allez le déplacer jusqu'au premier raglan de la manche droite (après la maille raglan, de sorte à ce qu'elle soit bien comprise dans le corps et non la manche). "
        f"Il suffit de tricoter jusqu'à cet endroit et d'y placer un marqueur différent des autres.\n"
    )

def separationManchesEtCorps(rang, mailles_aisselle, mailles_manches, maille_corps):
    """
    Génère les instructions pour la séparation des manches et du corps.

    Lors de cette étape, les mailles des raglans sont intégrées au corps. Les mailles des manches sont mises
    en attente et de nouvelles mailles sont montées sous les aisselles pour continuer à tricoter le corps en rond.

    :param rang: Numéro du rang où a lieu la séparation.
    :param mailles_aisselle: Nombre de mailles à monter sous chaque aisselle.
    :param mailles_manches: Nombre de mailles des manches à mettre en attente.
    :param maille_corps: Nombre total de mailles du corps après répartition.
    :return: Chaîne de caractères décrivant la séparation des manches et du corps.
    """
    return (
        f"Rang {rang} : Il faut maintenant séparer les manches et le corps du pull. Les mailles des raglans s'intègrent dans le corps. "
        f"On peut retirer tous les marqueurs sauf celui qui indique le début du rang. "
        f"Placer {mailles_manches} mailles en attente, monter {mailles_aisselle} mailles, RM, tricoter 1 m, RM, tricoter {maille_corps} mailles, "
        f"RM, tricoter 1 m, RM, placer {mailles_manches} mailles en attente, monter {mailles_aisselle} mailles, RM, tricoter 1 m, RM, "
        f"tricoter {maille_corps} mailles, tricoter 1 m.\n"
    )

def diminutionDebutEtFinDeRang(rang):
    """
    Génère l'instruction pour effectuer une diminution simple au début et à la fin d'un rang.

    Ce type de diminution est couramment utilisé pour affiner les manches ou le corps en réduisant
    progressivement le nombre de mailles.

    :param rang: Numéro du rang où la diminution est effectuée.
    :return: Chaîne de caractères décrivant la diminution.
    """
    return (
        f"Rang {rang} : Tricoter 1 m, glisser les 2 mailles suivantes à l'envers puis les tricoter ensemble, "
        f"tricoter jusqu'à 3 m de la fin, tricoter 2 m ensemble à l'endroit, tricoter 1 m.\n"
    )

def cotes(longueur):
    """
    Génère l'instruction pour tricoter des côtes sur une longueur spécifiée.

    On recommande d'utiliser des aiguilles d'une taille inférieure pour obtenir un bord plus élastique.

    :param longueur: Longueur en centimètres des côtes à tricoter.
    :return: Chaîne de caractères décrivant les côtes et le rabattage.
    """
    return (
        f"Changer d'aiguilles (prenez une taille en dessous) et tricoter en cotes sur {longueur}cm.\n"
        f"Rabattre les mailles avec un rabat elastique.\n"
    )

def maillesDencolure(mailles_manche, mailles_dos, rangs_encolure):
    """
    Calcule et génère l'instruction pour relever les mailles de l'encolure.

    Un nombre proportionnel de mailles est relevé le long de chaque section (manche droite, dos, manche gauche)
    et sur les côtés de l'encolure en V.

    :param mailles_manche: Nombre de mailles à relever le long de chaque manche.
    :param mailles_dos: Nombre de mailles à relever le long du dos.
    :param rangs_encolure: Nombre total de rangs utilisés pour former l'encolure.
    :return: Chaîne de caractères indiquant comment relever les mailles de l'encolure.
    """
    mailles_encolure = math.floor(rangs_encolure / 3 * 2)
    return (
        f"Avec les petites aiguilles, relever les mailles de l'encolure de la facon suivante : {mailles_manche} mailles le long de la manche droite, "
        f"{mailles_dos} mailles le long du dos, {mailles_manche} mailles le long de la manche gauche, {mailles_encolure} mailles de chaque cote de l'encolure (relever 2 mailles tous les 3 rangs).\n"
    )