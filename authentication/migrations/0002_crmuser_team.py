# Generated by Django 4.1.4 on 2023-01-03 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='crmuser',
            name='team',
            field=models.SmallIntegerField(choices=[(0, 'Management'), (1, 'Vente'), (2, 'Support')], null=True),
        ),
    ]