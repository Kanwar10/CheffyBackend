# Generated by Django 3.2 on 2021-04-29 08:46

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_chlumodel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='chlumodel',
        ),
        migrations.AddField(
            model_name='partnerprofile',
            name='qualification_doc',
            field=models.FileField(blank=True, storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\hichugh\\helperasservice\\cheffy-app-server\\CheffyBackend\\media'), upload_to='qualification_doc'),
        ),
    ]
