# Generated by Django 3.2.4 on 2021-06-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pred_app', '0004_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.FloatField(),
        ),
    ]