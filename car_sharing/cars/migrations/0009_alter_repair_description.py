# Generated by Django 4.1.3 on 2023-05-02 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_remove_insurance_paid_by_insuranceparticipation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
