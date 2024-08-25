# Generated by Django 4.1.7 on 2024-08-25 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rakuraku_apps', '0003_alter_waterqualitymodel_al_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waterqualitymodel',
            name='room_temperature',
            field=models.IntegerField(null=True, verbose_name='室温'),
        ),
        migrations.AlterField(
            model_name='waterqualitymodel',
            name='water_temperature',
            field=models.IntegerField(null=True, verbose_name='水温'),
        ),
    ]
