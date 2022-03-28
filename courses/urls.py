from django.http import HttpResponse
from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('home', lambda x: HttpResponse('home'), name='home'),
    path('<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course-modules-update'),
    path('create', views.CreateCourse.as_view(), name='create-course'),
    path('all/', views.CourseList.as_view(), name='view-course'),
    # path('subjects/', views.CourseList.as_view(), name='view-subjects'),
]