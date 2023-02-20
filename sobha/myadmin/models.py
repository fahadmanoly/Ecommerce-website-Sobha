from django.db import models
from django.urls import reverse

# Create your models here.


class Brand(models.Model):
    brand_name = models.CharField(max_length=50)
    offer_active = models.BooleanField(default=False)
    discount = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.id)
    def get_url(self):
            return reverse('products_by_category',args=[self.cat_slug])
         
   
CATEGORY_CHOICES = (
    ('Watches for Men','Watches for Men'),
    ('Watches for Women','Watches for Women'),
    ('Watches for Unisex','Watches for Unisex'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(null=True, blank=True)
    offer_price = models.FloatField(null=False)
    description = models.TextField(null=False)
    stock = models.PositiveBigIntegerField(default=0)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    
    
    

class ProductMultipleImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimg')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
    

class Coupon(models.Model):
    code = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    discount_price = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.id)



