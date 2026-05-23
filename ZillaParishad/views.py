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
from Main.models import Super_User



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

        district_name = request.POST.get(
            'district_name', ''
        ).strip()

        zillaParishad_name_code = request.POST.get(
            'zillaParishad_name_code', ''
        ).strip()

        contact_person = request.POST.get(
            'contact_person', ''
        ).strip()

        contact_email = request.POST.get(
            'contact_email', ''
        ).strip()

        contact_phone = request.POST.get(
            'contact_phone', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # ====================================================
        # REQUIRED VALIDATION
        # ====================================================

        if not zillaParishad_name:
            messages.error(request, "Zilla Parishad Name is required.")
            return redirect('ZP-Manage-Zilla-Parishad')

        if not district_name:
            messages.error(request, "District Name is required.")
            return redirect('ZP-Manage-Zilla-Parishad')

        if not zillaParishad_name_code:
            messages.error(request, "ZP Code is required.")
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
                district_name,
                "District Name"
            )

            validate_clean_text(
                zillaParishad_name_code,
                "ZP Code"
            )

            if contact_person:
                validate_clean_text(
                    contact_person,
                    "Contact Person"
                )

            if contact_phone:
                validate_mobile_number(
                    contact_phone
                )

            if contact_email:
                validate_email(
                    contact_email
                )

        except ValidationError as e:

            messages.error(request, str(e))
            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        if Zilla_Parishad.objects.filter(
            zillaParishad_name_code=zillaParishad_name_code
        ).exists():

            messages.error(request, "ZP Code already exists.")
            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # CREATE
        # ====================================================

        Zilla_Parishad.objects.create(
            zillaParishad_name=zillaParishad_name,
            district_name=district_name,
            zillaParishad_name_code=zillaParishad_name_code,
            contact_person=contact_person,
            contact_email=contact_email,
            contact_phone=contact_phone,
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
            ZillaParishad,
            id=edit_id
        )

        zillaParishad_name = request.POST.get(
            'zillaParishad_name', ''
        ).strip()

        district_name = request.POST.get(
            'district_name', ''
        ).strip()

        zillaParishad_name_code = request.POST.get(
            'zillaParishad_name_code', ''
        ).strip()

        contact_person = request.POST.get(
            'contact_person', ''
        ).strip()

        contact_email = request.POST.get(
            'contact_email', ''
        ).strip()

        contact_phone = request.POST.get(
            'contact_phone', ''
        ).strip()

        status = request.POST.get(
            'status', 'Active'
        ).strip()

        # ====================================================
        # REQUIRED VALIDATION
        # ====================================================

        if not zillaParishad_name:
            messages.error(request, "Zilla Parishad Name is required.")
            return redirect('ZP-Manage-Zilla-Parishad')

        if not district_name:
            messages.error(request, "District Name is required.")
            return redirect('ZP-Manage-Zilla-Parishad')

        if not zillaParishad_name_code:
            messages.error(request, "ZP Code is required.")
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
                district_name,
                "District Name"
            )

            validate_clean_text(
                zillaParishad_name_code,
                "ZP Code"
            )

            if contact_person:
                validate_clean_text(
                    contact_person,
                    "Contact Person"
                )

            if contact_phone:
                validate_mobile_number(
                    contact_phone
                )

            if contact_email:
                validate_email(
                    contact_email
                )

        except ValidationError as e:

            messages.error(request, str(e))
            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        if ZillaParishad.objects.filter(
            zillaParishad_name_code=zillaParishad_name_code
        ).exclude(id=edit_id).exists():

            messages.error(request, "ZP Code already exists.")
            return redirect('ZP-Manage-Zilla-Parishad')

        # ====================================================
        # UPDATE
        # ====================================================

        zp.zillaParishad_name = zillaParishad_name
        zp.district_name = district_name
        zp.zillaParishad_name_code = zillaParishad_name_code

        zp.contact_person = contact_person
        zp.contact_email = contact_email
        zp.contact_phone = contact_phone
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
            ZillaParishad,
            id=delete_id
        )

        zp.delete()

        messages.success(
            request,
            "Zilla Parishad Deleted Successfully."
        )

        return redirect('ZP-Manage-Zilla-Parishad')

    # ====================================================
    # SEARCH
    # ====================================================

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    all_zilla_parishad = ZillaParishad.objects.all().order_by('-id')

    # SEARCH FILTER

    if search:

        all_zilla_parishad = all_zilla_parishad.filter(

            Q(zillaParishad_name__icontains=search) |
            Q(district_name__icontains=search) |
            Q(zillaParishad_name_code__icontains=search)

        )

    # STATUS FILTER

    if status:

        all_zilla_parishad = all_zilla_parishad.filter(
            status=status
        )

    # ====================================================
    # CONTEXT
    # ====================================================

    context = {
        'user': user,
        'all_zilla_parishad': all_zilla_parishad,
        'search': search,
        'status': status,
    }

    return render(
        request,
        'ZP-Manage-Zilla-Parishad.html',
        context
    )

    


