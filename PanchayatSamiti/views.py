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
from django.core.paginator import Paginator

def PS_Dashboard(request):


    context = {

        'user_type': 'Panchayat Samiti'

    }

    return render(
        request,
        'PS-Dashboard.html',
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

    # Get all active Zilla Parishads for dropdown
    all_zilla_parishads = Zilla_Parishad.objects.filter(status='Active').select_related('district').order_by('zillaParishad_name')
    
    # Create a dictionary of talukas grouped by district for JavaScript
    talukas_by_district = {}
    all_districts = District.objects.all()
    for district in all_districts:
        talukas_by_district[str(district.id)] = list(
            Taluka.objects.filter(district=district).values('id', 'name').order_by('name')
        )

    # ================= ADD =================
    if request.method == 'POST' and 'add_samiti' in request.POST:
        try:
            # Get raw values
            raw_panchayat_samiti_name = request.POST.get('panchayat_samiti_name', '').strip()
            raw_zilla_parishad_id = request.POST.get('zilla_parishad_id', '').strip()
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
            
            if not raw_zilla_parishad_id:
                messages.error(request, 'जिल्हा परिषद निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not raw_taluka_id:
                messages.error(request, 'तालुका निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            try:
                zilla_parishad = Zilla_Parishad.objects.get(id=raw_zilla_parishad_id, status='Active')
            except Zilla_Parishad.DoesNotExist:
                messages.error(request, 'अवैध जिल्हा परिषद निवडली')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Verify taluka belongs to the district of selected Zilla Parishad
            try:
                taluka = Taluka.objects.get(id=raw_taluka_id, district=zilla_parishad.district)
            except Taluka.DoesNotExist:
                messages.error(request, 'अवैध तालुका निवडला')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Check duplicate code
            if panchayat_samiti_code and Panchayat_Samiti.objects.filter(panchayat_samiti_code=panchayat_samiti_code).exists():
                messages.error(request, 'हा समिती कोड आधीपासून अस्तित्वात आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Create record
            Panchayat_Samiti.objects.create(
                panchayat_samiti_name=panchayat_samiti_name,
                zilla_parishad=zilla_parishad,
                zilla_parishad_name=zilla_parishad.zillaParishad_name,
                taluka=taluka,
                panchayat_samiti_code=panchayat_samiti_code if panchayat_samiti_code else None,
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
            # Get raw values
            raw_panchayat_samiti_name = request.POST.get('panchayat_samiti_name', '').strip()
            raw_zilla_parishad_id = request.POST.get('zilla_parishad_id', '').strip()
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
            
            if not raw_zilla_parishad_id:
                messages.error(request, 'जिल्हा परिषद निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not raw_taluka_id:
                messages.error(request, 'तालुका निवड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            try:
                zilla_parishad = Zilla_Parishad.objects.get(id=raw_zilla_parishad_id, status='Active')
            except Zilla_Parishad.DoesNotExist:
                messages.error(request, 'अवैध जिल्हा परिषद निवडली')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Verify taluka belongs to the district of selected Zilla Parishad
            try:
                taluka = Taluka.objects.get(id=raw_taluka_id, district=zilla_parishad.district)
            except Taluka.DoesNotExist:
                messages.error(request, 'अवैध तालुका निवडला')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Check duplicate code (excluding current)
            if panchayat_samiti_code and Panchayat_Samiti.objects.filter(panchayat_samiti_code=panchayat_samiti_code).exclude(id=samiti_id).exists():
                messages.error(request, 'हा समिती कोड आधीपासून अस्तित्वात आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Update record
            samiti.panchayat_samiti_name = panchayat_samiti_name
            samiti.zilla_parishad = zilla_parishad
            samiti.zilla_parishad_name = zilla_parishad.zillaParishad_name
            samiti.taluka = taluka
            samiti.panchayat_samiti_code = panchayat_samiti_code if panchayat_samiti_code else None
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
    zilla_parishad_name = request.GET.get('zilla_parishad_name', '').strip()
    taluka_name = request.GET.get('taluka_name', '').strip()
    panchayat_samiti_code = request.GET.get('panchayat_samiti_code', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')

    # Reset filters
    if reset:
        panchayat_samiti_name = ''
        zilla_parishad_name = ''
        taluka_name = ''
        panchayat_samiti_code = ''
        status_filter = 'all'

    # Base queryset - order by latest first
    samitis = Panchayat_Samiti.objects.select_related('zilla_parishad', 'taluka', 'taluka__district').all()
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
    if zilla_parishad_name:
        samitis = samitis.filter(zilla_parishad_name__icontains=zilla_parishad_name)
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
        'zilla_parishad_name': zilla_parishad_name,
        'taluka_name': taluka_name,
        'panchayat_samiti_code': panchayat_samiti_code,
        'status_filter': status_filter,
        'all_zilla_parishads': all_zilla_parishads,
        'talukas_by_district_json': json.dumps(talukas_by_district),
    }

    return render(request, 'PS-Manage-Panchayat-Samitis.html', context)

from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
import json

def get_talukas_by_zilla_parishad(request, zilla_parishad_id):
    """API endpoint to get talukas for a specific Zilla Parishad's district"""
    try:
        from ZillaParishad.models import Zilla_Parishad
        from Main.models import Taluka
        
        # Validate zilla_parishad_id
        if not zilla_parishad_id:
            return JsonResponse({
                'success': False, 
                'error': 'Invalid Zilla Parishad ID provided',
                'talukas': []
            })
        
        # Get Zilla Parishad with its district
        try:
            zilla_parishad = Zilla_Parishad.objects.select_related('district').get(id=zilla_parishad_id, status='Active')
            district = zilla_parishad.district
        except Zilla_Parishad.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'Zilla Parishad not found or inactive',
                'talukas': []
            })
        
        if not district:
            return JsonResponse({
                'success': False, 
                'error': 'No district associated with this Zilla Parishad',
                'talukas': []
            })
        
        # Get talukas for the district
        talukas = Taluka.objects.filter(district=district, district__isnull=False).values('id', 'name').order_by('name')
        talukas_list = list(talukas)
        
        print(f"Found {len(talukas_list)} talukas for district {district.name}")  # Debug log
        
        return JsonResponse({
            'success': True, 
            'talukas': talukas_list,
            'count': len(talukas_list),
            'district_name': district.name
        })
        
    except Exception as e:
        print(f"Error in get_talukas_by_zilla_parishad: {str(e)}")  # Debug log
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
            role = request.POST.get('role', '').strip()
            raw_mobile = request.POST.get('mobile', '').strip()
            raw_email = request.POST.get('email', '').strip()
            raw_address = request.POST.get('address', '').strip()
            raw_username = request.POST.get('username', '').strip()
            raw_password = request.POST.get('password', '').strip()
            status = request.POST.get('status', 'Active')

            # Validate required fields
            if not raw_name:
                messages.error(request, 'नाव आवश्यक आहे')
                return redirect('PS-Manage-Users')

            if not raw_username:
                messages.error(request, 'यूजरनेम आवश्यक आहे')
                return redirect('PS-Manage-Users')

            if not raw_password:
                messages.error(request, 'पासवर्ड आवश्यक आहे')
                return redirect('PS-Manage-Users')

            # Clean text fields
            name = raw_name.strip()
            username = raw_username.strip()
            password = raw_password
            address = raw_address.strip() if raw_address else ""

            # Handle mobile number - store as is or empty string
            mobile = ""
            if raw_mobile:
                # Remove any non-digit characters
                mobile = ''.join(filter(str.isdigit, raw_mobile))
                # Validate 10 digits starting with 6-9
                if len(mobile) == 10 and mobile[0] in '6789':
                    pass  # Valid mobile
                else:
                    messages.warning(request, 'कृपया 10 अंकी वैध मोबाइल क्रमांक प्रविष्ट करा (सुरुवात 6,7,8,9 ने)')
                    return redirect('PS-Manage-Users')
            
            # Handle email - validate format
            email = ""
            if raw_email:
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, raw_email):
                    email = raw_email.strip().lower()
                else:
                    messages.warning(request, 'कृपया वैध ईमेल पत्ता प्रविष्ट करा')
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

        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
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

            # Validate required fields
            if not raw_name:
                messages.error(request, 'नाव आवश्यक आहे')
                return redirect('PS-Manage-Users')

            if not raw_username:
                messages.error(request, 'यूजरनेम आवश्यक आहे')
                return redirect('PS-Manage-Users')

            # Clean text fields
            name = raw_name.strip()
            username = raw_username.strip()
            address = raw_address.strip() if raw_address else ""

            # Handle mobile number
            mobile = ""
            if raw_mobile:
                # Remove any non-digit characters
                mobile = ''.join(filter(str.isdigit, raw_mobile))
                # Validate 10 digits starting with 6-9
                if len(mobile) == 10 and mobile[0] in '6789':
                    pass  # Valid mobile
                else:
                    messages.warning(request, 'कृपया 10 अंकी वैध मोबाइल क्रमांक प्रविष्ट करा (सुरुवात 6,7,8,9 ने)')
                    return redirect('PS-Manage-Users')
            
            # Handle email
            email = ""
            if raw_email:
                import re
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if re.match(email_pattern, raw_email):
                    email = raw_email.strip().lower()
                else:
                    messages.warning(request, 'कृपया वैध ईमेल पत्ता प्रविष्ट करा')
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

        except Exception as e:
            messages.error(request, f'त्रुटी: {str(e)}')
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
    paginator = Paginator(users, 15)
    page_number = request.GET.get('page', 1)
    users_page = paginator.get_page(page_number)
    start_index = (users_page.number - 1) * paginator.per_page + 1

    # Create pagination range with ellipsis
    pagination_range = []
    current_page = users_page.number
    total_pages = paginator.num_pages

    if total_pages <= 7:
        pagination_range = list(range(1, total_pages + 1))
    else:
        if current_page <= 3:
            pagination_range = list(range(1, 6)) + ['...', total_pages]
        elif current_page >= total_pages - 2:
            pagination_range = [1, '...'] + list(range(total_pages - 4, total_pages + 1))
        else:
            pagination_range = [1, '...'] + list(range(current_page - 1, current_page + 2)) + ['...', total_pages]

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
        'pagination_range': pagination_range,
        'total_pages': total_pages,
    }

    return render(request, 'PS-Manage-Users.html', context)





