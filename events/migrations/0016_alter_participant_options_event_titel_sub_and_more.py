# Generated by Django 5.0.6 on 2024-07-25 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_alter_historicalpayment_status_alter_payment_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'get_latest_by': 'pk'},
        ),
        migrations.AddField(
            model_name='event',
            name='titel_sub',
            field=models.CharField(default='a', max_length=100, verbose_name='Titel Subscript'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalevent',
            name='titel_sub',
            field=models.CharField(default='a', max_length=100, verbose_name='Titel Subscript'),
            preserve_default=False,
        ),
    ]
