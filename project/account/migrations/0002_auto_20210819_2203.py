# Generated by Django 3.2.6 on 2021-08-20 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='data_contratacao',
        ),
        migrations.RemoveField(
            model_name='user',
            name='demitido',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ultima_mudanca',
        ),
    ]