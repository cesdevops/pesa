from django.shortcuts import get_object_or_404, render
from Main.models import Kosh_Head
from django.db.models import Sum
from django.core.paginator import Paginator

# Create your views here.
from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from Main.models import Kosh_Head as KoshHead
from datetime import timedelta
from FundRelease.utils import calculate_kosh_release_amount
from Main.utils import validate_clean_text
from .models import *
from .models import Kosh_Fund_Allocation, HeadAllocation
from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse



def ZP_Fund_Release(request):

    # Login Check
    if not request.session.get('user_id'):
        return redirect('Login')

    if request.session.get('user_type') != 'ZillaParishad':
        return redirect('Login')

    # User Check
    try:
        user = Zilla_Parishad_User.objects.get(
            id=request.session.get('user_id'),
            status='Active'
        )

    except Zilla_Parishad_User.DoesNotExist:
        request.session.flush()
        return redirect('Login')

    # Active Financial Year
    financial_year = Financial_Year.objects.filter(status='Active').first()

    # Add Fund Release
    if request.method == "POST":

        release_name = request.POST.get('release_name', '').strip()
        installment = request.POST.get('installment', '').strip()
        release_order_no = request.POST.get('release_order_no', '').strip()
        total_amount = request.POST.get('total_amount', '').strip()
        confirm_amount = request.POST.get('confirm_amount', '').strip()
        remarks = request.POST.get('remarks', '').strip()

        # Required Validation
        if not release_name:
            messages.error(request, "Release Name is required.")
            return redirect('ZP-Fund-Release')

        if not installment:
            messages.error(request, "Installment is required.")
            return redirect('ZP-Fund-Release')

        if not release_order_no:
            messages.error(request, "Release Order Number is required.")
            return redirect('ZP-Fund-Release')

        if not total_amount:
            messages.error(request, "Total Amount is required.")
            return redirect('ZP-Fund-Release')

        if not confirm_amount:
            messages.error(request, "Confirm Amount is required.")
            return redirect('ZP-Fund-Release')

        # Text Validation
        try:
            validate_clean_text(release_name, "Release Name")
            validate_clean_text(release_order_no, "Release Order Number")

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('ZP-Fund-Release')

        # Installment Validation
        valid_installments = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        if installment not in valid_installments:
            messages.error(request, "Invalid Installment Selected.")
            return redirect('ZP-Fund-Release')

        # Amount Validation
        try:
            total_amount_decimal = Decimal(total_amount)
            confirm_amount_decimal = Decimal(confirm_amount)

        except:
            messages.error(request, "Invalid Amount Format.")
            return redirect('ZP-Fund-Release')

        if total_amount_decimal <= 0:
            messages.error(request, "Amount must be greater than 0.")
            return redirect('ZP-Fund-Release')

        if total_amount_decimal != confirm_amount_decimal:
            messages.error(request, "Total Amount and Confirm Amount must match.")
            return redirect('ZP-Fund-Release')

        # Duplicate Check
        if Fund_Release.objects.filter(release_order_no=release_order_no).exists():
            messages.error(request, "Release Order Number already exists.")
            return redirect('ZP-Fund-Release')

        # Create Fund Release
        Fund_Release.objects.create(
            financial_year=financial_year,
            zilla_parishad=user.zilla_parishad,
            added_by=user,
            release_name=release_name,
            installment=installment,
            release_order_no=release_order_no,
            release_date=timezone.now().date(),
            total_amount=total_amount_decimal,
            remarks=remarks,
            fund_distributed=False,
        )

        messages.success(request, "Fund Release Added Successfully.")
        return redirect('ZP-Fund-Release')

    # Search and Filter
    search = request.GET.get('search', '').strip()
    financial_year_id = request.GET.get('financial_year', '').strip()
    installment = request.GET.get('installment', '').strip()
    from_date = request.GET.get('from_date', '').strip()
    to_date = request.GET.get('to_date', '').strip()

    # Fund Release Queryset
    all_fund_release = Fund_Release.objects.select_related(
        'financial_year',
        'added_by',
        'zilla_parishad'
    ).filter(
        added_by=user
    ).order_by('-id')

    # Search Filter
    if search:
        all_fund_release = all_fund_release.filter(
            Q(release_name__icontains=search) |
            Q(release_order_no__icontains=search) |
            Q(remarks__icontains=search)
        )

    # Financial Year Filter
    if financial_year_id:
        all_fund_release = all_fund_release.filter(financial_year__id=financial_year_id)

    # Installment Filter
    if installment:
        all_fund_release = all_fund_release.filter(installment=installment)

    # Date Filter
    if from_date:
        all_fund_release = all_fund_release.filter(release_date__gte=from_date)

    if to_date:
        all_fund_release = all_fund_release.filter(release_date__lte=to_date)

    # Pagination
    paginator = Paginator(all_fund_release, 10)
    page_number = request.GET.get('page')
    all_fund_release = paginator.get_page(page_number)

    # All Financial Years
    all_financial_years = Financial_Year.objects.all().order_by('-id')

    # Available Installments
    used_installments = Fund_Release.objects.filter(
        zilla_parishad=user.zilla_parishad,
        financial_year=financial_year
    ).values_list('installment', flat=True)

    available_installments = []

    for i in range(1, 11):
        if str(i) not in used_installments:
            available_installments.append(str(i))

    # Context Data
    context = {
        'user': user,
        'user_type': request.session.get('user_type'),
        'financial_year': financial_year,
        'all_fund_release': all_fund_release,
        'all_financial_years': all_financial_years,
        'search': search,
        'financial_year_id': financial_year_id,
        'installment': installment,
        'from_date': from_date,
        'to_date': to_date,
        'available_installments': available_installments,
    }

    return render(request, 'ZP-Fund-Release.html', context)

