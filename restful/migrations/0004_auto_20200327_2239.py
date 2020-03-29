# Generated by Django 3.0.4 on 2020-03-28 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0003_auto_20200327_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='icon',
            field=models.ForeignKey(limit_choices_to={'category': 'icon'}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restful.EnumCategory'),
        ),
    ]