# *******************************************************
# Nom ......... : app.py
# Rôle ........ : Serveur Flask pour le générateur de patrons de tricot
# Auteurs ..... : M, L, M
# Version ..... : V2.0.4 du 01/07/2025
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
from instructions import montage, rangsAplat, synchronisationDesRangs

app = Flask(__name__)
CORS(app)

@app.route('/api/calculer-patron', methods=['POST'])
def calculer_patron():
    try:
        data = request.get_json()
        print("✅ Données reçues :", data)

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
            'tres_ajuste': -2.5,
            'ajuste': 7.5,
            'standard': 17.5,
            'large': 27.5,
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

        # --- Création des objets comme dans knit.py ---
        swatch = Swatch(mailles_10cm, rangs_10cm)
        my_front = Front(tour_poitrine, longueur_totale)
        my_back = Back(largeur_nuque, tour_poitrine, hauteur_emmanchure, longueur_totale)
        my_sleeve = Sleeve(tour_bras, tour_poignet, longueur_manches)

        # --- Calculs identiques à knit.py ---
        my_back.setNeckStitches(my_back.calculStitchesNeeded(swatch.getStitches(), my_back.getNeckWidth(), 0))
        my_sleeve.setTopSleeveStitches(my_sleeve.calculStitchesNeeded(swatch.getStitches(), my_sleeve.getTopSleeveWidth(), 0))

        # Instructions de montage
        debut = montage(
            my_front.getRightFrontStitches(),
            my_sleeve.getTopSleeveStitches(),
            my_back.getNeckStitches(),
            my_front.getLeftFrontStitches()
        )

        # Calcul des mailles d'aisselle
        nb_de_mailles_aisselle = my_back.calculStitchesNeeded(swatch.getStitches(), 3, 0)

        # Calcul des mailles avant séparation des manches et du corps (avec aisance)
        my_front.setChestStitches(my_front.calculStitchesNeeded(swatch.getStitches(), (my_front.getChestWidth() / 2), aisance_corps))
        my_back.setChestStitches(my_back.calculStitchesNeeded(swatch.getStitches(), (my_back.getChestWidth() / 2), aisance_corps))
        my_sleeve.setUpperarmStitches(my_sleeve.calculStitchesNeeded(swatch.getStitches(), my_sleeve.getUpperArmCircumference(), aisance_manches))

        # Calcul des augmentations nécessaires
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

        # Calcul du nombre de rangs pour arriver jusqu'à l'emmanchure
        my_back.setRowsToUnderarm(my_back.calculRowsNeeded(swatch.getRows(), my_back.getArmholeDepth()))

        # Raglan
        if hasattr(my_back, "setAugmentationsRaglan"):
            my_back.setAugmentationsRaglan(nb_augmentations_dos, my_back.getRowsToUnderarm())
        if hasattr(my_sleeve, "setAugmentationsRaglan"):
            my_sleeve.setAugmentationsRaglan(nb_augmentations_manches, my_back.getRowsToUnderarm())

        # --- Calcul "tricot à plat" (identique knit.py) ---
        rangs_a_plat = 1
        try:
            x = my_front.getRightFrontStitches() + my_front.getLeftFrontStitches()
            y = my_back.getNeckStitches() + 2
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
            texte_rangs_plat = (
                f"Il faut tricoter à plat sur {rangs_a_plat} rangs.\n"
                f"Nombre d'augmentations rapides : {my_back.getAugmentationsRapides()} tous les {my_back.getRythmeRapide()} rangs, "
                f"nombre d'augmentations lentes : {my_back.getAugmentationsLentes()} tous les {my_back.getRythmeLent()} rangs.\n"
            )
        except Exception as e:
            texte_rangs_plat = "Erreur dans le calcul des rangs à plat : " + str(e) + "\n"

        # --- Mise à jour des rangs d'augmentations lentes ---
        try:
            liste_modifiee = synchronisationDesRangs(
                my_back.GetNumeroRangsAugmentationLent(),
                my_sleeve.GetNumeroRangsAugmentationLent()
            )
            texte_liste_modifiee = f"Liste des rangs d’augmentations lentes (ajustée) : {liste_modifiee}\n"
        except Exception as e:
            texte_liste_modifiee = f"Erreur lors du calcul de la liste modifiée des rangs : {e}\n"

        # --- Résumé final + instructions ---
        patron = ""
        patron += debut
        patron += texte_rangs_plat
        patron += texte_liste_modifiee
        patron += (
            f"Aisance corps : {aisance_corps} cm | Aisance manches : {aisance_manches} cm\n"
            f"Montage dos : {my_back.getNeckStitches()} mailles\n"
            f"Montage manches : {my_sleeve.getTopSleeveStitches()} mailles\n"
            f"Après augmentations, dos : {my_back.getChestStitches()} mailles | manches : {my_sleeve.getUpperarmStitches()} mailles\n"
            f"Nombre de rangs avant aisselle : {my_back.getRowsToUnderarm()}\n"
            f"Augmentations raglan dos : {getattr(my_back, 'augmentations_raglan', 'N/A')}\n"
            f"Augmentations raglan manches : {getattr(my_sleeve, 'augmentations_raglan', 'N/A')}\n"
        )

        return jsonify({"patron": patron})

    except Exception as e:
        print("❌ Erreur dans calculer_patron() :", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)