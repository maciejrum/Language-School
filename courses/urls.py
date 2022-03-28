from django.http import HttpResponse
from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    # path('', views.ViewCourses.as_view(), name='courses'),
    path('edit/<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course-modules-update'),
    path('create', views.CreateCourse.as_view(), name='create-course'),
    path('create/module', views.CreateModule.as_view(), name='create-module'),
    path('create/module/content', views.CreateContent.as_view(), name='create-content'),
    path('all/', views.CourseList.as_view(), name='view-course'),
    path('subjects/', views.SubjectList.as_view(), name='view-subjects'),
    path('subjects/<int:subject_id>', views.SubjectDetails.as_view(), name='view-subject'),
    path('courses/<int:course_id>', views.CourseDetails.as_view(), name='view-course'),
]