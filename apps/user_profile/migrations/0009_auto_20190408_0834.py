# Generated by Django 2.1.7 on 2019-04-08 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_auto_20190329_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blood_groups',
            field=models.CharField(choices=[('A+', 'A+ve'), ('B+', 'B+ve'), ('A-', 'A-ve'), ('B-', 'B-ve'), ('AB+', 'AB+ve'), ('AB-', 'AB-ve'), ('O+', 'O+ve'), ('O+', 'O-ve')], max_length=2),
        ),
    ]
