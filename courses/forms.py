from django import forms
from django.forms import inlineformset_factory
from .models import Course, Module, Subject

ModuleFormset = inlineformset_factory(Course, Module, fields=['title', 'description'], extra=2, can_delete=True)


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']

