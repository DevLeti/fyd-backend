# Generated by Django 4.2.6 on 2023-10-31 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_server_server_detail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='server_detail',
            new_name='server_description',
        ),
    ]
