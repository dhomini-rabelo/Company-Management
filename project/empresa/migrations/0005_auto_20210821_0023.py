# Generated by Django 3.2.6 on 2021-08-21 03:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0004_alter_funcionario_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='data_contratacao',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='data_registro',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Data de registro'),
            preserve_default=False,
        ),
    ]
