# Generated by Django 3.0.4 on 2020-04-04 20:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0012_auto_20200404_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill_instance', to='restful.RecurringBill'),
        ),
        migrations.AlterField(
            model_name='recurringbill',
            name='card',
            field=models.ForeignKey(blank=True, limit_choices_to={'category': 'CAR'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recur_card', to='restful.EnumCategory'),
        ),
        migrations.AlterField(
            model_name='recurringbill',
            name='category',
            field=models.ForeignKey(blank=True, limit_choices_to={'category': 'CAT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recur_category', to='restful.EnumCategory'),
        ),
        migrations.AlterField(
            model_name='recurringbill',
            name='company',
            field=models.ForeignKey(blank=True, limit_choices_to={'category': 'COM'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recur_company', to='restful.EnumCategory'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='card',
            field=models.ForeignKey(blank=True, limit_choices_to={'category': 'CAR'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill_card', to='restful.EnumCategory'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(blank=True, limit_choices_to={'category': 'CAT'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill_category', to='restful.EnumCategory'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='company',
            field=models.ForeignKey(blank=True, limit_choices_to={'category': 'COM'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bill_company', to='restful.EnumCategory'),
        ),
    ]
