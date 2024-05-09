# Generated by Django 5.0.4 on 2024-05-07 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='grade',
            field=models.CharField(choices=[('1', '大一'), ('2', '大二'), ('3', '大三'), ('4', '大四')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='grade',
            field=models.CharField(choices=[('1', '大一'), ('2', '大二'), ('3', '大三'), ('4', '大四')], max_length=1),
        ),
        migrations.AddField(
            model_name='course',
            name='college',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='school.college', verbose_name='所属学院'),
        ),
        migrations.AddField(
            model_name='student',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.college'),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]
