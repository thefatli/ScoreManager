# Generated by Django 5.0.4 on 2024-05-07 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='学号'),
        ),
    ]
