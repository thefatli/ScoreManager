# Generated by Django 5.0.4 on 2024-05-07 06:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='学院名称')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='年级')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade', to='school.college', verbose_name='所属学院')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('point', models.FloatField(verbose_name='学分')),
                ('grade', models.ForeignKey(help_text='所属年级', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='school.grade', verbose_name='所属年级')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=500)),
                ('info', models.CharField(blank=True, max_length=200, null=True)),
                ('courses', models.ManyToManyField(blank=True, to='school.course')),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school.grade')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__name'],
            },
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=4, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(through='school.Enrollment', to='school.student', verbose_name='学生姓名'),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=500)),
                ('info', models.CharField(blank=True, max_length=200, null=True)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='teachers', to='school.college')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__name'],
            },
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher', verbose_name='教师姓名'),
        ),
    ]
