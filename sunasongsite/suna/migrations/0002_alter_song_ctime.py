# Generated by Django 4.2 on 2023-04-21 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suna', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='ctime',
            field=models.DateField(blank=True, null=True, verbose_name='최초 추가 일시'),
        ),
    ]
