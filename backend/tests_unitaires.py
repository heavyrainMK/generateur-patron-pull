import math
import unittest
from io import StringIO
import sys
import contextlib

# Importation des modules du backend
from calculs import Calculs
from back import Back
from front import Front
from sleeve import Sleeve
from swatch import Swatch
from instructions import (
    montage,
    rangsAplat,
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
    synchronisationDesRangs,
)


class CalculsFictifs(Calculs):
    """
    Sous-classe minimale utilisée uniquement pour tester Calculs sans effets secondaires.
    """
    pass


class TestMethodesCalculs(unittest.TestCase):
    def test_calculNombreMailles_pair_et_impair(self):
        """Vérifie que calculStitchesNeeded arrondit à un entier pair si nécessaire."""
        calc = Calculs()
        self.assertEqual(calc.calculStitchesNeeded(10, 5, 0), 6)
        self.assertEqual(calc.calculStitchesNeeded(10, 4, 0), 4)
        self.assertEqual(calc.calculStitchesNeeded(10, 1, 0), 2)
        self.assertEqual(calc.calculStitchesNeeded(10, 4, -1), 4)
        self.assertEqual(calc.calculStitchesNeeded(10, 0, 0), 0)

    def test_calculNombreRangs_basique(self):
        calc = Calculs()
        self.assertEqual(calc.calculRowsNeeded(10, 5), 5)
        self.assertEqual(calc.calculRowsNeeded(9, 5), 5)
        self.assertEqual(calc.calculRowsNeeded(0, 5), 0)
        attendu = math.ceil(10 / 10 * 3.2)
        self.assertEqual(calc.calculRowsNeeded(10, 3.2), attendu)

    def test_calculAugmentations(self):
        calc = Calculs()
        cas = [
            (10, 14, 4),   # différence paire
            (5, 10, 6),    # différence impaire -> +1
            (10, 5, -4),   # différence négative impaire -> +1 (vers zéro) mais ensuite paire négative
            (7, 4, -2),    # différence négative impaire -> -2
        ]
        for nb1, nb2, attendu in cas:
            with self.subTest(nb1=nb1, nb2=nb2):
                self.assertEqual(calc.calculIncreases(nb1, nb2), attendu)

    def test_calculDiminutions(self):
        calc = Calculs()
        cas = [
            (14, 10, 4),   # 14-10 = 4 (pair)
            (10, 5, 4),    # 10-5 = 5 -> 4 après arrondi à l'entier pair inférieur
            (5, 10, -6),   # 5-10 = -5 -> -6 après soustraction de 1 pour obtenir pair
            (7, 4, 2),     # 7-4 = 3 -> 2 après soustraction de 1
            (4, 7, -4),    # 4-7 = -3 -> -4 après soustraction de 1
        ]
        for nb1, nb2, attendu in cas:
            with self.subTest(nb1=nb1, nb2=nb2):
                self.assertEqual(calc.calculDecreases(nb1, nb2), attendu)

    def test_definirAugmentationsRaglan_cas1(self):
        """Quand les augmentations*2 > rangs, le rythme rapide est 1 et le lent est 2."""
        c = CalculsFictifs()
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            c.setAugmentationsRaglan(3, 5)
        self.assertEqual(c.getRythmeRapide(), 1)
        self.assertEqual(c.getRythmeLent(), 2)
        self.assertEqual(c.getAugmentationsRapides(), 2)
        self.assertEqual(c.getAugmentationsLentes(), 1)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [1, 2])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [3])

    def test_definirAugmentationsRaglan_cas2(self):
        """Quand les augmentations*3 > rangs, le rythme rapide est 1 et le lent est 3."""
        c = CalculsFictifs()
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            c.setAugmentationsRaglan(2, 5)
        self.assertEqual(c.getRythmeRapide(), 1)
        self.assertEqual(c.getRythmeLent(), 3)
        self.assertEqual(c.getAugmentationsRapides(), 1)
        self.assertEqual(c.getAugmentationsLentes(), 1)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [1])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [2])

    def test_definirAugmentationsRaglan_cas3(self):
        """Par défaut, utilise les rythmes 2 et 4 pour peu d'augmentations."""
        c = CalculsFictifs()
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            c.setAugmentationsRaglan(1, 10)
        self.assertEqual(c.getRythmeRapide(), 2)
        self.assertEqual(c.getRythmeLent(), 4)
        self.assertEqual(c.getAugmentationsRapides(), 0)
        self.assertEqual(c.getAugmentationsLentes(), 1)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [1])

    def test_definirAugmentationsRaglan_zero_augmentations(self):
        """Aucune augmentation : rythme par défaut mais pas de rangs d'augmentation."""
        c = CalculsFictifs()
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            c.setAugmentationsRaglan(0, 8)
        self.assertEqual(c.getRythmeRapide(), 2)
        self.assertEqual(c.getRythmeLent(), 4)
        self.assertEqual(c.getAugmentationsRapides(), 0)
        self.assertEqual(c.getAugmentationsLentes(), 0)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [])

    def test_calculRatio(self):
        c = Calculs()
        self.assertEqual(c.calculRatio(10, 2), 5)
        self.assertEqual(c.calculRatio(9, 2), 5)

    # --- Cas extrêmes pour les calculs unitaires ---
    def test_calculNombreMailles_négatif(self):
        calc = Calculs()
        # Le comportement dépend de l'implémentation ; on s'assure que cela ne plante pas
        resultat = calc.calculStitchesNeeded(-10, -5, 0)
        self.assertIsInstance(resultat, int)

    def test_calculNombreRangs_négatif(self):
        calc = Calculs()
        resultat = calc.calculRowsNeeded(-10, -5)
        self.assertIsInstance(resultat, int)

    def test_calculNombreMailles_large(self):
        calc = Calculs()
        resultat = calc.calculStitchesNeeded(100000, 10000, 0)
        self.assertIsInstance(resultat, int)

    def test_calculNombreRangs_zéro(self):
        calc = Calculs()
        resultat = calc.calculRowsNeeded(0, 0)
        self.assertEqual(resultat, 0)

    def test_calculAugmentations_grand_négatif(self):
        calc = Calculs()
        resultat = calc.calculIncreases(-1000, 1000)
        self.assertIsInstance(resultat, int)

    def test_calculDiminutions_grand_négatif(self):
        calc = Calculs()
        resultat = calc.calculDecreases(-1000, 1000)
        self.assertIsInstance(resultat, int)


