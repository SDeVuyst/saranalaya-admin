# Generated by Django 5.0.6 on 2024-07-08 13:07

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0002_auto_20240629_2044'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAdoptionParent',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('firm', models.CharField(blank=True, max_length=45, null=True, verbose_name='Firm')),
                ('street_name', models.CharField(max_length=100, verbose_name='Street Name')),
                ('address_number', models.IntegerField(verbose_name='Address Number')),
                ('bus', models.CharField(blank=True, max_length=15, null=True, verbose_name='Bus')),
                ('postcode', models.CharField(max_length=15, verbose_name='Postcode')),
                ('city', models.CharField(max_length=40, verbose_name='City')),
                ('country', models.CharField(default='Belgium', max_length=40, verbose_name='Country')),
                ('mail', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Phone Number')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Adoption Parent',
                'verbose_name_plural': 'historical Adoption Parents',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAdoptionParentSponsoring',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('child', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='admin_app.child', verbose_name='Child')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='admin_app.adoptionparent', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'historical Adoption Parent Payment',
                'verbose_name_plural': 'historical Adoption Parent Payments',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalChild',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='name')),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=1, verbose_name='gender')),
                ('day_of_birth', models.DateField(verbose_name='Day of Birth')),
                ('date_of_admission', models.DateField(verbose_name='Date of Admission')),
                ('date_of_leave', models.DateField(blank=True, null=True, verbose_name='Date of Leave')),
                ('indian_parent_status', models.CharField(choices=[('n', 'No Parents'), ('o', 'One Parent'), ('t', 'Two Parents')], max_length=1, verbose_name='Indian Parent Status')),
                ('status', models.CharField(choices=[('a', 'Active'), ('l', 'Left'), ('s', 'Support')], max_length=1, verbose_name='Status')),
                ('link_website', models.URLField(blank=True, null=True, verbose_name='Link website')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Child',
                'verbose_name_plural': 'historical Children',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalDonation',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('sponsor', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='admin_app.sponsor', verbose_name='Sponsor')),
            ],
            options={
                'verbose_name': 'historical Donation',
                'verbose_name_plural': 'historical Donations',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSponsor',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('firm', models.CharField(blank=True, max_length=45, null=True, verbose_name='Firm')),
                ('street_name', models.CharField(max_length=100, verbose_name='Street Name')),
                ('address_number', models.IntegerField(verbose_name='Address Number')),
                ('bus', models.CharField(blank=True, max_length=15, null=True, verbose_name='Bus')),
                ('postcode', models.CharField(max_length=15, verbose_name='Postcode')),
                ('city', models.CharField(max_length=40, verbose_name='City')),
                ('country', models.CharField(default='Belgium', max_length=40, verbose_name='Country')),
                ('mail', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('phone_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='Phone Number')),
                ('letters', models.BooleanField(default=True, verbose_name='Letters')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Sponsor',
                'verbose_name_plural': 'historical Sponsors',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
