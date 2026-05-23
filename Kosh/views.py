from django.shortcuts import redirect, render

from Main.models import Super_User
from PanchayatSamiti.models import Panchayat_Samiti
from django.contrib import messages
from .models import GramPanchayat
# Create your views here.
def Kosh_Dashboard(request):

    context = {

        'user_type': 'Kosh'

    }

    return render(
        request,
        'Kosh_dashboard.html',
        context
    )



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