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
from django.db.models import Q, Sum

from ZillaParishad.models import Zilla_Parishad_User
from PanchayatSamiti.models import Panchayat_Samiti, Panchayat_Samiti_User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Main.models import District, Kosh_Head, Super_User, Taluka
from ZillaParishad.models import Zilla_Parishad
from django.core.paginator import Paginator
from django.http import JsonResponse
from Main.utils import validate_email, validate_mobile_number, validate_clean_text

def Login(request):

    if request.method == "POST":

        login_type = request.POST.get('login_type')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not login_type:
            messages.error(request, "Please Select Login Type")
            return redirect('Login')

        if not username:
            messages.error(request, "Please Enter Username")
            return redirect('Login')

        if not password:
            messages.error(request, "Please Enter Password")
            return redirect('Login')

        # ── Zilla Parishad ──
        if login_type == "ZillaParishad":
            try:
                zp_user = Zilla_Parishad_User.objects.get(username=username, status='Active')
            except Zilla_Parishad_User.DoesNotExist:
                messages.error(request, "Zilla Parishad User Not Found")
                return redirect('Login')

            if zp_user.check_password(password):
                request.session['user_id']   = zp_user.id
                request.session['user_name'] = zp_user.name
                request.session['user_type'] = 'ZillaParishad'
                messages.success(request, "Zilla Parishad Login Successful")
                return redirect('ZP-Dashboard')
            else:
                messages.error(request, "Invalid Password")
                return redirect('Login')

        # ── Panchayat Samiti ──
        elif login_type == "PanchayatSamiti":
            try:
                ps_user = Panchayat_Samiti_User.objects.get(username=username, status='Active')
            except Panchayat_Samiti_User.DoesNotExist:
                messages.error(request, "Panchayat Samiti User Not Found")
                return redirect('Login')

            if ps_user.check_password(password):
                request.session['user_id']   = ps_user.id
                request.session['user_name'] = ps_user.name
                request.session['user_type'] = 'PanchayatSamiti'
                messages.success(request, "Panchayat Samiti Login Successful")
                return redirect('PS-Dashboard')
            else:
                messages.error(request, "Invalid Password")
                return redirect('Login')

        # ── Kosh ──
        elif login_type == "Kosh":
            try:
                kosh_user = Kosh_User.objects.get(username=username, status='Active')
            except Kosh_User.DoesNotExist:
                messages.error(request, "Kosh User Not Found")
                return redirect('Login')

            if kosh_user.check_password(password):
                request.session['user_id']   = kosh_user.id
                request.session['user_name'] = kosh_user.name
                request.session['user_type'] = 'Kosh'

                all_kosh     = kosh_user.kosh.filter(status='Active', is_deleted=False)
                primary_kosh = all_kosh.filter(is_primary=True).first()
                active_kosh  = primary_kosh or all_kosh.first()

                if active_kosh:
                    request.session['active_kosh_id']   = active_kosh.id
                    request.session['active_kosh_name'] = active_kosh.kosh_name
                    request.session['active_kosh_code'] = active_kosh.kosh_code

                messages.success(request, "Kosh Login Successful")
                return redirect('Kosh_Dashboard')
            else:
                messages.error(request, "Invalid Password")
                return redirect('Login')

        # ── Invalid login type ──
        else:
            messages.error(request, "Invalid Login Type")
            return redirect('Login')

    # ✅ GET request — render the login page
    return render(request, 'login.html')


def Logout(request):
    request.session.flush()
    messages.success(request, "Successfully logged out.")
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








