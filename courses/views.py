from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import TemplateResponseMixin, View

from courses.forms import ModuleFormset
from courses.models import Course, Module, Content, Subject


class CreateCourse(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Course
    fields = ['title', 'subject', 'overview']
    template_name = 'courses/create_course.html'
    permission_required = 'course.add_course'
    login_url = reverse_lazy('login')
    raise_exception = True
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/add_module_course.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormset(instance=self.course, data=data)

    def dispatch(self, request, *args, **kwargs):
        self.course = get_object_or_404(Course, id=kwargs['pk'], owner=request.user)
        return super().dispatch(request, kwargs['pk'])

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:home')
        return self.render_to_response({'course': self.course, 'formset': formset})


class CourseList(View):

    def get(self, request):
        courses_list = Course.objects.all().order_by("-created")

        paginator = Paginator(courses_list, 50)
        page = request.GET.get('page')
        courses = paginator.get_page(page)

        context = {"courses": courses}

        return render(request, 'courses/view_courses.html', context)


class CreateModule(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Module
    fields = ['course', 'title', 'description']
    template_name = 'courses/create_module.html'
    permission_required = 'course.add_module'
    login_url = reverse_lazy('login')
    raise_exception = True
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CreateContent(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Content
    fields = ['module', 'owner', 'title', 'content_text', 'content_files', 'content_images', 'content_urls']
    template_name = 'courses/create_content.html'
    permission_required = 'course.add_content'
    login_url = reverse_lazy('login')
    raise_exception = True
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SubjectList(ListView):
    template_name = "courses/view_subjects.html"
    model = Subject
    context_object_name = 'subjects'


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
