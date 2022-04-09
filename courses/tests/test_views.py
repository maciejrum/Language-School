from django.contrib.auth.models import Permission, Group
from django.urls import reverse


def test_view_create_course_for_anonymous_user(client):
    url = reverse('courses:create-course')
    response = client.get(url)
    assert response.status_code == 403


def test_view_create_subjects_for_anonymous_user(client):
    url = reverse('courses:create-subject')
    response = client.get(url)
    assert response.status_code == 403


