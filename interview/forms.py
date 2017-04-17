# -*- coding: utf-8 -*-
import datetime

from django import forms
from django.forms import Select
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Column, Fieldset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget

from interview.models import Subsidiary, Consultant, Interview, Candidate, Process, Sources, SourcesCategory
from pyoupyou.settings import DOCUMENT_TYPE, MINUTE_FORMAT

class MultipleConsultantWidget(ModelSelect2MultipleWidget):
    model = Consultant
    search_fields = [
        'user__trigramme__icontains',
        'user__full_name__icontains',
    ]


class SourcesWidget(ModelSelect2Widget):
    model = Sources
    search_fields = [
        'name__icontains',
    ]

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        helper = FormHelper()
        exclude = []

    cv = forms.FileField(label="CV (pour une candidature)", required=True)

    helper = FormHelper()
    helper.form_tag = False


class SelectOrCreate(SourcesWidget):
    def render(self, name, value, attrs=None):
        output = [super().render(name, value, attrs),]
        output.append(render_to_string('interview/select_or_create_source.html'))
        return mark_safe('\n'.join(output))


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        exclude = ['candidate', 'start_date', 'end_date']

        widgets = {
            'sources': SelectOrCreate
        }
    helper = FormHelper()
    helper.form_tag = False


class SourceForm(forms.ModelForm):
    class Meta:
        model = Sources
        fields = ['category', 'name']
    helper = FormHelper()
    helper.form_tag = False


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['planned_date', 'interviewers']

        widgets = {
            'interviewers': MultipleConsultantWidget,
        }

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('summit', _('Save'), css_class='btn-primary'))


class InterviewFormPlan(InterviewForm):
    class Meta:
        model = Interview
        fields = ['planned_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper.layout = Layout(
            Div(
                Column(
                    'planned_date',
                ),
                css_class='relative'
            )
        )

class InterviewFormEditInterviewers(InterviewForm):
    class Meta:
        model = Interview
        fields = ['interviewers']
        widgets = {
            'interviewers': MultipleConsultantWidget,
        }


class InterviewMinuteForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['minute', 'suggested_interviewer', 'next_interview_goal', 'next_state', ]

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('summit', _('Save'), css_class='btn-primary'))
