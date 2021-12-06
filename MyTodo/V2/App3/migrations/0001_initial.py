# Generated by Django 3.2.8 on 2021-11-19 10:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('App2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='td',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.TextField()),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_pending', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo', to='App2.profile')),
            ],
            options={
                'ordering': ('-is_pending', 'date_created'),
            },
        ),
    ]