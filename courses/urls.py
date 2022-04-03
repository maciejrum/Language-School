from django.http import HttpResponse
from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    # path('', views.ViewCourses.as_view(), name='courses'),
    # path('module/edit/<pk>/', views.CourseModuleUpdateView.as_view(), name='course-modules-update'),
    path('create', views.CreateCourse.as_view(), name='create-course'),
    path('create/module', views.CreateModule.as_view(), name='create-module'),
    path('create/module/content', views.CreateContent.as_view(), name='create-content'),
    path('all/', views.CourseList.as_view(), name='view-courses'),
    path('subjects/', views.SubjectList.as_view(), name='view-subjects'),
    path('subjects/<int:subject_id>', views.SubjectDetails.as_view(), name='view-subject'),
    path('subjects/edit/<pk>/', views.SubjectUpdateView.as_view(), name='edit-subject'),
    path('courses/<int:course_id>', views.CourseDetails.as_view(), name='view-course'),
    path('subject/delete/<int:subject_id>', views.SubjectDeleteView.as_view(), name='delete-subject'),
    path('subject/delete/course/<int:course_id>', views.CourseDeleteView.as_view(), name='delete-course'),
    path('subject/delete/module/<int:module_id>', views.ModuleDeleteView.as_view(), name='delete-module'),
    path('subject/create/', views.SubjectCreate.as_view(), name='create-subject'),
    path('subject/modules/', views.ContentListView.as_view(), name='view-content'),
    path('learn/', views.learn, name='learn'),
    path('mark_known/<id>', views.mark_known, name='mark_known'),
]