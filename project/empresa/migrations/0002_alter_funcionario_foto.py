# Generated by Django 3.2.6 on 2021-08-21 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='foto',
            field=models.ImageField(default='imagens/default.jpg', upload_to='imagens/%Y/%m/%d/%M/%f', verbose_name='Foto de perfil'),
        ),
    ]
