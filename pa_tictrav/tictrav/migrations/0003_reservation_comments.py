# Generated by Django 4.0.4 on 2022-06-11 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictrav', '0002_accountcustom_phone_number_reservation_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='comments',
            field=models.TextField(null=True),
        ),
    ]