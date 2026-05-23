from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from Main.models import District, Super_User, Taluka
from Main.utils import validate_clean_text, validate_email_field, validate_mobile_number
from ZillaParishad.models import Zilla_Parishad_User
from PanchayatSamiti.models import Panchayat_Samiti, Panchayat_Samiti_User
from Kosh.models import Kosh_User
from django.contrib import messages
from ZillaParishad.models import Zilla_Parishad
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import json
from django.http import JsonResponse
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

def PanchayatSamiti_Dashboard(request):


    context = {

        'user_type': 'Panchayat Samiti'

    }

    return render(
        request,
        'Panchayat_samiti_dashboard.html',
        context
    )





################################### Superuser Management ####################################
def PS_Manage_Panchayat_Samitis(request):
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

    # Get all districts and talukas for dropdown
    all_districts = District.objects.all().order_by('name')
    
    # Create a dictionary of talukas grouped by district for JavaScript
    talukas_by_district = {}
    for district in all_districts:
        talukas_by_district[str(district.id)] = list(
            Taluka.objects.filter(district=district).values('id', 'name').order_by('name')
        )
    
    # For edit modals - get all talukas with district info
    all_talukas_with_district = Taluka.objects.select_related('district').all().order_by('name')

    # ================= ADD =================
    if request.method == 'POST' and 'add_samiti' in request.POST:
        try:
            # Get raw values and apply clean_text
            raw_panchayat_samiti_name = request.POST.get('panchayat_samiti_name', '').strip()
            raw_district_id = request.POST.get('district_id', '').strip()
            raw_taluka_id = request.POST.get('taluka_id', '').strip()
            raw_panchayat_samiti_code = request.POST.get('panchayat_samiti_code', '').strip()
            raw_status = request.POST.get('status', 'Active')

            # Apply clean_text validation
            panchayat_samiti_name = validate_clean_text(raw_panchayat_samiti_name)
            panchayat_samiti_code = validate_clean_text(raw_panchayat_samiti_code)

            # Validate required fields
            if not panchayat_samiti_name:
                messages.error(request, 'समितीचे नाव आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not raw_district_id:
                messages.error(request, 'जिल्हा निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not raw_taluka_id:
                messages.error(request, 'तालुका निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            


            try:
                district = District.objects.get(id=raw_district_id)
            except District.DoesNotExist:
                messages.error(request, 'अवैध जिल्हा निवडला')
                return redirect('PS-Manage-Panchayat-Samitis')

            try:
                taluka = Taluka.objects.get(id=raw_taluka_id, district=district)
            except Taluka.DoesNotExist:
                messages.error(request, 'अवैध तालुका निवडला')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Check duplicate code
            if Panchayat_Samiti.objects.filter(panchayat_samiti_code=panchayat_samiti_code).exists():
                messages.error(request, 'हा समिती कोड आधीपासून अस्तित्वात आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Get Zilla Parishad from District (if you have Zilla_Parishad model)
            zilla_parishad = None
            zilla_parishad_name = None
            # If you have Zilla_Parishad model related to District, uncomment below
            # if hasattr(district, 'zilla_parishad'):
            #     zilla_parishad = district.zilla_parishad
            #     zilla_parishad_name = district.zilla_parishad.name

            # Create record
            Panchayat_Samiti.objects.create(
                panchayat_samiti_name=panchayat_samiti_name,
                zilla_parishad=zilla_parishad,
                zilla_parishad_name=zilla_parishad_name,
                taluka=taluka,
                panchayat_samiti_code=panchayat_samiti_code,
                status=raw_status
            )

            messages.success(request, 'पंचायत समिती यशस्वीरित्या जोडली')
            return redirect('PS-Manage-Panchayat-Samitis')

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('PS-Manage-Panchayat-Samitis')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('PS-Manage-Panchayat-Samitis')

    # ================= EDIT =================
    if request.method == 'POST' and 'edit_samiti' in request.POST:
        samiti_id = request.POST.get('samiti_id', '').strip()

        if not samiti_id:
            messages.error(request, 'अवैध विनंती')
            return redirect('PS-Manage-Panchayat-Samitis')

        try:
            samiti = Panchayat_Samiti.objects.get(id=samiti_id)
        except Panchayat_Samiti.DoesNotExist:
            messages.error(request, 'पंचायत समिती सापडली नाही')
            return redirect('PS-Manage-Panchayat-Samitis')

        try:
            # Get raw values and apply clean_text
            raw_panchayat_samiti_name = request.POST.get('panchayat_samiti_name', '').strip()
            raw_district_id = request.POST.get('district_id', '').strip()
            raw_taluka_id = request.POST.get('taluka_id', '').strip()
            raw_panchayat_samiti_code = request.POST.get('panchayat_samiti_code', '').strip()
            raw_status = request.POST.get('status', 'Active')

            # Apply clean_text validation
            panchayat_samiti_name = validate_clean_text(raw_panchayat_samiti_name)
            panchayat_samiti_code = validate_clean_text(raw_panchayat_samiti_code)

            # Validate required fields
            if not panchayat_samiti_name:
                messages.error(request, 'समितीचे नाव आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not raw_district_id:
                messages.error(request, 'जिल्हा निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not raw_taluka_id:
                messages.error(request, 'तालुका निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            

            try:
                district = District.objects.get(id=raw_district_id)
            except District.DoesNotExist:
                messages.error(request, 'अवैध जिल्हा निवडला')
                return redirect('PS-Manage-Panchayat-Samitis')

            try:
                taluka = Taluka.objects.get(id=raw_taluka_id, district=district)
            except Taluka.DoesNotExist:
                messages.error(request, 'अवैध तालुका निवडला')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Check duplicate code (excluding current)
            if Panchayat_Samiti.objects.filter(panchayat_samiti_code=panchayat_samiti_code).exclude(id=samiti_id).exists():
                messages.error(request, 'हा समिती कोड आधीपासून अस्तित्वात आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Get Zilla Parishad from District
            zilla_parishad = None
            zilla_parishad_name = None
            # If you have Zilla_Parishad model related to District, uncomment below
            # if hasattr(district, 'zilla_parishad'):
            #     zilla_parishad = district.zilla_parishad
            #     zilla_parishad_name = district.zilla_parishad.name

            # Update record
            samiti.panchayat_samiti_name = panchayat_samiti_name
            samiti.zilla_parishad = zilla_parishad
            samiti.zilla_parishad_name = zilla_parishad_name
            samiti.taluka = taluka
            samiti.panchayat_samiti_code = panchayat_samiti_code
            samiti.status = raw_status
            samiti.save()

            messages.success(request, 'पंचायत समिती यशस्वीरित्या अद्यतनित केली')
            return redirect('PS-Manage-Panchayat-Samitis')

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('PS-Manage-Panchayat-Samitis')
        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
            return redirect('PS-Manage-Panchayat-Samitis')

    # ================= DELETE =================
    if request.method == 'POST' and 'delete_samiti' in request.POST:
        samiti_id = request.POST.get('samiti_id', '').strip()

        if samiti_id:
            try:
                samiti = Panchayat_Samiti.objects.get(id=samiti_id)
                samiti_name = samiti.panchayat_samiti_name
                samiti.delete()
                messages.success(request, f'"{samiti_name}" यशस्वीरित्या हटविले')
            except Panchayat_Samiti.DoesNotExist:
                messages.error(request, 'पंचायत समिती सापडली नाही')

        return redirect('PS-Manage-Panchayat-Samitis')

    # ================= FILTERS =================
    panchayat_samiti_name = request.GET.get('panchayat_samiti_name', '').strip()
    district_name = request.GET.get('district_name', '').strip()
    taluka_name = request.GET.get('taluka_name', '').strip()
    panchayat_samiti_code = request.GET.get('panchayat_samiti_code', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')

    # Reset filters
    if reset:
        panchayat_samiti_name = ''
        district_name = ''
        taluka_name = ''
        panchayat_samiti_code = ''
        status_filter = 'all'

    # Base queryset - order by latest first
    samitis = Panchayat_Samiti.objects.select_related('taluka', 'taluka__district').all()
    total_samitis = samitis.count()
    active_count = Panchayat_Samiti.objects.filter(status='Active').count()

    # Apply status filter
    if status_filter == 'active':
        samitis = samitis.filter(status='Active')
    elif status_filter == 'inactive':
        samitis = samitis.filter(status='Inactive')

    # Apply search filters
    if panchayat_samiti_name:
        samitis = samitis.filter(panchayat_samiti_name__icontains=panchayat_samiti_name)
    if district_name:
        samitis = samitis.filter(taluka__district__name__icontains=district_name)
    if taluka_name:
        samitis = samitis.filter(taluka__name__icontains=taluka_name)
    if panchayat_samiti_code:
        samitis = samitis.filter(panchayat_samiti_code__icontains=panchayat_samiti_code)

    filtered_count = samitis.count()

    # Order by latest first
    samitis = samitis.order_by('-id')

    # Pagination
    paginator = Paginator(samitis, 15)
    page_number = request.GET.get('page', 1)
    samitis_page = paginator.get_page(page_number)
    start_index = (samitis_page.number - 1) * paginator.per_page + 1

    context = {
        'user': user,
        'samitis': samitis_page,
        'total_samitis': total_samitis,
        'filtered_count': filtered_count,
        'active_count': active_count,
        'start_index': start_index,
        'panchayat_samiti_name': panchayat_samiti_name,
        'district_name': district_name,
        'taluka_name': taluka_name,
        'panchayat_samiti_code': panchayat_samiti_code,
        'status_filter': status_filter,
        'all_districts': all_districts,
        'all_talukas_with_district': all_talukas_with_district,
        'talukas_by_district_json': json.dumps(talukas_by_district),  # Pass as JSON string
    }

    return render(request, 'PS-Manage-Panchayat-Samitis.html', context)


# API endpoint for getting talukas
def get_talukas_by_district(request, district_id):
    """API endpoint to get talukas for a specific district"""
    try:
        talukas = Taluka.objects.filter(district_id=district_id).values('id', 'name').order_by('name')
        talukas_list = list(talukas)
        return JsonResponse({
            'success': True, 
            'talukas': talukas_list,
            'count': len(talukas_list)
        })
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e), 
            'talukas': []
        })





def PS_Manage_Users(request):
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

    # Get all Panchayat Samitis for dropdown
    panchayat_samitis = Panchayat_Samiti.objects.filter(status='Active')

    # ================= ADD =================
    if request.method == 'POST' and 'add_user' in request.POST:
        try:
            # Get raw values
            raw_panchayat_samiti_id = request.POST.get('panchayat_samiti_id', '').strip()
            raw_name = request.POST.get('name', '').strip()
            raw_mobile = request.POST.get('mobile', '').strip()
            raw_email = request.POST.get('email', '').strip()
            raw_address = request.POST.get('address', '').strip()
            raw_username = request.POST.get('username', '').strip()
            raw_password = request.POST.get('password', '').strip()
            status = request.POST.get('status', 'Active')

            # Validate using your validation functions
            name = validate_clean_text(raw_name)
            username = validate_clean_text(raw_username)
            password = validate_clean_text(raw_password)
            address = validate_clean_text(raw_address)
            
            # Validate email if provided
            email = ""
            if raw_email:
                email = validate_email_field(raw_email)
            
            # Validate mobile if provided
            mobile = ""
            if raw_mobile:
                mobile = validate_mobile_number(raw_mobile)

        except ValidationError as ve:
            messages.warning(request, f"⚠ Validation Warning: {ve}")
            return redirect('PS-Manage-Users')

        # Validation
        if not name:
            messages.error(request, 'नाव आवश्यक आहे')
            return redirect('PS-Manage-Users')

        if not username:
            messages.error(request, 'यूजरनेम आवश्यक आहे')
            return redirect('PS-Manage-Users')

        if not password:
            messages.error(request, 'पासवर्ड आवश्यक आहे')
            return redirect('PS-Manage-Users')

        # Check duplicate username
        if Panchayat_Samiti_User.objects.filter(username=username).exists():
            messages.error(request, 'हा यूजरनेम आधीपासून अस्तित्वात आहे')
            return redirect('PS-Manage-Users')

        # Get Panchayat Samiti
        panchayat_samiti = None
        if raw_panchayat_samiti_id:
            try:
                panchayat_samiti = Panchayat_Samiti.objects.get(id=raw_panchayat_samiti_id)
            except Panchayat_Samiti.DoesNotExist:
                pass

        # Create Record
        Panchayat_Samiti_User.objects.create(
            panchayat_samiti=panchayat_samiti,
            name=name,
            mobile=mobile,
            email=email,
            address=address,
            username=username,
            password=password,
            status=status
        )

        messages.success(request, 'यूजर यशस्वीरित्या जोडला')
        return redirect('PS-Manage-Users')

    # ================= EDIT =================
    if request.method == 'POST' and 'edit_user' in request.POST:
        user_id = request.POST.get('user_id', '').strip()

        if not user_id:
            messages.error(request, 'अवैध विनंती')
            return redirect('PS-Manage-Users')

        try:
            user_obj = Panchayat_Samiti_User.objects.get(id=user_id)
        except Panchayat_Samiti_User.DoesNotExist:
            messages.error(request, 'यूजर सापडला नाही')
            return redirect('PS-Manage-Users')

        try:
            # Get raw values
            raw_panchayat_samiti_id = request.POST.get('panchayat_samiti_id', '').strip()
            raw_name = request.POST.get('name', '').strip()
            raw_mobile = request.POST.get('mobile', '').strip()
            raw_email = request.POST.get('email', '').strip()
            raw_address = request.POST.get('address', '').strip()
            raw_username = request.POST.get('username', '').strip()
            raw_password = request.POST.get('password', '').strip()
            status = request.POST.get('status', 'Active')

            # Validate using your validation functions
            name = validate_clean_text(raw_name)
            username = validate_clean_text(raw_username)
            address = validate_clean_text(raw_address)
            
            # Validate email if provided
            email = ""
            if raw_email:
                email = validate_email_field(raw_email)
            
            # Validate mobile if provided
            mobile = ""
            if raw_mobile:
                mobile = validate_mobile_number(raw_mobile)

        except ValidationError as ve:
            messages.warning(request, f"⚠ Validation Warning: {ve}")
            return redirect('PS-Manage-Users')

        # Validation
        if not name:
            messages.error(request, 'नाव आवश्यक आहे')
            return redirect('PS-Manage-Users')

        if not username:
            messages.error(request, 'यूजरनेम आवश्यक आहे')
            return redirect('PS-Manage-Users')

        # Check duplicate username (exclude current)
        if Panchayat_Samiti_User.objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, 'हा यूजरनेम आधीपासून अस्तित्वात आहे')
            return redirect('PS-Manage-Users')

        # Get Panchayat Samiti
        panchayat_samiti = None
        if raw_panchayat_samiti_id:
            try:
                panchayat_samiti = Panchayat_Samiti.objects.get(id=raw_panchayat_samiti_id)
            except Panchayat_Samiti.DoesNotExist:
                pass

        # Update Record
        user_obj.panchayat_samiti = panchayat_samiti
        user_obj.name = name
        user_obj.mobile = mobile
        user_obj.email = email
        user_obj.address = address
        user_obj.username = username
        
        # Only update password if provided
        if raw_password:
            user_obj.password = raw_password
        
        user_obj.status = status
        user_obj.save()

        messages.success(request, 'यूजर यशस्वीरित्या अद्यतनित केला')
        return redirect('PS-Manage-Users')

    # ================= DELETE =================
    if request.method == 'POST' and 'delete_user' in request.POST:
        user_id = request.POST.get('user_id', '').strip()

        if user_id:
            try:
                user_obj = Panchayat_Samiti_User.objects.get(id=user_id)
                user_name = user_obj.name
                user_obj.delete()
                messages.success(request, f'"{user_name}" यूजर यशस्वीरित्या हटविला')
            except Panchayat_Samiti_User.DoesNotExist:
                messages.error(request, 'यूजर सापडला नाही')

        return redirect('PS-Manage-Users')

    # ================= FILTERS =================
    name = request.GET.get('name', '').strip()
    mobile = request.GET.get('mobile', '').strip()
    email = request.GET.get('email', '').strip()
    username = request.GET.get('username', '').strip()
    panchayat_samiti_filter = request.GET.get('panchayat_samiti', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')

    # Reset
    if reset:
        name = ''
        mobile = ''
        email = ''
        username = ''
        panchayat_samiti_filter = ''
        status_filter = 'all'

    # Base queryset
    if status_filter == 'active':
        users = Panchayat_Samiti_User.objects.filter(status='Active')
    elif status_filter == 'inactive':
        users = Panchayat_Samiti_User.objects.filter(status='Inactive')
    else:
        users = Panchayat_Samiti_User.objects.all()

    total_users = users.count()

    # Search Filters
    if name:
        users = users.filter(name__icontains=name)
    if mobile:
        users = users.filter(mobile__icontains=mobile)
    if email:
        users = users.filter(email__icontains=email)
    if username:
        users = users.filter(username__icontains=username)
    if panchayat_samiti_filter:
        users = users.filter(panchayat_samiti_id=panchayat_samiti_filter)

    filtered_count = users.count()

    # ================= PAGINATION =================
    from django.core.paginator import Paginator
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page', 1)
    users_page = paginator.get_page(page_number)
    start_index = (users_page.number - 1) * paginator.per_page + 1

    context = {
        'user': user,
        'users': users_page,
        'total_users': total_users,
        'filtered_count': filtered_count,
        'start_index': start_index,
        'name': name,
        'mobile': mobile,
        'email': email,
        'username': username,
        'panchayat_samiti_filter': panchayat_samiti_filter,
        'status_filter': status_filter,
        'panchayat_samitis': panchayat_samitis,
    }

    return render(request, 'PS-Manage-Users.html', context)





