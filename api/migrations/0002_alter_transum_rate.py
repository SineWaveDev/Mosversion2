# Generated by Django 3.2.16 on 2022-11-11 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transum',
            name='rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=65),
        ),
    ]