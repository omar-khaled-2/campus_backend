# Generated by Django 4.2.5 on 2023-10-07 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_device_platform_device_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='platform',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
