# Generated by Django 4.1.4 on 2023-01-12 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0011_customer_client_contact'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='client',
            name='contact',
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.CheckConstraint(check=models.Q(('email__isnull', False), ('phone__isnull', False), ('mobile__isnull', False), _connector='OR'), name='contact', violation_error_message='You must add a phone, a mobile or a mail.'),
        ),
    ]
