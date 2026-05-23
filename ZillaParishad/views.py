from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from Main.utils import validate_email, validate_mobile_number, validate_clean_text
from ZillaParishad.models import Zilla_Parishad_User
from PanchayatSamiti.models import Panchayat_Samiti, Panchayat_Samiti_User
from Kosh.models import Kosh_User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib import messages
from ZillaParishad.models import Zilla_Parishad
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Zilla_Parishad
from Main.models import District, Super_User



def ZillaParishad_Dashboard(request):

    context = {

        'user_type': 'Zilla Parishad'

    }

    return render(
        request,
        'Zilla_parishad_dashboard.html',
        context
    )




def ZP_Manage_Zilla_Parishad(request):

    # ====================================================
    # LOGIN CHECK
    # ====================================================

    if not request.session.get('superuser_id'):
        return redirect('SuperUser-Login')

    # ====================================================
    # USER CHECK
    # ====================================================

    try:

        user = Super_User.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )

    except Super_User.DoesNotExist:

        request.session.flush()
        return redirect('SuperUser-Login')

    # ====================================================
    # ADD
    # ====================================================

    if request.method == 'POST' and request.POST.get('action') == 'add':

        zillaParishad_name = request.POST.get(
            'zillaParishad_name', ''
        ).strip()

        district_id = request.POST.get(
            'district', ''
        ).strip()

        zillaParishad_code = request.POST.get(
            'zillaParishad_code', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # ====================================================
        # REQUIRED VALIDATION
        # ====================================================

        if not zillaParishad_name:

            messages.error(
                request,
                "Zilla Parishad Name is required."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        if not district_id:

            messages.error(
                request,
                "District is required."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        if not zillaParishad_code:

            messages.error(
                request,
                "Zilla Parishad Code is required."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # FIELD VALIDATION
        # ====================================================

        try:
            validate_clean_text(
                zillaParishad_name,
                "Zilla Parishad Name"
            )

            validate_clean_text(
                zillaParishad_code,
                "Zilla Parishad Code"
            )

        except ValidationError as e:

            messages.error(request, str(e))

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # DISTRICT CHECK
        # ====================================================

        district = District.objects.filter(
            id=district_id
        ).first()

        if not district:

            messages.error(
                request,
                "Invalid District Selected."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        if Zilla_Parishad.objects.filter(
            zillaParishad_code=zillaParishad_code
        ).exists():

            messages.error(
                request,
                "Zilla Parishad Code already exists."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # CREATE
        # ====================================================

        Zilla_Parishad.objects.create(

            zillaParishad_name=zillaParishad_name,
            district=district,
            zillaParishad_code=zillaParishad_code,
            status=status

        )

        messages.success(
            request,
            "Zilla Parishad Added Successfully."
        )

        return redirect('ZP-Manage-Zilla-Parishad')

    # ====================================================
    # EDIT
    # ====================================================

    if request.method == 'POST' and request.POST.get('action') == 'edit':

        edit_id = request.POST.get('edit_id')

        zp = get_object_or_404(
            Zilla_Parishad,
            id=edit_id
        )

        zillaParishad_name = request.POST.get(
            'zillaParishad_name', ''
        ).strip()

        district_id = request.POST.get(
            'district', ''
        ).strip()

        zillaParishad_code = request.POST.get(
            'zillaParishad_code', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # ====================================================
        # REQUIRED VALIDATION
        # ====================================================

        if not zillaParishad_name:

            messages.error(
                request,
                "Zilla Parishad Name is required."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        if not district_id:

            messages.error(
                request,
                "District is required."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        if not zillaParishad_code:

            messages.error(
                request,
                "Zilla Parishad Code is required."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # FIELD VALIDATION
        # ====================================================

        try:

            validate_clean_text(
                zillaParishad_name,
                "Zilla Parishad Name"
            )

            validate_clean_text(
                zillaParishad_code,
                "Zilla Parishad Code"
            )

        except ValidationError as e:

            messages.error(request, str(e))

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # DISTRICT CHECK
        # ====================================================

        district = District.objects.filter(
            id=district_id
        ).first()

        if not district:

            messages.error(
                request,
                "Invalid District Selected."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        if Zilla_Parishad.objects.filter(
            zillaParishad_code=zillaParishad_code
        ).exclude(id=edit_id).exists():

            messages.error(
                request,
                "Zilla Parishad Code already exists."
            )

            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # UPDATE
        # ====================================================

        zp.zillaParishad_name = zillaParishad_name
        zp.district = district
        zp.zillaParishad_code = zillaParishad_code
        zp.status = status

        zp.save()

        messages.success(
            request,
            "Zilla Parishad Updated Successfully."
        )

        return redirect('ZP-Manage-Zilla-Parishad')

    # ====================================================
    # DELETE
    # ====================================================

    if request.GET.get('delete_id'):

        delete_id = request.GET.get('delete_id')

        zp = get_object_or_404(
            Zilla_Parishad,
            id=delete_id
        )

        zp.delete()

        messages.success(
            request,
            "Zilla Parishad Deleted Successfully."
        )

        return redirect('ZP-Manage-Zilla-Parishad')

    # ====================================================
    # SEARCH & FILTER
    # ====================================================

    search = request.GET.get(
        'search', ''
    ).strip()

    status = request.GET.get(
        'status', ''
    ).strip()

    all_zilla_parishad = Zilla_Parishad.objects.select_related(
        'district'
    ).all().order_by('-id')

    # ====================================================
    # SEARCH FILTER
    # ====================================================

    if search:

        all_zilla_parishad = all_zilla_parishad.filter(

            Q(zillaParishad_name__icontains=search) |
            Q(district__name__icontains=search) |
            Q(zillaParishad_code__icontains=search)

        )

    # ====================================================
    # STATUS FILTER
    # ====================================================

    if status:

        all_zilla_parishad = all_zilla_parishad.filter(
            status=status
        )

    # ====================================================
    # DISTRICT LIST
    # ====================================================

    all_districts = District.objects.all().order_by('name')

    # ====================================================
    # CONTEXT
    # ====================================================

    context = {

        'user': user,
        'all_zilla_parishad': all_zilla_parishad,
        'all_districts': all_districts,
        'search': search or '',
        'status': status or '',

    }

    return render(
        request,
        'ZP-Manage-Zilla-Parishad.html',
        context
    )
    



def ZP_Manage_Zilla_Parishad_User(request):

    try:

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
        # ADD USER
        # =====================================================

        if request.method == "POST" and request.POST.get("action") == "add":

            zilla_parishad_id = request.POST.get(
                "zilla_parishad"
            )

            name = request.POST.get(
                "name", ""
            ).strip()

            username = request.POST.get(
                "username", ""
            ).strip()

            password = request.POST.get(
                "password", ""
            ).strip()

            mobile = request.POST.get(
                "mobile", ""
            ).strip()

            email = request.POST.get(
                "email", ""
            ).strip()

            address = request.POST.get(
                "address", ""
            ).strip()

            status = request.POST.get(
                "status", "Active"
            ).strip()

            profile = request.FILES.get(
                "profile"
            )

            # =====================================================
            # REQUIRED VALIDATION
            # =====================================================

            if not zilla_parishad_id:

                messages.error(
                    request,
                    "Zilla Parishad is required."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            if not name:

                messages.error(
                    request,
                    "Name is required."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            if not username:

                messages.error(
                    request,
                    "Username is required."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            if not password:

                messages.error(
                    request,
                    "Password is required."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # GET ZP
            # =====================================================

            zilla_parishad = Zilla_Parishad.objects.filter(
                id=zilla_parishad_id
            ).first()

            if not zilla_parishad:

                messages.error(
                    request,
                    "Invalid Zilla Parishad."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # VALIDATION
            # =====================================================

            try:

                validate_clean_text(
                    name,
                    "Name"
                )

                validate_clean_text(
                    username,
                    "Username"
                )

                if mobile:

                    validate_mobile_number(
                        mobile
                    )

                if email:

                    validate_email(
                        email
                    )

            except ValidationError as e:

                messages.error(
                    request,
                    str(e)
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # USERNAME CHECK
            # =====================================================

            if Zilla_Parishad_User.objects.filter(
                username=username
            ).exists():

                messages.error(
                    request,
                    "Username already exists."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # CREATE USER
            # =====================================================

            Zilla_Parishad_User.objects.create(

                zilla_parishad=zilla_parishad,
                zilla_parishad_name=zilla_parishad.zillaParishad_name,

                name=name,
                username=username,
                password=password,

                mobile=mobile,
                email=email,
                address=address,

                profile=profile,

                status=status

            )

            messages.success(
                request,
                "Zilla Parishad User added successfully."
            )

            return redirect(
                "ZP-Manage-Zilla-Parishad-User"
            )

        # =====================================================
        # EDIT USER
        # =====================================================

        if request.method == "POST" and request.POST.get("action") == "edit":

            edit_id = request.POST.get(
                "edit_id"
            )

            obj = get_object_or_404(
                Zilla_Parishad_User,
                id=edit_id
            )

            zilla_parishad_id = request.POST.get(
                "zilla_parishad"
            )

            name = request.POST.get(
                "name", ""
            ).strip()

            username = request.POST.get(
                "username", ""
            ).strip()

            password = request.POST.get(
                "password", ""
            ).strip()

            mobile = request.POST.get(
                "mobile", ""
            ).strip()

            email = request.POST.get(
                "email", ""
            ).strip()

            address = request.POST.get(
                "address", ""
            ).strip()

            status = request.POST.get(
                "status", "Active"
            ).strip()

            profile = request.FILES.get(
                "profile"
            )

            # =====================================================
            # REQUIRED VALIDATION
            # =====================================================

            if not zilla_parishad_id:

                messages.error(
                    request,
                    "Zilla Parishad is required."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            if not name:

                messages.error(
                    request,
                    "Name is required."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            if not username:

                messages.error(
                    request,
                    "Username is required."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # GET ZP
            # =====================================================

            zilla_parishad = Zilla_Parishad.objects.filter(
                id=zilla_parishad_id
            ).first()

            if not zilla_parishad:

                messages.error(
                    request,
                    "Invalid Zilla Parishad."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # VALIDATION
            # =====================================================

            try:

                validate_clean_text(
                    name,
                    "Name"
                )

                validate_clean_text(
                    username,
                    "Username"
                )

                if mobile:

                    validate_mobile_number(
                        mobile
                    )

                if email:

                    validate_email(
                        email
                    )

            except ValidationError as e:

                messages.error(
                    request,
                    str(e)
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # USERNAME CHECK
            # =====================================================

            if Zilla_Parishad_User.objects.filter(
                username=username
            ).exclude(id=edit_id).exists():

                messages.error(
                    request,
                    "Username already exists."
                )

                return redirect(
                    "ZP-Manage-Zilla-Parishad-User"
                )

            # =====================================================
            # UPDATE USER
            # =====================================================

            obj.zilla_parishad = zilla_parishad
            obj.zilla_parishad_name = zilla_parishad.zillaParishad_name

            obj.name = name
            obj.username = username

            obj.mobile = mobile
            obj.email = email
            obj.address = address

            obj.status = status

            # =====================================================
            # PASSWORD UPDATE ONLY IF NEW PASSWORD GIVEN
            # =====================================================

            if password:

                obj.password = password

                messages.success(
                    request,
                    "Password updated successfully."
                )

            # =====================================================
            # PROFILE UPDATE
            # =====================================================

            if profile:

                obj.profile = profile

            obj.save()

            messages.success(
                request,
                "Zilla Parishad User updated successfully."
            )

            return redirect(
                "ZP-Manage-Zilla-Parishad-User"
            )

        # =====================================================
        # DELETE USER
        # =====================================================

        if request.GET.get("delete_id"):

            delete_id = request.GET.get(
                "delete_id"
            )

            obj = get_object_or_404(
                Zilla_Parishad_User,
                id=delete_id
            )

            obj.delete()

            messages.success(
                request,
                "Zilla Parishad User deleted successfully."
            )

            return redirect(
                "ZP-Manage-Zilla-Parishad-User"
            )

        # =====================================================
        # SEARCH + FILTER
        # =====================================================

        search = request.GET.get(
            "search", ""
        ).strip()

        status = request.GET.get(
            "status", ""
        ).strip()

        users = Zilla_Parishad_User.objects.select_related(
            "zilla_parishad"
        ).order_by("-id")

        # =====================================================
        # SEARCH
        # =====================================================

        if search:

            users = users.filter(

                Q(name__icontains=search) |
                Q(username__icontains=search) |
                Q(mobile__icontains=search) |
                Q(email__icontains=search) |
                Q(zilla_parishad_name__icontains=search)

            )

        # =====================================================
        # STATUS FILTER
        # =====================================================

        if status:

            users = users.filter(
                status=status
            )

        # =====================================================
        # PAGINATION
        # =====================================================

        paginator = Paginator(
            users,
            10
        )

        page_number = request.GET.get(
            "page"
        )

        users = paginator.get_page(
            page_number
        )

        # =====================================================
        # ALL ZP
        # =====================================================

        all_zilla_parishad = Zilla_Parishad.objects.all().order_by(
            "zillaParishad_name"
        )

        # =====================================================
        # CONTEXT
        # =====================================================

        context = {

            "user": user,
            "users": users,

            "search": search or '',
            "status": status or '',

            "all_zilla_parishad": all_zilla_parishad,

        }

        return render(

            request,
            "ZP-Manage-Zilla-Parishad-User.html",
            context

        )

    except Exception:

        messages.error(
            request,
            "Something went wrong."
        )

        return redirect(
            "ZP-Manage-Zilla-Parishad-User"
        )