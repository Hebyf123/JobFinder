# Generated by Django 5.0.6 on 2024-09-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialauth', '0003_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='surname',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Фамилия'),
        ),
    ]