def ZP_Allocation_Chart(request, financial_year, zp_id, fund_id):

    if not request.session.get('user_id') or request.session.get('user_type') != 'ZillaParishad':
        return redirect('Login')

    try:
        user = Zilla_Parishad_User.objects.get(id=zp_id, status='Active')
    except Zilla_Parishad_User.DoesNotExist:
        return redirect('Login')

    fund_release = Fund_Release.objects.filter(id=fund_id).first()

    already_allocated_kosh_ids = set(
        Kosh_Fund_Allocation.objects.filter(
            fund_release=fund_release
        ).values_list('kosh_id', flat=True)
    ) if fund_release else set()

    allocation_data = calculate_kosh_release_amount(
        financial_year=financial_year,
        zilla_parishad_id=user.id,
        fund_id=fund_id
    )

    # ── Only kosh with full valid chain: ZP → PS → GP → Kosh ──
    valid_kosh_qs = Kosh.objects.filter(
        status='Active',
        is_deleted=False,
        grampanchayat__isnull=False,                              # must have GP
        grampanchayat__status='Active',
        grampanchayat__is_deleted=False,
        grampanchayat__panchayat_samiti__isnull=False,            # must have PS
        grampanchayat__panchayat_samiti__status='Active',
        grampanchayat__panchayat_samiti__zilla_parishad=user.zilla_parishad,  # must belong to this ZP
        grampanchayat__panchayat_samiti__zilla_parishad__isnull=False,
    ).values('kosh_name', 'id')

    kosh_map = {k['kosh_name']: k['id'] for k in valid_kosh_qs}

    search      = request.GET.get('search', '').strip()
    kosh_filter = request.GET.get('kosh', '').strip()
    gp_filter   = request.GET.get('gram_panchayat', '').strip()

    for item in allocation_data:
        item['kosh_id'] = kosh_map.get(item.get('kosh_name'))

    # ── Drop rows where kosh_id is None (broken chain) ──
    allocation_data = [i for i in allocation_data if i.get('kosh_id') is not None]

    if search:
        allocation_data = [
            i for i in allocation_data
            if search.lower() in i.get('release_name', '').lower()
            or search.lower() in i.get('release_order_no', '').lower()
        ]

    if kosh_filter:
        allocation_data = [i for i in allocation_data if i.get('kosh_name') == kosh_filter]

    if gp_filter:
        allocation_data = [i for i in allocation_data if i.get('gram_panchayat_name') == gp_filter]

    unique_koshes = sorted(set(i.get('kosh_name') for i in allocation_data))
    unique_gps    = sorted(set(i.get('gram_panchayat_name') for i in allocation_data))

    all_heads = []
    for item in allocation_data:
        for head in item.get('heads', []):
            if head['head_name'] not in [h['name'] for h in all_heads]:
                all_heads.append({
                    'name': head['head_name'],
                    'percentage': head['percentage']
                })

    for item in allocation_data:
        item['head_values'] = [
            next((h['head_amount'] for h in item.get('heads', []) if h['head_name'] == head['name']), 0)
            for head in all_heads
        ]
        item['already_allocated'] = item.get('kosh_id') in already_allocated_kosh_ids

    total_count     = len(allocation_data)
    pending_count   = sum(1 for i in allocation_data if not i['already_allocated'])
    allocated_count = total_count - pending_count

    paginator   = Paginator(allocation_data, 15)
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)

    context = {
        'user'                       : user,
        'financial_year'             : financial_year,
        'allocation_data'            : page_obj,
        'all_heads'                  : all_heads,
        'unique_koshes'              : unique_koshes,
        'unique_gps'                 : unique_gps,
        'search'                     : search,
        'kosh_filter'                : kosh_filter,
        'gp_filter'                  : gp_filter,
        'fund_release'               : fund_release,
        'zp_id'                      : zp_id,
        'fund_id'                    : fund_id,
        'already_allocated_kosh_ids' : already_allocated_kosh_ids,
        'pending_count'              : pending_count,
        'allocated_count'            : allocated_count,
        'total_count'                : total_count,
        'page_obj'                   : page_obj,
    }

    return render(request, 'ZP-Allocation-Chart.html', context)



