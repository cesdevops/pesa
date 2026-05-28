from django.shortcuts import get_object_or_404, render
from Main.models import Kosh_Head

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

from FundRelease.utils import calculate_kosh_release_amount
from Main.utils import validate_clean_text

from .models import *

from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q



def ZP_Fund_Release(request):

    # =====================================================
    # LOGIN CHECK
    # =====================================================

    if not request.session.get('user_id'):
        return redirect('Login')

    if request.session.get('user_type') != 'ZillaParishad':
        return redirect('Login')

    # =====================================================
    # USER CHECK
    # =====================================================

    try:

        user = Zilla_Parishad_User.objects.get(
            id=request.session.get('user_id'),
            status='Active'
        )

    except Zilla_Parishad_User.DoesNotExist:

        request.session.flush()
        return redirect('Login')

    # =====================================================
    # ACTIVE FINANCIAL YEAR
    # =====================================================

    financial_year = Financial_Year.objects.filter(
        status='Active'
    ).first()

    # =====================================================
    # ADD FUND RELEASE
    # =====================================================

    if request.method == "POST":

        release_name = request.POST.get(
            'release_name', ''
        ).strip()

        installment = request.POST.get(
            'installment', ''
        ).strip()

        release_order_no = request.POST.get(
            'release_order_no', ''
        ).strip()

        total_amount = request.POST.get(
            'total_amount', ''
        ).strip()

        confirm_amount = request.POST.get(
            'confirm_amount', ''
        ).strip()

        remarks = request.POST.get(
            'remarks', ''
        ).strip()

        # =====================================================
        # REQUIRED VALIDATION
        # =====================================================

        if not release_name:

            messages.error(
                request,
                "Release Name is required."
            )

            return redirect('ZP-Fund-Release')

        if not installment:

            messages.error(
                request,
                "Installment is required."
            )

            return redirect('ZP-Fund-Release')

        if not release_order_no:

            messages.error(
                request,
                "Release Order Number is required."
            )

            return redirect('ZP-Fund-Release')

        if not total_amount:

            messages.error(
                request,
                "Total Amount is required."
            )

            return redirect('ZP-Fund-Release')

        if not confirm_amount:

            messages.error(
                request,
                "Confirm Amount is required."
            )

            return redirect('ZP-Fund-Release')

        # =====================================================
        # TEXT VALIDATION
        # =====================================================

        try:

            validate_clean_text(
                release_name,
                "Release Name"
            )

            validate_clean_text(
                release_order_no,
                "Release Order Number"
            )

        except ValidationError as e:

            messages.error(
                request,
                str(e)
            )

            return redirect('ZP-Fund-Release')

        # =====================================================
        # INSTALLMENT VALIDATION
        # =====================================================

        valid_installments = [
            '1', '2', '3', '4', '5',
            '6', '7', '8', '9', '10'
        ]

        if installment not in valid_installments:

            messages.error(
                request,
                "Invalid Installment Selected."
            )

            return redirect('ZP-Fund-Release')

        # =====================================================
        # AMOUNT VALIDATION
        # =====================================================

        try:

            total_amount_decimal = Decimal(
                total_amount
            )

            confirm_amount_decimal = Decimal(
                confirm_amount
            )

        except:

            messages.error(
                request,
                "Invalid Amount Format."
            )

            return redirect('ZP-Fund-Release')

        if total_amount_decimal <= 0:

            messages.error(
                request,
                "Amount must be greater than 0."
            )

            return redirect('ZP-Fund-Release')

        if total_amount_decimal != confirm_amount_decimal:

            messages.error(
                request,
                "Total Amount and Confirm Amount must match."
            )

            return redirect('ZP-Fund-Release')

        # =====================================================
        # DUPLICATE CHECK
        # =====================================================

        if Fund_Release.objects.filter(
            release_order_no=release_order_no
        ).exists():

            messages.error(
                request,
                "Release Order Number already exists."
            )

            return redirect('ZP-Fund-Release')


        if Fund_Release.objects.filter(
            release_order_no=release_order_no
        ).exists():

            messages.error(
                request,
                "Release Order Number already exists."
            )

            return redirect('ZP-Fund-Release')

        # =====================================================
        # CREATE
        # =====================================================

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

        messages.success(
            request,
            "Fund Release Added Successfully."
        )

        return redirect('ZP-Fund-Release')

    # =====================================================
    # SEARCH + FILTER
    # =====================================================

    search = request.GET.get(
        'search', ''
    ).strip()

    financial_year_id = request.GET.get(
        'financial_year', ''
    ).strip()

    installment = request.GET.get(
        'installment', ''
    ).strip()

    from_date = request.GET.get(
        'from_date', ''
    ).strip()

    to_date = request.GET.get(
        'to_date', ''
    ).strip()

    # =====================================================
    # QUERYSET
    # =====================================================

    all_fund_release = Fund_Release.objects.select_related(
        'financial_year',
        'added_by',
        'zilla_parishad'

    ).filter(
        added_by=user
    ).order_by('-id')

    # =====================================================
    # SEARCH
    # =====================================================

    if search:

        all_fund_release = all_fund_release.filter(

            Q(release_name__icontains=search) |
            Q(release_order_no__icontains=search) |
            Q(remarks__icontains=search)

        )

    # =====================================================
    # FINANCIAL YEAR FILTER
    # =====================================================

    if financial_year_id:

        all_fund_release = all_fund_release.filter(
            financial_year__id=financial_year_id
        )

    # =====================================================
    # INSTALLMENT FILTER
    # =====================================================

    if installment:

        all_fund_release = all_fund_release.filter(
            installment=installment
        )

    # =====================================================
    # DATE FILTER
    # =====================================================

    if from_date:

        all_fund_release = all_fund_release.filter(
            release_date__gte=from_date
        )

    if to_date:

        all_fund_release = all_fund_release.filter(
            release_date__lte=to_date
        )

    # =====================================================
    # PAGINATION
    # =====================================================

    paginator = Paginator(
        all_fund_release,
        10
    )

    page_number = request.GET.get('page')

    all_fund_release = paginator.get_page(
        page_number
    )

    # =====================================================
    # ALL FINANCIAL YEARS
    # =====================================================

    all_financial_years = Financial_Year.objects.all().order_by(
        '-id'
    )
    # =====================================================
    # USED INSTALLMENTS
    # =====================================================

    used_installments = Fund_Release.objects.filter(
        zilla_parishad=user.zilla_parishad,
        financial_year=financial_year
    ).values_list(
        'installment',
        flat=True
    )

    available_installments = []

    for i in range(1, 11):

        if str(i) not in used_installments:

            available_installments.append(str(i))
    # =====================================================
    # CONTEXT
    # =====================================================

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

    return render(
        request,
        'ZP-Fund-Release.html',
        context
    )




