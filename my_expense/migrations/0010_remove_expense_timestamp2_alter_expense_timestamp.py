# Generated by Django 4.1.3 on 2023-01-11 09:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('my_expense', '0009_expense_timestamp2_alter_expense_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='timestamp2',
        ),
        migrations.AlterField(
            model_name='expense',
            name='timestamp',
            field=models.DateField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