def Manage_Kosh_Head(request):

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

    if request.method == "POST" and request.POST.get("action") == "add":

        name       = request.POST.get("name", "").strip()
        percentage = request.POST.get("percentage", "0").strip()
        status     = request.POST.get("status", "Active").strip()

        if not name:
            messages.error(request, "Head name is required.")
            return redirect("Manage-Kosh-Head")

        try:
            validate_clean_text(name, "Head Name")
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("Manage-Kosh-Head")

        try:
            percentage = float(percentage)
            if percentage < 0 or percentage > 100:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, "Percentage must be a number between 0 and 100.")
            return redirect("Manage-Kosh-Head")

        if Kosh_Head.objects.filter(name=name).exists():
            messages.error(request, "Head already exists.")
            return redirect("Manage-Kosh-Head")

        existing_total = Kosh_Head.objects.aggregate(
            total=Sum("percentage")
        )["total"] or 0

        if float(existing_total) + percentage > 100:
            messages.error(
                request,
                f"Cannot add. Current total is {existing_total}%. "
                f"Adding {percentage}% would exceed 100%."
            )
            return redirect("Manage-Kosh-Head")

        Kosh_Head.objects.create(
            name=name,
            percentage=percentage,
            status=status
        )

        messages.success(request, "Kosh Head added successfully.")
        return redirect("Manage-Kosh-Head")

    # =====================================================
    # EDIT
    # =====================================================

    if request.method == "POST" and request.POST.get("action") == "edit":

        edit_id    = request.POST.get("edit_id")
        obj        = get_object_or_404(Kosh_Head, id=edit_id)
        name       = request.POST.get("name", "").strip()
        percentage = request.POST.get("percentage", "0").strip()
        status     = request.POST.get("status", "Active").strip()

        if not name:
            messages.error(request, "Head name is required.")
            return redirect("Manage-Kosh-Head")

        try:
            validate_clean_text(name, "Head Name")
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect("Manage-Kosh-Head")

        try:
            percentage = float(percentage)
            if percentage < 0 or percentage > 100:
                raise ValueError
        except (ValueError, TypeError):
            messages.error(request, "Percentage must be a number between 0 and 100.")
            return redirect("Manage-Kosh-Head")

        if Kosh_Head.objects.filter(name=name).exclude(id=edit_id).exists():
            messages.error(request, "Head already exists.")
            return redirect("Manage-Kosh-Head")

        other_total = Kosh_Head.objects.exclude(id=edit_id).aggregate(
            total=Sum("percentage")
        )["total"] or 0

        if float(other_total) + percentage > 100:
            messages.error(
                request,
                f"Cannot save. Other heads total {other_total}%. "
                f"This value ({percentage}%) would exceed 100%."
            )
            return redirect("Manage-Kosh-Head")

        obj.name       = name
        obj.percentage = percentage
        obj.status     = status
        obj.save()

        messages.success(request, "Kosh Head updated successfully.")
        return redirect("Manage-Kosh-Head")

    # =====================================================
    # DELETE (password-protected)
    # =====================================================

    if request.method == "POST" and request.POST.get("action") == "delete":

        delete_id        = request.POST.get("delete_id", "").strip()
        entered_password = request.POST.get("delete_password", "").strip()

        if not delete_id:
            messages.error(request, "Invalid delete request.")
            return redirect("Manage-Kosh-Head")

        obj = get_object_or_404(Kosh_Head, id=delete_id)

        if not entered_password:
            messages.error(request, "Password is required to delete.")
            return redirect("Manage-Kosh-Head")

        # Re-fetch fresh from DB so we always have the latest password value
        try:
            fresh_user = Super_User.objects.get(
                id=request.session.get('superuser_id'),
                status='Active'
            )
        except Super_User.DoesNotExist:
            request.session.flush()
            return redirect('SuperUser-Login')

        # Plain text comparison — strip both sides to avoid whitespace issues
        if not fresh_user.check_password(entered_password):
            messages.error(request, "Incorrect password. Deletion cancelled.")
            return redirect("Manage-Kosh-Head")

        obj.delete()
        messages.success(request, "Kosh Head deleted successfully.")
        return redirect("Manage-Kosh-Head")

    # =====================================================
    # SEARCH & FILTER
    # =====================================================

    search = request.GET.get("search", "").strip()
    status = request.GET.get("status", "").strip()

    heads = Kosh_Head.objects.all().order_by("-id")

    if search:
        heads = heads.filter(Q(name__icontains=search))

    if status:
        heads = heads.filter(status=status)

    total_percentage     = Kosh_Head.objects.aggregate(total=Sum("percentage"))["total"] or 0
    remaining_percentage = 100 - float(total_percentage)

    paginator   = Paginator(heads, 10)
    page_number = request.GET.get("page")
    heads       = paginator.get_page(page_number)

    context = {
        "user"                : user,
        "heads"               : heads,
        "search"              : search,
        "status"              : status,
        "total_percentage"    : total_percentage,
        "remaining_percentage": remaining_percentage,
    }

    return render(request, "Manage-Kosh-Head.html", context)