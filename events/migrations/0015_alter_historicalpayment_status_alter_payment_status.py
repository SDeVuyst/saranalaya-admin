# Generated by Django 5.0.6 on 2024-07-24 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_alter_historicalpayment_status_alter_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpayment',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('open', 'Open'), ('canceled', 'Canceled'), ('expired', 'Expired'), ('failed', 'Failed')], default='open', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('paid', 'Paid'), ('open', 'Open'), ('canceled', 'Canceled'), ('expired', 'Expired'), ('failed', 'Failed')], default='open', max_length=10),
        ),
    ]
