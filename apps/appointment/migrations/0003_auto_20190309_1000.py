# Generated by Django 2.1.7 on 2019-03-09 04:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_auto_20190308_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayschedule',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]