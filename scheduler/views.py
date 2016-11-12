from django.utils import timezone
from django.views.generic import TemplateView

from scheduler.graph import CoursesGraph
from scheduler.models import HallBooking


class Home(TemplateView):
    """
    TODO: Locate custom data for each user
    TODO: Let the user decide which courses she want to schedule
    """
    template_name = 'schedule.html'


class Schedule(TemplateView):
    template_name = 'schedule.html'

    def get_context_data(self, **kwargs):
        context = super(Schedule, self).get_context_data(**kwargs)

        context['data'] = {
            # 'graph': CoursesGraph().nodes_degree(),
            'halls': HallBooking.available_halls(timezone.now()),
            'len': [len(HallBooking.available_halls(timezone.now()))],
        }

        return context
