from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from Main.models import Super_User
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

    # ================= ADD =================
    if request.method == 'POST' and 'add_samiti' in request.POST:
        try:
            panchayat_samiti_name = request.POST.get('panchayat_samiti_name', '').strip()
            taluka_name = request.POST.get('taluka_name', '').strip()
            panchayat_samiti_code = request.POST.get('panchayat_samiti_code', '').strip()
            contact_person = request.POST.get('contact_person', '').strip()
            contact_phone = request.POST.get('contact_phone', '').strip()
            status = request.POST.get('status', 'Active')

            # Validate required fields
            if not panchayat_samiti_name:
                messages.error(request, 'समिती नाव आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not taluka_name:
                messages.error(request, 'तालुका नाव आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not panchayat_samiti_code:
                messages.error(request, 'समिती कोड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Validate phone if provided
            if contact_phone:
                contact_phone = validate_mobile_number(contact_phone)

            # Check duplicate code
            if Panchayat_Samiti.objects.filter(panchayat_samiti_code=panchayat_samiti_code).exists():
                messages.error(request, 'हा समिती कोड आधीच अस्तित्वात आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Create record
            Panchayat_Samiti.objects.create(
                panchayat_samiti_name=panchayat_samiti_name,
                taluka_name=taluka_name,
                panchayat_samiti_code=panchayat_samiti_code,
                contact_person=contact_person,
                contact_phone=contact_phone,
                status=status
            )

            messages.success(request, 'पंचायत समिती यशस्वीरित्या जोडली गेली')
            return redirect('PS-Manage-Panchayat-Samitis')

        except ValidationError as e:
            messages.error(request, str(e))
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
            panchayat_samiti_name = request.POST.get('panchayat_samiti_name', '').strip()
            taluka_name = request.POST.get('taluka_name', '').strip()
            panchayat_samiti_code = request.POST.get('panchayat_samiti_code', '').strip()
            contact_person = request.POST.get('contact_person', '').strip()
            contact_phone = request.POST.get('contact_phone', '').strip()
            status = request.POST.get('status', 'Active')

            # Validate required fields
            if not panchayat_samiti_name:
                messages.error(request, 'समिती नाव आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not taluka_name:
                messages.error(request, 'तालुका नाव आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')
            
            if not panchayat_samiti_code:
                messages.error(request, 'समिती कोड आवश्यक आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Validate phone if provided
            if contact_phone:
                contact_phone = validate_mobile_number(contact_phone)

            # Check duplicate code (excluding current)
            if Panchayat_Samiti.objects.filter(panchayat_samiti_code=panchayat_samiti_code).exclude(id=samiti_id).exists():
                messages.error(request, 'हा समिती कोड आधीच अस्तित्वात आहे')
                return redirect('PS-Manage-Panchayat-Samitis')

            # Update record
            samiti.panchayat_samiti_name = panchayat_samiti_name
            samiti.taluka_name = taluka_name
            samiti.panchayat_samiti_code = panchayat_samiti_code
            samiti.contact_person = contact_person
            samiti.contact_phone = contact_phone
            samiti.status = status
            samiti.save()

            messages.success(request, 'पंचायत समिती यशस्वीरित्या अद्यतनित केली गेली')
            return redirect('PS-Manage-Panchayat-Samitis')

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('PS-Manage-Panchayat-Samitis')

    # ================= DELETE =================
    if request.method == 'POST' and 'delete_samiti' in request.POST:
        samiti_id = request.POST.get('samiti_id', '').strip()

        if samiti_id:
            try:
                samiti = Panchayat_Samiti.objects.get(id=samiti_id)
                samiti_name = samiti.panchayat_samiti_name
                samiti.delete()
                messages.success(request, f'"{samiti_name}" यशस्वीरित्या हटवली गेली')
            except Panchayat_Samiti.DoesNotExist:
                messages.error(request, 'पंचायत समिती सापडली नाही')

        return redirect('PS-Manage-Panchayat-Samitis')

    # ================= FILTERS =================
    panchayat_samiti_name = request.GET.get('panchayat_samiti_name', '').strip()
    taluka_name = request.GET.get('taluka_name', '').strip()
    panchayat_samiti_code = request.GET.get('panchayat_samiti_code', '').strip()
    contact_person = request.GET.get('contact_person', '').strip()
    contact_phone = request.GET.get('contact_phone', '').strip()
    status_filter = request.GET.get('status', 'all')
    reset = request.GET.get('reset', '')
    edit_id = request.GET.get('edit_id', None)

    # Reset filters
    if reset:
        panchayat_samiti_name = ''
        taluka_name = ''
        panchayat_samiti_code = ''
        contact_person = ''
        contact_phone = ''
        status_filter = 'all'

    # Base queryset
    if status_filter == 'active':
        samitis = Panchayat_Samiti.objects.filter(status='Active')
    elif status_filter == 'inactive':
        samitis = Panchayat_Samiti.objects.filter(status='Inactive')
    else:
        samitis = Panchayat_Samiti.objects.all()

    total_samitis = samitis.count()

    # Apply search filters
    if panchayat_samiti_name:
        samitis = samitis.filter(panchayat_samiti_name__icontains=panchayat_samiti_name)
    if taluka_name:
        samitis = samitis.filter(taluka_name__icontains=taluka_name)
    if panchayat_samiti_code:
        samitis = samitis.filter(panchayat_samiti_code__icontains=panchayat_samiti_code)
    if contact_person:
        samitis = samitis.filter(contact_person__icontains=contact_person)
    if contact_phone:
        samitis = samitis.filter(contact_phone__icontains=contact_phone)

    filtered_count = samitis.count()

    # Order by latest first
    samitis = samitis.order_by('-id')

    # Pagination
    paginator = Paginator(samitis, 15)
    page_number = request.GET.get('page', 1)
    samitis_page = paginator.get_page(page_number)
    start_index = (samitis_page.number - 1) * paginator.per_page + 1

    # Edit data
    edit_samiti = None
    if edit_id:
        try:
            edit_samiti = Panchayat_Samiti.objects.get(id=edit_id)
        except Panchayat_Samiti.DoesNotExist:
            pass

    context = {
        'user': user,
        'samitis': samitis_page,
        'total_samitis': total_samitis,
        'filtered_count': filtered_count,
        'start_index': start_index,
        'panchayat_samiti_name': panchayat_samiti_name,
        'taluka_name': taluka_name,
        'panchayat_samiti_code': panchayat_samiti_code,
        'contact_person': contact_person,
        'contact_phone': contact_phone,
        'status_filter': status_filter,
        'edit_samiti': edit_samiti,
    }

    return render(request, 'PS-Manage-Panchayat-Samitis.html', context)




def PS_Manage_Users(request):
    try:
        if not request.session.get('superuser_id'):
            return redirect('SuperUser-Login')

        try:
            user = SuperUser.objects.get(
                id=request.session.get('superuser_id'),
                status='Active'
            )
        except SuperUser.DoesNotExist:
            request.session.flush()
            return redirect('SuperUser-Login')

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
                
                # Validate mobile if provided (10 digits starting with 6-9)
                mobile = ""
                if raw_mobile:
                    mobile = validate_mobile_number(raw_mobile)

            except ValidationError as ve:
                messages.warning(request, f"⚠ Validation Warning: {ve}")
                return redirect('PS-Manage-Users')


            # Validation
            if not name:
                messages.error(request, 'Name is required')
                return redirect('PS-Manage-Users')

            if not username:
                messages.error(request, 'Username is required')
                return redirect('PS-Manage-Users')

            if not password:
                messages.error(request, 'Password is required')
                return redirect('PS-Manage-Users')

            # Check duplicate username
            if Panchayat_Samiti_User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('PS-Manage-Users')


            # Get Panchayat Samiti
            panchayat_samiti = None
            if panchayat_samiti_id:
                try:
                    panchayat_samiti = Panchayat_Samiti.objects.get(id=panchayat_samiti_id)
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
                password=password,  # Will be hashed by the model's save method
                status=status
            )

            messages.success(request, 'User added successfully')
            return redirect('PS-Manage-Users')

        # ================= EDIT =================
        if request.method == 'POST' and 'edit_user' in request.POST:
            user_id = request.POST.get('user_id', '').strip()

            if not user_id:
                messages.error(request, 'Invalid request')
                return redirect('PS-Manage-Users')

            try:
                user_obj = Panchayat_Samiti_User.objects.get(id=user_id)
            except Panchayat_Samiti_User.DoesNotExist:
                messages.error(request, 'User not found')
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
                
                # Validate mobile if provided (10 digits starting with 6-9)
                mobile = ""
                if raw_mobile:
                    mobile = validate_mobile_number(raw_mobile)

            except ValidationError as ve:
                messages.warning(request, f"⚠ Validation Warning: {ve}")
                return redirect('PS-Manage-Users')

            # Validation
            if not name:
                messages.error(request, 'Name is required')
                return redirect('PS-Manage-Users')

            if not username:
                messages.error(request, 'Username is required')
                return redirect('PS-Manage-Users')

            # Check duplicate username (exclude current)
            if Panchayat_Samiti_User.objects.filter(username=username).exclude(id=user_id).exists():
                messages.error(request, 'Username already exists')
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
            if password:
                user_obj.password = password  # Will be hashed by save method
            
            user_obj.status = status
            user_obj.save()

            messages.success(request, 'User updated successfully')
            return redirect('PS-Manage-Users')

        # ================= DELETE =================
        if request.method == 'POST' and 'delete_user' in request.POST:
            user_id = request.POST.get('user_id', '').strip()

            if user_id:
                try:
                    user_obj = Panchayat_Samiti_User.objects.get(id=user_id)
                    user_name = user_obj.name
                    user_obj.delete()
                    messages.success(request, f'User "{user_name}" deleted successfully')
                except Panchayat_Samiti_User.DoesNotExist:
                    messages.error(request, 'User not found')

            return redirect('PS-Manage-Users')

        # ================= FILTERS =================
        name = request.GET.get('name', '').strip()
        mobile = request.GET.get('mobile', '').strip()
        email = request.GET.get('email', '').strip()
        username = request.GET.get('username', '').strip()
        panchayat_samiti_filter = request.GET.get('panchayat_samiti', '').strip()
        status_filter = request.GET.get('status', 'all')
        reset = request.GET.get('reset', '')
        edit_id = request.GET.get('edit_id', None)

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

        # Pagination range
        pagination_range = []
        current_page = users_page.number
        total_pages = paginator.num_pages

        if total_pages <= 7:
            pagination_range = range(1, total_pages + 1)
        else:
            if current_page <= 3:
                pagination_range = list(range(1, 6)) + ['...', total_pages]
            elif current_page >= total_pages - 2:
                pagination_range = [1, '...'] + list(range(total_pages - 4, total_pages + 1))
            else:
                pagination_range = [1, '...'] + list(range(current_page - 1, current_page + 2)) + ['...', total_pages]

        # Get all Panchayat Samitis for dropdown
        panchayat_samitis = Panchayat_Samiti.objects.filter(status='Active')

        # Edit Data
        edit_user = None
        if edit_id:
            try:
                edit_user = Panchayat_Samiti_User.objects.get(id=edit_id)
            except Panchayat_Samiti_User.DoesNotExist:
                pass

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
            'pagination_range': pagination_range,
            'total_pages': total_pages,
            'panchayat_samitis': panchayat_samitis,
            'edit_user': edit_user,
        }

        return render(request, 'PS-Manage-Users.html', context)

    except Exception as e:
        print("ERROR IN PS_Manage_Users :", str(e))
        messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('Superuser-Dashboard')





