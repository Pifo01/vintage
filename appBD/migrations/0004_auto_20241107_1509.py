# Generated by Django 3.1 on 2024-11-07 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appBD', '0003_auto_20241107_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulos',
            name='talla',
            field=models.IntegerField(choices=[(0, 'S'), (1, 'M'), (2, 'L'), (3, 'XL')]),
        ),
    ]
