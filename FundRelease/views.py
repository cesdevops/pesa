from django.shortcuts import render

# Create your views here.
from decimal import Decimal
from django.utils import timezone

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect

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

        # =====================================================
        # CREATE
        # =====================================================

        Fund_Release.objects.create(

            financial_year=financial_year,
            added_by=user,
            release_name=release_name,
            installment=installment,
            release_order_no=release_order_no,
            release_date=timezone.now().date(),
            total_amount=total_amount_decimal,
            remarks=remarks

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
        'added_by'
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

    }

    return render(
        request,
        'ZP-Fund-Release.html',
        context
    )



