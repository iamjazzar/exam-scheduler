from django.db import models


class Course(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Do add the instructor

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Student(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    courses = models.ManyToManyField(
        Course, help_text='The current courses this student enrolls '
                          'in.')

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Hall(models.Model):
    hall_number = models.CharField(
        max_length=16, unique=True, help_text='The unique hall number')
    not_available = models.BooleanField(
        help_text='Check if this hall cannot hold exam sessions '
                  'whether it\'s booked or not.')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.hall_number

    def __str__(self):
        return self.hall_number


class HallBooking(models.Model):
    start = models.DateTimeField(
        help_text='The start date and time the hall is booked in.')
    end = models.DateTimeField(
        help_text='The last date and time the hall is booked in.'
    )
    hall = models.ForeignKey(to=Hall)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'From {} to {}'.format(self.start, self.end)

    def __str__(self):
        return 'From {} to {}'.format(self.start, self.end)


class ScheduleConfig(models.Model):
    start = models.DateTimeField(
        help_text='The start date of the first exam and the start '
                  'time of the first session in each day.')
    end = models.DateTimeField(
        help_text='The end date of the last exam and the end time '
                  'of the last session in each day.')

    exam_period = models.PositiveSmallIntegerField(
        help_text='Set it to 2 For if for example, your university '
                  'uses a 2-hours exam period')
    maximum_daily_exams = models.PositiveSmallIntegerField(
        help_text='A fairness requirement that each student shall not '
                  'have more exams than it per day.')
    maximum_gap = models.PositiveSmallIntegerField(
        help_text='A student shall not have a gap of more than the '
                  'specified days between two successive exams ('
                  'another fairness requirement).')
    halls = models.ManyToManyField(
        Hall, help_text='The halls the exams will be held in.')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def days_number(self):
        """
        Calculates the exact number of days scheduled for examining
        :return: The total number of exams days
        """
        return self.end.day - self.start.day + 1

    def time_slots(self):
        """
        The number of exam periods per day (Time Slots (TS)) model.
        It depends on college/department specific constraints.

        :return: The time slots (TS)
        """
        total_hours = self.end.hour - self.start.hour
        return total_hours / self.exam_period

    def __unicode__(self):
        return '{}Daily {}Gap {}Days'.format(
            self.maximum_daily_exams, self.maximum_gap,
            self.days_number())

    def __str__(self):
        return '{}Daily {}Gap {}Days'.format(
            self.maximum_daily_exams, self.maximum_gap,
            self.days_number())
