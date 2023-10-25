from django.contrib import admin
from .models import User, Lab, Payment, Reservation
# Register your models here.

admin.site.register(User)
admin.site.register(Lab)
admin.site.register(Payment)
admin.site.register(Reservation)
