from django.contrib import admin
from .models import *

#Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_no','building','is_active','status','total_price')



@admin.register(Renter)
class RenterAdmin(admin.ModelAdmin):
    pass

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('total_paid',)


# admin.site.register(Penality)
admin.site.register(Payment)
admin.site.register(Building)
admin.site.register(UserAdditionalInfo)