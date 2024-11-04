import django_filters
from django.utils.translation import gettext as _
from django.utils.timezone import now
from datetime import timedelta
from .models import Job, Education, Language, JobCategory, JobSubCategory, WORK_TYPE_CHOICES, WORK_FORMAT_CHOICES

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', field_name='title', label=_('Название вакансии'))
    salary_min = django_filters.NumberFilter(field_name='salary_min', lookup_expr='gte', label=_('Минимальная зарплата от'))
    salary_max = django_filters.NumberFilter(field_name='salary_max', lookup_expr='lte', label=_('Максимальная зарплата до'))
    city = django_filters.CharFilter(lookup_expr='icontains', label=_('Город'))
    work_type = django_filters.ChoiceFilter(choices=WORK_TYPE_CHOICES, label=_('Тип занятости'))
    work_format = django_filters.ChoiceFilter(choices=WORK_FORMAT_CHOICES, label=_('Формат работы'))
    education_levels = django_filters.ModelMultipleChoiceFilter(queryset=Education.objects.all(), label=_('Образование'))
    languages = django_filters.ModelMultipleChoiceFilter(queryset=Language.objects.all(), label=_('Языки'))
    category = django_filters.ModelChoiceFilter(queryset=JobCategory.objects.all(), label=_('Категория'))
    subcategory = django_filters.ModelChoiceFilter(queryset=JobSubCategory.objects.all(), label=_('Подкатегория'))
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label=_('Создано после (дата)'))
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label=_('Создано до (дата)'))
    created_today = django_filters.BooleanFilter(method='filter_created_today', label=_('За сегодня'))
    created_this_week = django_filters.BooleanFilter(method='filter_created_this_week', label=_('За эту неделю'))

    class Meta:
        model = Job
        fields = [
            'title', 'salary_min', 'salary_max', 'city', 'work_type', 'work_format',
            'education_levels', 'languages', 'category', 'subcategory', 
            'created_at__gte', 'created_at__lte'
        ]

    def filter_created_today(self, queryset, name, value):
        if value:
            today = now().date()
            return queryset.filter(created_at__date=today)
        return queryset

    def filter_created_this_week(self, queryset, name, value):
        if value:
            start_of_week = now() - timedelta(days=now().weekday())  # Начало недели (понедельник)
            return queryset.filter(created_at__gte=start_of_week)
        return queryset
