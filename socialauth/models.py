from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _
WORK_TYPES_CHOICES = [
    ('Company', _('компания')),
    ('Agents', _('агенство')),

]
class CustomUser(AbstractUser):
    USER_ROLES = (
        ('employee', _('Работник')),
        ('employer', _('Работодатель')),
        ('moderator', _('Модератор')),
    )
    email = models.EmailField(unique=True)  # Email для входа
    name = models.CharField(max_length=80, verbose_name=_("Имя"), blank=True, null=True)
    surname = models.CharField(max_length=80, verbose_name=_("Фамилия"), blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='employee')
    photo = models.ImageField(upload_to='user_photos/', blank=True, null=True, verbose_name=_("Фото"))
    telegram_id = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Telegram ID"))

    # Поля, которые будут использоваться только для "Работодателей"
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Название компании"))
    type = models.CharField(max_length=20, choices=WORK_TYPES_CHOICES, default='pending', verbose_name=_("тайпы работы"), blank=True, null=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  

    def save(self, *args, **kwargs):

        if not self.username:
            self.username = self.email
        elif not self.email:
            self.email = self.username
        
        if self.role != 'employer':
            self.company_name = None
            self.type = None
            
        super().save(*args, **kwargs)
