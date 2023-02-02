# Generated by Django 4.1.3 on 2023-01-31 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_expense', '0013_alter_expense_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='telegram_chat_id',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