# def ZP_Allocation_Chart(request, financial_year, zp_id, fund_id):

#     if not request.session.get('user_id') or request.session.get('user_type') != 'ZillaParishad':
#         return redirect('Login')

#     try:
#         user = Zilla_Parishad_User.objects.get(id=zp_id, status='Active')
#     except Zilla_Parishad_User.DoesNotExist:
#         return redirect('Login')

#     fund_release = Fund_Release.objects.filter(id=fund_id).first()

#     already_allocated_kosh_ids = set(
#         Kosh_Fund_Allocation.objects.filter(
#             fund_release=fund_release
#         ).values_list('kosh_id', flat=True)
#     ) if fund_release else set()

#     allocation_data = calculate_kosh_release_amount(
#         financial_year=financial_year,
#         zilla_parishad_id=user.id,
#         fund_id=fund_id
#     )

#     kosh_map = {k.kosh_name: k.id for k in Kosh.objects.all()}

#     search    = request.GET.get('search', '').strip()
#     kosh_filter = request.GET.get('kosh', '').strip()
#     gp_filter   = request.GET.get('gram_panchayat', '').strip()

#     for item in allocation_data:
#         item['kosh_id'] = kosh_map.get(item.get('kosh_name'))

#     if search:
#         allocation_data = [
#             i for i in allocation_data
#             if search.lower() in i.get('release_name', '').lower()
#             or search.lower() in i.get('release_order_no', '').lower()
#         ]

#     if kosh_filter:
#         allocation_data = [i for i in allocation_data if i.get('kosh_name') == kosh_filter]

#     if gp_filter:
#         allocation_data = [i for i in allocation_data if i.get('gram_panchayat_name') == gp_filter]

#     # ── Dropdown data (from full filtered list, before pagination) ──
#     unique_koshes = sorted(set(i.get('kosh_name') for i in allocation_data))
#     unique_gps    = sorted(set(i.get('gram_panchayat_name') for i in allocation_data))

#     # ── Build all_heads & head_values on full list ──
#     all_heads = []
#     for item in allocation_data:
#         for head in item.get('heads', []):
#             if head['head_name'] not in [h['name'] for h in all_heads]:
#                 all_heads.append({
#                     'name': head['head_name'],
#                     'percentage': head['percentage']
#                 })

#     for item in allocation_data:
#         item['head_values'] = [
#             next((h['head_amount'] for h in item.get('heads', []) if h['head_name'] == head['name']), 0)
#             for head in all_heads
#         ]
#         item['already_allocated'] = item.get('kosh_id') in already_allocated_kosh_ids

#     # ── Counts on FULL filtered list (before pagination) ──
#     total_count    = len(allocation_data)
#     pending_count  = sum(1 for i in allocation_data if not i['already_allocated'])
#     allocated_count = total_count - pending_count

#     # ── Pagination ──
#     paginator   = Paginator(allocation_data, 15)          # 15 rows per page
#     page_number = request.GET.get('page')
#     page_obj    = paginator.get_page(page_number)

