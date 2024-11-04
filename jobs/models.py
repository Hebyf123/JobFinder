from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from .validators import validate_file_size, validate_positive,validate_positive_exp, validate_email, validate_phone
from django.utils import timezone
WORK_TYPE_CHOICES = [
    ('fulltime', _('Полный рабочий день')),
    ('parttime', _('Частичная занятость')),
    ('contract', _('Контракт')),
]

WORK_FORMAT_CHOICES = [
    ('offline', _('Оффлайн')),
    ('online', _('Онлайн')),
    ('hybrid', _('Гибрид')),
]

WORK_TYPES_CHOICES = [
    ('Sturtup', _('Стартап')),
    ('Product', _('Продукт')),
    ('Outsource', _('Аутсорс')),
    ('Outstaff', _('Аутстаф')),
]


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class JobCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название категории"))

    def __str__(self):
        return self.name


class JobSubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название подкатегории"))
    category = models.ForeignKey(JobCategory, related_name='subcategories', on_delete=models.CASCADE, verbose_name=_("Категория"))

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Education(models.Model):
    LEVEL_CHOICES = [
        ('highschool', _('Среднее образование')),
        ('bachelor', _('Бакалавр')),
        ('master', _('Магистр')),
        ('phd', _('Доктор наук')),
    ]
    
    city = models.CharField(max_length=100, verbose_name=_("Город"))
    specialty = models.CharField(max_length=255, verbose_name=_("Специальность"))
    start_date = models.DateField(verbose_name=_("Начало обучения"))
    end_date = models.DateField(verbose_name=_("Окончание обучения"), blank=True, null=True)
    education_level = models.CharField(max_length=50, choices=LEVEL_CHOICES, verbose_name=_("Уровень образования"))

    def __str__(self):
        return f"{self.specialty}, {self.get_education_level_display()}"


class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    phone = models.CharField(max_length=20, validators=[validate_phone], verbose_name=_("Телефон"))
    email = models.EmailField(validators=[validate_email], verbose_name=_("Электронная почта"))
    linkedin = models.URLField(blank=True, null=True, verbose_name=_("Профиль LinkedIn"))
    skills = models.ManyToManyField('Skill', verbose_name=_("Навыки"))
    experience_years = models.IntegerField(validators=[validate_positive], verbose_name=_("Опыт работы (в годах)"))
    preferred_city = models.CharField(max_length=100, verbose_name=_("Предпочитаемый город"))
    birth_date = models.DateField(verbose_name=_("Дата рождения"))
    education = models.ManyToManyField(Education, verbose_name=_("Образование"))
    languages = models.ManyToManyField('Language', verbose_name=_("Языки"))
    salary_range_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], verbose_name=_("Минимальная зарплата"))
    salary_range_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], verbose_name=_("Максимальная зарплата"))
    resume_file = models.FileField(upload_to='resumes/', validators=[validate_file_size], blank=True, null=True, verbose_name=_("Резюме (файл)"))
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES, verbose_name=_("Тип занятости"))
    work_format = models.CharField(max_length=50, choices=WORK_FORMAT_CHOICES, verbose_name=_("Формат работы"))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("Количество просмотров"))
    created_at = models.DateTimeField(auto_now_add=True, null = True,verbose_name=_("Дата создания"))

    def increment_view_count(self):
     
        self.view_count += 1
        self.save()
        from .tasks import send_notification_email
        if self.view_count % 5 == 0: 
            message = f"Ваше Резюме  было просмотрено {self.view_count} раз."
            send_notification_email.delay(self.user.id, "Уведомление о просмотрах", message)
    def clean(self):
        if self.salary_max < self.salary_min:
            raise ValidationError({
                'salary_max': _('Максимальная зарплата не может быть меньше минимальной зарплаты.')
            })

    def __str__(self):
        return f"{self.user.username}'s Resume"


class WorkType(models.Model):
    name = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES, verbose_name=_("Тип занятости"))

    def __str__(self):
        return self.get_name_display()


