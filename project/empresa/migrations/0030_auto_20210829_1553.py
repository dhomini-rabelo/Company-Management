# Generated by Django 3.2.6 on 2021-08-29 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0029_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/%Y/%m/%d/%M/%f', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='resposta',
            field=models.CharField(choices=[('aceito', 'ACEITO'), ('recusado', 'RECUSADO'), ('nenhuma', 'NENHUMA')], default='nenhuma', max_length=15),
        ),
        migrations.AlterField(
            model_name='solicitacao',
            name='status',
            field=models.CharField(choices=[('respondido', 'RESPONDIDO'), ('em_andamento', 'EM ANDAMENTO'), ('interrompido', 'INTERROMPIDO'), ('finalizado', 'FINALIZADO')], default='em_andamento', max_length=15),
        ),
    ]