class TestSynchronisation(unittest.TestCase):
    def test_synchronisation_vide(self):
        l1 = []
        l2 = [1, 3, 5]
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            resultat = synchronisationDesRangs(l1, l2)
        self.assertEqual(resultat, [])
        self.assertEqual(l1, [])
        self.assertEqual(l2, [1, 3, 5])

    def test_synchronisation_liste1_plus_courte(self):
        l1 = [1, 5]
        l2 = [2, 4, 6]
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            synchronisationDesRangs(l1, l2)
        self.assertEqual(l1[0], 2)
        self.assertEqual(l1[1], 6)
        self.assertEqual(l2, [2, 4, 6])

    def test_synchronisation_deja_alignee(self):
        l1 = [4, 7]
        l2 = [4, 6, 8]
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            synchronisationDesRangs(l1, l2)
        self.assertEqual(l1, [4, 7])
        self.assertEqual(l2, [4, 6, 8])

    def test_synchronisation_liste2_plus_courte(self):
        l1 = [1, 3, 5]
        l2 = [2, 4]
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            synchronisationDesRangs(l1, l2)
        self.assertEqual(l2[0], 3)
        self.assertEqual(l2[1], 5)
        self.assertEqual(l1, [1, 3, 5])


class TestFormatageInstructions(unittest.TestCase):
    def test_chaines_instructions_de_base(self):
        m = montage(2, 3, 4, 5)
        self.assertTrue(m.startswith("Début : monter 2 m, PM"))
        self.assertIn("3 m", m)
        self.assertIn("4 m", m)
        self.assertIn("5 m", m)
        self.assertIn("(4 augmentations)", augmentationsCorps(3))
        self.assertTrue(augmentationsCorps(1).endswith("\n"))
        self.assertIn("(4 augmentations)", augmentationsManches(2))
        self.assertTrue(augmentationsManches(2).endswith("\n"))
        self.assertIn("(8 augmentations)", augmentationsCorpsEtManches(5))
        self.assertTrue(augmentationsCorpsEtManches(5).endswith("\n"))
        self.assertIn("Tricoter le rang normalement.", tricoterUnRang(4))
        self.assertIn("a", tricoterPlusieursRangs(1, 3))
        aplat = rangsAplat(4)
        self.assertIn("4 rangs", aplat)
        self.assertIn("augmenter d'une maille", aplat.lower())

    def test_chaines_instructions_complexes(self):
        j = joindre(5)
        self.assertIn("Joindre les deux côtés du tricot", j)
        self.assertIn("pointe du V", j)
        s = separationManchesEtCorps(10, 2, 20, 30)
        self.assertIn("Rang 10", s)
        self.assertIn("20 mailles", s)
        d = diminutionDebutEtFinDeRang(1)
        self.assertIn("glisser les 2 mailles", d)
        c_str = cotes(5)
        self.assertIn("Changer d'aiguilles", c_str)
        self.assertIn("5cm", c_str)
        m_str = maillesDencolure(5, 10, 6)
        self.assertIn("relever les mailles de l'encolure", m_str)
        self.assertIn("5 mailles le long de la manche droite", m_str)


