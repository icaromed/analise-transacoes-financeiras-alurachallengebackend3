# Generated by Django 4.0.4 on 2022-04-27 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transacoes', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Controller',
            new_name='Transacao',
        ),
    ]
