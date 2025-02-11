import os
from celery import Celery

# Définir le module Django par défaut pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automatisation_app.settings')

# Créer une instance de Celery
app = Celery('automatisation_app')

# Charger la configuration depuis les paramètres Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Découvrir automatiquement les tâches dans les applications Django
app.autodiscover_tasks()