# Generated by Django 4.1.3 on 2023-04-25 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
        ('members', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='car',
            field=models.ManyToManyField(blank=True, related_name='user_cars', to='cars.car'),
        ),
        migrations.CreateModel(
            name='PurchaseParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_paid', models.FloatField(max_length=100)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='purchase_participation', to='cars.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_participation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
