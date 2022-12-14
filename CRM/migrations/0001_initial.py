# Generated by Django 4.1.4 on 2023-01-03 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Création')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')),
                ('first_name', models.CharField(max_length=25, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=25, verbose_name='Nom')),
                ('email', models.CharField(max_length=100, verbose_name='Email')),
                ('phone', models.CharField(max_length=20, verbose_name='Téléphone')),
                ('mobile', models.CharField(max_length=20, verbose_name='Portable')),
                ('company', models.CharField(max_length=250, verbose_name='Société')),
                ('sales_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Création')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour')),
                ('status', models.IntegerField(choices=[(0, 'Created'), (1, 'Signed'), (2, 'Payed')], default=0, verbose_name='Statut')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Montant')),
                ('payment_due', models.DateTimeField(verbose_name='A régler le')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='CRM.client')),
                ('sales_contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'On Going'), (1, 'Canceled'), (2, 'Done')], verbose_name='Statut')),
                ('attendees', models.IntegerField(verbose_name='Nombre de participants')),
                ('date', models.DateTimeField(verbose_name='Date')),
                ('notes', models.TextField(verbose_name='Notes')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.contract')),
                ('support_contact', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
