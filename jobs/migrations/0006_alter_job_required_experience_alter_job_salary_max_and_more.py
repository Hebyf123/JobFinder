# Generated by Django 5.0.6 on 2024-09-13 22:32

import django.db.models.deletion
import jobs.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_remove_resume_programming_languages_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='required_experience',
            field=models.IntegerField(validators=[jobs.validators.validate_positive], verbose_name='Опыт работы (в годах)'),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary_max',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[jobs.validators.validate_positive], verbose_name='Максимальная зарплата'),
        ),
        migrations.AlterField(
            model_name='job',
            name='salary_min',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[jobs.validators.validate_positive], verbose_name='Минимальная зарплата'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='email',
            field=models.EmailField(max_length=254, validators=[jobs.validators.validate_email], verbose_name='Электронная почта'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='experience_years',
            field=models.IntegerField(validators=[jobs.validators.validate_positive], verbose_name='Опыт работы (в годах)'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='phone',
            field=models.CharField(max_length=20, validators=[jobs.validators.validate_phone], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='salary_range_max',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[jobs.validators.validate_positive], verbose_name='Максимальная зарплата'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='salary_range_min',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[jobs.validators.validate_positive], verbose_name='Минимальная зарплата'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteWorker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_workers', to=settings.AUTH_USER_MODEL)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by_employers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('employer', 'worker')},
            },
        ),
    ]