# Generated by Django 3.2.6 on 2021-08-26 16:26

from django.db import migrations, models
import empresa.models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0021_empresa_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='codigo',
            field=models.PositiveBigIntegerField(blank=True, default=empresa.models.get_codigo),
        ),
    ]