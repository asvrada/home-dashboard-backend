# Generated by Django 2.2.13 on 2020-07-03 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_user_has_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='has_password',
            field=models.BooleanField(default=True),
        ),
    ]
