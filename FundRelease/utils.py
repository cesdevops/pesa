from decimal import Decimal
from FundRelease.models import Fund_Release
from Kosh.models import Kosh_Total_Population
from Main.models import Kosh_Head




<<<<<<< HEAD
def calculate_kosh_release_amount(financial_year, zilla_parishad_id):
=======
def calculate_kosh_release_amount(financial_year, zilla_parishad_id,fund_id):
>>>>>>> main
    """
    Calculate Kosh Release Amount
    Returns formatted data for frontend/template usage
    """
    final_data = []
    try:
        # Fetch Fund Releases
        fund_releases = Fund_Release.objects.filter(
            financial_year__year=financial_year,
<<<<<<< HEAD
            zilla_parishad_id=zilla_parishad_id
=======
            zilla_parishad_id=zilla_parishad_id,
            id=fund_id
>>>>>>> main
        )
        if not fund_releases.exists():
            return final_data
        # Fetch Active Heads
        kosh_heads = Kosh_Head.objects.filter(status='Active')

        # Loop Through Each Fund Release
        for fund in fund_releases:
            try:
                # Fetch Kosh Population Data
                kosh_populations = Kosh_Total_Population.objects.filter( financial_year=fund.financial_year )

                if not kosh_populations.exists():
                    continue

                # Calculate Total Population
                total_population_sum = sum( kosh.total_population or 0 for kosh in kosh_populations)

                if total_population_sum == 0:
                    continue

                total_amount = fund.total_amount or Decimal('0')

                # Per Citizen Amount
                per_citizen_amount = ( total_amount / Decimal(total_population_sum))

                # Kosh Wise Calculation
                for kosh_data in kosh_populations:
                    try:
                        kosh_population = ( kosh_data.total_population or 0 )
                        kosh_amount = ( Decimal(kosh_population) * per_citizen_amount )
                        # Gram Panchayat Name
                        gram_panchayat_name = ''
                        if ( kosh_data.kosh and kosh_data.kosh.grampanchayat):
                            gram_panchayat_name = ( kosh_data.kosh.grampanchayat.gram_panchayat_name )

                        # Head Wise Data
                        head_data = []

                        for head in kosh_heads:

                            try:
                                head_percentage = ( head.percentage or Decimal('0') )
                                head_amount = ( kosh_amount * head_percentage) / Decimal('100')
                                head_data.append({
                                    'head_name': head.name,
                                    'percentage': head_percentage,
                                    'head_amount': round(head_amount, 2)
                                })

                            except Exception as head_error:
                                print(f"Head Calculation Error: {head_error}")
                                continue

                        # Final Data Append
                        final_data.append({
<<<<<<< HEAD
=======
                            
>>>>>>> main
                            'financial_year': fund.financial_year.year,
                            'release_name': fund.release_name,
                            'installment': fund.installment,
                            'release_order_no': fund.release_order_no,
                            'release_date': fund.release_date,
                            'total_amount': total_amount,

                            'gram_panchayat_name': gram_panchayat_name,

                            'total_population_sum': total_population_sum,
                            'per_citizen_amount': round( per_citizen_amount, 2 ),

                            'kosh_name': (
                                kosh_data.kosh.kosh_name
                                if kosh_data.kosh else ''),
                            'kosh_population': kosh_population,
                            'kosh_amount': round(kosh_amount, 2),
                            'heads': head_data
                        })

                    except Exception as kosh_error:
                        print( f"Kosh Calculation Error: {kosh_error}")
                        continue

            except Exception as fund_error:
                print(f"Fund Processing Error: {fund_error}")
                continue

    except Exception as main_error:
        print(
            f"Main Function Error: {main_error}"
        )

    # Debug Print
    print("\n=================================================")
    print("FINAL DATA")
    print("=================================================")

    for item in final_data:
        print(item)

    return final_data