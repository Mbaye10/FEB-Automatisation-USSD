# tests.py
from django.test import TestCase
from .automatisation_tests import simuler_parcours_ussd
from .models import CanalUSSD

class SimulateurTests(TestCase):
    def test_simuler_parcours_ussd(self):
        # Récupérer les codes USSD depuis la base de données
        codes_ussd = CanalUSSD.objects.values_list('code', flat=True)

        # Itérer sur chaque code USSD
        for code in codes_ussd:
            print(f"\nTest du code USSD : {code}")
            resultats = simuler_parcours_ussd(code)
            
            if resultats:
                for resultat in resultats:
                    print(f"Étape {resultat['numerousecase']} - {resultat['nom']}: {resultat['statut']}")
                    # Vérifier que le statut est OK
                    self.assertEqual(resultat['statut'], 'OK')
            else:
                print(f"Code USSD {code} non trouvé.")
                self.fail(f"Code USSD {code} non trouvé.")