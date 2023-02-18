# Generated by Django 4.1.5 on 2023-01-14 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('offer_price', models.FloatField()),
                ('description', models.TextField()),
                ('brand', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Watches for Men', 'Watches for Men'), ('Watches for Women', 'Watches for Women'), ('Watches for Kids', 'Watches for Kids')], max_length=200)),
                ('product_images', models.ImageField(upload_to='productimg')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=200)),
                ('pincode', models.IntegerField()),
                ('state', models.CharField(choices=[('Kerala', 'Kerala'), ('Pondicherry', 'Pondicherry'), ('Tamil Nadu', 'Tamil Nadu'), ('Karnataka', 'Karnataka'), ('Andhra Pradesh', 'Andhra Pradesh')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
