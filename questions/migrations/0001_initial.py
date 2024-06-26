# Generated by Django 4.2.5 on 2023-09-28 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'permissions': [('delete_own_answer', 'Can delete own answer'), ('change_own_answer', 'Can change own answer')],
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField()),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'permissions': [('delete_own_question', 'Can delete own question'), ('change_own_question', 'Can change own question')],
                'default_permissions': ['add', 'delete', 'view', 'change'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.SmallAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('up', 'Up'), ('down', 'Down')], max_length=4)),
                ('answer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.answer')),
                ('comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='questions.comment')),
            ],
        ),
    ]
