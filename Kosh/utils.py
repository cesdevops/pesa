
from Kosh.models import Kosh_User


def switch_kosh(request):
    """
    Returns kosh switcher data for navbar.
    Call this in any view and merge into context.
    """
    if request.session.get('user_type') != 'Kosh':
        return {}

    user_id = request.session.get('user_id')
    active_kosh_id = request.session.get('active_kosh_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        return {}

    all_kosh = kosh_user.kosh.filter(status='Active', is_deleted=False)

    return {
        'all_kosh': all_kosh,
        'active_kosh_id': active_kosh_id,
        'show_switcher': all_kosh.count() > 1,
    }


