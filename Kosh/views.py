from django.shortcuts import get_object_or_404, redirect, render
from Main.models import Financial_Year, Kosh_Head, Super_User, Kosh_Head
from Main.utils import validate_clean_text, validate_file, validate_mobile_number
from PanchayatSamiti.models import Panchayat_Samiti
from django.contrib import messages
from .models import GramPanchayat, Kosh, Kosh_Bank_Detail, Kosh_Cast_Category, Kosh_Committee, Kosh_Population, Kosh_Total_Population, Kosh_User
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from decimal import Decimal
from .utils import switch_kosh
from django.contrib.auth.hashers import make_password, check_password



def Switch_Kosh(request, kosh_id):
    if request.session.get('user_type') != 'Kosh':
        return redirect('Login')

    try:
        kosh_user = Kosh_User.objects.get(id=request.session['user_id'], status='Active')
        selected_kosh = kosh_user.kosh.get(id=kosh_id, status='Active', is_deleted=False)
    except (Kosh_User.DoesNotExist, Kosh.DoesNotExist):
        messages.error(request, "Access denied")
        return redirect('Kosh_Dashboard')

    # Update session
    request.session['active_kosh_id']   = selected_kosh.id
    request.session['active_kosh_name'] = selected_kosh.kosh_name
    request.session['active_kosh_code'] = selected_kosh.kosh_code

    messages.success(request, f"Switched to {selected_kosh.kosh_name}")
    return redirect('Kosh_Dashboard')


    
def Kosh_Dashboard(request):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # # Get all active Kosh Heads
    # all_heads = Kosh_Head.objects.filter(status='Active')
    
    # # Prepare heads with their percentages
    # heads_with_percentages = []
    # total_percentage = 0
    
    # for head in all_heads:
    #     # Get percentage for this head
    #     percentage_obj = Head_Percentage.objects.filter(kosh_head=head).first()
    #     percentage = float(percentage_obj.percentage) if percentage_obj else 0
    #     total_percentage += percentage
        
    #     heads_with_percentages.append({
    #         'head': head,
    #         'percentage': percentage
    #     })
    
    # # Calculate remaining percentage
    # remaining_percentage = max(0, 100 - total_percentage)
    
    # # Calculate statistics
    # total_heads = all_heads.count()
    # active_heads = all_heads.filter(status='Active').count()

    context = {
        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        # 'heads_with_percentages': heads_with_percentages,
        # 'total_percentage': round(total_percentage, 2),
        # 'remaining_percentage': round(remaining_percentage, 2),
        # 'total_heads': total_heads,
        # 'active_heads': active_heads,
        **switch_kosh(request),
    }

    return render(request, 'Kosh_dashboard.html', context)

