# Generated by Django 4.2.11 on 2024-06-16 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='payment_gateway',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='paymentmodel',
            name='recipt_code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
