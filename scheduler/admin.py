from django.contrib import admin

from models import Course, Student

admin.site.register(Course, admin.ModelAdmin)
admin.site.register(Student, admin.ModelAdmin)
