# Generated by Django 3.1.1 on 2020-10-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=2048)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
