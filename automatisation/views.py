from django.http import HttpResponse
from django.shortcuts import redirect, render
import pandas as pd
from .automatisation_tests import simulate_ussd_menu
from .models import CanalUSSD, UseCase, TestResult, AlertConfiguration, DetailedTestResult
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .utils import get_dashboard_stats, get_failed_tests_details, export_to_excel
from django.db.models import Count
from django.db.models.functions import TruncDate
import json
from datetime import datetime, timedelta

def index(request):
    try:
        # Chemins des fichiers
        chemin_dossier = 'C:/Users/stg_sall86922/Desktop/Automatisationtests/Export-USSD'
        fichiers_excel1 = f"{chemin_dossier}/DonneesExporter.xlsx"
        fichiers_excel2 = f"{chemin_dossier}/DonneesSimule1.xlsx"
        fichiers_excel3 = f"{chemin_dossier}/DonneesSimule2.xlsx"

        # Lire les fichiers
        dataExpo = pd.read_excel(fichiers_excel1)
        datasimu1 = pd.read_excel(fichiers_excel2)
        datasimu2 = pd.read_excel(fichiers_excel3)

        # Récupérer le canal sélectionné depuis le formulaire
        canal_selectionne = request.GET.get('code', None)
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        # Filtrage des données si un canal est sélectionné
        if canal_selectionne:
            dataExpo_filtre = dataExpo[dataExpo['CODE'] == canal_selectionne]
        else:
            dataExpo_filtre = dataExpo

        # Filtrage par date si une date est sélectionnée
        if start_date and end_date:
            dataExpo_filtre = dataExpo_filtre[(dataExpo_filtre['DATE'] >= start_date) & (dataExpo_filtre['DATE'] <= end_date)]

        nombre_tests = len(dataExpo_filtre)
        nombre_echecs = 0
        use_cases_en_echec = []

        # Parcourir les données pour calculer les échecs
        for index, row in dataExpo_filtre.iterrows():
            numero = row['NUMCLI']
            code = row['CODE']

            # Filtrage des données dans les autres fichiers
            resultat2 = datasimu2[(datasimu2['Numero'] == numero) & (datasimu2['Canal'] == code)]

            # Vérification des erreurs dans les commentaires de datasimu2
            commentaires = resultat2['Commentaire'].values
            use_cases = resultat2['Usecaseconcerne'].values

            if any('Erreur' in str(comment) for comment in commentaires):
                nombre_echecs += 1
                for use_case in use_cases:
                    use_cases_en_echec.append({
                        'use_case': use_case,
                        'numero': numero,
                        'code': code,
                    })

        # Calcul du taux de défaut
        tauxdefaut = (nombre_echecs / nombre_tests) * 100 if nombre_tests > 0 else 0

        # Simuler les canaux USSD
        canal_codes = ["#144#", "#237#", "#1413#", "#111#", "#148#", "#605#", "#336#", "#1441#"]  # Liste des codes USSD
        simulation_results = simulate_ussd_menu(canal_codes)
        #nombre_testsP=0
       # nombre_tests_ok=0
        #nombre_tests_NOK=0

        #for canal_code, canal_data in simulation_results.items():
            #if not canal_data.get('error'):
                #nombre_testsP += len(canal_data['results'])
                #for result in canal_data['results']:
                    #if result['statut'] == "OK":
                       # nombre_tests_ok += 1
                    #else:
                        #nombre_tests_NOK += 1

            #taux_dysfonctionnement = (nombre_tests_NOK / nombre_testsP) * 100 if nombre_testsP >0 else 0





        # Préparer les colonnes et le contexte
        table_columns = datasimu2.columns
        valeurs_canal = dataExpo['CODE'].unique()

        # Créer un dictionnaire pour transmettre les données au template
        context = {
            'datasimu2': datasimu2.to_dict('records'),
            'table_columns': table_columns,
            'tauxdefaut': tauxdefaut,
            'nombre_echecs': nombre_echecs,
            'nombre_tests': nombre_tests,
            'nombre_tests_ok': nombre_tests - nombre_echecs,  # Calcul des tests OK
            'parcours_concerne': canal_selectionne or "Tous les canaux",
            'valeurs_canal': valeurs_canal,
            'code_selectionne': canal_selectionne,
            'use_cases_en_echec': use_cases_en_echec,
            'start_date': start_date,
            'end_date': end_date,
            'simulation_results': simulation_results,  # Ajout des résultats de la simulation
            #'nombre_testsP':nombre_testsP,
            #'nombre_tests_ok':nombre_tests_ok,
            #'nombre_tests_NOK':nombre_tests_NOK,
            #'taux_dysfonctionnement ':taux_dysfonctionnement ,

        }

        # Exporter les données si demandé
        if 'export' in request.GET:
            try:
                # Filtrer les données à exporter
                if canal_selectionne:
                    data_to_export = datasimu2[datasimu2['Canal'] == canal_selectionne]
                else:
                    data_to_export = datasimu2

                if start_date and end_date:
                    data_to_export = data_to_export[(data_to_export['DATE'] >= start_date) & (data_to_export['DATE'] <= end_date)]

                # Créer un fichier Excel
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="export_donnees.xlsx"'
                with pd.ExcelWriter(response, engine='openpyxl') as writer:
                    data_to_export.to_excel(writer, index=False)
                return response
            except Exception as e:
                return render(request, 'index.html', {'error': str(e)})

        return render(request, 'index.html', context)

    except Exception as e:
        import traceback
        error_message = traceback.format_exc()
        return render(request, 'index.html', {'error': error_message})


