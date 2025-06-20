from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import math
import traceback

from backend.swatch import Swatch
from backend.back import Back
from backend.front import Front
from backend.sleeve import Sleeve

app = Flask(__name__)
CORS(app)  # Autorise les requêtes depuis le frontend


@app.route('/api/calculer-patron', methods=['POST'])
def calculer_patron():
    try:
        data = request.json
        print("✅ Données reçues :", data)

        # Extraction des données
        mode_aisance = data.get('mode_aisance')
        aisance = float(data['aisance']) if 'aisance' in data and data['aisance'] else None

        mailles_10cm = float(data['mailles_10cm'])
        rangs_10cm = float(data['rangs_10cm'])
        taille_aig_corps = float(data['taille_aig_corps'])
        taille_aig_cotes = float(data['taille_aig_cotes'])

        tour_cou = float(data['tour_cou'])
        tour_poitrine = float(data['tour_poitrine'])
        largeur_nuque = float(data['largeur_nuque'])
        hauteur_emmanchure = float(data['hauteur_emmanchure'])
        longueur_totale = float(data['longueur_totale'])

        tour_taille = float(data['tour_taille']) if data.get('tour_taille') else None
        hauteur_nuque_taille = float(data['hauteur_nuque_taille']) if data.get('hauteur_nuque_taille') else None
        tour_hanches = float(data['tour_hanches']) if data.get('tour_hanches') else None

        longueur_manches = float(data['longueur_manches'])
        tour_bras = float(data['tour_bras'])
        tour_poignet = float(data['tour_poignet'])
        tour_coude = float(data['tour_coude']) if data.get('tour_coude') else None

        appliquer_aisance = data.get('appliquer_aisance')
        encolure = data.get('encolure')
        cotes_bas = float(data['cotes_bas'])
        cotes_poignets = float(data['cotes_poignets'])

        # Application de l’aisance
        if mode_aisance == "personnalise":
            aisance_corps = aisance if appliquer_aisance in ["corps_seulement", "corps_et_manches"] else 0
            aisance_manches = aisance if appliquer_aisance == "corps_et_manches" else 0
        elif mode_aisance == "tres_ajuste":
            aisance_corps = -2.5 if appliquer_aisance in ["corps_seulement", "corps_et_manches"] else 0
            aisance_manches = -2.5 if appliquer_aisance == "corps_et_manches" else 0
        elif mode_aisance == "ajuste":
            aisance_corps = 7.5 if appliquer_aisance in ["corps_seulement", "corps_et_manches"] else 0
            aisance_manches = 7.5 if appliquer_aisance == "corps_et_manches" else 0
        elif mode_aisance == "standard":
            aisance_corps = 17.5 if appliquer_aisance in ["corps_seulement", "corps_et_manches"] else 0
            aisance_manches = 17.5 if appliquer_aisance == "corps_et_manches" else 0
        elif mode_aisance == "large":
            aisance_corps = 27.5 if appliquer_aisance in ["corps_seulement", "corps_et_manches"] else 0
            aisance_manches = 27.5 if appliquer_aisance == "corps_et_manches" else 0
        else:
            aisance_corps = 10
            aisance_manches = 0

        # Création des objets
        swatch = Swatch(mailles_10cm, rangs_10cm)
        my_back = Back(largeur_nuque, tour_poitrine, hauteur_emmanchure, longueur_totale)
        my_front = Front(tour_poitrine, longueur_totale)
        my_sleeve = Sleeve(tour_bras, tour_poignet, longueur_manches)

        # Calculs
        nb_de_mailles_aisselle = my_back.calculStitchesNeeded(swatch.getStitches(), 3, 0)

        my_back.setNeckStitches(my_back.calculStitchesNeeded(swatch.getStitches(), my_back.getNeckWidth(), 0))
        my_sleeve.setTopSleeveStitches(my_sleeve.calculStitchesNeeded(swatch.getStitches(), my_sleeve.getTopSleeveWidth(), 0))

        my_front.setChestStitches(my_front.calculStitchesNeeded(swatch.getStitches(), (my_front.getChestWidth() / 2), aisance_corps))
        my_back.setChestStitches(my_back.calculStitchesNeeded(swatch.getStitches(), (my_back.getChestWidth() / 2), aisance_corps))
        my_sleeve.setUpperarmStitches(my_sleeve.calculStitchesNeeded(swatch.getStitches(), my_sleeve.getUpperArmCircumference(), aisance_manches))

        nb_augmentations_dos = math.ceil((my_back.calculIncreases(my_back.getNeckStitches(), my_back.getChestStitches()) - nb_de_mailles_aisselle - 2) / 2)
        my_back.setChestStitches(my_back.getNeckStitches() + nb_augmentations_dos * 2 + 2 + nb_de_mailles_aisselle)
        my_front.setChestStitches(my_back.getChestStitches())
        nb_augmentations_manches = math.ceil((my_sleeve.calculIncreases(my_sleeve.getTopSleeveStitches(), my_sleeve.getUpperarmStitches()) - nb_de_mailles_aisselle)  / 2)
        my_sleeve.setUpperarmStitches(my_sleeve.getTopSleeveStitches() + nb_augmentations_manches * 2 + nb_de_mailles_aisselle)

        my_back.setRowsToUnderarm(my_back.calculRowsNeeded(swatch.getRows(), my_back.getArmholeDepth()))
        my_back.augmentationsRaglan(nb_augmentations_dos, my_back.getRowsToUnderarm())
        my_sleeve.augmentationsRaglan(nb_augmentations_manches, my_back.getRowsToUnderarm())

        # Patron résumé
        patron = ""
        patron += f"Dos : {my_back}\n"
        patron += f"Devant : {my_front}\n"
        patron += f"Manches : {my_sleeve}\n"
        patron += f"Aisance corps : {aisance_corps} cm | Aisance manches : {aisance_manches} cm\n"
        patron += f"Montage dos : {my_back.getNeckStitches()} mailles\n"
        patron += f"Montage manches : {my_sleeve.getTopSleeveStitches()} mailles\n"
        patron += f"Après augmentations, dos : {my_back.getChestStitches()} mailles | manches : {my_sleeve.getUpperarmStitches()} mailles\n"
        patron += f"Nombre de rangs avant aisselle : {my_back.getRowsToUnderarm()}\n"
        patron += f"Augmentations raglan dos : {my_back.augmentations_raglan}\n"
        patron += f"Augmentations raglan manches : {my_sleeve.augmentations_raglan}\n"

        return jsonify({"patron": patron})

    except Exception as e:
        print("❌ Erreur dans calculer_patron() :", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('../frontend', path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render fournit le port via la variable d'environnement PORT
    app.run(host="0.0.0.0", port=port)