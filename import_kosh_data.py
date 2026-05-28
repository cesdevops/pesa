
# import_kosh_data.py

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pesa.settings')

django.setup()

import pandas as pd
import random

from Main.models import Financial_Year

from Kosh.models import (
    GramPanchayat,
    Kosh,
    Kosh_Cast_Category,
    Kosh_Population,
    Kosh_Total_Population,
    Kosh_User
)

print("\nSTARTING IMPORT...\n")

# ==========================================
# EXCEL FILE
# ==========================================

file_path = "kosh_master_data.xlsx"

try:
    df = pd.read_excel(file_path)
    print("Excel Loaded Successfully")

except Exception as e:
    print("Excel Read Error:", e)
    exit()

# ==========================================
# FINANCIAL YEAR
# ==========================================

financial_year = Financial_Year.objects.first()

if not financial_year:
    print("No Financial Year Found")
    exit()

print("Financial Year Found")

# ==========================================
# CREATE CAST CATEGORIES
# ==========================================

categories = {}

for category in ["SC", "ST", "OBC", "OPEN"]:

    category_obj, created = Kosh_Cast_Category.objects.get_or_create(
        category_name=category
    )

    categories[category] = category_obj

print("Categories Ready")

# ==========================================
# START IMPORT
# ==========================================

total_imported = 0

for _, row in df.iterrows():

    try:

        # ==========================================
        # CREATE GRAM PANCHAYAT
        # ==========================================

        gram_panchayat, created = GramPanchayat.objects.get_or_create(
            gram_panchayat_code=row['gram_panchayat_code'],
            defaults={
                'gram_panchayat_name': row['gram_panchayat_name'],
                'status': 'Active'
            }
        )

        # ==========================================
        # CREATE KOSH
        # ==========================================

        kosh, created = Kosh.objects.get_or_create(
            kosh_code=row['kosh_code'],
            defaults={
                'grampanchayat': gram_panchayat,
                'kosh_name': row['kosh_name'],
                'is_primary': True,
                'status': 'Active'
            }
        )

        # ==========================================
        # CREATE USER
        # ==========================================

        username = str(row['username']).lower()
        password = str(row['password'])

        kosh_user, created = Kosh_User.objects.get_or_create(
            username=username,
            defaults={
                'name': f"{row['kosh_name']} User",
                'mobile': f"9{random.randint(100000000,999999999)}",
                'email': f"{username}@gmail.com",
                'password': password,
                'status': 'Active'
            }
        )

        # MANY TO MANY
        kosh_user.kosh.add(kosh)

        # ==========================================
        # TOTAL POPULATION
        # ==========================================

        total_population = int(row['total_population'])

        tribal_population = int(row['ST'])

        Kosh_Total_Population.objects.update_or_create(
            kosh=kosh,
            financial_year=financial_year,
            defaults={
                'total_population': total_population,
                'tribal_population': tribal_population
            }
        )

        # ==========================================
        # CATEGORY POPULATION
        # ==========================================

        for category in ["SC", "ST", "OBC", "OPEN"]:

            population_count = int(row[category])

            Kosh_Population.objects.update_or_create(
                kosh=kosh,
                cast_category=categories[category],
                financial_year=financial_year,
                defaults={
                    'population_count': population_count,
                    'status': 'Active'
                }
            )

        total_imported += 1

        print(
            f"Imported -> "
            f"{gram_panchayat.gram_panchayat_name} | "
            f"{kosh.kosh_name} | "
            f"{username}"
        )

    except Exception as e:

        print("\nERROR IMPORTING ROW")
        print(row)
        print("ERROR:", e)

print(f"\nSUCCESSFULLY IMPORTED {total_imported} RECORDS")