def ZP_Manage_Zilla_Parishad_User(request):

    try:
        # ======================
        # LOGIN CHECK
        # ======================
        if not request.session.get('superuser_id'):
            return redirect('SuperUser-Login')

        user = SuperUser.objects.get(
            id=request.session.get('superuser_id'),
            status='Active'
        )

        # ======================
        # ADD USER
        # ======================
        if request.method == "POST" and request.POST.get("action") == "add":

            zp_id = request.POST.get("zilla_parishad")
            name = request.POST.get("name")
            username = request.POST.get("username")
            password = request.POST.get("password")
            mobile = request.POST.get("mobile")
            email = request.POST.get("email")
            address = request.POST.get("address")
            status = request.POST.get("status")

            if not zp_id or not name or not username or not password:
                messages.error(request, "Required fields missing.")
                return redirect("ZP-Manage-Zilla-Parishad-User")

            try:
                zp = ZillaParishad.objects.get(id=zp_id)

                validate_clean_text(name, "Name")
                validate_clean_text(username, "Username")

                if mobile:
                    validate_mobile_number(mobile)
                if email:
                    validate_email(email)

            except ValidationError as e:
                messages.error(request, str(e))
                return redirect("ZP-Manage-Zilla-Parishad-User")

            if Zilla_Parishad_User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                return redirect("ZP-Manage-Zilla-Parishad-User")

            Zilla_Parishad_User.objects.create(
                zilla_parishad=zp,
                zilla_parishad_name=zp.zillaParishad_name,
                name=name,
                username=username,
                password=password,
                mobile=mobile,
                email=email,
                address=address,
                status=status
            )

            messages.success(request, "User created successfully.")
            return redirect("ZP-Manage-Zilla-Parishad-User")

        # ======================
        # EDIT USER (FIXED)
        # ======================
        if request.method == "POST" and request.POST.get("action") == "edit":

            edit_id = request.POST.get("edit_id")
            obj = get_object_or_404(Zilla_Parishad_User, id=edit_id)

            zp_id = request.POST.get("zilla_parishad") or obj.zilla_parishad.id
            name = request.POST.get("name")
            username = request.POST.get("username")
            password = request.POST.get("password")
            mobile = request.POST.get("mobile")
            email = request.POST.get("email")
            status = request.POST.get("status")

            if not name or not username:
                messages.error(request, "Required fields missing.")
                return redirect("ZP-Manage-Zilla-Parishad-User")

            try:
                zp = ZillaParishad.objects.get(id=zp_id)

                validate_clean_text(name, "Name")
                validate_clean_text(username, "Username")

                if mobile:
                    validate_mobile_number(mobile)
                if email:
                    validate_email(email)

            except ValidationError as e:
                messages.error(request, str(e))
                return redirect("ZP-Manage-Zilla-Parishad-User")

            if Zilla_Parishad_User.objects.filter(username=username).exclude(id=edit_id).exists():
                messages.error(request, "Username already exists.")
                return redirect("ZP-Manage-Zilla-Parishad-User")

            obj.zilla_parishad = zp
            obj.zilla_parishad_name = zp.zillaParishad_name
            obj.name = name
            obj.username = username
            obj.mobile = mobile
            obj.email = email
            obj.status = status

            if password and password.strip():
                obj.password = password

            obj.save()

            messages.success(request, "User updated successfully.")
            return redirect("ZP-Manage-Zilla-Parishad-User")

        # ======================
        # DELETE
        # ======================
        if request.GET.get("delete_id"):
            Zilla_Parishad_User.objects.filter(
                id=request.GET.get("delete_id")
            ).delete()

            messages.success(request, "User deleted successfully.")
            return redirect("ZP-Manage-Zilla-Parishad-User")

        # ======================
        # SEARCH + FILTER
        # ======================
        search = request.GET.get("search") or ""
        status = request.GET.get("status")

        users = Zilla_Parishad_User.objects.select_related("zilla_parishad").order_by("-id")

        if search:
            users = users.filter(
                Q(name__icontains=search) |
                Q(username__icontains=search) |
                Q(mobile__icontains=search) |
                Q(email__icontains=search) |
                Q(zilla_parishad_name__icontains=search)
            )

        if status:
            users = users.filter(status=status)

        paginator = Paginator(users, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "ZP-Manage-Zilla-Parishad-User.html", {
            "user": user,
            "users": page_obj,
            "search": search,
            "status": status,
            "all_zilla_parishad": ZillaParishad.objects.all()
        })

    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong.")
        return redirect("ZP-Manage-Zilla-Parishad-User")