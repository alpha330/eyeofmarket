# Generated by Django 4.2.11 on 2024-06-17 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_paymentmodel_recipt_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodel',
            name='currency',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]