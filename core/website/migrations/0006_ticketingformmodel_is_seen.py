# Generated by Django 4.2.11 on 2024-05-27 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_newslettermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketingformmodel',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
