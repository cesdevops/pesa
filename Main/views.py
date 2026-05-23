from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from ZillaParishad.models import Zilla_Parishad_User
from Kosh.models import Kosh_User
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from ZillaParishad.models import Zilla_Parishad_User
from PanchayatSamiti.models import Panchayat_Samiti, Panchayat_Samiti_User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Main.models import Super_User
from ZillaParishad.models import Zilla_Parishad
from django.core.paginator import Paginator
from django.http import JsonResponse


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

                    ps_user = PanchayatSamitiUser.objects.get(
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

                except PanchayatSamitiUser.DoesNotExist:

                    messages.error(request, "Panchayat Samiti User Not Found")
                    return redirect('Login')



            # =====================================================
            # Kosh Login
            # =====================================================

            elif login_type == "Kosh":

                try:

                    kosh_user = KoshUser.objects.get(
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

                except KoshUser.DoesNotExist:

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











