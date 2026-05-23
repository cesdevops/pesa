from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from Main.utils import validate_clean_text
from django.db.models import Q
from ZillaParishad.models import Zilla_Parishad_User
from Kosh.models import Kosh_User
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib import messages
from ZillaParishad.models import Zilla_Parishad_User
from PanchayatSamiti.models import Panchayat_Samiti, Panchayat_Samiti_User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Main.models import District, Super_User, Taluka
from ZillaParishad.models import Zilla_Parishad
from django.core.paginator import Paginator
from django.http import JsonResponse
from Main.utils import validate_email, validate_mobile_number, validate_clean_text


def Login(request):

    try:

        if request.method == "POST":

            login_type = request.POST.get('login_type')
            username = request.POST.get('username')
            password = request.POST.get('password')

            # =====================================================
            # Validation
            # =====================================================

            if not login_type:
                messages.error(request, "Please Select Login Type")
                return redirect('Login')

            if not username:
                messages.error(request, "Please Enter Username")
                return redirect('Login')

            if not password:
                messages.error(request, "Please Enter Password")
                return redirect('Login')

            # =====================================================
            # Zilla Parishad Login
            # =====================================================

            if login_type == "ZillaParishad":

                try:

                    zp_user = Zilla_Parishad_User.objects.get(
                        username=username,
                        status='Active'
                    )

                    if zp_user.check_password(password):

                        request.session['user_id'] = zp_user.id
                        request.session['user_name'] = zp_user.name
                        request.session['user_type'] = 'ZillaParishad'

                        messages.success(
                            request,
                            "Zilla Parishad Login Successful"
                        )

                        return redirect('ZillaParishad_Dashboard')

                    else:

                        messages.error(request, "Invalid Password")
                        return redirect('Login')

                except Zilla_Parishad_User.DoesNotExist:

                    messages.error(request, "Zilla Parishad User Not Found")
                    return redirect('Login')



            # =====================================================
            # Panchayat Samiti Login
            # =====================================================

            elif login_type == "PanchayatSamiti":

                try:

                    ps_user = Panchayat_Samiti_User.objects.get(
                        username=username,
                        status='Active'
                    )

                    if ps_user.check_password(password):

                        request.session['user_id'] = ps_user.id
                        request.session['user_name'] = ps_user.name
                        request.session['user_type'] = 'PanchayatSamiti'

                        messages.success(
                            request,
                            "Panchayat Samiti Login Successful"
                        )

                        return redirect('PanchayatSamiti_Dashboard')

                    else:

                        messages.error(request, "Invalid Password")
                        return redirect('Login')

                except Panchayat_Samiti_User.DoesNotExist:

                    messages.error(request, "Panchayat Samiti User Not Found")
                    return redirect('Login')



            # =====================================================
            # Kosh Login
            # =====================================================

            elif login_type == "Kosh":

                try:

                    kosh_user = Kosh_User.objects.get(
                        username=username,
                        status='Active'
                    )

                    if kosh_user.check_password(password):

                        request.session['user_id'] = kosh_user.id
                        request.session['user_name'] = kosh_user.name
                        request.session['user_type'] = 'Kosh'

                        messages.success(
                            request,
                            "Kosh Login Successful"
                        )

                        return redirect('Kosh_Dashboard')

                    else:

                        messages.error(request, "Invalid Password")
                        return redirect('Login')

                except Kosh_User.DoesNotExist:

                    messages.error(request, "Kosh User Not Found")
                    return redirect('Login')



            # =====================================================
            # Invalid Login Type
            # =====================================================

            else:

                messages.error(request, "Invalid Login Type")
                return redirect('Login')



        return render(request, 'login.html')


    except Exception as e:

        messages.error(request, "Something Went Wrong")

        return redirect('Login')
   





def SuperUser_Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Super_User.objects.get(
                username=username,
                status='Active'
            )

            if user.check_password(password):

                # Create Session
                request.session['superuser_id'] = user.id

                messages.success(request, "Login Successful")

                return redirect('Superuser-Dashboard')

            else:
                messages.error(request, "Invalid Password")

        except Super_User.DoesNotExist:
            messages.error(request, "Invalid Username")

    return render(request, 'SuperUser-Login.html')


def Superuser_Dashboard(request):
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

    context = {
        'user': user
    }

    return render(request, 'Superuser-Dashboard.html', context)

