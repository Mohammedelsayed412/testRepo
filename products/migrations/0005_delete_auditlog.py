# Generated by Django 4.0.4 on 2022-04-30 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_auditlog_obj'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuditLog',
        ),
    ]