# ---- Abréviations utilisées dans le patron ----
abbreviations = {
    "m": "maille", 
    "M": "marqueur",
    "GM": "glisser le marqueur",
    "aug": "augmentation",
    "dim": "diminution",
    "PM": "placer le marqueur",
    "RM": "retirer le marqueur"
}

def afficher_abreviations():
    texte = "## Abréviations utilisées\n"
    for abbr, mot in abbreviations.items():
        texte += f"- **{abbr}** : {mot}\n"
    return texte + "\n"

def montage(devant_droit, manche, dos, devant_gauche):
    return (
        f"### Montage\n"
        f"Début : monter {devant_droit} m, PM, 1 m, PM, {manche} m, PM, 1 m, PM, "
        f"{dos} m, PM, 1 m, PM, {manche} m, PM, 1 m, PM, {devant_gauche} m.\n"
    )

def rangsAplat(rangs):
    return (
        f"### Formation de l'encolure en V\n"
        f"Il faut tricoter à plat sur {rangs} rangs pour créer l'encolure en V. "
        f"Augmenter d'une maille au début et à la fin de chaque rang, en plus des augmentations des raglans.\n"
    )

def synchronisationDesRangs(liste_1, liste_2):
    if not liste_1 or not liste_2:
        print("synchronisationDesRangs : au moins une des deux listes est vide, aucune synchronisation possible.")
        return []
    if len(liste_1) < len(liste_2):
        i = 0
        while liste_1[0] not in liste_2:
            i += 1
            liste_1[0] += 1
        for n in range(1, len(liste_1)):
            liste_1[n] += i
        print(f"Après modification : {liste_1}, {liste_2}")
    else:
        i = 0
        while liste_2[0] not in liste_1:
            i += 1
            liste_2[0] += 1
        for n in range(1, len(liste_2)):
            liste_2[n] += i
        print(f"Après modification : {liste_1}, {liste_2}")

def augmentationsCorps(rang):
    return (
        f"### Rang {rang} — Augmentations sur le corps (4 augmentations)\n"
        f"Pour chaque raglan du corps :\n"
        f"- Tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, tricoter jusqu'au M suivant, GM, 1 m, GM, 1 aug.\n"
        f"Répéter pour le devant et le dos.\n"
    )

def augmentationsManches(rang):
    return (
        f"### Rang {rang} — Augmentations sur les manches (4 augmentations)\n"
        f"Pour chaque manche :\n"
        f"- Tricoter jusqu'au premier M, GM, tricoter 1 m, GM, 1 aug.\n"
        f"- Tricoter jusqu'à 1 m avant M, 1 aug, GM, tricoter 1 m, GM.\n"
        f"Répéter l'opération pour chaque manche.\n"
    )

def augmentationsCorpsEtManches(rang):
    return (
        f"### Rang {rang} — Augmentations raglan complètes (8 augmentations)\n"
        f"Pour chaque maille raglan :\n"
        f"- Tricoter jusqu'à 1 m avant M, 1 aug, GM, 1 m, GM, 1 aug.\n"
        f"Répéter autour de chaque maille raglan.\n"
    )

def tricoter(rang):
    return f"### Rang {rang}\nTricoter le rang normalement.\n"

def joindre(rang):
    return (
        f"### Rang {rang} — Passage en rond\n"
        f"Joindre les deux côtés du tricot pour commencer à tricoter en rond.\n"
        f"Tricoter la dernière maille du rang ensemble à l'endroit avec la première maille du rang.\n"
        f"Attention : toujours joindre sur un rang endroit.\n"
        f"Si le rang en cours est un rang envers, tricoter un rang endroit (sans augmenter l'encolure), puis joindre à la fin de ce rang.\n"
        f"Le début du rang se place à la pointe du V, puis déplacer jusqu'au premier raglan de la manche droite "
        f"(après la maille raglan, pour l'intégrer au corps).\n"
        f"Placer un marqueur distinct à ce nouvel endroit.\n"
    )

def separationManchesEtCorps(rang, mailles_aisselle, mailles_manches, maille_corps):
    return (
        f"### Rang {rang} — Séparation du corps et des manches\n"
        f"À ce stade, séparer les manches du corps. Les mailles des raglans s'intègrent dans le corps.\n"
        f"On peut retirer tous les marqueurs sauf celui du début du rang.\n\n"
        f"- Placer {mailles_manches} mailles en attente (manche)\n"
        f"- Monter {mailles_aisselle} mailles (aisselle), RM, tricoter 1 m, RM\n"
        f"- Tricoter {maille_corps} mailles (corps), RM, tricoter 1 m, RM\n"
        f"- Placer {mailles_manches} mailles en attente (autre manche), monter {mailles_aisselle} mailles, RM, tricoter 1 m, RM\n"
        f"- Tricoter {maille_corps} mailles, tricoter 1 m\n"
    )

def diminutionDebutEtFinDeRang(rang):
    return (
        f"### Rang {rang} — Diminutions début et fin de rang\n"
        f"- Tricoter 1 m\n"
        f"- Glisser les 2 mailles suivantes à l'envers puis les tricoter ensemble\n"
        f"- Tricoter jusqu'à 3 m de la fin\n"
        f"- Tricoter 2 m ensemble à l'endroit\n"
        f"- Tricoter 1 m\n"
    )