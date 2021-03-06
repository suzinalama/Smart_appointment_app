# Generated by Django 2.1.7 on 2019-03-08 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_profile', '0001_initial'),
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('hospital_name', models.CharField(max_length=100)),
                ('no_of_beds', models.IntegerField()),
                ('latitude', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
    ]