def login_view(request):
    return render(request, 'login.html')

def home_redirect(request):
    return redirect('index')

@login_required
def dashboard(request):
    # Récupération des paramètres de filtrage
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    canal_id = request.GET.get('canal')
    
    # Si pas de dates spécifiées, utiliser les 7 derniers jours
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()
    
    # Récupération des statistiques
    stats = get_dashboard_stats(start_date, end_date, canal_id)
    failed_tests = get_failed_tests_details(start_date, end_date, canal_id)
    
    # Données pour le graphique d'évolution
    evolution_data = TestResult.objects.filter(
        date_test__range=[start_date, end_date]
    ).annotate(
        date=TruncDate('date_test')
    ).values('date', 'statut').annotate(
        count=Count('id')
    ).order_by('date')
    
    # Préparation des données pour les graphiques
    dates = []
    ok_counts = []
    nok_counts = []
    current_date = start_date
    
    while current_date <= end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        ok_count = 0
        nok_count = 0
        
        for entry in evolution_data:
            if entry['date'].strftime('%Y-%m-%d') == current_date.strftime('%Y-%m-%d'):
                if entry['statut'] == 'OK':
                    ok_count = entry['count']
                else:
                    nok_count = entry['count']
        
        ok_counts.append(ok_count)
        nok_counts.append(nok_count)
        current_date += timedelta(days=1)
    
    # Données pour le graphique de distribution par canal
    canal_stats = TestResult.objects.filter(
        date_test__range=[start_date, end_date]
    ).values(
        'use_case__canal__code'
    ).annotate(
        count=Count('id')
    )
    
    canal_labels = [stat['use_case__canal__code'] for stat in canal_stats]
    canal_data = [stat['count'] for stat in canal_stats]
    
    # Récupération des canaux pour le filtre
    canaux = CanalUSSD.objects.all()
    use_cases = UseCase.objects.all().select_related('canal')
    
    context = {
        'stats': stats,
        'failed_tests': failed_tests,
        'canaux': canaux,
        'use_cases': use_cases,
        'selected_canal': canal_id,
        'start_date': start_date,
        'end_date': end_date,
        'evolution_dates': json.dumps(dates),
        'evolution_ok': json.dumps(ok_counts),
        'evolution_nok': json.dumps(nok_counts),
        'canal_labels': json.dumps(canal_labels),
        'canal_data': json.dumps(canal_data),
    }
    
    return render(request, 'automatisation/dashboard.html', context)

@login_required
def export_results(request):
    # Récupération des paramètres de filtrage
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    canal_id = request.GET.get('canal')
    
    # Conversion des dates
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()
    
    # Récupération des tests en échec
    failed_tests = get_failed_tests_details(start_date, end_date, canal_id)
    
    # Création du fichier Excel
    df = export_to_excel(failed_tests)
    
    # Génération de la réponse HTTP
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="rapport_tests_ussd.xlsx"'
    
    # Écriture du DataFrame dans le fichier Excel
    df.to_excel(response, index=False)
    
    return response

@login_required
def alert_configuration(request):
    if request.method == 'POST':
        use_case_id = request.POST.get('use_case')
        email = request.POST.get('email')
        
        # Création ou mise à jour de la configuration d'alerte
        AlertConfiguration.objects.update_or_create(
            user=request.user,
            use_case_id=use_case_id,
            email=email,
            defaults={'is_active': True}
        )
    
    # Récupération des configurations existantes
    user_alerts = AlertConfiguration.objects.filter(user=request.user)
    use_cases = UseCase.objects.all()
    
    context = {
        'user_alerts': user_alerts,
        'use_cases': use_cases,
    }
    
    return render(request, 'automatisation/alert_configuration.html', context)