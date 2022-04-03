from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.loader import render_to_string
from django.utils.text import slugify


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Course(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='courses_created')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='courses')

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(get_user_model(), related_name='courses_joined', blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Module(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey('Module', related_name='contents', on_delete=models.CASCADE)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='%(class)s_related')
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content_text = models.TextField(blank=True)
    content_files = models.FileField(upload_to='files', blank=True)
    content_images = models.FileField(upload_to='content_images', blank=True)
    content_urls = models.URLField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)


class Word(models.Model):
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    translation = models.CharField(max_length=200, blank=True)
    language = models.ForeignKey('Subject', related_name='words', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    known = models.IntegerField(default=0)
    category = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.source


class UserWord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    word = models.ForeignKey('Word', related_name='user_words', on_delete=models.CASCADE)
    known = models.IntegerField(default=0)