def Kosh_Manage_Grampanchayat(request):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get all panchayat samitis for dropdowns
    all_panchayat_samitis = Panchayat_Samiti.objects.filter(status='Active').order_by('panchayat_samiti_name')
    
    # ================= ADD =================
    if request.method == 'POST' and 'add_grampanchayat' in request.POST:
        try:
            # Get raw values
            raw_gram_panchayat_name = request.POST.get('gram_panchayat_name', '').strip()
            raw_panchayat_samiti_id = request.POST.get('panchayat_samiti_id', '').strip()
            raw_gram_panchayat_code = request.POST.get('gram_panchayat_code', '').strip()
            raw_address = request.POST.get('address', '').strip()
            raw_status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            gram_panchayat_name = validate_clean_text(raw_gram_panchayat_name)
            gram_panchayat_code = validate_clean_text(raw_gram_panchayat_code) if raw_gram_panchayat_code else None
            address = validate_clean_text(raw_address) if raw_address else None
            
            # Validate required fields
            if not gram_panchayat_name:
                messages.error(request, 'ग्रामपंचायत नाव आवश्यक आहे')
                return redirect('Kosh-Manage-Grampanchayat')
            
            if not raw_panchayat_samiti_id:
                messages.error(request, 'पंचायत समिती निवड आवश्यक आहे')
                return redirect('Kosh-Manage-Grampanchayat')
            
            try:
                panchayat_samiti = Panchayat_Samiti.objects.get(id=raw_panchayat_samiti_id)
            except Panchayat_Samiti.DoesNotExist:
                messages.error(request, 'अवैध पंचायत समिती निवडली')
                return redirect('Kosh-Manage-Grampanchayat')
            
            # Create record - REMOVED panchayat_samiti_name
            GramPanchayat.objects.create(
                panchayat_samiti=panchayat_samiti,
                gram_panchayat_name=gram_panchayat_name,
                gram_panchayat_code=gram_panchayat_code,
                address=address,
                status=raw_status
            )
            
            messages.success(request, 'ग्रामपंचायत यशस्वीरित्या जोडली')
            return redirect('Kosh-Manage-Grampanchayat')
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('Kosh-Manage-Grampanchayat')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('Kosh-Manage-Grampanchayat')
    
    # ================= EDIT =================
    if request.method == 'POST' and 'edit_grampanchayat' in request.POST:
        grampanchayat_id = request.POST.get('grampanchayat_id', '').strip()
        
        if not grampanchayat_id:
            messages.error(request, 'अवैध विनंती')
            return redirect('Kosh-Manage-Grampanchayat')
        
        try:
            grampanchayat = GramPanchayat.objects.get(id=grampanchayat_id)
        except GramPanchayat.DoesNotExist:
            messages.error(request, 'ग्रामपंचायत सापडली नाही')
            return redirect('Kosh-Manage-Grampanchayat')
        
        try:
            # Get raw values
            raw_gram_panchayat_name = request.POST.get('gram_panchayat_name', '').strip()
            raw_panchayat_samiti_id = request.POST.get('panchayat_samiti_id', '').strip()
            raw_gram_panchayat_code = request.POST.get('gram_panchayat_code', '').strip()
            raw_address = request.POST.get('address', '').strip()
            raw_status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            gram_panchayat_name = validate_clean_text(raw_gram_panchayat_name)
            gram_panchayat_code = validate_clean_text(raw_gram_panchayat_code) if raw_gram_panchayat_code else None
            address = validate_clean_text(raw_address) if raw_address else None
            
            # Validate required fields
            if not gram_panchayat_name:
                messages.error(request, 'ग्रामपंचायत नाव आवश्यक आहे')
                return redirect('Kosh-Manage-Grampanchayat')
            
            if not raw_panchayat_samiti_id:
                messages.error(request, 'पंचायत समिती निवड आवश्यक आहे')
                return redirect('Kosh-Manage-Grampanchayat')
            
            try:
                panchayat_samiti = Panchayat_Samiti.objects.get(id=raw_panchayat_samiti_id)
            except Panchayat_Samiti.DoesNotExist:
                messages.error(request, 'अवैध पंचायत समिती निवडली')
                return redirect('Kosh-Manage-Grampanchayat')
                        
            # Update record - REMOVED panchayat_samiti_name
            grampanchayat.panchayat_samiti = panchayat_samiti
            grampanchayat.gram_panchayat_name = gram_panchayat_name
            grampanchayat.gram_panchayat_code = gram_panchayat_code
            grampanchayat.address = address
            grampanchayat.status = raw_status
            grampanchayat.save()
            
            messages.success(request, 'ग्रामपंचायत यशस्वीरित्या अद्यतनित केली')
            return redirect('Kosh-Manage-Grampanchayat')
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('Kosh-Manage-Grampanchayat')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('Kosh-Manage-Grampanchayat')
    
    # ================= DELETE =================
    if request.method == 'POST' and 'delete_grampanchayat' in request.POST:
        grampanchayat_id = request.POST.get('grampanchayat_id', '').strip()
        
        if grampanchayat_id:
            try:
                grampanchayat = GramPanchayat.objects.get(id=grampanchayat_id)
                gp_name = grampanchayat.gram_panchayat_name
                grampanchayat.delete()
                messages.success(request, f'"{gp_name}" यशस्वीरित्या हटविले')
            except GramPanchayat.DoesNotExist:
                messages.error(request, 'ग्रामपंचायत सापडली नाही')
        
        return redirect('Kosh-Manage-Grampanchayat')
    
    # ================= FILTERS =================
    gram_panchayat_name = request.GET.get('gram_panchayat_name', '').strip()
    panchayat_samiti_name = request.GET.get('panchayat_samiti_name', '').strip()
    gram_panchayat_code = request.GET.get('gram_panchayat_code', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')
    
    # Reset filters
    if reset:
        gram_panchayat_name = ''
        panchayat_samiti_name = ''
        gram_panchayat_code = ''
        status_filter = 'all'
    
    # Base queryset - order by latest first, exclude deleted
    grampanchayats = GramPanchayat.objects.filter(is_deleted=False).select_related('panchayat_samiti').all()
    total_grampanchayats = grampanchayats.count()
    active_count = grampanchayats.filter(status='Active').count()
    
    # Apply status filter
    if status_filter == 'active':
        grampanchayats = grampanchayats.filter(status='Active')
    elif status_filter == 'inactive':
        grampanchayats = grampanchayats.filter(status='Inactive')
    
    # Apply search filters
    if gram_panchayat_name:
        grampanchayats = grampanchayats.filter(gram_panchayat_name__icontains=gram_panchayat_name)
    if panchayat_samiti_name:
        # Filter by panchayat samiti name through the foreign key
        grampanchayats = grampanchayats.filter(panchayat_samiti__panchayat_samiti_name__icontains=panchayat_samiti_name)
    if gram_panchayat_code:
        grampanchayats = grampanchayats.filter(gram_panchayat_code__icontains=gram_panchayat_code)
    
    filtered_count = grampanchayats.count()
    
    # Order by latest first
    grampanchayats = grampanchayats.order_by('-id')
    
    # Pagination
    paginator = Paginator(grampanchayats, 15)
    page_number = request.GET.get('page', 1)
    grampanchayats_page = paginator.get_page(page_number)
    start_index = (grampanchayats_page.number - 1) * paginator.per_page + 1
    
    context = {
        'user': user,
        'grampanchayats': grampanchayats_page,
        'total_grampanchayats': total_grampanchayats,
        'filtered_count': filtered_count,
        'active_count': active_count,
        'start_index': start_index,
        'gram_panchayat_name': gram_panchayat_name,
        'panchayat_samiti_name': panchayat_samiti_name,
        'gram_panchayat_code': gram_panchayat_code,
        'status_filter': status_filter,
        'all_panchayat_samitis': all_panchayat_samitis,
    }
    
    return render(request, 'Kosh-Manage-Grampanchayat.html', context)

def Kosh_Management(request, grampanchayat_id):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get the Gram Panchayat details
    try:
        gram_panchayat = GramPanchayat.objects.get(
            id=grampanchayat_id, 
            is_deleted=False,
            status='Active'
        )
    except GramPanchayat.DoesNotExist:
        messages.error(request, 'ग्रामपंचायत सापडली नाही')
        return redirect('Kosh-Manage-Grampanchayat')
    
    # Get all Kosh records for this Gram Panchayat - FIXED: use 'grampanchayat' not 'gramPanchayat'
    kosh_list = Kosh.objects.filter(
        grampanchayat=gram_panchayat,  # Changed from gramPanchayat to grampanchayat
        is_deleted=False
    ).order_by('-id')
    
    total_kosh = kosh_list.count()
    active_count = kosh_list.filter(status='Active').count()
    primary_count = kosh_list.filter(is_primary=True).count()
    
    # ================= FILTERS =================
    kosh_name = request.GET.get('kosh_name', '').strip()
    kosh_code = request.GET.get('kosh_code', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')
    
    # Reset filters
    if reset:
        kosh_name = ''
        kosh_code = ''
        status_filter = 'all'
    
    # Apply filters
    if status_filter == 'active':
        kosh_list = kosh_list.filter(status='Active')
    elif status_filter == 'inactive':
        kosh_list = kosh_list.filter(status='Inactive')
    elif status_filter == 'closed':
        kosh_list = kosh_list.filter(status='Closed')
    
    if kosh_name:
        kosh_list = kosh_list.filter(kosh_name__icontains=kosh_name)
    if kosh_code:
        kosh_list = kosh_list.filter(kosh_code__icontains=kosh_code)
    
    filtered_count = kosh_list.count()
    
    # Pagination
    paginator = Paginator(kosh_list, 15)
    page_number = request.GET.get('page', 1)
    kosh_page = paginator.get_page(page_number)
    start_index = (kosh_page.number - 1) * paginator.per_page + 1
    
    context = {
        'user': user,
        'gram_panchayat': gram_panchayat,
        'kosh_list': kosh_page,
        'total_kosh': total_kosh,
        'filtered_count': filtered_count,
        'active_count': active_count,
        'primary_count': primary_count,
        'start_index': start_index,
        'kosh_name': kosh_name,
        'kosh_code': kosh_code,
        'status_filter': status_filter,
    }
    
    return render(request, 'Kosh-Management.html', context)

def Kosh_Add(request, grampanchayat_id):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get Gram Panchayat details
    try:
        gram_panchayat = GramPanchayat.objects.get(
            id=grampanchayat_id, 
            is_deleted=False,
            status='Active'
        )
    except GramPanchayat.DoesNotExist:
        messages.error(request, 'ग्रामपंचायत सापडली नाही')
        return redirect('Kosh-Manage-Grampanchayat')
    
    # ================= ADD KOSH =================
    if request.method == 'POST':
        try:
            raw_kosh_name = request.POST.get('kosh_name', '').strip()
            raw_kosh_code = request.POST.get('kosh_code', '').strip()
            raw_is_primary = request.POST.get('is_primary', 'False')
            raw_status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            kosh_name = validate_clean_text(raw_kosh_name)
            kosh_code = validate_clean_text(raw_kosh_code) if raw_kosh_code else None
            
            if not kosh_name:
                messages.error(request, 'कोष नाव आवश्यक आहे')
                return redirect('Kosh-Add', grampanchayat_id=grampanchayat_id)
            
            # If is_primary is True, unset other primary kosh for this Gram Panchayat
            is_primary = raw_is_primary == 'True'
            if is_primary:
                Kosh.objects.filter(grampanchayat=gram_panchayat, is_primary=True).update(is_primary=False)
            
            # Create record
            new_kosh = Kosh.objects.create(
                grampanchayat=gram_panchayat,
                kosh_name=kosh_name,
                kosh_code=kosh_code,
                is_primary=is_primary,
                status=raw_status
            )
            
            messages.success(request, 'कोष यशस्वीरित्या जोडला')
            return redirect('Kosh-Edit', grampanchayat_id=gram_panchayat.id, kosh_id=new_kosh.id)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('Kosh-Add', grampanchayat_id=grampanchayat_id)
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('Kosh-Add', grampanchayat_id=grampanchayat_id)
    
    # Get all Kosh records for this Gram Panchayat (for display)
    kosh_list = Kosh.objects.filter(
        grampanchayat=gram_panchayat,
        is_deleted=False
    ).order_by('-id')
    
    total_kosh = kosh_list.count()
    active_count = kosh_list.filter(status='Active').count()
    primary_count = kosh_list.filter(is_primary=True).count()
    
    # Filters
    kosh_name = request.GET.get('kosh_name', '').strip()
    kosh_code = request.GET.get('kosh_code', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')
    
    if reset:
        kosh_name = ''
        kosh_code = ''
        status_filter = 'all'
    
    if status_filter == 'active':
        kosh_list = kosh_list.filter(status='Active')
    elif status_filter == 'inactive':
        kosh_list = kosh_list.filter(status='Inactive')
    elif status_filter == 'closed':
        kosh_list = kosh_list.filter(status='Closed')
    
    if kosh_name:
        kosh_list = kosh_list.filter(kosh_name__icontains=kosh_name)
    if kosh_code:
        kosh_list = kosh_list.filter(kosh_code__icontains=kosh_code)
    
    filtered_count = kosh_list.count()
    
    # Pagination
    paginator = Paginator(kosh_list, 15)
    page_number = request.GET.get('page', 1)
    kosh_page = paginator.get_page(page_number)
    start_index = (kosh_page.number - 1) * paginator.per_page + 1
    
    context = {
        'user': user,
        'gram_panchayat': gram_panchayat,
        'kosh_list': kosh_page,
        'total_kosh': total_kosh,
        'filtered_count': filtered_count,
        'active_count': active_count,
        'primary_count': primary_count,
        'start_index': start_index,
        'kosh_name': kosh_name,
        'kosh_code': kosh_code,
        'status_filter': status_filter,
    }
    
    return render(request, 'Kosh-Add.html', context)

def Kosh_Edit(request, grampanchayat_id, kosh_id):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get Gram Panchayat details
    try:
        gram_panchayat = GramPanchayat.objects.get(
            id=grampanchayat_id, 
            is_deleted=False,
            status='Active'
        )
    except GramPanchayat.DoesNotExist:
        messages.error(request, 'ग्रामपंचायत सापडली नाही')
        return redirect('Kosh-Manage-Grampanchayat')
    
    try:
        edit_kosh = Kosh.objects.get(id=kosh_id, is_deleted=False)
    except Kosh.DoesNotExist:
        messages.error(request, 'कोष सापडला नाही')
        return redirect('Kosh-Add', grampanchayat_id=grampanchayat_id)
    # Get cast categories and financial years for dropdowns
    cast_categories = Kosh_Cast_Category.objects.all().order_by('category_name')
    financial_years = Financial_Year.objects.filter(status='Active').order_by('-year')
    # Get population records
    population_list = Kosh_Population.objects.filter(
        kosh=edit_kosh
    ).select_related('cast_category', 'financial_year').order_by('-id')
    
    # Get total population records
    total_population_list = Kosh_Total_Population.objects.filter(
        kosh=edit_kosh
    ).select_related('financial_year').order_by('-id')
    # Get Kosh details for editing
    
    # Get bank details
    bank_details_list = Kosh_Bank_Detail.objects.filter(
        kosh=edit_kosh
    ).order_by('-id')

    # ================= EDIT KOSH =================
    if request.method == 'POST':
        try:
            raw_kosh_name = request.POST.get('kosh_name', '').strip()
            raw_kosh_code = request.POST.get('kosh_code', '').strip()
            raw_is_primary = request.POST.get('is_primary', 'False')
            raw_status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            kosh_name = validate_clean_text(raw_kosh_name)
            kosh_code = validate_clean_text(raw_kosh_code) if raw_kosh_code else None
            
            if not kosh_name:
                messages.error(request, 'कोष नाव आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
        
            # If is_primary is True, unset other primary kosh for this Gram Panchayat
            is_primary = raw_is_primary == 'True'
            if is_primary and not edit_kosh.is_primary:
                Kosh.objects.filter(grampanchayat=gram_panchayat, is_primary=True).update(is_primary=False)
            
            # Update record
            edit_kosh.kosh_name = kosh_name
            edit_kosh.kosh_code = kosh_code
            edit_kosh.is_primary = is_primary
            edit_kosh.status = raw_status
            edit_kosh.save()
            
            messages.success(request, 'कोष यशस्वीरित्या अद्यतनित केला')
            return redirect('Kosh-Management', grampanchayat_id=grampanchayat_id)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # Get all Kosh records for this Gram Panchayat (for display)
    kosh_list = Kosh.objects.filter(
        grampanchayat=gram_panchayat,
        is_deleted=False
    ).order_by('-id')
    
    total_kosh = kosh_list.count()
    active_count = kosh_list.filter(status='Active').count()
    primary_count = kosh_list.filter(is_primary=True).count()
    
    # Filters
    kosh_name = request.GET.get('kosh_name', '').strip()
    kosh_code = request.GET.get('kosh_code', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')
    
    if reset:
        kosh_name = ''
        kosh_code = ''
        status_filter = 'all'
    
    if status_filter == 'active':
        kosh_list = kosh_list.filter(status='Active')
    elif status_filter == 'inactive':
        kosh_list = kosh_list.filter(status='Inactive')
    elif status_filter == 'closed':
        kosh_list = kosh_list.filter(status='Closed')
    
    if kosh_name:
        kosh_list = kosh_list.filter(kosh_name__icontains=kosh_name)
    if kosh_code:
        kosh_list = kosh_list.filter(kosh_code__icontains=kosh_code)
    
    filtered_count = kosh_list.count()
    
    # Pagination
    paginator = Paginator(kosh_list, 15)
    page_number = request.GET.get('page', 1)
    kosh_page = paginator.get_page(page_number)
    start_index = (kosh_page.number - 1) * paginator.per_page + 1
    
    context = {
        'user': user,
        'gram_panchayat': gram_panchayat,
        'edit_kosh': edit_kosh,
        'kosh_list': kosh_page,
        'total_kosh': total_kosh,
        'filtered_count': filtered_count,
        'active_count': active_count,
        'primary_count': primary_count,
        'start_index': start_index,
        'kosh_name': kosh_name,
        'kosh_code': kosh_code,
        'status_filter': status_filter,
        'cast_categories': cast_categories,
        'financial_years': financial_years,
        'population_list': population_list,  
        'total_population_list': total_population_list,
        'bank_details_list': bank_details_list,

    }
    
    return render(request, 'Kosh-Edit.html', context)


# ================= SINGLE VIEW FOR POPULATION MANAGEMENT (ADD, EDIT, DELETE) =================

def Kosh_Population_Manage(request, grampanchayat_id, kosh_id, population_id=None):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get Kosh
    try:
        kosh = Kosh.objects.get(
            id=kosh_id,
            is_deleted=False
        )
    except Kosh.DoesNotExist:
        messages.error(request, 'कोष सापडला नाही')
        return redirect('Kosh-Manage-Grampanchayat')
    
    # ================= ADD POPULATION =================
    if request.method == 'POST' and 'add_population' in request.POST:
        try:
            cast_category_id = request.POST.get('cast_category_id')
            financial_year_id = request.POST.get('financial_year_id')
            raw_population_count = request.POST.get('population_count')
            status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            population_count = validate_clean_text(raw_population_count) if raw_population_count else ''
            
            # Validate required fields
            if not cast_category_id:
                messages.error(request, 'जात श्रेणी निवड आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not financial_year_id:
                messages.error(request, 'आर्थिक वर्ष निवड आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not population_count:
                messages.error(request, 'लोकसंख्या आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Check if population already exists for this category and year
            existing = Kosh_Population.objects.filter(
                kosh=kosh,
                cast_category_id=cast_category_id,
                financial_year_id=financial_year_id
            ).first()
            
            if existing:
                messages.error(request, 'या जात श्रेणी आणि आर्थिक वर्षासाठी लोकसंख्या आधीपासून अस्तित्वात आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Create population record
            Kosh_Population.objects.create(
                kosh=kosh,
                cast_category_id=cast_category_id,
                financial_year_id=financial_year_id,
                population_count=population_count,
                status=status
            )
            
            messages.success(request, 'लोकसंख्या यशस्वीरित्या जोडली')
            
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= EDIT POPULATION =================
    if request.method == 'POST' and 'edit_population' in request.POST and population_id:
        try:
            population = Kosh_Population.objects.get(id=population_id)
            
            cast_category_id = request.POST.get('cast_category_id')
            financial_year_id = request.POST.get('financial_year_id')
            raw_population_count = request.POST.get('population_count')
            status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            population_count = validate_clean_text(raw_population_count) if raw_population_count else ''
            
            # Validate required fields
            if not cast_category_id:
                messages.error(request, 'जात श्रेणी निवड आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not financial_year_id:
                messages.error(request, 'आर्थिक वर्ष निवड आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not population_count:
                messages.error(request, 'लोकसंख्या आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Check if population already exists for this category and year (excluding current)
            existing = Kosh_Population.objects.filter(
                kosh=kosh,
                cast_category_id=cast_category_id,
                financial_year_id=financial_year_id
            ).exclude(id=population_id).first()   

            if existing:
                messages.error(request, 'या जात श्रेणी आणि आर्थिक वर्षासाठी लोकसंख्या आधीपासून अस्तित्वात आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Update population record
            population.cast_category_id = cast_category_id
            population.financial_year_id = financial_year_id
            population.population_count = population_count
            population.status = status
            population.save()
            
            messages.success(request, 'लोकसंख्या यशस्वीरित्या अद्यतनित केली')
            
        except Kosh_Population.DoesNotExist:
            messages.error(request, 'लोकसंख्या सापडली नाही')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= DELETE POPULATION =================
    if request.method == 'POST' and 'delete_population' in request.POST and population_id:
        try:
            population = Kosh_Population.objects.get(id=population_id)
            population.delete()
            messages.success(request, 'लोकसंख्या यशस्वीरित्या हटविली')
        except Kosh_Population.DoesNotExist:
            messages.error(request, 'लोकसंख्या सापडली नाही')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # If no valid operation, redirect back
    return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
# ================= TOTAL POPULATION MANAGEMENT =================
def Kosh_Total_Population_Manage(request, grampanchayat_id, kosh_id, total_population_id=None):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get Kosh
    try:
        kosh = Kosh.objects.get(id=kosh_id, is_deleted=False)
    except Kosh.DoesNotExist:
        messages.error(request, 'कोष सापडला नाही')
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= ADD TOTAL POPULATION =================
    if request.method == 'POST' and 'add_total_population' in request.POST:
        try:
            financial_year_id = request.POST.get('financial_year_id')
            raw_total_population = request.POST.get('total_population')
            raw_tribal_population = request.POST.get('tribal_population', 0)
            
            # Apply clean_text validation
            total_population = validate_clean_text(raw_total_population) if raw_total_population else ''
            tribal_population = validate_clean_text(raw_tribal_population) if raw_tribal_population else 0
            
            if not financial_year_id:
                messages.error(request, 'आर्थिक वर्ष निवड आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not total_population:
                messages.error(request, 'एकूण लोकसंख्या आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Get financial year for message
            financial_year = Financial_Year.objects.get(id=financial_year_id)
            
            # Check if total population already exists for this year
            existing = Kosh_Total_Population.objects.filter(
                kosh=kosh,
                financial_year_id=financial_year_id
            ).first()
            
            if existing:
                existing_fy = Financial_Year.objects.get(id=existing.financial_year_id)
                messages.warning(
                    request, 
                    f'⚠️ आर्थिक वर्ष {existing_fy.year} साठी एकूण लोकसंख्या आधीपासून अस्तित्वात आहे. कृपया वेगळे आर्थिक वर्ष निवडा.'
                )
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Create record
            Kosh_Total_Population.objects.create(
                kosh=kosh,
                financial_year_id=financial_year_id,
                total_population=total_population,
                tribal_population=int(tribal_population) if tribal_population else 0
            )
            
            messages.success(request, f'✅ आर्थिक वर्ष {financial_year.year} साठी एकूण लोकसंख्या यशस्वीरित्या जोडली')
            
        except Financial_Year.DoesNotExist:
            messages.error(request, 'आर्थिक वर्ष सापडले नाही')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= EDIT TOTAL POPULATION =================
    if request.method == 'POST' and 'edit_total_population' in request.POST and total_population_id:
        try:
            total_pop = Kosh_Total_Population.objects.get(id=total_population_id)
            
            financial_year_id = request.POST.get('financial_year_id')
            raw_total_population = request.POST.get('total_population')
            raw_tribal_population = request.POST.get('tribal_population', 0)
            
            # Apply clean_text validation
            total_population = validate_clean_text(raw_total_population) if raw_total_population else ''
            tribal_population = validate_clean_text(raw_tribal_population) if raw_tribal_population else 0
            
            if not financial_year_id:
                messages.error(request, 'आर्थिक वर्ष निवड आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not total_population:
                messages.error(request, 'एकूण लोकसंख्या आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Get financial year for message
            financial_year = Financial_Year.objects.get(id=financial_year_id)
            
            # Check if total population already exists for this year (excluding current)
            existing = Kosh_Total_Population.objects.filter(
                kosh=kosh,
                financial_year_id=financial_year_id
            ).exclude(id=total_population_id).first()
            
            if existing:
                existing_fy = Financial_Year.objects.get(id=existing.financial_year_id)
                messages.warning(
                    request, 
                    f'⚠️ आर्थिक वर्ष {existing_fy.year} साठी एकूण लोकसंख्या आधीपासून अस्तित्वात आहे. कृपया वेगळे आर्थिक वर्ष निवडा.'
                )
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Update record
            total_pop.financial_year_id = financial_year_id
            total_pop.total_population = total_population
            total_pop.tribal_population = int(tribal_population) if tribal_population else 0
            total_pop.save()
            
            messages.success(request, f'✅ आर्थिक वर्ष {financial_year.year} साठी एकूण लोकसंख्या यशस्वीरित्या अद्यतनित केली')
            
        except Kosh_Total_Population.DoesNotExist:
            messages.error(request, 'एकूण लोकसंख्या सापडली नाही')
        except Financial_Year.DoesNotExist:
            messages.error(request, 'आर्थिक वर्ष सापडले नाही')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= DELETE TOTAL POPULATION =================
    if request.method == 'POST' and 'delete_total_population' in request.POST and total_population_id:
        try:
            total_pop = Kosh_Total_Population.objects.get(id=total_population_id)
            financial_year_name = total_pop.financial_year.year if total_pop.financial_year else 'Unknown'
            total_pop.delete()
            messages.success(request, f'✅ आर्थिक वर्ष {financial_year_name} साठी एकूण लोकसंख्या यशस्वीरित्या हटविली')
        except Kosh_Total_Population.DoesNotExist:
            messages.error(request, 'एकूण लोकसंख्या सापडली नाही')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)




# ================= BANK DETAILS MANAGEMENT =================
def Kosh_Bank_Detail_Manage(request, grampanchayat_id, kosh_id, bank_detail_id=None):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get Kosh
    try:
        kosh = Kosh.objects.get(id=kosh_id, is_deleted=False)
    except Kosh.DoesNotExist:
        messages.error(request, 'कोष सापडला नाही')
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= ADD BANK DETAIL =================
    if request.method == 'POST' and 'add_bank_detail' in request.POST:
        try:
            raw_bank_name = request.POST.get('bank_name', '').strip()
            raw_branch_name = request.POST.get('branch_name', '').strip()
            raw_account_holder_name = request.POST.get('account_holder_name', '').strip()
            raw_account_number = request.POST.get('account_number', '').strip()
            raw_ifsc_code = request.POST.get('ifsc_code', '').strip().upper()
            raw_account_type = request.POST.get('account_type', '').strip()
            raw_opening_balance = request.POST.get('opening_balance', 0)
            raw_current_balance = request.POST.get('current_balance', 0)
            raw_bank_address = request.POST.get('bank_address', '').strip()
            status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            bank_name = validate_clean_text(raw_bank_name)
            branch_name = validate_clean_text(raw_branch_name) if raw_branch_name else ""
            account_holder_name = validate_clean_text(raw_account_holder_name) if raw_account_holder_name else ""
            account_number = validate_clean_text(raw_account_number)
            ifsc_code = validate_clean_text(raw_ifsc_code) if raw_ifsc_code else ""
            account_type = validate_clean_text(raw_account_type) if raw_account_type else ""
            bank_address = validate_clean_text(raw_bank_address) if raw_bank_address else ""
            
            if not bank_name:
                messages.error(request, 'बँक नाव आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not account_number:
                messages.error(request, 'खाते क्रमांक आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Check if account number already exists
            existing = Kosh_Bank_Detail.objects.filter(
                kosh=kosh,
                account_number=account_number
            ).first()
            
            if existing:
                messages.warning(request, f'⚠️ खाते क्रमांक {account_number} आधीपासून अस्तित्वात आहे. कृपया वेगळा खाते क्रमांक वापरा.')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # ========== LOGIC: If new bank detail is Active, deactivate all others ==========
            if status == 'Active':
                # Set all other bank details for this Kosh to 'Inactive'
                Kosh_Bank_Detail.objects.filter(kosh=kosh).exclude(id=bank_detail_id if bank_detail_id else None).update(status='Inactive')
            
            # Create record
            bank_detail = Kosh_Bank_Detail(
                kosh=kosh,
                kosh_name=kosh.kosh_name,
                bank_name=bank_name,
                branch_name=branch_name,
                account_holder_name=account_holder_name,
                account_number=account_number,
                ifsc_code=ifsc_code,
                account_type=account_type,
                opening_balance=Decimal(raw_opening_balance) if raw_opening_balance else Decimal(0),
                current_balance=Decimal(raw_current_balance) if raw_current_balance else Decimal(0),
                bank_address=bank_address,
                status=status
            )
            
            bank_detail.save()
            
            messages.success(request, f'✅ बँक तपशील "{bank_name}" यशस्वीरित्या जोडला')
            
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= EDIT BANK DETAIL =================
    if request.method == 'POST' and 'edit_bank_detail' in request.POST and bank_detail_id:
        try:
            bank = Kosh_Bank_Detail.objects.get(id=bank_detail_id)
            
            raw_bank_name = request.POST.get('bank_name', '').strip()
            raw_branch_name = request.POST.get('branch_name', '').strip()
            raw_account_holder_name = request.POST.get('account_holder_name', '').strip()
            raw_account_number = request.POST.get('account_number', '').strip()
            raw_ifsc_code = request.POST.get('ifsc_code', '').strip().upper()
            raw_account_type = request.POST.get('account_type', '').strip()
            raw_opening_balance = request.POST.get('opening_balance', 0)
            raw_current_balance = request.POST.get('current_balance', 0)
            raw_bank_address = request.POST.get('bank_address', '').strip()
            new_status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            bank_name = validate_clean_text(raw_bank_name)
            branch_name = validate_clean_text(raw_branch_name) if raw_branch_name else ""
            account_holder_name = validate_clean_text(raw_account_holder_name) if raw_account_holder_name else ""
            account_number = validate_clean_text(raw_account_number)
            ifsc_code = validate_clean_text(raw_ifsc_code) if raw_ifsc_code else ""
            account_type = validate_clean_text(raw_account_type) if raw_account_type else ""
            bank_address = validate_clean_text(raw_bank_address) if raw_bank_address else ""
            
            if not bank_name:
                messages.error(request, 'बँक नाव आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            if not account_number:
                messages.error(request, 'खाते क्रमांक आवश्यक आहे')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # Check if account number already exists (excluding current)
            existing = Kosh_Bank_Detail.objects.filter(
                kosh=kosh,
                account_number=account_number
            ).exclude(id=bank_detail_id).first()
            
            if existing:
                messages.warning(request, f'⚠️ खाते क्रमांक {account_number} आधीपासून अस्तित्वात आहे. कृपया वेगळा खाते क्रमांक वापरा.')
                return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
            
            # ========== LOGIC: If updating to Active, deactivate all others ==========
            if new_status == 'Active' and bank.status != 'Active':
                # Set all other bank details for this Kosh to 'Inactive'
                Kosh_Bank_Detail.objects.filter(kosh=kosh).exclude(id=bank_detail_id).update(status='Inactive')
            
            # Update record
            bank.bank_name = bank_name
            bank.branch_name = branch_name
            bank.account_holder_name = account_holder_name
            bank.account_number = account_number
            bank.ifsc_code = ifsc_code
            bank.account_type = account_type
            bank.opening_balance = Decimal(raw_opening_balance) if raw_opening_balance else Decimal(0)
            bank.current_balance = Decimal(raw_current_balance) if raw_current_balance else Decimal(0)
            bank.bank_address = bank_address
            bank.status = new_status
            bank.save()
            
            messages.success(request, f'✅ बँक तपशील "{bank_name}" यशस्वीरित्या अद्यतनित केला')
            
        except Kosh_Bank_Detail.DoesNotExist:
            messages.error(request, 'बँक तपशील सापडला नाही')
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    # ================= DELETE BANK DETAIL =================
    if request.method == 'POST' and 'delete_bank_detail' in request.POST and bank_detail_id:
        try:
            bank = Kosh_Bank_Detail.objects.get(id=bank_detail_id)
            bank_name = bank.bank_name
            
            # Check if we're deleting an Active bank detail
            was_active = (bank.status == 'Active')
            bank.delete()
            
            # If we deleted the Active bank detail, set the most recent one as Active
            if was_active:
                most_recent = Kosh_Bank_Detail.objects.filter(kosh=kosh).order_by('-id').first()
                if most_recent:
                    most_recent.status = 'Active'
                    most_recent.save()
                    messages.info(request, f'⚠️ "{bank_name}" हटवल्यामुळे "{most_recent.bank_name}" ही बँक सक्रिय करण्यात आली.')
            
            messages.success(request, f'✅ बँक तपशील "{bank_name}" यशस्वीरित्या हटविला')
        except Kosh_Bank_Detail.DoesNotExist:
            messages.error(request, 'बँक तपशील सापडला नाही')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
        
        return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)
    
    return redirect('Kosh-Edit', grampanchayat_id=grampanchayat_id, kosh_id=kosh_id)




def Kosh_Users(request, grampanchayat_id):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')    
    
    # Get all Kosh Users with their related Kosh - FIXED field names
    # Use 'grampanchayat' (lowercase) not 'gramPanchayat'
    all_users = Kosh_User.objects.filter(is_retired=False).prefetch_related(
        'kosh__grampanchayat__panchayat_samiti__taluka__district'
    )
    
    total_users = all_users.count()
    
    # ================= FILTERS =================
    kosh_name = request.GET.get('kosh_name', '').strip()
    user_name = request.GET.get('user_name', '').strip()
    mobile = request.GET.get('mobile', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')
    page_num = request.GET.get('page', 1)
    
    if reset:
        kosh_name = ''
        user_name = ''
        mobile = ''
        status_filter = 'all'
    
    # Filter Users
    user_queryset = all_users
    
    if user_name:
        user_queryset = user_queryset.filter(name__icontains=user_name)
    if mobile:
        user_queryset = user_queryset.filter(mobile__icontains=mobile)
    if status_filter == 'active':
        user_queryset = user_queryset.filter(status='Active')
    elif status_filter == 'inactive':
        user_queryset = user_queryset.filter(status='Inactive')
    
    # Filter users by kosh name
    if kosh_name:
        user_queryset = user_queryset.filter(kosh__kosh_name__icontains=kosh_name).distinct()
    
    # Pagination for Users
    paginator = Paginator(user_queryset, 15)
    user_page = paginator.get_page(page_num)
    user_start_index = (user_page.number - 1) * paginator.per_page + 1
    
    context = {
        'user_type': 'Kosh',
        'kosh_user': all_users,
        'user_list': user_page,
        'total_users': total_users,
        'user_start_index': user_start_index,
        'kosh_name': kosh_name,
        'user_name': user_name,
        'mobile': mobile,
        'status_filter': status_filter,
        'grampanchayat_id': grampanchayat_id,
    }
    
    return render(request, 'Kosh-Users.html', context)



    
def Kosh_Add_User(request, grampanchayat_id):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        super_user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get Gram Panchayat
    try:
        gram_panchayat = GramPanchayat.objects.get(
            id=grampanchayat_id, 
            is_deleted=False,
            status='Active'
        )
    except GramPanchayat.DoesNotExist:
        messages.error(request, 'ग्रामपंचायत सापडली नाही')
        return redirect('Kosh-Manage-Grampanchayat')
    
    # Get all active Kosh under this Gram Panchayat - FIXED: use 'grampanchayat' not 'gramPanchayat'
    all_kosh = Kosh.objects.filter(
        grampanchayat=gram_panchayat,  # Changed from gramPanchayat to grampanchayat
        status='Active', 
        is_deleted=False
    ).select_related('grampanchayat')
    
    # ================= ADD USER =================
    if request.method == 'POST':
        try:
            raw_name = request.POST.get('name', '').strip()
            raw_mobile = request.POST.get('mobile', '').strip()
            raw_email = request.POST.get('email', '').strip()
            raw_address = request.POST.get('address', '').strip()
            raw_username = request.POST.get('username', '').strip()
            raw_password = request.POST.get('password', '').strip()
            kosh_ids = request.POST.getlist('kosh_ids')
            status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            name = validate_clean_text(raw_name)
            username = validate_clean_text(raw_username)
            address = validate_clean_text(raw_address) if raw_address else None
            
            # Mobile validation (digits only)
            mobile = ''.join(filter(str.isdigit, raw_mobile)) if raw_mobile else ''
            if mobile and (len(mobile) != 10 or mobile[0] not in '6789'):
                messages.error(request, 'कृपया 10 अंकी वैध मोबाइल क्रमांक प्रविष्ट करा (सुरुवात 6,7,8,9 ने)')
                return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
            
            
            # Email validation (don't use clean_text)
            email = None
            if raw_email:
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, raw_email):
                    email = raw_email.strip().lower()
                else:
                    messages.error(request, 'कृपया वैध ईमेल पत्ता प्रविष्ट करा')
                    return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
            
            # Validation
            if not name:
                messages.error(request, 'नाव आवश्यक आहे')
                return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
            
            if not username:
                messages.error(request, 'यूजरनेम आवश्यक आहे')
                return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
            
            if not raw_password:
                messages.error(request, 'पासवर्ड आवश्यक आहे')
                return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
            
            # Check if username already exists
            if Kosh_User.objects.filter(username=username).exists():
                messages.error(request, 'हा यूजरनेम आधीपासून अस्तित्वात आहे')
                return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
                        
            # Handle profile image upload
            profile = request.FILES.get('profile')
            
            # Create user
            new_user = Kosh_User.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                address=address,
                username=username,
                password=make_password(raw_password),
                status=status
            )
            
            # Add profile image if provided
            if profile:
                new_user.profile = profile
                new_user.save()
            
            # Add Kosh relationships (Many-to-Many)
            if kosh_ids:
                new_user.kosh.set(kosh_ids)
                kosh_names = Kosh.objects.filter(id__in=kosh_ids).values_list('kosh_name', flat=True)
                new_user.kosh_name = ', '.join(kosh_names)
                new_user.save()
            
            messages.success(request, f'✅ यूजर "{name}" यशस्वीरित्या जोडला')
            return redirect('Kosh-Users-With-GP', grampanchayat_id=grampanchayat_id)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('Kosh-Add-User', grampanchayat_id=grampanchayat_id)
    
    context = {
        'super_user': super_user,
        'gram_panchayat': gram_panchayat,
        'all_kosh': all_kosh,
        'page_title': 'नवीन कोष यूजर जोडा',
        'button_text': 'यूजर जोडा',
    }
    
    return render(request, 'Kosh-Add-User.html', context)


def Kosh_Edit_User(request, grampanchayat_id, kosh_user_id):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    
    try:
        super_user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    
    # Get Gram Panchayat
    try:
        gram_panchayat = GramPanchayat.objects.get(
            id=grampanchayat_id, 
            is_deleted=False,
            status='Active'
        )
    except GramPanchayat.DoesNotExist:
        messages.error(request, 'ग्रामपंचायत सापडली नाही')
        return redirect('Kosh-Manage-Grampanchayat')
    
    # Get Kosh User
    try:
        edit_user = Kosh_User.objects.get(id=kosh_user_id, is_retired=False)
    except Kosh_User.DoesNotExist:
        messages.error(request, 'यूजर सापडला नाही')
        return redirect('Kosh-Users-With-GP', grampanchayat_id=grampanchayat_id)
    
    # Get all active Kosh under this Gram Panchayat - FIXED: use 'grampanchayat' not 'gramPanchayat'
    all_kosh = Kosh.objects.filter(
        grampanchayat=gram_panchayat,  # Changed from gramPanchayat to grampanchayat
        status='Active', 
        is_deleted=False
    ).select_related('grampanchayat')
    
    # Get selected Kosh IDs for this user
    selected_kosh_ids = list(edit_user.kosh.values_list('id', flat=True))
    
    # ================= EDIT USER =================
    if request.method == 'POST':
        try:
            raw_name = request.POST.get('name', '').strip()
            raw_mobile = request.POST.get('mobile', '').strip()
            raw_email = request.POST.get('email', '').strip()
            raw_address = request.POST.get('address', '').strip()
            raw_username = request.POST.get('username', '').strip()
            raw_password = request.POST.get('password', '').strip()
            kosh_ids = request.POST.getlist('kosh_ids')
            status = request.POST.get('status', 'Active')
            
            # Apply clean_text validation
            name = validate_clean_text(raw_name)
            username = validate_clean_text(raw_username)
            address = validate_clean_text(raw_address) if raw_address else None
            
            # Mobile validation (digits only)
            mobile = ''.join(filter(str.isdigit, raw_mobile)) if raw_mobile else ''
            if mobile and (len(mobile) != 10 or mobile[0] not in '6789'):
                messages.error(request, 'कृपया 10 अंकी वैध मोबाइल क्रमांक प्रविष्ट करा (सुरुवात 6,7,8,9 ने)')
                return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
            
            if not mobile:
                messages.error(request, 'मोबाइल क्रमांक आवश्यक आहे')
                return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
            
            # Email validation (don't use clean_text)
            email = None
            if raw_email:
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, raw_email):
                    email = raw_email.strip().lower()
                else:
                    messages.error(request, 'कृपया वैध ईमेल पत्ता प्रविष्ट करा')
                    return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
            
            # Validation
            if not name:
                messages.error(request, 'नाव आवश्यक आहे')
                return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
            
            if not username:
                messages.error(request, 'यूजरनेम आवश्यक आहे')
                return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
            
            # Check if username already exists (excluding current)
            if Kosh_User.objects.filter(username=username).exclude(id=kosh_user_id).exists():
                messages.error(request, 'हा यूजरनेम आधीपासून अस्तित्वात आहे')
                return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
            
            # Check if mobile already exists (excluding current)
            if Kosh_User.objects.filter(mobile=mobile).exclude(id=kosh_user_id).exists():
                messages.error(request, 'हा मोबाइल क्रमांक आधीपासून नोंदणीकृत आहे')
                return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
            
            # Handle profile image upload
            profile = request.FILES.get('profile')
            
            # Update user details
            edit_user.name = name
            edit_user.mobile = mobile
            edit_user.email = email
            edit_user.address = address
            edit_user.username = username
            edit_user.status = status
            
            if raw_password:
                edit_user.password = make_password(raw_password)
            
            if profile:
                # Delete old profile if exists
                if edit_user.profile:
                    edit_user.profile.delete()
                edit_user.profile = profile
            
            edit_user.save()
            
            # Update Kosh relationships (Many-to-Many)
            if kosh_ids:
                edit_user.kosh.set(kosh_ids)
                kosh_names = Kosh.objects.filter(id__in=kosh_ids).values_list('kosh_name', flat=True)
                edit_user.kosh_name = ', '.join(kosh_names)
            else:
                edit_user.kosh.clear()
                edit_user.kosh_name = None
            
            edit_user.save()
            
            messages.success(request, f'✅ यूजर "{name}" यशस्वीरित्या अद्यतनित केला')
            return redirect('Kosh-Users-With-GP', grampanchayat_id=grampanchayat_id)
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('Kosh-Edit-User', grampanchayat_id=grampanchayat_id, kosh_user_id=kosh_user_id)
    
    context = {
        'super_user': super_user,
        'gram_panchayat': gram_panchayat,
        'edit_user': edit_user,
        'all_kosh': all_kosh,
        'selected_kosh_ids': selected_kosh_ids,
        'page_title': 'कोष यूजर संपादित करा',
        'button_text': 'अद्यतनित करा',
    }
    
    return render(request, 'Kosh-Edit-User.html', context)






def Super_User_Kosh_Add_Grampanchayat(request):
    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')
    try:
        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )
    except Super_User.DoesNotExist:
        request.session.flush()
        return redirect('SuperUser-Login')
    if request.method == 'POST':
        try:
            panchayat_samiti_id = request.POST.get('panchayat_samiti')
            panchayat_samiti_name = request.POST.get('panchayat_samiti_name')
            gram_panchayat_name = request.POST.get('gram_panchayat_name')
            gram_panchayat_code = request.POST.get('gram_panchayat_code')
            address = request.POST.get('address')
            status = request.POST.get('status')

            panchayat_samiti = None
            if panchayat_samiti_id:
                panchayat_samiti = Panchayat_Samiti.objects.get(
                    id=panchayat_samiti_id
                )

            GramPanchayat.objects.create(
                panchayat_samiti=panchayat_samiti,
                panchayat_samiti_name=panchayat_samiti_name,
                gram_panchayat_name=gram_panchayat_name,
                gram_panchayat_code=gram_panchayat_code,
                address=address,
                status=status
            )

            messages.success(request, "ग्रामपंचायत माहिती यशस्वीरित्या जतन करण्यात आली.")
            return redirect('Super_User_Kosh_Add_Grampanchayat')

        except Exception as e:
            messages.error(request, f"त्रुटी : {str(e)}")

    panchayat_samiti_list = Panchayat_Samiti.objects.all().order_by(
        'panchayat_samiti_name'
    )

    context = {
        'user':user,
        'panchayat_samiti_list': panchayat_samiti_list,
    }
    return render(request, 'Super_User_Kosh_Add_Grampanchayat.html', context)




def Kosh_Manage_Kosh_Committee(request):

    # =====================================================
    # LOGIN CHECK
    # =====================================================

    if not request.session.get('user_id') or request.session.get('user_type') != 'Kosh':
        return redirect('Login')

    # =====================================================
    # USER CHECK
    # =====================================================

    try:
        kosh_user = Kosh_User.objects.get(
            id=request.session.get('user_id'),
            status='Active'
        )
    except Kosh_User.DoesNotExist:
        request.session.flush()
        return redirect('Login')

    active_kosh_id = request.session.get('active_kosh_id')
    if not active_kosh_id:
        messages.error(request, "No active Kosh found. Please login again.")
        return redirect('Login')

    try:
        active_kosh = Kosh.objects.get(id=active_kosh_id, status='Active', is_deleted=False)
    except Kosh.DoesNotExist:
        messages.error(request, "Active Kosh not found.")
        return redirect('Kosh_Dashboard')

    # =====================================================
    # ADD COMMITTEE MEMBER
    # =====================================================

    if request.method == "POST" and request.POST.get("action") == "add":

        name     = request.POST.get("name", "").strip()
        mobile   = request.POST.get("mobile", "").strip()
        email    = request.POST.get("email", "").strip()
        address  = request.POST.get("address", "").strip()
        role     = request.POST.get("role", "").strip()
        status   = request.POST.get("status", "Active").strip()
        profile  = request.FILES.get("profile")

        # ── Profile validation ──
        if profile:
            if not validate_file(
                file=profile,
                request=request,
                max_size_mb=2,
                allowed_extensions=["jpg", "jpeg", "png"]
            ):
                return redirect("Kosh-Manage-Kosh-Committee")

        # ── Required fields ──
        if not name:
            messages.error(request, "Name is required.")
            return redirect("Kosh-Manage-Kosh-Committee")

        if not role:
            messages.error(request, "Role is required.")
            return redirect("Kosh-Manage-Kosh-Committee")

        # ── Field validation ──
        try:
            validate_clean_text(name, "Name")

            if address:
                validate_clean_text(address, "Address")

            if role:
                validate_clean_text(role, "Role")

            if mobile:
                validate_mobile_number(mobile)

            # if email:
            #     validate_email(email)

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("Kosh-Manage-Kosh-Committee")

        # ── Create ──
        Kosh_Committee.objects.create(
            kosh=active_kosh,
            kosh_name=active_kosh.kosh_name,
            name=name,
            mobile=mobile,
            email=email,
            address=address,
            role=role,
            profile=profile,
            status=status
        )

        messages.success(request, "Committee member added successfully.")
        return redirect("Kosh-Manage-Kosh-Committee")

    # =====================================================
    # EDIT COMMITTEE MEMBER
    # =====================================================

    if request.method == "POST" and request.POST.get("action") == "edit":

        edit_id = request.POST.get("edit_id")
        obj     = get_object_or_404(Kosh_Committee, id=edit_id, kosh=active_kosh)

        name    = request.POST.get("name", "").strip()
        mobile  = request.POST.get("mobile", "").strip()
        email   = request.POST.get("email", "").strip()
        address = request.POST.get("address", "").strip()
        role    = request.POST.get("role", "").strip()
        status  = request.POST.get("status", "Active").strip()
        profile = request.FILES.get("profile")

        # ── Profile validation ──
        if profile:
            if not validate_file(
                file=profile,
                request=request,
                max_size_mb=2,
                allowed_extensions=["jpg", "jpeg", "png"]
            ):
                return redirect("Kosh-Manage-Kosh-Committee")

        # ── Required fields ──
        if not name:
            messages.error(request, "Name is required.")
            return redirect("Kosh-Manage-Kosh-Committee")

        if not role:
            messages.error(request, "Role is required.")
            return redirect("Kosh-Manage-Kosh-Committee")

        # ── Field validation ──
        try:
            validate_clean_text(name, "Name")

            if address:
                validate_clean_text(address, "Address")

            if role:
                validate_clean_text(role, "Role")

            if mobile:
                validate_mobile_number(mobile)

            # if email:
            #     validate_email(email)

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("Kosh-Manage-Kosh-Committee")

        # ── Update ──
        obj.name       = name
        obj.mobile     = mobile
        obj.email      = email
        obj.address    = address
        obj.role       = role
        obj.status     = status

        if profile:
            obj.profile = profile

        obj.save()

        messages.success(request, "Committee member updated successfully.")
        return redirect("Kosh-Manage-Kosh-Committee")

    # =====================================================
    # DELETE COMMITTEE MEMBER
    # =====================================================

    if request.GET.get("delete_id"):
        delete_id = request.GET.get("delete_id")
        obj       = get_object_or_404(Kosh_Committee, id=delete_id, kosh=active_kosh)
        obj.delete()

        messages.success(request, "Committee member deleted successfully.")
        return redirect("Kosh-Manage-Kosh-Committee")

    # =====================================================
    # SEARCH + FILTER
    # =====================================================

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()
    role   = request.GET.get("role", "").strip()

    members = Kosh_Committee.objects.filter(
        kosh=active_kosh
    ).order_by("-id")

    if search:
        members = members.filter(
            Q(name__icontains=search)   |
            Q(mobile__icontains=search) |
            Q(email__icontains=search)  |
            Q(role__icontains=search)
        )

    if status:
        members = members.filter(status=status)

    if role:
        members = members.filter(role=role)

    # =====================================================
    # COUNTS
    # =====================================================

    total_members    = Kosh_Committee.objects.filter(kosh=active_kosh).count()
    filtered_count   = members.count()
    chairman_count   = Kosh_Committee.objects.filter(kosh=active_kosh, role='Chairman', status='Active').count()
    member_count     = Kosh_Committee.objects.filter(kosh=active_kosh, role='Member',   status='Active').count()

    # =====================================================
    # PAGINATION
    # =====================================================

    paginator   = Paginator(members, 10)
    page_number = request.GET.get("page")
    members     = paginator.get_page(page_number)

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {
        "kosh_user":       kosh_user,
        "active_kosh":     active_kosh,
        "members":         members,
        "search":          search or '',
        "status":          status or '',
        "role":            role or '',
        "total_members":   total_members,
        "filtered_count":  filtered_count,
        "chairman_count":  chairman_count,
        "member_count":    member_count,
        'user_type': 'Kosh',
        **switch_kosh(request),

    }

    return render(request, "Kosh-Manage-Kosh-Committee.html", context)




def Kosh_fund_alloted_details(request):

    # =========================
    # LOGIN CHECK
    # =========================
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # =========================
    # FUND ALLOCATION DATA
    # =========================
    fund_allocations = Kosh_Fund_Allocation.objects.all()

    context = {
        'kosh_user': kosh_user,
        'fund_allocations': fund_allocations,
    }

    return render(request, 'Kosh_fund_alloted_details.html', context)