# Generated by Django 3.0.3 on 2020-12-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_pp2m', '0006_city_pref_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='code_insee',
            field=models.CharField(default='', max_length=200),
        ),
    ]
