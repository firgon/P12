# Generated by Django 4.1.4 on 2023-01-23 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0018_alter_contract_amount_alter_contract_payment_due_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='last_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Dernière mise à jour'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.IntegerField(choices=[(0, 'Created'), (1, 'Signed'), (2, 'Paid')], default=0, verbose_name='Status'),
        ),
    ]
