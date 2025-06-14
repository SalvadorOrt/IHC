# Generated by Django 5.2 on 2025-05-31 02:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miapp', '0004_alter_categoria_options_alter_producto_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrito',
            name='cantidad',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='cantidad',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)]),
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
