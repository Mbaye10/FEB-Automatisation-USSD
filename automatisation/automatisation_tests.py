from django.utils import timezone
from .models import CanalUSSD, UseCase, TestResult

def simulate_ussd_menu(canal_codes):
    """
    Simule les menus USSD pour une liste de codes de canaux.
    :param canal_codes: Une liste de codes de canaux (exemple : ["#144#", "#237#"])
    :return: Un dictionnaire contenant les résultats de la simulation pour chaque canal.
    """
    results = {}
    
    for canal_code in canal_codes:
        try:
            # Récupérer le canal USSD
            canal = CanalUSSD.objects.get(code=canal_code)
            
            # Récupérer tous les use cases pour ce canal
            use_cases = UseCase.objects.filter(canal=canal)
            
            # Simuler les interactions
            canal_results = []
            for use_case in use_cases:
                # Simuler une interaction (ici, on suppose que tout est OK)
                status = "OK"  # Par défaut, le test est OK
                error_message = None  # Aucun message d'erreur par défaut
                
                # Vérifier si la sortie attendue correspond à une sortie simulée
                # (Ici, vous pouvez ajouter une logique de validation réelle)
                if "erreur" in use_case.sortie_attendue.lower():
                    status = "NOK"
                    error_message = "Erreur détectée dans la sortie attendue."
                
                # Enregistrer le résultat du test dans la base de données
                test_result = TestResult.objects.create(
                    use_case=use_case,
                    statut=status,
                    message_erreur=error_message
                )
                
                # Ajouter le résultat à la liste
                canal_results.append({
                    'numero': use_case.canal.code,  # ND concerné
                    'code': use_case.canal.code,  # Canal concerné
                    'use_case': use_case.nom,  # Use case concerné
                    'etape': use_case.entree,  # Étape concernée
                    'date_test': test_result.date_test,  # Date et heure d’échec
                    'message_erreur': error_message,  # Message d’erreur
                })
            
            # Ajouter les résultats pour ce canal
            results[canal_code] = {
                'canal': canal.code,
                'results': canal_results,
            }
        
        except CanalUSSD.DoesNotExist:
            results[canal_code] = {
                'error': f"Canal USSD '{canal_code}' non trouvé."
            }
    
    return results