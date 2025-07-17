# *******************************************************
# Nom ......... : app.py
# Rôle ........ : Serveur Flask pour le générateur de patrons de tricot
# Auteurs ..... : M, L, M
# Version ..... : V2.0.5 du 10/07/2025
# Licence ..... : Réalisé dans le cadre du cours de Réalisation de Programmes
# Description . : API REST pour calculer un patron de tricot à partir des mesures utilisateur,
#                 traitement des données, calculs personnalisés, génération du résumé du patron.
#
# Technologies  : Python, Flask
# Dépendances . : flask, flask-cors, gunicorn
# Usage ....... : Déploiement sur Render ; endpoint principal : POST /api/calculer-patron
#                 Le frontend est accessible à la racine du site (/).
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
    tricoter,
    joindre,
    separationManchesEtCorps,
    diminutionDebutEtFinDeRang,
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

        # --- Extraction des mesures utilisateur ---
        mailles_10cm = float(data.get('mailles_10cm', 0))
        rangs_10cm = float(data.get('rangs_10cm', 0))
        tour_poitrine = float(data.get('tour_poitrine', 0))
        longueur_totale = float(data.get('longueur_totale', 0))
        largeur_nuque = float(data.get('largeur_nuque', 0))
        hauteur_emmanchure = float(data.get('hauteur_emmanchure', 0))
        longueur_manches = float(data.get('longueur_manches', 0))
        tour_bras = float(data.get('tour_bras', 0))
        tour_poignet = float(data.get('tour_poignet', 0))

        # --- Aisance ---
        mode_aisance_corps = data.get('mode_aisance_corps')
        mode_aisance_manches = data.get('mode_aisance_manches')

        # Table de correspondance pour les aisances prédéfinies
        table_aisance = {
            'pres_corps': -5,
            'ajuste': 0,
            'standard': 5,
            'large': 10,
            'tres_large': 20,
        }

        # Corps
        if mode_aisance_corps == 'personnalise':
            aisance_corps = float(data.get('aisance_corps', 0))
        else:
            aisance_corps = table_aisance.get(mode_aisance_corps, 10)  # 10cm par défaut

        # Manches
        if mode_aisance_manches == 'personnalise':
            aisance_manches = float(data.get('aisance_manches', 0))
        else:
            aisance_manches = table_aisance.get(mode_aisance_manches, 10)

        # --- Création des objets ---
        my_front = Front(tour_poitrine, longueur_totale)
        my_back = Back(largeur_nuque, tour_poitrine, hauteur_emmanchure, longueur_totale)
        my_sleeve = Sleeve(tour_bras, tour_poignet, longueur_manches)
        my_swatch = Swatch(mailles_10cm, rangs_10cm)

        # --- Variables communes ---
        nb_de_mailles_aisselle = 0
        nb_augmentations_dos = 0
        nb_augmentations_manches = 0

        # --- Calcul des mailles au montage ---
        my_back.setNeckStitches(my_back.calculStitchesNeeded(my_swatch.getStitches(), my_back.getNeckWidth(), 0))
        my_sleeve.setTopSleeveStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getTopSleeveWidth(), 0))

        # --- Calcul des mailles avant séparation manches/corps ---
        my_front.setChestStitches(my_front.calculStitchesNeeded(my_swatch.getStitches(), (my_front.getChestWidth() / 2), aisance_corps))
        my_back.setChestStitches(my_back.calculStitchesNeeded(my_swatch.getStitches(), (my_back.getChestWidth() / 2), aisance_corps))
        my_sleeve.setUpperarmStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getUpperArmCircumference(), aisance_manches))

        # --- Calcul des mailles d'aisselle ---
        nb_de_mailles_aisselle = my_back.calculStitchesNeeded(my_swatch.getStitches(), 3, 0)

        # --- Calcul des augmentations ---
        nb_augmentations_dos = math.ceil(
            (my_back.calculIncreases(my_back.getNeckStitches(), my_back.getChestStitches()) - nb_de_mailles_aisselle - 2) / 2
        )
        # Actualisation des mailles après augmentations
        my_back.setChestStitches(my_back.getNeckStitches() + nb_augmentations_dos * 2 + 2 + nb_de_mailles_aisselle)
        my_front.setChestStitches(my_back.getChestStitches())

        nb_augmentations_manches = math.ceil(
            (my_sleeve.calculIncreases(my_sleeve.getTopSleeveStitches(), my_sleeve.getUpperarmStitches()) - nb_de_mailles_aisselle) / 2
        )
        my_sleeve.setUpperarmStitches(my_sleeve.getTopSleeveStitches() + nb_augmentations_manches * 2 + nb_de_mailles_aisselle)

        # --- Calcul du nombre de rangs pour arriver à l'emmanchure ---
        my_back.setRowsToUnderarm(my_back.calculRowsNeeded(my_swatch.getRows(), my_back.getArmholeDepth()))

        # --- Augmentations raglan (mêmes méthodes que knit.py) ---
        my_back.setAugmentationsRaglan(nb_augmentations_dos, my_back.getRowsToUnderarm())
        my_sleeve.setAugmentationsRaglan(nb_augmentations_manches, my_back.getRowsToUnderarm())

        # --- Calcul des rangs à plat (identique knit.py) ---
        rangs_a_plat = 1
        x = my_front.getRightFrontStitches() + my_front.getLeftFrontStitches()
        y = my_back.getNeckStitches()
        while (x <= y):
            if (rangs_a_plat <= ((my_back.getAugmentationsRapides() * my_back.getRythmeRapide()) + 1)):
                if ((rangs_a_plat - 1) % my_back.getRythmeRapide() == 0):
                    x += 4
                    y += 2
                    rangs_a_plat += 1
                else:
                    x += 2
                    rangs_a_plat += 1
            else:
                if ((rangs_a_plat - (my_back.getAugmentationsRapides() * my_back.getRythmeRapide()) - 1) % my_back.getRythmeLent() == 0):
                    x += 4
                    y += 2
                    rangs_a_plat += 1
                else:
                    x += 2
                    rangs_a_plat += 1

        # --- Synchronisation des rangs d’augmentation lent ---
        if my_back.getRythmeLent() == my_sleeve.getRythmeLent():
            synchronisationDesRangs(my_back.getNumeroRangsAugmentationLent(), my_sleeve.getNumeroRangsAugmentationLent())

        # --- Construction des instructions (exact knit.py, mais stockées dans une liste) ---
        instructions = []

        instructions.append(montage(
            my_front.getRightFrontStitches(),
            my_sleeve.getTopSleeveStitches(),
            my_back.getNeckStitches(),
            my_front.getLeftFrontStitches()
        ))
        instructions.append(rangsAplat(rangs_a_plat))

        for rang_en_cours in range(1, my_back.getRowsToUnderarm()):
            if rang_en_cours == rangs_a_plat + 1:
                instructions.append(joindre(rang_en_cours))

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
                instructions.append(tricoter(rang_en_cours))

        instructions.append(
            separationManchesEtCorps(
                rang_en_cours + 1,
                nb_de_mailles_aisselle,
                my_sleeve.getUpperarmStitches(),
                my_back.getChestStitches()
            )
        )

        # --- Corps après séparation ---
        my_back.setRowsToHem(my_back.calculRowsNeeded(my_swatch.getRows(), my_back.getUnderArmToHemLength()))
        instructions.append(
            f"Le corps : \n Rang 1 à {my_back.getRowsToHem()} : tricoter normalement\n"
        )

        # --- Partie manches/diminutions après séparation ---
        my_sleeve.setRowsToWrist(my_sleeve.calculRowsNeeded(my_swatch.getRows(), my_sleeve.getUnderArmToHemLength()))
        my_sleeve.setWristStitches(my_sleeve.calculStitchesNeeded(my_swatch.getStitches(), my_sleeve.getWristCircumference(), 0))

        # Diminutions manches
        nb_diminutions_manches = my_sleeve.calculDecreases(
            my_sleeve.getUpperarmStitches() + nb_de_mailles_aisselle,
            my_sleeve.getWristStitches()
        ) / 2
        ratio_diminution_manche = my_sleeve.calculRatio(my_sleeve.getRowsToWrist(), nb_diminutions_manches)

        instructions.append("La manche :\n")
        instructions.append(diminutionDebutEtFinDeRang(1))
        instructions.append(
            f"Rangs 2-{ratio_diminution_manche} : tricoter le rang normalement.\n"
            f"Répéter les {math.trunc(ratio_diminution_manche)} rangs précédents {nb_diminutions_manches} fois"
        )

        # --- Retourne toutes les instructions ---
        return jsonify({"patron": "\n".join([str(i) for i in instructions])})

    except Exception as e:
        print("Erreur dans calculer_patron() :", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)