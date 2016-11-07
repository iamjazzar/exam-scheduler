from django.db import models


class Course(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=64)

    # Do add the instructor

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Student(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)

    # The current courses this student is enroll in
    courses = models.ManyToManyField(Course)

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
