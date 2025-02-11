from django.core.management.base import BaseCommand
from automatisation.models import CanalUSSD, UseCase, TestResult
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Initialise les données de test pour l\'application'

    def handle(self, *args, **kwargs):
        # Créer les canaux USSD
        canaux = [
            "#144#",
            "#237#",
            "#1413#",
            "#111#",
            "#148#",
            "#605#",
            "#336#",
            "#1441#"
        ]

        for code in canaux:
            canal, created = CanalUSSD.objects.get_or_create(
                code=code,
                defaults={'description': f'Canal {code}'}
            )
            self.stdout.write(f'Canal {code} {"créé" if created else "existant"}')

            # Créer des use cases pour chaque canal
            use_cases_data = [
                {
                    'nom': f'Consultation solde {code}',
                    'description': 'Consultation du solde',
                    'entree': '1',
                    'sortie_attendue': 'Votre solde est de',
                },
                {
                    'nom': f'Transfert argent {code}',
                    'description': 'Transfert d\'argent',
                    'entree': '2',
                    'sortie_attendue': 'Transfert effectué avec succès',
                },
                {
                    'nom': f'Achat forfait {code}',
                    'description': 'Achat de forfait',
                    'entree': '3',
                    'sortie_attendue': 'Forfait activé avec succès',
                }
            ]

            for uc_data in use_cases_data:
                use_case, created = UseCase.objects.get_or_create(
                    canal=canal,
                    nom=uc_data['nom'],
                    defaults={
                        'description': uc_data['description'],
                        'entree': uc_data['entree'],
                        'sortie_attendue': uc_data['sortie_attendue']
                    }
                )
                self.stdout.write(f'Use case {uc_data["nom"]} {"créé" if created else "existant"}')

                # Créer des résultats de test pour les 7 derniers jours
                end_date = datetime.now()
                start_date = end_date - timedelta(days=7)
                current_date = start_date

                while current_date <= end_date:
                    # 80% de chance d'avoir un test OK
                    status = "OK" if random.random() < 0.8 else "NOK"
                    error_message = None if status == "OK" else "Erreur de connexion"

                    TestResult.objects.create(
                        use_case=use_case,
                        statut=status,
                        message_erreur=error_message,
                        date_test=current_date
                    )

                    current_date += timedelta(hours=random.randint(1, 8))

        self.stdout.write(self.style.SUCCESS('Données de test initialisées avec succès'))
