# Generated by Django 3.0.4 on 2020-05-01 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0006_auto_20200425_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringbill',
            name='skip_summary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='skip_summary',
            field=models.BooleanField(default=False),
        ),
    ]