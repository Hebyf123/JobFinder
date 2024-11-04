from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_file_size(file):
    max_size_kb = 10 * 1024 * 1024  # 10 MB
    if file.size > max_size_kb:
        raise ValidationError(_(f"Размер файла не может превышать 10 MB. Ваш файл весит {file.size / (1024 * 1024):.2f} MB."))

def validate_positive(value):
    if value <= 0:
        raise ValidationError(_('Значение должно быть положительным.'))

def validate_positive_exp(value):
    if value < 0:
        raise ValidationError(_('Значение должно быть положительным.'))

def validate_email(value):
    if '@' not in value:
        raise ValidationError(_('Введите корректный адрес электронной почты.'))

def validate_phone(value):
    if len(value) < 10 or not value.isdigit():
        raise ValidationError(_('Введите корректный номер телефона.'))
