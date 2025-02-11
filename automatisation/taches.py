from celery import shared_task
from .automatisation_tests import simulate_ussd_menu

@shared_task
def run_ussd_tests():
    canal_codes = ["#144#", "#237#", "#1413#", "#111#", "#148#", "#605#", "#336#", "#1441#"]
    simulate_ussd_menu(canal_codes)