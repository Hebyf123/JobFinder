# Generated by Django 5.1.1 on 2024-09-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_job_county_job_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='county',
        ),
        migrations.AddField(
            model_name='job',
            name='country',
            field=models.CharField(max_length=40, null=True, verbose_name='старана'),
        ),
        migrations.AddField(
            model_name='job',
            name='name_company',
            field=models.CharField(max_length=255, null=True, verbose_name='Название компании'),
        ),
        migrations.AlterField(
            model_name='job',
            name='position',
            field=models.CharField(max_length=40, null=True, verbose_name='название роли '),
        ),
    ]