from django.contrib import admin
from .models import JobCategory, JobSubCategory, Education,WorkType, WorkFormat,CompanyType,Resume, Language, Job, Skill, FavoriteJob, SentResume
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(JobSubCategory)
class JobSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('specialty', 'education_level', 'city')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'experience_years', 'preferred_city')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'city', 'salary_min', 'salary_max', 'category', 'subcategory')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)  

@admin.register(WorkFormat)
class WorkFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(FavoriteJob)
class FavoriteJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job')

@admin.register(SentResume)
class SentResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'resume')
