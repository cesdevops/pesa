import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pesa.settings')

django.setup()

from FundRelease.utils import calculate_kosh_release_amount

calculate_kosh_release_amount("2025-26",zilla_parishad_id=1)