# Generated by Django 3.2.4 on 2021-06-18 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pred_app', '0007_auto_20210613_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('symbol', models.CharField(max_length=150)),
            ],
        ),
    ]