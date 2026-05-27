from decimal import Decimal
from FundRelease.models import Fund_Release
from Kosh.models import Kosh_Total_Population
from Main.models import Kosh_Head



def calculate_kosh_release_amount(financial_year, zilla_parishad_id):
    """
    Calculate Kosh Release Amount
    Return data for frontend/template usage
    """

    final_data = []

    fund_releases = Fund_Release.objects.filter(
        financial_year__year=financial_year,
        zilla_parishad_id=zilla_parishad_id
    )

    if not fund_releases.exists():
        return final_data

    kosh_heads = Kosh_Head.objects.filter(status='Active')

    for fund in fund_releases:

        # Fetch Kosh Population Data
        kosh_populations = Kosh_Total_Population.objects.filter(
            financial_year=fund.financial_year
        )

        if not kosh_populations.exists():
            continue

        # Total Population
        total_population_sum = sum(
            kosh.total_population or 0
            for kosh in kosh_populations
        )

        if total_population_sum == 0:
            continue

        total_amount = fund.total_amount or Decimal('0')

        # Per Citizen Amount
        per_citizen_amount = ( total_amount / total_population_sum)

        # Kosh Wise Calculation
        for kosh_data in kosh_populations:
            kosh_population = ( kosh_data.total_population or 0)
            kosh_amount = ( kosh_population * per_citizen_amount)
            head_data = []

            # Kosh Head Wise Amount
            for head in kosh_heads:

                head_amount = (kosh_amount * head.percentage) / 100

                head_data.append({
                    'head_name': head.name,
                    'percentage': head.percentage,
                    'head_amount': round(head_amount, 2)
                })

            final_data.append({
                'fund_id': fund.id,
                'financial_year': fund.financial_year.year,
                'release_name': fund.release_name,
                'installment': fund.installment,
                'release_order_no': fund.release_order_no,
                'release_date': fund.release_date,
                'total_amount': total_amount,

                'total_population_sum': total_population_sum,
                'per_citizen_amount': round(per_citizen_amount, 2),

                'kosh_name': kosh_data.kosh.kosh_name,
                'kosh_population': kosh_population,
                'kosh_amount': round(kosh_amount, 2),

                'heads': head_data
            })

    print("\n=================================================")
    print("FINAL DATA")
    print("=================================================")

    for item in final_data:
        print(item)

    return final_data