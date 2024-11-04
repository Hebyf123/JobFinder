# Generated by Django 5.1.1 on 2024-10-01 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialauth', '0008_customuser_company_name_customuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(blank=True, choices=[('Company', 'компания'), ('Agents', 'агенство')], default='pending', max_length=20, null=True, verbose_name='тайпы работы'),
        ),
    ]