from django.conf import settings

def active_clients_to_context(request):
    #active_clients = request.session.get('active_clients', 0)
    
    logged_user = request.session.get('logged_user', '')

    active_clients = request.session.get('active_clients', 0)

    return {'global_active_clients': settings.ACTIVE_CONNECTIONS,'active_clients': active_clients,'active_user': logged_user}
