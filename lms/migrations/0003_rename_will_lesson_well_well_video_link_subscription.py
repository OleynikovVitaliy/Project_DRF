# Generated by Django 5.0.4 on 2024-05-07 17:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_lesson_owner_well_owner'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='will',
            new_name='well',
        ),
        migrations.AddField(
            model_name='well',
            name='video_link',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ссылка на видео'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=False, verbose_name='Активна')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.well', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
    ]
