from django.contrib import admin

from models import Course, Student, ScheduleConfig, TimeSlot


class StudentAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(Course, admin.ModelAdmin)
admin.site.register(TimeSlot, admin.ModelAdmin)
admin.site.register(ScheduleConfig, admin.ModelAdmin)
admin.site.register(Student, StudentAdmin)
