# Generated by Django 3.2.20 on 2023-09-07 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_data', '0034_auto_20230907_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprisesubsidybudget',
            name='id',
            field=models.CharField(db_index=True, help_text='Hashed surrogate key based on subsidy_access_policy_uuid and subsidy_uuid', max_length=32, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='enterprisesubsidybudget',
            name='subsidy_access_policy_uuid',
            field=models.UUIDField(help_text='Budget Id'),
        ),
    ]
