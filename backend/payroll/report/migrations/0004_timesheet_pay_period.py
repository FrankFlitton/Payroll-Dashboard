# Generated by Django 2.1.1 on 2018-09-28 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0003_auto_20180927_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='pay_period',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