class TestAccesseursClasse(unittest.TestCase):
    def test_accesseurs_devant_dos_manche(self):
        f = Front(80, 50)
        self.assertEqual(f.getChestWidth(), 80)
        self.assertEqual(f.getUnderArmToHemLength(), 50)
        f.setChestStitches(100)
        self.assertEqual(f.getChestStitches(), 100)
        f.setRowsToHem(200)
        self.assertEqual(f.getRowsToHem(), 200)
        self.assertEqual(f.getRightFrontStitches(), 2)
        self.assertEqual(f.getLeftFrontStitches(), 2)
        b = Back(20, 80, 25, 55)
        self.assertEqual(b.getNeckWidth(), 20)
        self.assertEqual(b.getChestWidth(), 80)
        self.assertEqual(b.getArmholeDepth(), 25)
        self.assertEqual(b.getUnderArmToHemLength(), 55)
        b.setNeckStitches(10)
        self.assertEqual(b.getNeckStitches(), 10)
        b.setChestStitches(50)
        self.assertEqual(b.getChestStitches(), 50)
        b.setRowsToUnderarm(15)
        self.assertEqual(b.getRowsToUnderarm(), 15)
        b.setRowsToHem(30)
        self.assertEqual(b.getRowsToHem(), 30)
        s = Sleeve(30, 15, 40)
        self.assertEqual(s.getTopSleeveWidth(), 3)
        self.assertEqual(s.getUpperArmCircumference(), 30)
        self.assertEqual(s.getWristCircumference(), 15)
        self.assertEqual(s.getUnderArmToHemLength(), 40)
        s.setTopSleeveStitches(12)
        self.assertEqual(s.getTopSleeveStitches(), 12)
        s.setUpperarmStitches(34)
        self.assertEqual(s.getUpperarmStitches(), 34)
        s.setWristStitches(20)
        self.assertEqual(s.getWristStitches(), 20)
        s.setRowsToWrist(60)
        self.assertEqual(s.getRowsToWrist(), 60)

    def test_impressions_augmentation_depuis_surcharges(self):
        f = StringIO()
        with contextlib.redirect_stdout(f):
            b = Back(20, 80, 25, 55)
            b.setAugmentationsRaglan(1, 4)
        output = f.getvalue()
        self.assertIn("le corps", output)
        f2 = StringIO()
        with contextlib.redirect_stdout(f2):
            s = Sleeve(30, 15, 40)
            s.setAugmentationsRaglan(1, 4)
        output2 = f2.getvalue()
        self.assertIn("la manche", output2)


