from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.http import HttpResponse, HttpResponseRedirect

from courses.forms import ModuleFormset
from courses.models import Course, Module, Content, Subject, Word, UserWord
from django.contrib.auth.decorators import login_required

from .forms import SubjectForm, FlashCardForm
import random


class CreateCourse(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'subject', 'overview']
    template_name = 'courses/create_course.html'
    permission_required = 'course.add_course'
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('courses:view-subject', kwargs={"subject_id": self.object.subject.id})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateModule(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Module
    fields = ['course', 'title', 'description']
    template_name = 'courses/create_module.html'
    permission_required = 'course.add_module'
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('courses:view-course', kwargs={"course_id": self.object.course.id})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# class CourseModuleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
#     model = Module
#     fields = ['course', 'title', 'description']
#     template_name = 'courses/create_module.html'
#     permission_required = 'course.add_course'
#     login_url = reverse_lazy('login')
#     raise_exception = True
#
#     def get_success_url(self):
#         return reverse_lazy('courses:view-subjects', kwargs={"course_id": self.object.course.id})
#
#     def form_valid(self, form):
#         form.instance.owner = self.request.user
#         return super().form_valid(form)


# class CourseModuleUpdateView(TemplateResponseMixin, View):
#     template_name = 'courses/add_module_course.html'
#     course = None
#
#     def get_formset(self, data=None):
#         return ModuleFormset(instance=self.course, data=data)
#
#     def dispatch(self, request, *args, **kwargs):
#         self.course = get_object_or_404(Course, id=kwargs['pk'], owner=request.user)
#         return super().dispatch(request, kwargs['pk'])
#
#     def get(self, request, *args, **kwargs):
#         formset = self.get_formset()
#         return self.render_to_response({'course': self.course, 'formset': formset})
#
#     def post(self, request, *args, **kwargs):
#         formset = self.get_formset(data=request.POST)
#         if formset.is_valid():
#             formset.save()
#             return redirect('courses:view-course', kwargs={"course_id": self.course.id})
#             # return HttpResponseRedirect(request.META['HTTP_REFERER'])
#         return self.render_to_response({'course': self.course, 'formset': formset})


class CourseList(View):

    def get(self, request):
        courses_list = Course.objects.all().order_by("-created")

        paginator = Paginator(courses_list, 50)
        page = request.GET.get('page')
        courses = paginator.get_page(page)

        context = {"courses": courses}

        return render(request, 'courses/view_courses.html', context)


class CreateContent(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Content
    fields = ['module', 'owner', 'title', 'content_text', 'content_files', 'content_images', 'content_urls']
    template_name = 'courses/create_content.html'
    permission_required = 'course.add_content'
    login_url = reverse_lazy('login')
    raise_exception = True
    success_url = reverse_lazy('courses:view-subjects')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SubjectList(ListView):
    template_name = "courses/view_subjects.html"
    model = Subject
    context_object_name = 'subjects'


# class ModelList(ListView):
#     template_name = "courses/view.html"
#     model = Subject
#     context_object_name = 'subjects'


class SubjectDetails(View):
    def get(self, request, subject_id):
        subject = Subject.objects.get(pk=subject_id)
        courses = Course.objects.filter(subject=subject)

        return render(request, 'courses/view_subject.html', {'subject': subject, 'courses': courses})


class CourseDetails(View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        modules = Module.objects.filter(course=course)

        return render(request, 'courses/view_course.html', {'course': course, 'modules': modules})


class SubjectUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/edit_subject.html'
    subject = None

    def get_formset(self, data=None):
        return SubjectForm(instance=self.subject, data=data)

    def dispatch(self, request, *args, **kwargs):
        self.subject = get_object_or_404(Subject, id=kwargs['pk'])
        return super().dispatch(request, kwargs['pk'])

    def get(self, request, *args, **kwargs):
        form = self.get_formset()
        return self.render_to_response({'subject': self.subject, 'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_formset(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses:view-subjects')
        return self.render_to_response({'subject': self.subject, 'form': form})


class SubjectDeleteView(View):
    def get(self, request, subject_id):
        subject = Subject.objects.get(id=subject_id)
        subject.delete()
        return redirect("courses:view-subjects")


class ModuleDeleteView(View):
    def get(self, request, module_id):
        module = Module.objects.get(id=module_id)
        module.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ContentDeleteView(View):
    def get(self, request, content_id):
        content = Content.objects.get(id=content_id)
        content.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class SubjectCreate(LoginRequiredMixin, CreateView):
    model = Subject
    fields = ['title']
    template_name = 'courses/create_subject.html'
    login_url = reverse_lazy('login')
    raise_exception = True
    success_url = reverse_lazy('courses:view-subjects')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ContentListView(ListView):
    template_name = "courses/view_contents.html"
    model = Content
    context_object_name = 'contents'


class CourseDeleteView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def learn(request):
    all_cards = Word.objects.all()
    cards = all_cards.filter(known=0)
    cards = sorted(cards.order_by('likes'), key=lambda x: random.random())
    context = {'card': cards[0]}
    return render(request, 'courses/learn.html', context)


def mark_known(request, id):
    card = UserWord.objects.get(id=id)
    card.known += 1
    card.save()
    return redirect('courses:learn')

