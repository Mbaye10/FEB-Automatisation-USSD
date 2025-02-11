import pandas as pd
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import TestResult, DetailedTestResult, UseCase

def get_dashboard_stats(start_date=None, end_date=None, canal=None):
    """Récupère les statistiques pour le dashboard"""
    queryset = TestResult.objects.all()
    
    if start_date and end_date:
        queryset = queryset.filter(date_test__range=[start_date, end_date])
    
    if canal:
        queryset = queryset.filter(use_case__canal=canal)
    
    total_tests = queryset.count()
    tests_ok = queryset.filter(statut='OK').count()
    tests_nok = queryset.filter(statut='NOK').count()
    
    taux_dysfonctionnement = (tests_nok / total_tests * 100) if total_tests > 0 else 0
    
    return {
        'total_tests': total_tests,
        'tests_ok': tests_ok,
        'tests_nok': tests_nok,
        'taux_dysfonctionnement': round(taux_dysfonctionnement, 2)
    }

def get_failed_tests_details(start_date=None, end_date=None, canal=None):
    """Récupère les détails des tests en échec"""
    queryset = DetailedTestResult.objects.filter(statut='NOK')
    
    if start_date and end_date:
        queryset = queryset.filter(date_heure__range=[start_date, end_date])
    
    if canal:
        queryset = queryset.filter(test_result__use_case__canal=canal)
    
    return queryset

def export_to_excel(queryset):
    """Exporte les résultats de test vers Excel"""
    data = []
    for result in queryset:
        data.append({
            'Numéro de téléphone': result.numero_telephone,
            'Canal': result.test_result.use_case.canal.code,
            'Use Case': result.test_result.use_case.nom,
            'Étape': result.step.step_number,
            'Date et heure': result.date_heure,
            'Message d\'erreur': result.message_erreur
        })
    
    df = pd.DataFrame(data)
    return df
