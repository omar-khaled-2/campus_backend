# Generated by Django 4.2.5 on 2023-09-28 14:30

import campus.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateField(auto_now=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='academic.course')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.folder')),
            ],
            options={
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', campus.models.AutoNameFileField(upload_to='files/')),
                ('created_at', models.DateField(auto_now=True)),
                ('size', models.PositiveIntegerField(editable=False)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.folder')),
            ],
            options={
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
    ]