# Generated by Django 3.2.6 on 2021-08-27 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0027_alter_solicitacao_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacao',
            name='status',
            field=models.CharField(choices=[('respondido', 'RESPONDIDO'), ('em_andamento', 'EM ANDAMENTO'), ('interrompido', 'INTERROMPIDO'), ('finalizado', 'FINALIZADO')], max_length=15),
        ),
    ]