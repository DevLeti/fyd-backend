# Generated by Django 4.2.6 on 2023-10-31 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='server_detail',
            field=models.CharField(blank=True, max_length=4000, null=True),
        ),
    ]
