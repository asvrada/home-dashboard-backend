# Generated by Django 3.0.4 on 2020-04-11 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enumcategory',
            unique_together={('category', 'name')},
        ),
    ]
