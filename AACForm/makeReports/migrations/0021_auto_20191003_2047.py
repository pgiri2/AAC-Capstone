# Generated by Django 2.2.5 on 2019-10-04 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makeReports', '0020_auto_20191003_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='college',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='degreeprogram',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='department',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
