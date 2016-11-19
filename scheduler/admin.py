from django.contrib import admin

from models import Course, Student, ScheduleConfig, Hall, HallBooking
from scheduler.forms import ScheduleConfigForm, HallBookingForm


class HallBookingInline(admin.TabularInline):
    model = HallBooking
    form = HallBookingForm
    extra = 1


class StudentAdmin(admin.ModelAdmin):
    search_fields = [
        'id',
    ]


class HallAdmin(admin.ModelAdmin):
    inlines = [
        HallBookingInline,
    ]


class ScheduleConfigAdmin(admin.ModelAdmin):
    form = ScheduleConfigForm

admin.site.register(Course, admin.ModelAdmin)
admin.site.register(ScheduleConfig, ScheduleConfigAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Hall, HallAdmin)
