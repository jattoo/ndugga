# Generated by Django 3.2.4 on 2021-06-17 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='valit_to',
            new_name='valid_to',
        ),
    ]
