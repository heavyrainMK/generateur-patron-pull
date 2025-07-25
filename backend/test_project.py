import math
import unittest
from io import StringIO
import sys
import contextlib

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

class DummyCalculs(Calculs):
    """
    Sous-classe minimale utilisée uniquement pour tester Calculs sans effets secondaires.
    """
    pass

class TestCalculsMethods(unittest.TestCase):
    def test_calculStitchesNeeded_even_and_odd(self):
        """Vérifie que calculStitchesNeeded arrondit à un entier pair si nécessaire."""
        calc = Calculs()
        self.assertEqual(calc.calculStitchesNeeded(10, 5, 0), 6)
        self.assertEqual(calc.calculStitchesNeeded(10, 4, 0), 4)
        self.assertEqual(calc.calculStitchesNeeded(10, 1, 0), 2)
        self.assertEqual(calc.calculStitchesNeeded(10, 4, -1), 4)
        self.assertEqual(calc.calculStitchesNeeded(10, 0, 0), 0)

    def test_calculRowsNeeded_basic(self):
        calc = Calculs()
        self.assertEqual(calc.calculRowsNeeded(10, 5), 5)
        self.assertEqual(calc.calculRowsNeeded(9, 5), 5)
        self.assertEqual(calc.calculRowsNeeded(0, 5), 0)
        expected = math.ceil(10 / 10 * 3.2)
        self.assertEqual(calc.calculRowsNeeded(10, 3.2), expected)

    def test_calculIncreases(self):
        calc = Calculs()
        cases = [
            (10, 14, 4),   # différence paire
            (5, 10, 6),    # différence impaire -> +1
            (10, 5, -4),   # différence négative impaire -> +1 (vers zéro) mais ensuite paire négative
            (7, 4, -2),    # différence négative impaire -> -2
        ]
        for nb1, nb2, expected in cases:
            with self.subTest(nb1=nb1, nb2=nb2):
                self.assertEqual(calc.calculIncreases(nb1, nb2), expected)

    def test_calculDecreases(self):
        calc = Calculs()
        cases = [
            (14, 10, 4),   # 14-10 = 4 (pair)
            (10, 5, 4),    # 10-5 = 5 -> 4 après arrondi à l'entier pair inférieur
            (5, 10, -6),   # 5-10 = -5 -> -6 après soustraction de 1 pour obtenir pair
            (7, 4, 2),     # 7-4 = 3 -> 2 après soustraction de 1
            (4, 7, -4),    # 4-7 = -3 -> -4 après soustraction de 1
        ]
        for nb1, nb2, expected in cases:
            with self.subTest(nb1=nb1, nb2=nb2):
                self.assertEqual(calc.calculDecreases(nb1, nb2), expected)

    def test_setAugmentationsRaglan_case1(self):
        """Quand les augmentations*2 > rangs, le rythme rapide est 1 et le lent est 2."""
        c = DummyCalculs()
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            c.setAugmentationsRaglan(3, 5)
        self.assertEqual(c.getRythmeRapide(), 1)
        self.assertEqual(c.getRythmeLent(), 2)
        self.assertEqual(c.getAugmentationsRapides(), 2)
        self.assertEqual(c.getAugmentationsLentes(), 1)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [1, 2])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [3])

    def test_setAugmentationsRaglan_case2(self):
        """Quand les augmentations*3 > rangs, le rythme rapide est 1 et le lent est 3."""
        c = DummyCalculs()
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            c.setAugmentationsRaglan(2, 5)
        self.assertEqual(c.getRythmeRapide(), 1)
        self.assertEqual(c.getRythmeLent(), 3)
        self.assertEqual(c.getAugmentationsRapides(), 1)
        self.assertEqual(c.getAugmentationsLentes(), 1)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [1])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [2])

    def test_setAugmentationsRaglan_case3(self):
        """Par défaut, utilise les rythmes 2 et 4 pour peu d'augmentations."""
        c = DummyCalculs()
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            c.setAugmentationsRaglan(1, 10)
        self.assertEqual(c.getRythmeRapide(), 2)
        self.assertEqual(c.getRythmeLent(), 4)
        self.assertEqual(c.getAugmentationsRapides(), 0)
        self.assertEqual(c.getAugmentationsLentes(), 1)
        self.assertEqual(c.getNumeroRangsAugmentationRapide(), [])
        self.assertEqual(c.getNumeroRangsAugmentationLent(), [1])

    def test_setAugmentationsRaglan_zero_increases(self):
        """Aucune augmentation : rythme par défaut mais pas de rangs d'augmentation."""
        c = DummyCalculs()
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
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
    def test_calculStitchesNeeded_negative(self):
        calc = Calculs()
        # Le comportement dépend de l'implémentation, on s'assure que ça ne crashe pas
        result = calc.calculStitchesNeeded(-10, -5, 0)
        self.assertIsInstance(result, int)

    def test_calculRowsNeeded_negative(self):
        calc = Calculs()
        result = calc.calculRowsNeeded(-10, -5)
        self.assertIsInstance(result, int)

    def test_calculStitchesNeeded_large(self):
        calc = Calculs()
        result = calc.calculStitchesNeeded(100000, 10000, 0)
        self.assertIsInstance(result, int)

    def test_calculRowsNeeded_zero(self):
        calc = Calculs()
        result = calc.calculRowsNeeded(0, 0)
        self.assertEqual(result, 0)

    def test_calculIncreases_large_negative(self):
        calc = Calculs()
        result = calc.calculIncreases(-1000, 1000)
        self.assertIsInstance(result, int)

    def test_calculDecreases_large_negative(self):
        calc = Calculs()
        result = calc.calculDecreases(-1000, 1000)
        self.assertIsInstance(result, int)


