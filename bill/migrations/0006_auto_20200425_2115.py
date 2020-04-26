# Generated by Django 3.0.4 on 2020-04-26 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0005_auto_20200412_1103'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enumcategory',
            options={'ordering': ['category', 'name']},
        ),
        migrations.AlterField(
            model_name='recurringbill',
            name='note',
            field=models.CharField(blank=True, default='', max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='note',
            field=models.CharField(blank=True, default='', max_length=512, null=True),
        ),
    ]
