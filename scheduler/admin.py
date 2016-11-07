from django.contrib import admin

from models import Course, Student

class StudentAdmin(admin.ModelAdmin):
    search_fields = ['id']

admin.site.register(Course, admin.ModelAdmin)
admin.site.register(Student, StudentAdmin)