class WorkFormat(models.Model):
    name = models.CharField(max_length=50, choices=WORK_FORMAT_CHOICES, verbose_name=_("Формат работы"))

    def __str__(self):
        return self.get_name_display()


class CompanyType(models.Model):
    name = models.CharField(max_length=50, choices=WORK_TYPES_CHOICES, verbose_name=_("Тип компании"))

    def __str__(self):
        return self.get_name_display()


class Language(models.Model):
    LEVEL_CHOICES = [
        ('beginner', _('Начальный')),
        ('intermediate', _('Средний')),
        ('advanced', _('Продвинутый')),
        ('native', _('Носитель языка')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_("Язык"))
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, verbose_name=_("Уровень владения"))

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Ожидает модерации')),
        ('approved', _('Одобрено')),
        ('rejected', _('Отклонено')),
    ]
    
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Работодатель"), default=None)
    title = models.CharField(max_length=255, verbose_name=_("Название вакансии"))
    description = models.TextField(verbose_name=_("Описание работы"))
    skills = models.ManyToManyField('Skill', verbose_name=_("Навыки"))
    required_experience = models.IntegerField(validators=[validate_positive_exp], verbose_name=_("Опыт работы (в годах)"))
    city = models.CharField(max_length=100, verbose_name=_("Город"))
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], verbose_name=_("Минимальная зарплата"))
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], verbose_name=_("Максимальная зарплата"))
    category = models.ForeignKey(JobCategory, related_name='jobs', on_delete=models.SET_NULL, null=True, verbose_name=_("Категория"))
    subcategory = models.ForeignKey(JobSubCategory, related_name='jobs', on_delete=models.SET_NULL, null=True, verbose_name=_("Подкатегория"))
    education_levels = models.ManyToManyField(Education, related_name='required_jobs', blank=True, verbose_name=_("Образование (требуется)"))
    languages = models.ManyToManyField(Language, related_name='preferred_jobs', blank=True, verbose_name=_("Языки (предпочтительны)"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name=_("Статус"))
    moderation_comment = models.TextField(blank=True, null=True, verbose_name=_("Комментарий модератора"))
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("Количество просмотров"))
    country = models.CharField(max_length = 40,null=True, verbose_name=_("старана"))
    best_candidant = models.CharField(max_length = 400,null=True, verbose_name=_("Идеальный кандидат "))
    created_at = models.DateTimeField(auto_now_add=True, null = True,verbose_name=_("Дата создания"))
    work_type = models.ManyToManyField('WorkType', verbose_name=_("Тип занятости"))
    work_format = models.ManyToManyField('WorkFormat', verbose_name=_("Формат работы"))
    type = models.ManyToManyField('CompanyType', verbose_name=_("Тип компании"))

    def increment_view_count(self):

        self.view_count += 1
        self.save()
        from .tasks import send_notification_email
        if self.view_count % 5 == 0: 
            message = f"Ваша вакансия {self.title} была просмотрена {self.view_count} раз."
            send_notification_email.delay(self.employer.id, "Уведомление о просмотрах", message)
    def clean(self):
        if self.salary_max < self.salary_min:
            raise ValidationError({
                'salary_max': _('Максимальная зарплата не может быть меньше минимальной зарплаты.')
            })
    def __str__(self):
        return self.title


class FavoriteWorker(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_workers')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorited_by_employers')

    class Meta:
        unique_together = ('employer', 'worker')

    def __str__(self):
        return f"{self.employer.username} - {self.worker.username} (Избранный работник)"


class FavoriteJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class EmployerOffer(models.Model):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employer_offers')
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='worker_offers')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name=_("Вакансия"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    class Meta:
        unique_together = ('employer', 'worker', 'job')

    def __str__(self):
        return f"{self.employer.username} предлагает работу {self.job.title} {self.worker.username}"


class Skill(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Навык"))

    def __str__(self):
        return self.name


class SentResume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    resume = models.ForeignKey('Resume', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"Resume sent by {self.user.username} to job {self.job.title}"