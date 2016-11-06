from django.db import models


class Student(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)

    # The current courses this student is enroll in
    courses = models.ForeignKey(to='scheduler.Course')


class Course(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=64)

    # Do add the instructor
