# Generated by Django 4.1.5 on 2023-02-04 09:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_brand_product_delete_otp'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveBigIntegerField(default=1)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('Accepted', 'Accepted'), ('Shipped', 'Shipped'), ('On the Way', 'On the Way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50)),
                ('payment_status', models.CharField(choices=[('paid', 'paid'), ('Cash on Delivery', 'Cash On Delivery'), ('Pending', 'Pending')], default='Pending', max_length=50)),
                ('payment_method', models.CharField(choices=[('credit card', 'credit card'), ('Cash on Delivery', 'Cash On Delivery'), ('PayPal', 'PayPal'), ('Razorpay', 'Razorpay')], default='Select', max_length=50)),
                ('payment_id', models.CharField(default='Enter', max_length=300)),
            ],
        ),
        migrations.DeleteModel(
            name='Products',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='locality',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='user',
            new_name='user_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='name',
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='email', max_length=254),
        ),
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(default='user', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(default='user', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='customer',
            name='district',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='orders',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customadmin.customer'),
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myadmin.product'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]