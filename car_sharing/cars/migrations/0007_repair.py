# Generated by Django 4.1.3 on 2023-04-26 13:59

import cars.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0006_remove_energy_type_energy_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0, max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('paid_day', models.DateField()),
                ('type_repair', models.CharField(choices=[('entretien', 'entretien'), ('importante', 'réparation importante')], default='entretien', max_length=32)),
                ('picture', models.ImageField(blank=True, max_length=255, null=True, upload_to=cars.models.path_and_rename_bill)),
                ('slug', models.SlugField(default=None, max_length=255, null=True, unique=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_bill', to='cars.car')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_repair_bill', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
