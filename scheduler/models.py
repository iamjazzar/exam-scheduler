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

    courses = models.ManyToManyField(
        Course, help_text='The current courses this student enrolls in')

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class TimeSlot(models.Model):
    exam_period = models.PositiveSmallIntegerField(
        help_text='Set it to 2 For if for example, your university '
                  'uses a 2-hours exam period')
    starting_time = models.TimeField(
        help_text='First exam starting hour')
    closing_time = models.TimeField(
        help_text='Last exam finishing hour')

    def time_slots(self):
        """
        The number of exam periods per day (Time Slots (TS)) model.
        It depends on college/department specific constraints.

        :return: The time slots (TS)
        """
        total_hours = self.closing_time.hour - self.starting_time.hour
        return total_hours / self.exam_period

    def __unicode__(self):
        return '{} Time Slots'.format(self.time_slots())

    def __str__(self):
        return '{} Time Slots'.format(self.time_slots())


class ScheduleConfig(models.Model):
    start_day = models.DateField()
    end_day = models.DateField()
    slots = models.ForeignKey(to=TimeSlot, null=True)

    def days_number(self):
        return (self.end_day - self.start_day).days

    def __unicode__(self):
        return '{} Hours for {} days'.format(
            self.slots.exam_period, self.days_number())

    def __str__(self):
        return '{} Hours for {} days'.format(
            self.slots.exam_period, self.days_number())
