# Generated by Django 3.1.2 on 2021-02-01 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0002_schedule_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_name', models.CharField(max_length=50)),
                ('server_id', models.IntegerField()),
            ],
        ),
    ]