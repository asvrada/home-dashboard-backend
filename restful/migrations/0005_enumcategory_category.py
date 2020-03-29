# Generated by Django 3.0.4 on 2020-03-28 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0004_auto_20200327_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='enumcategory',
            name='category',
            field=models.CharField(choices=[('ICO', 'Icon'), ('CAT', 'Category'), ('COM', 'Company'), ('CAR', 'Card'), ('NUL', 'NULL')], default='NUL', max_length=3),
        ),
    ]