def ZP_Allocation_Chart(request, financial_year, zp_id, fund_id):

    # =========================
    # LOGIN CHECK
    # =========================
    if not request.session.get('user_id'):
        return redirect('Login')

    if request.session.get('user_type') != 'ZillaParishad':
        return redirect('Login')

    # =========================
    # USER
    # =========================
    try:
        user = Zilla_Parishad_User.objects.get(id=zp_id, status='Active')
    except:
        return redirect('Login')

    # =========================
    # FUND RELEASE & ALLOCATED KOSH IDs
    # =========================
    fund_release = Fund_Release.objects.filter(id=fund_id).first()

    already_allocated_kosh_ids = set()
    if fund_release:
        already_allocated_kosh_ids = set(
            Kosh_Fund_Allocation.objects.filter(fund_release=fund_release)
            .values_list('kosh_id', flat=True)
        )

    # =========================
    # RAW DATA FROM UTILITY
    # =========================
    allocation_data = calculate_kosh_release_amount(
        financial_year=financial_year,
        zilla_parishad_id=user.id,
        fund_id=fund_id
    )

    kosh_name_to_id = {k.kosh_name: k.id for k in Kosh.objects.all()}
    for i in allocation_data:
        i['kosh_id'] = kosh_name_to_id.get(i.get('kosh_name'))

    # =========================

    # FILTERS
    # =========================
    search      = request.GET.get('search', '').strip()
    kosh_filter = request.GET.get('kosh', '').strip()
    gp_filter   = request.GET.get('gram_panchayat', '').strip()

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

    # =========================
    # UNIQUE DROPDOWNS
    # =========================
    unique_koshes = sorted(set(i.get('kosh_name') for i in allocation_data))
    unique_gps    = sorted(set(i.get('gram_panchayat_name') for i in allocation_data))

    # =========================
    # HEAD STRUCTURE (NAME + %)
    # =========================
    all_heads = []
    for i in allocation_data:
        for h in i.get('heads', []):
            if h['head_name'] not in [x['name'] for x in all_heads]:
                all_heads.append({
                    "name": h['head_name'],
                    "percentage": h['percentage']
                })

    # =========================
    # HEAD VALUE MATRIX + ALREADY ALLOCATED FLAG
    # =========================
    for i in allocation_data:
        head_values = []
        for h in all_heads:
            value = 0
            for item in i.get('heads', []):
                if item['head_name'] == h['name']:
                    value = item['head_amount']
            head_values.append(value)
        i['head_values']       = head_values
        i['already_allocated'] = i.get('kosh_id') in already_allocated_kosh_ids

    # ← OUTSIDE the loop, at this indentation level
    pending_count   = sum(1 for i in allocation_data if not i['already_allocated'])
    allocated_count = len(allocation_data) - pending_count

    context = {
        "user"                      : user,
        "financial_year"            : financial_year,
        "allocation_data"           : allocation_data,
        "all_heads"                 : all_heads,
        "unique_koshes"             : unique_koshes,
        "unique_gps"                : unique_gps,
        "search"                    : search,
        "kosh_filter"               : kosh_filter,
        "gp_filter"                 : gp_filter,
        "fund_release"              : fund_release,
        "zp_id"                     : zp_id,
        "fund_id"                   : fund_id,
        "already_allocated_kosh_ids": already_allocated_kosh_ids,
        "pending_count"             : pending_count,       # ← ADD
        "allocated_count"           : allocated_count,     # ← ADD
    }

    return render(request, "ZP-Allocation-Chart.html", context)




