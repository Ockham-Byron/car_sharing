# Generated by Django 4.1.3 on 2023-04-27 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0007_repair'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurance',
            name='paid_by',
        ),
        migrations.CreateModel(
            name='InsuranceParticipation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_paid', models.FloatField(max_length=100)),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_participation', to='cars.insurance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_insurance_participation', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
