# *******************************************************
# Nom ......... : app.py
# Rôle ........ : Serveur Flask pour le générateur de patrons de tricot
# Auteurs ..... : M, L, M
# Version ..... : V2.1.6 du 23/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : API REST pour calculer un patron de tricot à partir des mesures utilisateur,
#                 traitement des données, calculs personnalisés, génération du résumé du patron.
# Technologies  : Python, Flask
# Dépendances . : flask, flask-cors, gunicorn
# Usage ....... : Déploiement sur Render ; endpoint principal : POST /api/calculer-patron
# *******************************************************

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import math
import traceback

from swatch import Swatch
from back import Back
from front import Front
from sleeve import Sleeve
from instructions import (
    montage,
    rangsAplat,
    synchronisationDesRangs,
    augmentationsCorps,
    augmentationsManches,
    augmentationsCorpsEtManches,
    tricoterUnRang,
    tricoterPlusieursRangs,
    joindre,
    separationManchesEtCorps,
    diminutionDebutEtFinDeRang,
    cotes,
    maillesDencolure,
    abbreviations
)

app = Flask(__name__)
CORS(app)

@app.route('/api/calculer-patron', methods=['POST'])
def calculer_patron():
    try:
        data = request.get_json()
        print("Données reçues :", data)

        if data is None:
            return jsonify({"error": "Aucune donnée JSON reçue."}), 400
        
        # Vérification des champs obligatoires
        champs_obligatoires = [
            'mailles_10cm', 'rangs_10cm', 'tour_poitrine', 'longueur_totale', 'largeur_nuque',
            'hauteur_emmanchure', 'longueur_manches', 'tour_bras', 'tour_poignet'
        ]
        for champ in champs_obligatoires:
            if champ not in data:
                return jsonify({"error": f"Champ obligatoire manquant : {champ}"}), 400

        # Vérifie la présence et la valeur des aisances personnalisées
        if data.get('mode_aisance_corps') == 'personnalise':
            if 'aisance_corps' not in data or data.get('aisance_corps') in [None, '', 0]:
                return jsonify({"error": "Le mode d'aisance corps est personnalisé mais aucune valeur n'a été fournie."}), 400
        if data.get('mode_aisance_manches') == 'personnalise':
            if 'aisance_manches' not in data or data.get('aisance_manches') in [None, '', 0]:
                return jsonify({"error": "Le mode d'aisance manches est personnalisé mais aucune valeur n'a été fournie."}), 400

        # Extraction stricte des mesures utilisateur et conversion en float avec gestion d'erreur
        try:
            mailles_10cm = float(data.get('mailles_10cm'))
            rangs_10cm = float(data.get('rangs_10cm'))
            tour_poitrine = float(data.get('tour_poitrine'))
            longueur_totale = float(data.get('longueur_totale'))
            largeur_nuque = float(data.get('largeur_nuque'))
            hauteur_emmanchure = float(data.get('hauteur_emmanchure'))
            longueur_manches = float(data.get('longueur_manches'))
            tour_bras = float(data.get('tour_bras'))
            tour_poignet = float(data.get('tour_poignet'))
            cotes_bas = float(data.get('cotes_bas', 5))
            cotes_poignets = float(data.get('cotes_poignets', 5))
            cotes_encolure = float(data.get('cotes_encolure', 5))
        except Exception:
            return jsonify({"error": "Toutes les mesures doivent être des nombres valides."}), 400

        # Refuse toute valeur négative ou nulle
        mesures = [
            mailles_10cm, rangs_10cm, tour_poitrine, longueur_totale,
            largeur_nuque, hauteur_emmanchure, longueur_manches, tour_bras, tour_poignet
        ]
        for v in mesures:
            if v is None or v <= 0:
                return jsonify({"error": "Toutes les mesures doivent être strictement positives."}), 400

        # --- Ajustement des longueurs nettes (sans côtes) ---
        longueur_corps = longueur_totale - cotes_bas
        longueur_manche = longueur_manches - cotes_poignets

        # --- Aisance ---
        mode_aisance_corps = data.get('mode_aisance_corps')
        mode_aisance_manches = data.get('mode_aisance_manches')
        table_aisance = {
            'pres_corps': -5,
            'ajuste': 0,
            'standard': 5,
            'large': 10,
            'tres_large': 20,
        }
        aisance_corps = float(data.get('aisance_corps', 0)) if mode_aisance_corps == 'personnalise' else table_aisance.get(mode_aisance_corps, 10)
        aisance_manches = float(data.get('aisance_manches', 0)) if mode_aisance_manches == 'personnalise' else table_aisance.get(mode_aisance_manches, 10)

        # --- Création des objets ---
        my_front = Front(tour_poitrine, longueur_corps)
        my_back = Back(largeur_nuque, tour_poitrine, hauteur_emmanchure, longueur_corps)
        my_sleeve = Sleeve(tour_bras, tour_poignet, longueur_manche)
        my_swatch = Swatch(mailles_10cm, rangs_10cm)

        # --- Calculs des mailles et augmentations ---
        nb_de_mailles_aisselle = my_back.calculStitchesNeeded(my_swatch.getStitches(), 3, 0)
        my_back.setNeckStitches(my_back.calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth(), 0))
        my_sleeve.setTopSleeveStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getTopSleeveWidth(), 0))
        my_front.setChestStitches(my_front.calculStitchesNeeded(my_swatch.getStitches(), my_front.getChestWidth() / 2, aisance_corps))
        my_back.setChestStitches(my_back.calculStitchesNeeded(my_swatch.getStitches(), my_back.getChestWidth() / 2, aisance_corps))
        my_sleeve.setUpperarmStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getUpperArmCircumference(), aisance_manches))

        nb_augmentations_dos = math.ceil((my_back.calculIncreases(my_back.getNeckStitches(), my_back.getChestStitches()) - nb_de_mailles_aisselle - 2) / 2)
        my_back.setChestStitches(my_back.getNeckStitches() + nb_augmentations_dos * 2 + 2 + nb_de_mailles_aisselle)
        my_front.setChestStitches(my_back.getChestStitches())
        nb_augmentations_manches = math.ceil((my_sleeve.calculIncreases(my_sleeve.getTopSleeveStitches(), my_sleeve.getUpperarmStitches()) - nb_de_mailles_aisselle) / 2)
        my_sleeve.setUpperarmStitches(my_sleeve.getTopSleeveStitches() + nb_augmentations_manches * 2 + nb_de_mailles_aisselle)

        # --- Calcul du nombre de rangs pour arriver à l'emmanchure ---
        my_back.setRowsToUnderarm(my_back.calculRowsNeeded(my_swatch.getRows(), my_back.getArmholeDepth()))
        my_back.setAugmentationsRaglan(nb_augmentations_dos, my_back.getRowsToUnderarm())
        my_sleeve.setAugmentationsRaglan(nb_augmentations_manches, my_back.getRowsToUnderarm())

        # --- Calcul des rangs à plat (avant de joindre en rond) ---
        rangs_a_plat = 1
        x = my_front.getRightFrontStitches() + my_front.getLeftFrontStitches()
        y = my_back.getNeckStitches()
        while x <= y:
            if rangs_a_plat <= (my_back.getAugmentationsRapides() * my_back.getRythmeRapide() + 1):
                if (rangs_a_plat - 1) % my_back.getRythmeRapide() == 0:
                    x += 4
                    y += 2
                else:
                    x += 2
            else:
                if (rangs_a_plat - my_back.getAugmentationsRapides() * my_back.getRythmeRapide() - 1) % my_back.getRythmeLent() == 0:
                    x += 4
                    y += 2
                else:
                    x += 2
            rangs_a_plat += 1

        # Synchronisation des rangs d’augmentation lent si nécessaire
        if my_back.getRythmeLent() == my_sleeve.getRythmeLent():
            synchronisationDesRangs(my_back.getNumeroRangsAugmentationLent(), my_sleeve.getNumeroRangsAugmentationLent())

        # ----------------------- Génération du patron -----------------------

        instructions = []
        instructions.append("============================================================")
        instructions.append("                  Patron de pull raglan top-down            ")
        instructions.append("============================================================\n")

        instructions.append("ABRÉVIATIONS UTILISÉES :")
        for k, v in abbreviations.items():
            instructions.append(f"  - {k.ljust(3)}: {v}")
        instructions.append("\n")

        # 1. MONTAGE
        instructions.append("------------------------------------------------------------")
        instructions.append("1. MONTAGE")
        instructions.append("------------------------------------------------------------")
        instructions.append(montage(
            my_front.getRightFrontStitches(),
            my_sleeve.getTopSleeveStitches(),
            my_back.getNeckStitches(),
            my_front.getLeftFrontStitches()
        ))
        instructions.append(f"Répartition : [devant droit] - raglan - [manche droite] - raglan - [dos] - raglan - [manche gauche] - raglan - [devant gauche]")
        total = (
            my_front.getRightFrontStitches() + 1 +
            my_sleeve.getTopSleeveStitches() + 1 +
            my_back.getNeckStitches() + 1 +
            my_sleeve.getTopSleeveStitches() + 1 +
            my_front.getLeftFrontStitches()
        )
        instructions.append(f"Total mailles au montage : {total}\n")

        # 2. FORMATION DE L’ENCOLURE EN V
        mailles_encolure = math.floor(rangs_a_plat / 3 * 2)
        instructions.append("------------------------------------------------------------")
        instructions.append("2. FORMATION DE L'ENCOLURE EN V")
        instructions.append("------------------------------------------------------------")
        instructions.append(rangsAplat(rangs_a_plat))

        # 3. AUGMENTATIONS RAGLAN
        instructions.append("------------------------------------------------------------")
        instructions.append("3. AUGMENTATIONS RAGLAN")
        instructions.append("------------------------------------------------------------")
        for rang_en_cours in range(1, my_back.getRowsToUnderarm()):
            if rang_en_cours == rangs_a_plat + 1:
                instructions.append(joindre(rang_en_cours))
            # Affiche et génère les instructions en utilisant rang_en_cours directement :
            if (
                (rang_en_cours in my_back.getNumeroRangsAugmentationRapide() and rang_en_cours in my_sleeve.getNumeroRangsAugmentationRapide()) or
                (rang_en_cours in my_back.getNumeroRangsAugmentationRapide() and rang_en_cours in my_sleeve.getNumeroRangsAugmentationLent()) or
                (rang_en_cours in my_back.getNumeroRangsAugmentationLent() and rang_en_cours in my_sleeve.getNumeroRangsAugmentationRapide()) or
                (rang_en_cours in my_back.getNumeroRangsAugmentationLent() and rang_en_cours in my_sleeve.getNumeroRangsAugmentationLent())
            ):
                instructions.append(augmentationsCorpsEtManches(rang_en_cours))
            elif (
                rang_en_cours in my_back.getNumeroRangsAugmentationRapide() or
                rang_en_cours in my_back.getNumeroRangsAugmentationLent()
            ):
                instructions.append(augmentationsCorps(rang_en_cours))
            elif (
                rang_en_cours in my_sleeve.getNumeroRangsAugmentationRapide() or
                rang_en_cours in my_sleeve.getNumeroRangsAugmentationLent()
            ):
                instructions.append(augmentationsManches(rang_en_cours))
            else:
                instructions.append(tricoterUnRang(rang_en_cours))

        # 4. SÉPARATION MANCHES ET CORPS
        instructions.append("------------------------------------------------------------")
        instructions.append("4. SÉPARATION MANCHES ET CORPS")
        instructions.append("------------------------------------------------------------")
        instructions.append(
            separationManchesEtCorps(
                rang_en_cours + 1,
                nb_de_mailles_aisselle,
                my_sleeve.getUpperarmStitches(),
                my_back.getChestStitches()
            )
        )

        # 5. CORPS APRÈS SÉPARATION
        my_back.setRowsToHem(my_back.calculRowsNeeded(my_swatch.getRows(), my_back.getUnderArmToHemLength()))
        instructions.append("------------------------------------------------------------")
        instructions.append("5. CORPS APRÈS SÉPARATION")
        instructions.append("------------------------------------------------------------")
        instructions.append(tricoterPlusieursRangs(1, my_back.getRowsToHem()))
        instructions.append(cotes(cotes_bas))

        instructions.append("------------------------------------------------------------")
        instructions.append("6. FINITIONS ENCOLURE")
        instructions.append("------------------------------------------------------------")
        instructions.append(
            f"Avec les petites aiguilles, relever les mailles de l'encolure de la façon suivante : "
            f"{my_sleeve.getTopSleeveStitches()} mailles le long de la manche droite, "
            f"{my_back.getNeckStitches()} mailles le long du dos, "
            f"{my_sleeve.getTopSleeveStitches()} mailles le long de la manche gauche, "
            f"{mailles_encolure} mailles de chaque côté de l'encolure (relever 2 mailles tous les 3 rangs).\n"
            f"Tricoter en côtes sur {cotes_encolure} cm, en effectuant une double diminution centrale à la pointe du V.\n"
            f"Rabattre souplement en utilisant un rabat élastique."
        )
        instructions.append("\n")

        # 6. MANCHES
        my_sleeve.setRowsToWrist(my_sleeve.calculRowsNeeded(my_swatch.getRows(), my_sleeve.getUnderArmToHemLength()))
        my_sleeve.setWristStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getWristCircumference(), 0))
        nb_diminutions_manches = my_sleeve.calculDecreases(
            my_sleeve.getUpperarmStitches() + nb_de_mailles_aisselle,
            my_sleeve.getWristStitches()
        ) / 2
        ratio_diminution_manche = my_sleeve.calculRatio(my_sleeve.getRowsToWrist(), nb_diminutions_manches)

        instructions.append("------------------------------------------------------------")
        instructions.append("7. MANCHES")
        instructions.append("------------------------------------------------------------")
        instructions.append(diminutionDebutEtFinDeRang(1))
        instructions.append(tricoterPlusieursRangs(2, int(ratio_diminution_manche)))
        instructions.append(
            f"Répéter les {math.trunc(ratio_diminution_manche)} rangs précédents {int(nb_diminutions_manches)} fois\n"
        )
        instructions.append(cotes(cotes_poignets))

        instructions.append("============================================================")

        return jsonify({"patron": "\n".join(str(i) for i in instructions)})

    except Exception as e:
        print("Erreur dans calculer_patron() :", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)