#     context = {
#         'user'                       : user,
#         'financial_year'             : financial_year,
#         'allocation_data'            : page_obj,          # ← paginated now
#         'all_heads'                  : all_heads,
#         'unique_koshes'              : unique_koshes,
#         'unique_gps'                 : unique_gps,
#         'search'                     : search,
#         'kosh_filter'                : kosh_filter,
#         'gp_filter'                  : gp_filter,
#         'fund_release'               : fund_release,
#         'zp_id'                      : zp_id,
#         'fund_id'                    : fund_id,
#         'already_allocated_kosh_ids' : already_allocated_kosh_ids,
#         'pending_count'              : pending_count,       # ← full list count
#         'allocated_count'            : allocated_count,     # ← full list count
#         'total_count'                : total_count,
#         'page_obj'                   : page_obj,
#     }

#     return render(request, 'ZP-Allocation-Chart.html', context)



def ZP_Kosh_Fund_Allocation(request, financial_year, zp_id, fund_id):

    # Login, User, Fund & Allocation
    if not request.session.get('user_id') or request.session.get('user_type') != 'ZillaParishad':
        return redirect('Login')

    try:
        user = Zilla_Parishad_User.objects.get(id=zp_id, status='Active')
    except Zilla_Parishad_User.DoesNotExist:
        return redirect('Login')

    fund_release = get_object_or_404(Fund_Release, id=fund_id)

    if request.method == 'POST':

        try:
            with transaction.atomic():

                fund_release = Fund_Release.objects.select_for_update().get(id=fund_id)

                if fund_release.fund_distributed:
                    messages.warning(request, 'हा निधी आधीच वितरित केला गेला आहे.')
                    return redirect(request.path)

                allocation_data = calculate_kosh_release_amount(
                    financial_year=financial_year,
                    zilla_parishad_id=zp_id,
                    fund_id=fund_id
                )

                if not allocation_data:
                    messages.error(request, 'कोणताही कोष डेटा आढळला नाही.')
                    return redirect(request.path)

                allocated_ids = set(
                    Kosh_Fund_Allocation.objects.filter(
                        fund_release=fund_release
                    ).values_list('kosh_id', flat=True)
                )

                kosh_map = {k.kosh_name: k for k in Kosh.objects.all()}
                head_map = {h.name: h for h in KoshHead.objects.filter(status='Active')}

                any_new = False

                for row in allocation_data:

                    kosh = kosh_map.get(row.get('kosh_name'))

                    if not kosh or kosh.id in allocated_ids:
                        continue

                    amount = Decimal(str(row['kosh_amount']))

                    kfa = Kosh_Fund_Allocation.objects.create(
                        fund_release=fund_release,
                        kosh=kosh,
                        allocated_amount=amount,
                        released_amount=amount,
                        balance_amount=amount,
                        status='Allocated',
                        is_fund_given=True,
                        distributed_by=user,
                        remark='Fund Distributed'
                    )

                    for head in row.get('heads', []):

                        kosh_head = head_map.get(head['head_name'])

                        if not kosh_head:
                            continue

                        head_amount = Decimal(str(head['head_amount']))

                        HeadAllocation.objects.create(
                            kosh_fund_allocation=kfa,
                            kosh_head=kosh_head,
                            allocated_amount=head_amount,
                            utilize_amount=0,
                            remaining_amount=head_amount,
                            is_fund_given=True
                        )

                    any_new = True

                if any_new:
                    fund_release.fund_distributed = True
                    fund_release.save()
                    messages.success(request, 'सर्व कोषांना निधी यशस्वीरित्या वाटप केला गेला.')
                else:
                    messages.warning(request, 'सर्व कोष आधीच वाटप केले गेले आहेत.')

        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')

        return redirect(request.path)

    search = request.GET.get('search', '').strip()
    kosh_filter = request.GET.get('kosh', '').strip()
    gp_filter = request.GET.get('gram_panchayat', '').strip()

    allocation_data = calculate_kosh_release_amount(
        financial_year=financial_year,
        zilla_parishad_id=zp_id,
        fund_id=fund_id
    )

    if search:
        allocation_data = [
            i for i in allocation_data
            if search.lower() in i.get('release_name', '').lower()
            or search.lower() in i.get('release_order_no', '').lower()
        ]

    if kosh_filter:
        allocation_data = [i for i in allocation_data if i.get('kosh_name') == kosh_filter]

    if gp_filter:
        allocation_data = [i for i in allocation_data if i.get('gram_panchayat_name') == gp_filter]

    unique_koshes = sorted(set(i.get('kosh_name') for i in allocation_data))
    unique_gps = sorted(set(i.get('gram_panchayat_name') for i in allocation_data))

    all_heads = []

    for item in allocation_data:

        for head in item.get('heads', []):

            if head['head_name'] not in [h['name'] for h in all_heads]:
                all_heads.append({
                    'name': head['head_name'],
                    'percentage': head['percentage']
                })

    allocated_ids = set(
        Kosh_Fund_Allocation.objects.filter(
            fund_release=fund_release
        ).values_list('kosh_id', flat=True)
    )

    kosh_map = {k.kosh_name: k.id for k in Kosh.objects.all()}

    for item in allocation_data:

        item['kosh_id'] = kosh_map.get(item.get('kosh_name'))

        item['head_values'] = [
            next((h['head_amount'] for h in item.get('heads', []) if h['head_name'] == head['name']), 0)
            for head in all_heads
        ]

        item['already_allocated'] = item.get('kosh_id') in allocated_ids

    pending_count = sum(1 for i in allocation_data if not i['already_allocated'])

    context = {
        'user': user,
        'financial_year': financial_year,
        'fund_release': fund_release,
        'allocation_data': allocation_data,
        'all_heads': all_heads,
        'unique_koshes': unique_koshes,
        'unique_gps': unique_gps,
        'search': search,
        'kosh_filter': kosh_filter,
        'gp_filter': gp_filter,
        'zp_id': zp_id,
        'fund_id': fund_id,
        'already_allocated_kosh_ids': allocated_ids,
        'pending_count': pending_count,
    }

    return render(request, 'ZP-Allocation-Chart.html', context)





