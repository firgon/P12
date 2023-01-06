# Generated by Django 4.1.4 on 2023-01-04 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('CRM', '0005_alter_event_attendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='company',
            field=models.CharField(max_length=250, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(max_length=25, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(max_length=25, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Mobile'),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='payment_due',
            field=models.DateTimeField(verbose_name='Due on'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.IntegerField(choices=[(0, 'Created'), (1, 'Signed'), (2, 'Payed')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='event',
            name='assignee',
            field=models.ForeignKey(blank=True, limit_choices_to={'team': 2}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Expected attendees'),
        ),
        migrations.AlterField(
            model_name='event',
            name='contract',
            field=models.ForeignKey(limit_choices_to={'status': 1}, on_delete=django.db.models.deletion.CASCADE, to='CRM.contract'),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.IntegerField(choices=[(0, 'On Going'), (1, 'Canceled'), (2, 'Done')], default=0, verbose_name='Statut'),
        ),
    ]
