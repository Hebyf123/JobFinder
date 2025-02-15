# Generated by Django 5.0.6 on 2024-09-13 09:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_employeroffer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='employer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Работодатель'),
        ),
        migrations.AddField(
            model_name='employeroffer',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employer_offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employeroffer',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.job', verbose_name='Вакансия'),
        ),
        migrations.AddField(
            model_name='employeroffer',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worker_offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='employeroffer',
            unique_together={('employer', 'worker', 'job')},
        ),
    ]
