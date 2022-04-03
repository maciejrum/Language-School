from django.contrib import admin

from .models import Subject, Module, Course, Content, Word, UserWord


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created')
    list_filter = ('created', 'subject')
    search_fields = ('title', 'overview')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (ModuleInline,)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'title']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('module', 'owner', 'title', 'content_text', 'content_files', 'content_images', 'content_urls')


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'source', 'translation', 'language', 'likes', 'known')


@admin.register(UserWord)
class UserWordAdmin(admin.ModelAdmin):
    list_display = ('user', 'word', 'known')


