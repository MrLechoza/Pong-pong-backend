# Generated by Django 5.1.4 on 2025-01-12 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball_x', models.FloatField()),
                ('ball_y', models.FloatField()),
            ],
        ),
    ]