class TestSynchronisation(unittest.TestCase):
    def test_synchronisation_empty(self):
        l1 = []
        l2 = [1, 3, 5]
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            result = synchronisationDesRangs(l1, l2)
        self.assertEqual(result, [])
        self.assertEqual(l1, [])
        self.assertEqual(l2, [1, 3, 5])

    def test_synchronisation_list1_shorter(self):
        l1 = [1, 5]
        l2 = [2, 4, 6]
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            synchronisationDesRangs(l1, l2)
        self.assertEqual(l1[0], 2)
        self.assertEqual(l1[1], 6)
        self.assertEqual(l2, [2, 4, 6])

    def test_synchronisation_already_aligned(self):
        l1 = [4, 7]
        l2 = [4, 6, 8]
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            synchronisationDesRangs(l1, l2)
        self.assertEqual(l1, [4, 7])
        self.assertEqual(l2, [4, 6, 8])

    def test_synchronisation_list2_shorter(self):
        l1 = [1, 3, 5]
        l2 = [2, 4]
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            synchronisationDesRangs(l1, l2)
        self.assertEqual(l2[0], 3)
        self.assertEqual(l2[1], 5)
        self.assertEqual(l1, [1, 3, 5])


class TestInstructionsFormatting(unittest.TestCase):
    def test_basic_instruction_strings(self):
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

    def test_complex_instruction_strings(self):
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


class TestClassAccessors(unittest.TestCase):
    def test_front_back_sleeve_accessors(self):
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

    def test_augmentation_prints_from_overrides(self):
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


class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        try:
            from app import app
        except ModuleNotFoundError:
            self.skipTest("Flask n'est pas installé ; tests API ignorés.")
            return
        app.testing = True
        self.client = app.test_client()

    def test_api_success(self):
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

    def test_api_no_json(self):
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

    def test_api_invalid_values(self):
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

    def test_api_negative_values(self):
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

    def test_api_zero_values(self):
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

    def test_api_missing_fields(self):
        payload = {
            "tour_poitrine": 80
        }
        resp = self.client.post("/api/calculer-patron", json=payload)
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_api_large_values(self):
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

    def test_api_wrong_type(self):
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

    def test_api_aisance_personnalisee_without_value(self):
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

if __name__ == "__main__":
    unittest.main()