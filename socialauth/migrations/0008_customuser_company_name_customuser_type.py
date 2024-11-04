# Generated by Django 5.1.1 on 2024-10-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialauth', '0007_alter_customuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название компании'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='type',
            field=models.CharField(blank=True, choices=[('Sturtup', 'Стартап'), ('Product', 'Продукт'), ('Outsource', 'Аутсорс'), ('Outstaff', 'Аутстаф')], default='pending', max_length=20, null=True, verbose_name='тайпы работы'),
        ),
    ]
