# Generated by Django 3.2.6 on 2021-08-22 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empresa', '0006_alter_funcionario_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='admin',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='profissao',
            field=models.CharField(default='desempregado', max_length=120),
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('gastos', models.DecimalField(blank=True, decimal_places=2, max_digits=12, verbose_name='Despesas Mensais')),
                ('data_de_criacao', models.DateField(blank=True, verbose_name='Data de criação')),
                ('fundador', models.CharField(blank=True, max_length=120)),
                ('funcionarios', models.ManyToManyField(blank=True, to='empresa.Funcionario', verbose_name='Funcionários')),
                ('presidente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]