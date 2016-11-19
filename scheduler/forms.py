from django import forms
from django.utils.translation import gettext_lazy as _


class ScheduleConfigForm(forms.ModelForm):
    def clean_end(self):
        """
        Checks if the end date and hour values are correct
        :return: the passed date and hour or raise a validation error
        """
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']

        if end.day <= start.day:
            raise forms.ValidationError(
                _('The End day must be after the start day!'))

        if end.hour <= start.hour:
            raise forms.ValidationError(
                _('The last session hour must be after the first one!'))

        return end

    def clean_exam_period(self):
        """
        Checks if the exam period exceeded the allocated hours for
        all exams
        :return: exam period if cleaned or raise a validation error
        """
        exam_period = self.cleaned_data['exam_period']
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']

        if exam_period > end.hour - start.hour:
            raise forms.ValidationError(
                _('The exam period must not exceed the the daily '
                  'available time between the session start and end '
                  'hours'))

        return exam_period


class HallBookingForm(forms.ModelForm):
    def clean_end(self):
        """
        Checks if the end date is after the start date
        :return: the passed date and hour or raise a validation error
        """
        start = self.cleaned_data['start']
        end = self.cleaned_data['end']

        if end <= start:
            raise forms.ValidationError(
                _('The End date must be after the start date!'))

        return end
