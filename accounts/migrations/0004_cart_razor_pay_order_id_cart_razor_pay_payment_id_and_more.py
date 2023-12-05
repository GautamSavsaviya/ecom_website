# Generated by Django 4.2.4 on 2023-08-17 08:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_cart_coupon"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="razor_pay_order_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razor_pay_payment_id",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="cart",
            name="razor_pay_payment_signature",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
