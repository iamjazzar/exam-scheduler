from django.db import models
from django.db.models import Q


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


class TimeSlot(models.Model):
    exam_period = models.PositiveSmallIntegerField(
        help_text='Set it to 2 For if for example, your university '
                  'uses a 2-hours exam period')
    starting_time = models.TimeField(
        help_text='First exam starting hour.')
    closing_time = models.TimeField(
        help_text='Last exam finishing hour.')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

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


class Hall(models.Model):
    hall_number = models.CharField(
        max_length=16, unique=True, help_text='The unique hall number')
    not_availble = models.BooleanField(
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

    @staticmethod
    def available_times(time):
        """
        Filters the objects in a given time to fetch the available
        times QuerySet.

        :param time: The time we need to check the available halls in.
        :return: A QuerySet of the available time in the given time.
        """
        return HallBooking.objects.filter(
            Q(start__gt=time) | Q(end__lt=time)
        )

    @staticmethod
    def available_halls(time):
        """
        Generates a set of the available halls in a given time.
        It represents he number of concurrent exam sessions or
        concurrency level (Np) and the availability of faculty to
        conduct the exams.

        :param time: The time we need to check the available halls in.
        :return: The available halls in the given time.
        """
        return {
            b.hall for b in HallBooking.available_times(time) if
            not b.hall.not_availble
        }

    def __unicode__(self):
        return 'From {} to {}'.format(self.start, self.end)

    def __str__(self):
        return 'From {} to {}'.format(self.start, self.end)


class ScheduleConfig(models.Model):
    start_day = models.DateField()
    end_day = models.DateField()

    maximum_daily_exams = models.PositiveSmallIntegerField(
        help_text='A fairness requirement that each student shall not '
                  'have more exams than it per day.')
    maximum_gap = models.PositiveSmallIntegerField(
        help_text='A student shall not have a gap of more than the '
                  'specified days between two successive exams ('
                  'another fairness requirement).')
    halls = models.ManyToManyField(
        Hall, help_text='The halls the exams will be held in.')
    slots = models.ForeignKey(to=TimeSlot, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def days_number(self):
        return (self.end_day - self.start_day).days

    def __unicode__(self):
        return '{} Hours for {} days'.format(
            self.slots.exam_period, self.days_number())

    def __str__(self):
        return '{} Hours for {} days'.format(
            self.slots.exam_period, self.days_number())
