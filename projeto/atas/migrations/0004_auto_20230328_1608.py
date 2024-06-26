# Generated by Django 3.1.5 on 2023-03-28 19:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('atas', '0003_ata_curso'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ata',
            options={'ordering': ['-codigo', '-data', '-hora'], 'verbose_name': 'ata', 'verbose_name_plural': 'atas'},
        ),
        migrations.AlterField(
            model_name='ata',
            name='codigo',
            field=models.CharField(help_text='Fique atento ao último código de memória informado', max_length=20, unique=True, verbose_name='Código *'),
        ),
        migrations.AlterField(
            model_name='ata',
            name='data',
            field=models.DateField(help_text='Use: dd/mm/aaaa', max_length=11, verbose_name='Data *'),
        ),
        migrations.AlterField(
            model_name='ata',
            name='hora',
            field=models.CharField(help_text='Use: hh:mm', max_length=5, verbose_name='Hora *'),
        ),
        migrations.AlterField(
            model_name='ata',
            name='integrantes',
            field=models.ManyToManyField(blank=True, help_text='Para selecionar mais de um integrante, use a tecla CTRL ou CMD', null=True, related_name='integrantes', to=settings.AUTH_USER_MODEL, verbose_name='Integrantes'),
        ),
        migrations.AlterField(
            model_name='ata',
            name='local',
            field=models.CharField(max_length=50, verbose_name='Local *'),
        ),
        migrations.AlterField(
            model_name='ata',
            name='pauta',
            field=models.TextField(max_length=200, verbose_name='Pauta'),
        ),
        migrations.AlterField(
            model_name='ata',
            name='texto',
            field=models.TextField(blank=True, max_length=50000, null=True, verbose_name='Texto'),
        ),
    ]
