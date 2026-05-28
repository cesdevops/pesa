from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from decimal import Decimal
from django.utils import timezone

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect

from Main.utils import validate_clean_text
from Kosh.models import Kosh

from Activity.models import Activity, Work_Master, Kosh_User
from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect


def Activity_Work_Master(request):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # Get all kosh IDs that this user has access to
    user_kosh_ids = kosh_user.kosh.values_list('id', flat=True)
    
    # Base queryset for Work Masters filtered by user's kosh
    work_masters = Work_Master.objects.filter(
        kosh_fund_allocation__kosh_id__in=user_kosh_ids
    ).select_related(
        'activity',
        'activity__kosh_head',
        'kosh_fund_allocation',
        'kosh_fund_allocation__kosh',
        'kosh_fund_allocation__kosh__grampanchayat'
    ).distinct()

    # ================= FILTERS =================
    work_name = request.GET.get('work_name', '').strip()
    work_code = request.GET.get('work_code', '').strip()
    activity_id = request.GET.get('activity_id', '').strip()
    kosh_id = request.GET.get('kosh_id', '').strip()
    overall_status = request.GET.get('overall_status', '').strip()
    is_fully_completed_filter = request.GET.get('is_fully_completed', '').strip()
    reset = request.GET.get('reset', '')
    
    if reset:
        work_name = ''
        work_code = ''
        activity_id = ''
        kosh_id = ''
        overall_status = ''
        is_fully_completed_filter = ''

    if work_name:
        work_masters = work_masters.filter(work_name__icontains=work_name)
    if work_code:
        work_masters = work_masters.filter(work_code__icontains=work_code)
    if activity_id:
        work_masters = work_masters.filter(activity_id=activity_id)
    if kosh_id:
        work_masters = work_masters.filter(kosh_fund_allocation__kosh_id=kosh_id)
    if overall_status:
        work_masters = work_masters.filter(overall_status=overall_status)
    if is_fully_completed_filter:
        if is_fully_completed_filter == 'yes':
            work_masters = work_masters.filter(is_fully_completed=True)
        elif is_fully_completed_filter == 'no':
            work_masters = work_masters.filter(is_fully_completed=False)

    total_work_masters = work_masters.count()
    work_masters = work_masters.order_by('-id')

    # ================= PAGINATION =================
    paginator = Paginator(work_masters, 15)
    page_number = request.GET.get('page', 1)
    work_masters_page = paginator.get_page(page_number)
    start_index = (work_masters_page.number - 1) * paginator.per_page + 1

    # Get data for filters dropdown
    activities = Activity.objects.filter(status='Active').order_by('activity_name')
    kosh_list = Kosh.objects.filter(
        id__in=user_kosh_ids,
        status='Active'
    ).select_related('grampanchayat').order_by('kosh_name')
    
    status_choices = Work_Master.WORK_STATUS_CHOICES

    context = {
        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        'work_masters': work_masters_page,
        'total_work_masters': total_work_masters,
        'start_index': start_index,
        'activities': activities,
        'kosh_list': kosh_list,
        'status_choices': status_choices,
        'work_name': work_name,
        'work_code': work_code,
        'activity_id': activity_id,
        'kosh_id': kosh_id,
        'overall_status': overall_status,
        'is_fully_completed_filter': is_fully_completed_filter,
    }

    return render(request, 'Activity-Work-Master.html', context)