# Generated by Django 3.0.3 on 2020-04-07 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_pp2m', '0004_auto_20200406_1200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journey',
            options={'verbose_name': 'trajet'},
        ),
        migrations.AddField(
            model_name='department',
            name='polygon',
            field=models.TextField(null=True),
        ),
    ]
