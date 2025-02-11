from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import AlertConfiguration, DetailedTestResult

def send_test_failure_alert(test_result):
    """Envoie des alertes par email pour les tests en échec"""
    
    # Récupérer les configurations d'alerte pour ce use case
    alert_configs = AlertConfiguration.objects.filter(
        use_case=test_result.test_result.use_case,
        is_active=True
    )
    
    if not alert_configs:
        return
    
    # Préparer le contexte pour le template d'email
    context = {
        'test_result': test_result,
        'canal': test_result.test_result.use_case.canal.code,
        'use_case': test_result.test_result.use_case.nom,
        'step': test_result.step.step_number,
        'error': test_result.message_erreur,
        'date': test_result.date_heure,
        'numero': test_result.numero_telephone
    }
    
    # Rendre le contenu HTML de l'email
    html_message = render_to_string('automatisation/email/alert_email.html', context)
    
    # Envoyer l'email à tous les destinataires configurés
    for config in alert_configs:
        send_mail(
            subject=f'[ALERTE] Échec test USSD - {context["canal"]} - {context["use_case"]}',
            message=f"""
                Test USSD en échec :
                Canal : {context['canal']}
                Use Case : {context['use_case']}
                Étape : {context['step']}
                Numéro : {context['numero']}
                Date : {context['date']}
                Erreur : {context['error']}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[config.email],
            html_message=html_message
        )
