# Generated by Django 4.2.7 on 2023-11-16 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='images',
            new_name='image',
        ),
    ]
