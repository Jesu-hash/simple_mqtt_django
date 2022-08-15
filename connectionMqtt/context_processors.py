from django.conf import settings

def active_clients_to_context(request):
    #active_clients = request.session.get('active_clients', 0)

    return {'active_clients': settings.ACTIVE_CONNECTIONS}