def ZP_Kosh_Fund_Allocation(request, financial_year, zp_id, fund_id):

    fund_release = get_object_or_404(Fund_Release, id=fund_id)
    all_heads    = KoshHead.objects.filter(status='Active')

    # ── POST: Allocate ALL unallocated kosh atomically ────────────────
    if request.method == 'POST':

        allocation_date = request.POST.get(
            'allocation_date',
            str(fund_release.release_date)
        )

        try:
            with transaction.atomic():

                # Lock the fund_release row to prevent concurrent double-submit
                fund_release = Fund_Release.objects.select_for_update().get(
                    id=fund_id
                )

                # If already fully distributed, do nothing (idempotent)
                if fund_release.fund_distributed:
                    messages.warning(
                        request,
                        'हा निधी आधीच वितरित केला गेला आहे.'
                    )
                    return redirect(request.path)

                # Get the full allocation data (same utility as GET)
                allocation_data = calculate_kosh_release_amount(
                    financial_year=financial_year,
                    zilla_parishad_id=zp_id,
                    fund_id=fund_id
                )

                if not allocation_data:
                    messages.error(
                        request,
                        'कोणताही कोष डेटा आढळला नाही.'
                    )
                    return redirect(request.path)

                # Already-allocated kosh IDs (skip them — safe retry)
                already_allocated_kosh_ids = set(
                    Kosh_Fund_Allocation.objects
                    .filter(fund_release=fund_release)
                    .values_list('kosh_id', flat=True)
                )

                # Build kosh_id map
                kosh_name_to_id = {
                    k.kosh_name: k.id
                    for k in Kosh.objects.all()
                }
                for row in allocation_data:
                    row['kosh_id'] = kosh_name_to_id.get(row.get('kosh_name'))

                any_new = False

                for row in allocation_data:
                    kosh_id = row.get('kosh_id')
                    if not kosh_id:
                        continue
                    if kosh_id in already_allocated_kosh_ids:
                        continue  # skip — already done

                    try:
                        population      = int(row.get('kosh_population', 0))
                        per_citizen_amt = Decimal(
                            str(row.get('per_citizen_amount', '0'))
                        )
                    except (ValueError, InvalidOperation):
                        raise ValueError(
                            f"कोष '{row.get('kosh_name')}' साठी रक्कम अवैध आहे."
                        )

                    allocated_amount = (
                        per_citizen_amt * population
                    ).quantize(Decimal('0.01'))

                    kosh = Kosh.objects.get(id=kosh_id)

                    kfa = Kosh_Fund_Allocation.objects.create(
                        fund_release     = fund_release,
                        kosh             = kosh,
                        allocated_amount = allocated_amount,
                        released_amount  = Decimal('0'),
                        balance_amount   = allocated_amount,
                        allocated_date   = allocation_date,
                        status           = 'Allocated',
                        is_fund_given    = True,   # set immediately
                    )

                    for head in all_heads:
                        head_amt = (
                            allocated_amount * head.percentage / Decimal('100')
                        ).quantize(Decimal('0.01'))

                        HeadAllocation.objects.create(
                            kosh_fund_allocation = kfa,
                            kosh_head            = head,
                            allocated_amount     = head_amt,
                            utilize_amount       = Decimal('0'),
                            remaining_amount     = head_amt,
                        )

                    any_new = True

                if any_new:
                    fund_release.fund_distributed = True
                    fund_release.save()
                    messages.success(
                        request,
                        'सर्व कोषांना निधी यशस्वीरित्या वाटप केला गेला.'
                    )
                else:
                    messages.warning(
                        request,
                        'सर्व कोष आधीच वाटप केले गेले आहेत.'
                    )

        except Kosh.DoesNotExist:
            messages.error(request, 'कोष सापडला नाही. वाटप रद्द केले.')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)} — कोणतेही वाटप जतन केले नाही.')

        return redirect(request.path)

    # ── GET ───────────────────────────────────────────────────────────
    search      = request.GET.get('search', '').strip()
    kosh_filter = request.GET.get('kosh', '').strip()
    gp_filter   = request.GET.get('gram_panchayat', '').strip()

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
        allocation_data = [
            i for i in allocation_data
            if i.get('kosh_name') == kosh_filter
        ]
    if gp_filter:
        allocation_data = [
            i for i in allocation_data
            if i.get('gram_panchayat_name') == gp_filter
        ]

    unique_koshes = sorted(set(i.get('kosh_name') for i in allocation_data))
    unique_gps    = sorted(set(i.get('gram_panchayat_name') for i in allocation_data))

    # Head structure
    all_heads_list = []
    for i in allocation_data:
        for h in i.get('heads', []):
            if h['head_name'] not in [x['name'] for x in all_heads_list]:
                all_heads_list.append({
                    'name': h['head_name'],
                    'percentage': h['percentage']
                })

    # Already-allocated kosh IDs
    already_allocated_kosh_ids = set(
        Kosh_Fund_Allocation.objects
        .filter(fund_release=fund_release)
        .values_list('kosh_id', flat=True)
    )

    # Build kosh_id map + head value matrix
    kosh_name_to_id = {k.kosh_name: k.id for k in Kosh.objects.all()}
    for i in allocation_data:
        i['kosh_id'] = kosh_name_to_id.get(i.get('kosh_name'))
        head_values  = []
        for h in all_heads_list:
            value = 0
            for item in i.get('heads', []):
                if item['head_name'] == h['name']:
                    value = item['head_amount']
            head_values.append(value)
        i['head_values']       = head_values
        i['already_allocated'] = i.get('kosh_id') in already_allocated_kosh_ids

    # Count how many are still pending
    pending_count = sum(
        1 for i in allocation_data if not i['already_allocated']
    )

    context = {
        'financial_year'            : financial_year,
        'fund_release'              : fund_release,
        'allocation_data'           : allocation_data,
        'all_heads'                 : all_heads_list,
        'unique_koshes'             : unique_koshes,
        'unique_gps'                : unique_gps,
        'search'                    : search,
        'kosh_filter'               : kosh_filter,
        'gp_filter'                 : gp_filter,
        'zp_id'                     : zp_id,
        'fund_id'                   : fund_id,
        'already_allocated_kosh_ids': already_allocated_kosh_ids,
        'pending_count'             : pending_count,
    }

    return render(request, 'ZP-Allocation-Chart.html', context)