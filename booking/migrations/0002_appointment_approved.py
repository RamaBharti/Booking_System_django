# Generated by Django 4.1.7 on 2023-04-04 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
