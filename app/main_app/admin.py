from django.contrib import admin
from .models import Brigade, Locomotive, Worker, Repair

admin.site.register(Brigade)
admin.site.register(Locomotive)
admin.site.register(Worker)
admin.site.register(Repair)
