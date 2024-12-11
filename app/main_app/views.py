from django.shortcuts import render
from .models import Brigade, Locomotive, Worker, Repair

def index(request):
    brigades = Brigade.objects.all()
    locomotives = Locomotive.objects.all()
    workers = Worker.objects.all()
    repairs = Repair.objects.all()

    return render(request, 'index.html', {
        'brigades': brigades,
        'locomotives': locomotives,
        'workers': workers,
        'repairs': repairs
    })
