from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet,FavoriteWorkerViewSet,    CompanyTypeViewSet,WorkTypeViewSet,WorkFormatViewSet, SkillViewSet,EmployerOfferViewSet, EducationViewSet, JobViewSet, LanguageViewSet, JobCategoryViewSet, JobSubCategoryViewSet, FavoriteJobViewSet, SentResumeViewSet
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi
router = DefaultRouter()
router.register(r'resumes', ResumeViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'languages', LanguageViewSet)
router.register(r'job-categories', JobCategoryViewSet)
router.register(r'job-sub-categories', JobSubCategoryViewSet)
router.register(r'employer-offers', EmployerOfferViewSet, basename='employer-offers')
router.register(r'favorite-worker', FavoriteWorkerViewSet, basename='favorite-worker')
router.register(r'favorite-jobs', FavoriteJobViewSet, basename='favorite-jobs')
router.register(r'employer-offers', EmployerOfferViewSet)
router.register(r'sent-resumes', SentResumeViewSet)
router.register(r'company-type', CompanyTypeViewSet)
router.register(r'work-type', WorkTypeViewSet)
router.register(r'work-format', WorkFormatViewSet)
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API для работы с продуктами, категориями, вариантами и отзывами.",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,  
    permission_classes=(permissions.IsAdminUser,),
)
urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]