def Check_Lapsed_Amount(request):

    try:
        # =========================
        # TODAY DATE
        # =========================
        one_year_ago = timezone.now().date() - timedelta(days=365)

        print("\n==============================")
        print("CHECKING TODAY RECORDS")
        print("==============================\n")

        # =========================
        # TODAY HEAD ALLOCATION
        # =========================
        expired_head_allocations = HeadAllocation.objects.filter(
            created_at__date=one_year_ago
        ).order_by('-created_at')

        if expired_head_allocations.exists():

            print("\n===== TODAY HEAD ALLOCATIONS =====\n")

            for data in expired_head_allocations:

                try:

                    # =========================
                    # MOVE REMAINING TO LAPSED
                    # =========================
                    remaining_amount = data.remaining_amount or 0

                    data.lapsed_amount += remaining_amount
                    data.remaining_amount = 0

                    # =========================
                    # SAVE HEAD ALLOCATION
                    # =========================
                    data.save()

                    # ==========================================
                    # UPDATE KOSH FUND ALLOCATION LAPSED AMOUNT
                    # ==========================================
                    if data.kosh_fund_allocation:

                        total_lapsed = HeadAllocation.objects.filter(
                            kosh_fund_allocation=data.kosh_fund_allocation
                        ).aggregate(
                            total=Sum('lapsed_amount')
                        )['total'] or 0

                        data.kosh_fund_allocation.total_lapsed_amount = total_lapsed
                        data.kosh_fund_allocation.save()

                        print(
                            f"Kosh Fund Allocation Updated "
                            f"with Total Lapsed Amount = {total_lapsed}"
                        )

                    print(f"Kosh Head          : {data.kosh_head}")
                    print(f"Allocated Amount   : {data.allocated_amount}")
                    print(f"Utilize Amount     : {data.utilize_amount}")
                    print(f"Lapsed Amount      : {data.lapsed_amount}")
                    print(f"Remaining Amount   : {data.remaining_amount}")
                    print(f"Created At         : {data.created_at}")
                    print("----------------------------------------")

                except Exception as e:

                    print("\nERROR IN SINGLE RECORD")
                    print("--------------------------------")
                    print(f"Head ID : {data.id}")
                    print(f"Error   : {str(e)}")
                    print("--------------------------------\n")

        else:
            print("No Today Head Allocation Found.\n")

        print("\n==============================")
        print("CHECK COMPLETED")
        print("==============================\n")

        return HttpResponse("Lapsed Amount Updated Successfully.")

    except Exception as e:

        print("\n==============================")
        print("MAIN EXCEPTION OCCURRED")
        print("==============================")
        print(f"Error : {str(e)}")
        print("==============================\n")

        return HttpResponse(
            f"Something went wrong : {str(e)}",
            status=500
        )
