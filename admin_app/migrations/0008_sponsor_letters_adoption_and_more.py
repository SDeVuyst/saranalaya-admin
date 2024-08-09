# Generated by Django 5.0.6 on 2024-08-09 14:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0007_alter_adoptionparent_options_alter_sponsor_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adoption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('adoptionparent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.adoptionparent')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.child')),
            ],
        ),
        migrations.RemoveField(
            model_name='adoptionparent',
            name='children',
        ),
        migrations.AddField(
            model_name='adoptionparent',
            name='children',
            field=models.ManyToManyField(blank=True, through='admin_app.Adoption', to='admin_app.child', verbose_name='Children'),
        ),
    ]
