# Generated by Django 4.1.3 on 2023-05-16 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_purchaseparticipation_first_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='energy',
            name='type_energy',
            field=models.CharField(blank=True, choices=[('essence', 'essence'), ('diesel', 'diesel'), ('électricité', 'kwatt'), ('gpl', 'GPL')], default='essence', max_length=32, null=True),
        ),
    ]