def Superuser_Logout(request):
    request.session.flush()

    messages.success(request, "Logout Successful")

    return redirect('SuperUser-Login')








# =========================================================
# MANAGE DISTRICT
# =========================================================

def Manage_District(request):

    # =====================================================
    # LOGIN CHECK
    # =====================================================

    if not request.session.get('superuser_id'):

        return redirect('SuperUser-Login')

    # =====================================================
    # USER CHECK
    # =====================================================

    try:

        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )

    except Super_User.DoesNotExist:

        request.session.flush()

        return redirect('SuperUser-Login')

    # =====================================================
    # ADD
    # =====================================================

    if request.method == 'POST' and request.POST.get('action') == 'add':

        name = request.POST.get(
            'name', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # =====================================================
        # REQUIRED VALIDATION
        # =====================================================

        if not name:

            messages.error(
                request,
                "District Name is required."
            )

            return redirect('Manage-District')

        # =====================================================
        # FIELD VALIDATION
        # =====================================================

        try:

            validate_clean_text(
                name,
                "District Name"
            )

        except ValidationError as e:

            messages.error(
                request,
                str(e)
            )

            return redirect('Manage-District')

        # =====================================================
        # DUPLICATE CHECK
        # =====================================================

        if District.objects.filter(
            name__iexact=name
        ).exists():

            messages.error(
                request,
                "District already exists."
            )

            return redirect('Manage-District')

        # =====================================================
        # CREATE
        # =====================================================

        District.objects.create(

            name=name,
            # status=status

        )

        messages.success(
            request,
            "District Added Successfully."
        )

        return redirect('Manage-District')

    # =====================================================
    # EDIT
    # =====================================================

    if request.method == 'POST' and request.POST.get('action') == 'edit':

        edit_id = request.POST.get(
            'edit_id'
        )

        district = get_object_or_404(
            District,
            id=edit_id
        )

        name = request.POST.get(
            'name', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # =====================================================
        # REQUIRED VALIDATION
        # =====================================================

        if not name:

            messages.error(
                request,
                "District Name is required."
            )

            return redirect('Manage-District')

        # =====================================================
        # FIELD VALIDATION
        # =====================================================

        try:

            validate_clean_text(
                name,
                "District Name"
            )

        except ValidationError as e:

            messages.error(
                request,
                str(e)
            )

            return redirect('Manage-District')

        # =====================================================
        # DUPLICATE CHECK
        # =====================================================

        if District.objects.filter(
            name__iexact=name
        ).exclude(id=edit_id).exists():

            messages.error(
                request,
                "District already exists."
            )

            return redirect('Manage-District')

        # =====================================================
        # UPDATE
        # =====================================================

        district.name = name

        district.save()

        messages.success(
            request,
            "District Updated Successfully."
        )

        return redirect('Manage-District')

    # =====================================================
    # DELETE
    # =====================================================

    if request.GET.get('delete_id'):

        delete_id = request.GET.get(
            'delete_id'
        )

        district = get_object_or_404(
            District,
            id=delete_id
        )

        district.delete()

        messages.success(
            request,
            "District Deleted Successfully."
        )

        return redirect('Manage-District')

    # =====================================================
    # SEARCH
    # =====================================================

    search = request.GET.get(
        'search', ''
    ).strip()

    status = request.GET.get(
        'status', ''
    ).strip()

    all_districts = District.objects.all().order_by('-id')

    if search:

        all_districts = all_districts.filter(
            name__icontains=search
        )

    if status:

        all_districts = all_districts.filter(
            status=status
        )

    # =====================================================
    # PAGINATION
    # =====================================================

    paginator = Paginator(
        all_districts,
        10
    )

    page_number = request.GET.get('page')

    all_districts = paginator.get_page(
        page_number
    )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'user': user,
        'all_districts': all_districts,
        'search': search or '',
        'status': status or '',

    }

    return render(
        request,
        'Manage-District.html',
        context
    )


# =========================================================
# MANAGE TALUKA
# =========================================================

def Manage_Taluka(request):

    # =====================================================
    # LOGIN CHECK
    # =====================================================

    if not request.session.get('superuser_id'):

        return redirect('SuperUser-Login')

    # =====================================================
    # USER CHECK
    # =====================================================

    try:

        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )

    except Super_User.DoesNotExist:

        request.session.flush()

        return redirect('SuperUser-Login')

    # =====================================================
    # ADD
    # =====================================================

    if request.method == 'POST' and request.POST.get('action') == 'add':

        district_id = request.POST.get(
            'district', ''
        ).strip()

        name = request.POST.get(
            'name', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # =====================================================
        # REQUIRED VALIDATION
        # =====================================================

        if not district_id:

            messages.error(
                request,
                "District is required."
            )

            return redirect('Manage-Taluka')

        if not name:

            messages.error(
                request,
                "Taluka Name is required."
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # VALIDATION
        # =====================================================

        try:

            validate_clean_text(
                name,
                "Taluka Name"
            )

        except ValidationError as e:

            messages.error(
                request,
                str(e)
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # DISTRICT CHECK
        # =====================================================

        district = District.objects.filter(
            id=district_id
        ).first()

        if not district:

            messages.error(
                request,
                "Invalid District Selected."
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # DUPLICATE CHECK
        # =====================================================

        if Taluka.objects.filter(
            district=district,
            name__iexact=name
        ).exists():

            messages.error(
                request,
                "Taluka already exists in this district."
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # CREATE
        # =====================================================

        Taluka.objects.create(

            district=district,
            name=name,

        )

        messages.success(
            request,
            "Taluka Added Successfully."
        )

        return redirect('Manage-Taluka')

    # =====================================================
    # EDIT
    # =====================================================

    if request.method == 'POST' and request.POST.get('action') == 'edit':

        edit_id = request.POST.get(
            'edit_id'
        )

        taluka = get_object_or_404(
            Taluka,
            id=edit_id
        )

        district_id = request.POST.get(
            'district', ''
        ).strip()

        name = request.POST.get(
            'name', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # =====================================================
        # REQUIRED VALIDATION
        # =====================================================

        if not district_id:

            messages.error(
                request,
                "District is required."
            )

            return redirect('Manage-Taluka')

        if not name:

            messages.error(
                request,
                "Taluka Name is required."
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # VALIDATION
        # =====================================================

        try:

            validate_clean_text(
                name,
                "Taluka Name"
            )

        except ValidationError as e:

            messages.error(
                request,
                str(e)
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # DISTRICT CHECK
        # =====================================================

        district = District.objects.filter(
            id=district_id
        ).first()

        if not district:

            messages.error(
                request,
                "Invalid District Selected."
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # DUPLICATE CHECK
        # =====================================================

        if Taluka.objects.filter(
            district=district,
            name__iexact=name
        ).exclude(id=edit_id).exists():

            messages.error(
                request,
                "Taluka already exists in this district."
            )

            return redirect('Manage-Taluka')

        # =====================================================
        # UPDATE
        # =====================================================

        taluka.district = district
        taluka.name = name
        taluka.status = status

        taluka.save()

        messages.success(
            request,
            "Taluka Updated Successfully."
        )

        return redirect('Manage-Taluka')

    # =====================================================
    # DELETE
    # =====================================================

    if request.GET.get('delete_id'):

        delete_id = request.GET.get(
            'delete_id'
        )

        taluka = get_object_or_404(
            Taluka,
            id=delete_id
        )

        taluka.delete()

        messages.success(
            request,
            "Taluka Deleted Successfully."
        )

        return redirect('Manage-Taluka')

    # =====================================================
    # SEARCH
    # =====================================================

    search = request.GET.get(
        'search', ''
    ).strip()

    status = request.GET.get(
        'status', ''
    ).strip()

    all_talukas = Taluka.objects.select_related(
        'district'
    ).all().order_by('-id')

    if search:

        all_talukas = all_talukas.filter(

            Q(name__icontains=search) |
            Q(district__name__icontains=search)

        )

    if status:

        all_talukas = all_talukas.filter(
            status=status
        )

    # =====================================================
    # PAGINATION
    # =====================================================

    paginator = Paginator(
        all_talukas,
        10
    )

    page_number = request.GET.get('page')

    all_talukas = paginator.get_page(
        page_number
    )

    # =====================================================
    # DISTRICT LIST
    # =====================================================

    all_districts = District.objects.all().order_by(
        'name'
    )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        'user': user,
        'all_talukas': all_talukas,
        'all_districts': all_districts,
        'search': search or '',
        'status': status or '',

    }

    return render(
        request,
        'Manage-Taluka.html',
        context
    )


