
def fund_realse():
    """
    Fetch and print all Fund Release records in terminal
    """

    fund_releases = Fund_Release.objects.all()

    if not fund_releases.exists():
        print("No Fund Release records found.")
        return

    print("\n========== FUND RELEASE DATA ==========\n")

    for fund in fund_releases:
        print(f"ID                : {fund.id}")
        print(f"Financial Year    : {fund.financial_year}")
        print(f"Added By          : {fund.added_by}")
        print(f"Release Name      : {fund.release_name}")
        print(f"Installment       : {fund.installment}")
        print(f"Release Order No  : {fund.release_order_no}")
        print(f"Release Date      : {fund.release_date}")
        print(f"Total Amount      : {fund.total_amount}")
        print(f"Remarks           : {fund.remarks}")
        print(f"Created At        : {fund.created_at}")
        print(f"Updated At        : {fund.updated_at}")
        print("-" * 50)