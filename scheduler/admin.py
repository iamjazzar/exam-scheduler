from django.contrib import admin

from models import Course, Student, ScheduleConfig, TimeSlot, Hall, \
    HallBooking


class StudentAdmin(admin.ModelAdmin):
    search_fields = [
        'id',
    ]


class HallBookingInline(admin.TabularInline):  # pylint: disable=C0111
    model = HallBooking


class HallAdmin(admin.ModelAdmin):
    inlines = [
        HallBookingInline,
    ]

admin.site.register(Course, admin.ModelAdmin)
admin.site.register(TimeSlot, admin.ModelAdmin)
admin.site.register(ScheduleConfig, admin.ModelAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Hall, HallAdmin)
