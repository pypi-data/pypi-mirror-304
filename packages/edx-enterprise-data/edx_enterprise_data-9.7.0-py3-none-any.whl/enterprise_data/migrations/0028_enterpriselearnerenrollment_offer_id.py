# Generated by Django 3.2.13 on 2022-06-15 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_data', '0027_enterpriselearnerenrollment_total_learning_time_seconds'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterpriselearnerenrollment',
            name='offer_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
