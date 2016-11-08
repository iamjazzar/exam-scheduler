from django.views.generic import TemplateView

from scheduler.graph import CoursesGraph


class Home(TemplateView):
    """
    TODO: Locate custom data for each user
    TODO: Let the user decide which courses she want to schedule
    """
    template_name = 'schedule.html'


class Schedule(TemplateView):
    template_name = 'schedule.html'
