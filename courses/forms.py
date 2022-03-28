from django import forms
from django.forms import inlineformset_factory, BaseFormSet
from .models import Course, Module, Subject

ModuleFormset = inlineformset_factory(Course, Module, fields=['title', 'description'], extra=0, can_delete=True)

# CourseFormset = inlineformset_factory(Subject, Course, fields=['title', 'overview'], extra=0, can_delete=True)
