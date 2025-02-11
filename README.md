# FEB Automatisation Audit Parcours USSD

Application Django pour l'automatisation des tests des parcours USSD avec tableau de bord et système d'alertes.

## Fonctionnalités

- Dashboard de suivi des tests USSD
- Statistiques détaillées (tests OK/NOK, taux de dysfonctionnement)
- Visualisation graphique des résultats
- Export des résultats en Excel
- Système d'alertes par email
- Filtrage par canal et par date

## Prérequis

- Python 3.10+
- Django 5.1+
- Pandas
- Celery (pour les tâches asynchrones)

## Installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
cd ProjetDjango
```

2. Créer un environnement virtuel
```bash
python -m venv env
source env/Scripts/activate  # Sur Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Appliquer les migrations
```bash
python manage.py migrate
```

5. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

6. Lancer le serveur
```bash
python manage.py runserver
```

## Utilisation

1. Accéder à l'application via : http://127.0.0.1:8000
2. Se connecter avec les identifiants créés
3. Accéder au dashboard pour voir les statistiques
4. Configurer les alertes dans la section dédiée

## Structure du Projet

- `automatisation/` : Application principale
  - `models.py` : Modèles de données
  - `views.py` : Vues et logique métier
  - `templates/` : Templates HTML
  - `utils.py` : Fonctions utilitaires
  - `email_service.py` : Service d'envoi d'emails

## Contribution

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## Licence

Ce projet est sous licence MIT.
