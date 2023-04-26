# Generated by Django 4.1.3 on 2023-04-26 13:27

import cars.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0003_alter_trip_nb_km_end_alter_trip_nb_km_start'),
    ]

    operations = [
        migrations.CreateModel(
            name='Energy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_day', models.DateField()),
                ('type', models.CharField(choices=[('essence', "Fonctionne à l'essence"), ('diesel', 'Fonctionne au diesel'), ('électricité', 'Véhicule électrique'), ('gpl', 'Fonctionne au GPL')], default='essence', max_length=32)),
                ('picture', models.ImageField(blank=True, max_length=255, null=True, upload_to=cars.models.path_and_rename_bill)),
                ('slug', models.SlugField(default=None, max_length=255, null=True, unique=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='energy_bill', to='cars.car')),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_energy_bill', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
