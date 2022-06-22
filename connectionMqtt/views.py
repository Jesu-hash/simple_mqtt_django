from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def connectConnection(request):
    return render(request,"menuConnection.html")

