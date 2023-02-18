from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from myadmin.models import Product,Brand



# Create your models here.
STATE_CHOICES = (
    ('Kerala','Kerala'),
    ('Pondicherry','Pondicherry'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Karnataka','Karnataka'),
    ('Andhra Pradesh','Andhra Pradesh')
)

class Customer(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default='First Name')
    last_name = models.CharField(max_length=100, default='Last Name')
    email = models.EmailField(default='email')
    phone_number = PhoneNumberField(blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def price(self):
        if self.product.brand.offer_active:
            return self.quantity * self.product.price 
        else:
            return (self.quantity * self.product.offer_price)

    @property
    def vat(self):
        return (self.quantity * self.product.offer_price * 5)/100
    




ORDER_STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Shipped','Shipped'),
    ('Cancelled by Customer','Cancelled by Customer'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
    ('Product Return','Product Return'),
    ('Product Return Approved','Product Return Approved'),
)

PAYMENT_STATUS = (
    ('paid','paid'),
    ('Cash on Delivery','Cash On Delivery'),
    ('Pending','Pending'),
)

PAYMENT_METHOD = (
    ('credit card','credit card'),
    ('Cash on Delivery','Cash On Delivery'),
    ('PayPal','PayPal'),
)

class Orders(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=50,choices=ORDER_STATUS_CHOICES,default='Pending')
    payment_status = models.CharField(max_length=50,choices=PAYMENT_STATUS,default='Pending')
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD,default='Select')
    payment_id = models.CharField(max_length=300, default='Enter')


    @property
    def price(self):
        if self.product.brand.offer_active:
            return self.quantity * self.product.price 
        else:
            return self.quantity * self.product.offer_price 
    

def menu_links(request):
    brands=Brand.objects.all()
    return dict(brands=brands)



        


