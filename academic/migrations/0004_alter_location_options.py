# Generated by Django 4.2.5 on 2023-10-02 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0003_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'default_permissions': ['add', 'delete', 'view', 'change']},
        ),
    ]
