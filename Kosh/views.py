from django.shortcuts import render

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