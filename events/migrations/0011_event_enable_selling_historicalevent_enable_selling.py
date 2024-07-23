# Generated by Django 5.0.6 on 2024-07-23 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_event_email_text_historicalevent_email_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='enable_selling',
            field=models.BooleanField(default=True, verbose_name='Enable Selling'),
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='enable_selling',
            field=models.BooleanField(default=True, verbose_name='Enable Selling'),
        ),
    ]