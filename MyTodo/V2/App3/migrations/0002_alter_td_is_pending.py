# Generated by Django 3.2.8 on 2021-12-01 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App3', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='td',
            name='is_pending',
            field=models.BooleanField(default=False),
        ),
    ]
