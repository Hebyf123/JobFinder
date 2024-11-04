from django.db.models import Q

def recommend_jobs_for_worker(worker_resume):

    jobs = Job.objects.all()

    # Фильтруем вакансии по категориям и подкатегориям
    jobs = jobs.filter(
        Q(category=worker_resume.category) |
        Q(subcategory=worker_resume.subcategory)
    )
    
    # Фильтруем по навыкам (минимум 75% совпадение)
    worker_skills = set(worker_resume.skills.all())
    jobs = jobs.filter(
        skills__in=worker_skills
    ).distinct()

    # Проверяем опыт работы
    jobs = jobs.filter(required_experience__lte=worker_resume.experience_years)

    # Проверяем зарплатный диапазон (с учётом 20% отклонения)
    salary_min = worker_resume.salary_range_min * 0.8
    salary_max = worker_resume.salary_range_max * 1.2
    jobs = jobs.filter(
        Q(salary_min__gte=salary_min) &
        Q(salary_max__lte=salary_max)
    )

    # Проверяем формат работы (если офлайн - сравниваем город)
    if worker_resume.work_format == 'offline':
        jobs = jobs.filter(city=worker_resume.preferred_city)

    # Проверка английского языка, если требуется
    jobs = jobs.filter(
        Q(languages__level__lte='intermediate') |
        Q(languages__isnull=True)
    )

    # Проверка уровня образования (бакалавр или ниже)
    jobs = jobs.filter(
        Q(education_levels__education_level__lte='bachelor') |
        Q(education_levels__isnull=True)
    )

    return jobs
from django.db.models import Q
from decimal import Decimal

def recommend_worker_for_jobs(job):


    # Определяем диапазон допустимых зарплат (± 20%)
    salary_min_threshold = job.salary_min * Decimal('0.80')
    salary_max_threshold = job.salary_max * Decimal('1.20')

    # Начальные фильтры по навыкам, опыту и категории
    recommended_workers = Resume.objects.filter(
        skills__in=job.skills.all(),  # Учитываем совпадение навыков
        experience_years__gte=job.required_experience,  # Опыт работы не меньше требуемого
        salary_range_min__lte=salary_max_threshold,  # Проверка на минимальную зарплату работника
        salary_range_max__gte=salary_min_threshold,  # Проверка на максимальную зарплату работника
        work_type=job.work_type  # Тип занятости (полный/частичный/контракт)
    ).distinct()

    # Учитываем формат работы (онлайн/офлайн)
    if job.work_format == 'offline':
        # Если формат офлайн, проверяем город
        recommended_workers = recommended_workers.filter(preferred_city=job.city)
    elif job.work_format == 'online':
        # Для онлайн работы город не учитывается
        pass

    # Учитываем требования к образованию
    education_levels = job.education_levels.all()
    if education_levels.exists():
        recommended_workers = recommended_workers.filter(education__education_level__in=education_levels.values_list('education_level', flat=True))

    # Учитываем требования к языкам
    required_languages = job.languages.all()
    if required_languages.exists():
        recommended_workers = recommended_workers.filter(
            Q(languages__name__in=required_languages.values_list('name', flat=True),
              languages__level__gte='intermediate')  # Учитываем минимальный уровень английского (средний)
        )

    # Сортировка по количеству совпадений навыков (75% и выше)
    final_recommended_workers = []
    for worker in recommended_workers:
        matched_skills = worker.skills.filter(id__in=job.skills.all()).count()
        total_skills = job.skills.count()

        if total_skills > 0 and (matched_skills / total_skills) >= 0.75:
            final_recommended_workers.append(worker)

    return final_recommended_workers
