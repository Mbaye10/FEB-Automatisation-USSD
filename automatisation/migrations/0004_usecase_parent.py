# Generated by Django 5.1.4 on 2025-02-06 13:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automatisation', '0003_usecase_numerousecase'),
    ]

    operations = [
        migrations.AddField(
            model_name='usecase',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='automatisation.usecase'),
        ),
    ]