class TestAPIFlask(unittest.TestCase):
    def setUp(self):
        try:
            from app import app
        except ModuleNotFoundError:
            self.skipTest("Flask n'est pas installé ; tests API ignorés.")
            return
        app.testing = True
        self.client = app.test_client()

    def test_api_succes(self):
        payload = {
            "mailles_10cm": 20,
            "rangs_10cm": 30,
            "tour_poitrine": 80,
            "longueur_totale": 60,
            "largeur_nuque": 20,
            "hauteur_emmanchure": 20,
            "longueur_manches": 50,
            "tour_bras": 30,
            "tour_poignet": 15,
            "mode_aisance_corps": "standard",
            "mode_aisance_manches": "ajuste",
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("patron", data)
        patron = data["patron"]
        self.assertIn("Patron de pull raglan top-down", patron)
        self.assertIn("1. MONTAGE", patron)
        self.assertIn("4. SÉPARATION MANCHES ET CORPS", patron)

    def test_api_pas_de_json(self):
        resp = self.client.post(
            "/api/calculer-patron", data="not json", content_type="text/plain"
        )
        self.assertEqual(resp.status_code, 500)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertTrue(
            "unsupported media type" in data["error"].lower()
            or "not attempt to load json" in data["error"].lower()
        )

    def test_api_valeurs_invalides(self):
        payload = {
            "mailles_10cm": "abc",
            "rangs_10cm": 10,
            "tour_poitrine": 80,
            "longueur_totale": 60,
            "largeur_nuque": 20,
            "hauteur_emmanchure": 20,
            "longueur_manches": 50,
            "tour_bras": 30,
            "tour_poignet": 15,
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)
        self.assertIn("error", data)
        self.assertIn("nombres valides", data["error"].lower())

    def test_api_valeurs_negatives(self):
        payload = {
            "mailles_10cm": -20,
            "rangs_10cm": -30,
            "tour_poitrine": -80,
            "longueur_totale": -60,
            "largeur_nuque": -20,
            "hauteur_emmanchure": -20,
            "longueur_manches": -50,
            "tour_bras": -30,
            "tour_poignet": -15,
            "mode_aisance_corps": "standard",
            "mode_aisance_manches": "ajuste",
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_api_valeurs_nulles(self):
        payload = {
            "mailles_10cm": 0,
            "rangs_10cm": 0,
            "tour_poitrine": 0,
            "longueur_totale": 0,
            "largeur_nuque": 0,
            "hauteur_emmanchure": 0,
            "longueur_manches": 0,
            "tour_bras": 0,
            "tour_poignet": 0,
            "mode_aisance_corps": "standard",
            "mode_aisance_manches": "ajuste",
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_api_champs_manquants(self):
        payload = {
            "tour_poitrine": 80
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_api_valeurs_grandes(self):
        payload = {
            "mailles_10cm": 2000,
            "rangs_10cm": 1000,
            "tour_poitrine": 1500,
            "longueur_totale": 800,
            "largeur_nuque": 200,
            "hauteur_emmanchure": 150,
            "longueur_manches": 600,
            "tour_bras": 400,
            "tour_poignet": 150,
            "mode_aisance_corps": "standard",
            "mode_aisance_manches": "ajuste",
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 200)

    def test_api_mauvais_type(self):
        payload = {
            "mailles_10cm": [20, 30],  # liste au lieu de float
            "rangs_10cm": None,
            "tour_poitrine": "quatre-vingt",
            "longueur_totale": {},
            "largeur_nuque": "20cm",
            "hauteur_emmanchure": "vingt",
            "longueur_manches": [],
            "tour_bras": "trente",
            "tour_poignet": "quinze",
            "mode_aisance_corps": "standard",
            "mode_aisance_manches": "ajuste",
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_api_aisance_personnalisee_sans_valeur(self):
        payload = {
            "mailles_10cm": 20,
            "rangs_10cm": 30,
            "tour_poitrine": 80,
            "longueur_totale": 60,
            "largeur_nuque": 20,
            "hauteur_emmanchure": 20,
            "longueur_manches": 50,
            "tour_bras": 30,
            "tour_poignet": 15,
            "mode_aisance_corps": "personnalise",  # mais pas de "aisance_corps"
            "mode_aisance_manches": "personnalise" # mais pas de "aisance_manches"
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)


class TestCalculsEtendus(unittest.TestCase):
    """Vérifie des cas supplémentaires pour les méthodes de la classe Calculs."""

    def test_calculNombreMailles_négatif_et_zéro(self):
        c = Calculs()
        # Largeur + aisance négatif et impair : le résultat doit être pair
        self.assertEqual(c.calculStitchesNeeded(10, -5, 0), -4)
        # Largeur + aisance négatif et pair : pas d'arrondi supplémentaire
        self.assertEqual(c.calculStitchesNeeded(10, -4, 0), -4)
        # Largeur ou aisance nul : la sortie doit être nulle ou paire
        self.assertEqual(c.calculStitchesNeeded(10, 0, 0), 0)
        # Largeur nulle mais aisance non nulle
        self.assertEqual(c.calculStitchesNeeded(10, 0, 3), 4)

    def test_calculNombreRangs_entrées_négatives(self):
        c = Calculs()
        self.assertEqual(c.calculRowsNeeded(10, -3), -3)
        self.assertEqual(c.calculRowsNeeded(-10, 5), -5)
        self.assertEqual(c.calculRowsNeeded(-10, -5), 5)

    def test_calculAugmentations_zéro_et_pairs(self):
        c = Calculs()
        self.assertEqual(c.calculIncreases(5, 5), 0)
        self.assertEqual(c.calculIncreases(2, 6), 4)
        self.assertEqual(c.calculIncreases(3, 6), 4)
        self.assertEqual(c.calculIncreases(10, 6), -4)
        self.assertEqual(c.calculIncreases(9, 4), -4)

    def test_calculDiminutions_zéro_et_pairs(self):
        c = Calculs()
        self.assertEqual(c.calculDecreases(5, 5), 0)
        self.assertEqual(c.calculDecreases(10, 6), 4)
        self.assertEqual(c.calculDecreases(9, 4), 4)
        self.assertEqual(c.calculDecreases(2, 6), -4)
        self.assertEqual(c.calculDecreases(3, 6), -4)

    def test_definirAugmentationsRaglan_cas_limite(self):
        # Cas où 2*increases == rows -> deuxième branche (rythmes 1 et 3)
        c = CalculsFictifs()
        with contextlib.redirect_stdout(StringIO()):
            c.setAugmentationsRaglan(2, 4)
        self.assertEqual(c.getRythmeRapide(), 1)
        self.assertEqual(c.getRythmeLent(), 3)
        self.assertEqual(c.getAugmentationsRapides(), 2)
        self.assertEqual(c.getAugmentationsLentes(), 0)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [1, 2])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [])

        # Cas où 3*increases == rows -> branche lente (rythmes 2 et 4)
        c2 = CalculsFictifs()
        with contextlib.redirect_stdout(StringIO()):
            c2.setAugmentationsRaglan(2, 6)
        self.assertEqual(c2.getRythmeRapide(), 2)
        self.assertEqual(c2.getRythmeLent(), 4)
        # Avec 2 augmentations réparties sur 6 rangs, les rangs rapides sont 2 et 4
        self.assertEqual(c2.getNumeroRangsAugmentationRapide(), [2, 4])
        # Il n’y a pas d’augmentations lentes dans ce cas
        self.assertEqual(c2.getNumeroRangsAugmentationLent(), [])

    def test_definirAugmentationsRaglan_zéro_rangs_augmentation_zéro(self):
        c = CalculsFictifs()
        with contextlib.redirect_stdout(StringIO()):
            c.setAugmentationsRaglan(0, 0)
        self.assertEqual(c.getRythmeRapide(), 2)
        self.assertEqual(c.getRythmeLent(), 4)
        self.assertEqual(c.getAugmentationsRapides(), 1)
        self.assertTrue(isinstance(c.getAugmentationsLentes(), int))

    def test_calculRatio_cas_limite(self):
        c = Calculs()
        with self.assertRaises(ZeroDivisionError):
            c.calculRatio(10, 0)
        self.assertEqual(c.calculRatio(10, -2), math.ceil(10 / -2))


class TestEchantillonEtVetements(unittest.TestCase):
    """Tests supplémentaires pour les classes Swatch, Front, Back et Manche."""

    def test_accesseurs_et_str_echantillon(self):
        s = Swatch(22, 30)
        self.assertEqual(s.getStitches(), 22)
        self.assertEqual(s.getRows(), 30)
        self.assertIn("22 stitches", str(s))
        self.assertIn("30 rows", str(s))

    def test_repr_devant_et_défauts(self):
        f = Front(80, 50)
        self.assertEqual(f.getRightFrontStitches(), 2)
        self.assertEqual(f.getLeftFrontStitches(), 2)
        rep = str(f)
        self.assertIn("80", rep)
        self.assertIn("50", rep)

    def test_repr_dos(self):
        b = Back(20, 90, 25, 60)
        rep = str(b)
        for val in ["25", "60", "90"]:
            self.assertIn(val, rep)

    def test_repr_manche_et_largeur(self):
        s = Sleeve(28, 14, 42)
        self.assertEqual(s.getTopSleeveWidth(), 3)
        rep = str(s)
        for val in ["28", "14", "42"]:
            self.assertIn(val, rep)


class TestInstructionsEtendues(unittest.TestCase):
    """Vérifie le comportement des fonctions d'instructions avec des valeurs variées."""

    def test_montage_divers(self):
        m = montage(2, 3, 4, 5)
        self.assertTrue(m.startswith("Début : monter 2 m"))
        m2 = montage(-1, 0, -5, 0)
        self.assertIn("-1 m", m2)
        self.assertIn("0 m", m2)

    def test_rangsAplat_zero_et_negatif(self):
        self.assertIn("0 rangs", rangsAplat(0))
        self.assertIn("-3 rangs", rangsAplat(-3))

    def test_fonctions_augmentations_rangs_divers(self):
        a_corps = augmentationsCorps(0)
        self.assertIn("Rang 0", a_corps)
        self.assertTrue(a_corps.endswith("\n"))
        a_manches = augmentationsManches(-1)
        self.assertIn("Rang -1", a_manches)
        a_both = augmentationsCorpsEtManches(5)
        self.assertIn("(8 augmentations)", a_both)

    def test_fonctions_tricotage(self):
        self.assertIn("Rang 5", tricoterUnRang(5))
        multi = tricoterPlusieursRangs(5, 3)
        self.assertIn("Rang 5", multi)
        self.assertIn("3", multi)
        self.assertTrue(multi.endswith("\n"))

    def test_instructions_complexes(self):
        j = joindre(1)
        self.assertIn("Joindre les deux côtés", j)
        self.assertIn("pointe du V", j)
        s = separationManchesEtCorps(-1, 0, 0, 0)
        self.assertIn("Rang -1", s)
        self.assertIn("0 mailles", s)
        d = diminutionDebutEtFinDeRang(2)
        self.assertIn("Rang 2", d)
        c = cotes(-5)
        self.assertIn("-5cm", c)
        m_enc = maillesDencolure(5, 10, 6)
        self.assertIn("4 mailles de chaque cote", m_enc.lower())


class TestSynchronisationEtendue(unittest.TestCase):
    """Couvre des scénarios supplémentaires pour la synchronisation des rangs."""

    def test_deux_listes_vides(self):
        l1, l2 = [], []
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            resultat = synchronisationDesRangs(l1, l2)
        self.assertEqual(resultat, [])
        self.assertEqual(l1, [])
        self.assertEqual(l2, [])

    def test_deuxieme_vide_premiere_non_vide(self):
        l1 = [1, 2]
        l2 = []
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            resultat = synchronisationDesRangs(l1, l2)
        self.assertEqual(resultat, [])
        self.assertEqual(l1, [1, 2])
        self.assertEqual(l2, [])

    def test_longueurs_egales_mal_alignees(self):
        l1 = [1, 4]
        l2 = [2, 5]
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            synchronisationDesRangs(l1, l2)
        self.assertEqual(l2[0], 4)
        self.assertEqual(l2[1], 7)
        self.assertEqual(l1, [1, 4])

    def test_listes_avec_valeurs_negatives(self):
        l1 = [-3, -1]
        l2 = [-2, 2]
        tampon = StringIO()
        with contextlib.redirect_stdout(tampon):
            synchronisationDesRangs(l1, l2)
        self.assertIn(l2[0], l1)
        self.assertEqual(l2[1] - l2[0], 4)


class TestAPIFlaskEtendu(unittest.TestCase):
    """Teste des scénarios supplémentaires pour l'API Flask."""

    def setUp(self):
        try:
            from app import app
        except ModuleNotFoundError:
            self.skipTest("Flask n'est pas installé ; tests API ignorés.")
            return
        app.testing = True
        self.client = app.test_client()

    def test_api_personnalise_valide(self):
        payload = {
            "mailles_10cm": 20,
            "rangs_10cm": 30,
            "tour_poitrine": 80,
            "longueur_totale": 60,
            "largeur_nuque": 20,
            "hauteur_emmanchure": 20,
            "longueur_manches": 50,
            "tour_bras": 30,
            "tour_poignet": 15,
            "mode_aisance_corps": "personnalise",
            "mode_aisance_manches": "personnalise",
            "aisance_corps": 8,
            "aisance_manches": 4,
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("Patron de pull raglan", data.get("patron", ""))

    def test_api_personnalise_valeur_manquante(self):
        payload = {
            "mailles_10cm": 20,
            "rangs_10cm": 30,
            "tour_poitrine": 80,
            "longueur_totale": 60,
            "largeur_nuque": 20,
            "hauteur_emmanchure": 20,
            "longueur_manches": 50,
            "tour_bras": 30,
            "tour_poignet": 15,
            "mode_aisance_corps": "personnalise",
            "mode_aisance_manches": "personnalise",
            "aisance_corps": "",
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_api_mode_aisance_inconnu(self):
        payload = {
            "mailles_10cm": 20,
            "rangs_10cm": 30,
            "tour_poitrine": 80,
            "longueur_totale": 60,
            "largeur_nuque": 20,
            "hauteur_emmanchure": 20,
            "longueur_manches": 50,
            "tour_bras": 30,
            "tour_poignet": 15,
            "mode_aisance_corps": "super_large",
            "mode_aisance_manches": "extra",
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("Patron de pull raglan", data.get("patron", ""))

    def test_api_cotes_invalides_negatives(self):
        payload = {
            "mailles_10cm": 20,
            "rangs_10cm": 30,
            "tour_poitrine": 80,
            "longueur_totale": 60,
            "largeur_nuque": 20,
            "hauteur_emmanchure": 20,
            "longueur_manches": 50,
            "tour_bras": 30,
            "tour_poignet": 15,
            "mode_aisance_corps": "standard",
            "mode_aisance_manches": "standard",
            "cotes_bas": -5,
            "cotes_poignets": -2,
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("Patron de pull raglan", data.get("patron", ""))


if __name__ == "__main__":
    unittest.main()