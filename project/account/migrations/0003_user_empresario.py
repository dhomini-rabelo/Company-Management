# Generated by Django 3.2.6 on 2021-08-20 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20210819_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='empresario',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
