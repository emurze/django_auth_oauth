# Generated by Django 4.2.3 on 2023-08-08 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_rename_verbose_action_verb'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='content_id',
            new_name='object_id',
        ),
    ]
