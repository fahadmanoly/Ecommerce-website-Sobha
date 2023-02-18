from django.contrib import admin
from .models import Customer
# from .models import Product
from .models import Cart
from .models import Orders
from myadmin.models import Brand,Product


# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_name', 'first_name', 'last_name', 'email','phone_number', 'address', 'city', 'district', 'pincode', 'state']
    list_display_links = ['id', 'user_name']
    readonly_fields = ['id']


@admin.register(Product)
class ProductsModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'offer_price','description', 'brand', 'category', 'product_image']
    list_display_links = ['id', 'title']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_display_links = ['id', 'user']
    readonly_fields = ['id', 'user', 'product', 'quantity']



@admin.register(Orders)
class OrdersModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'order_date', 'order_status', 'payment_status']






admin.site.register(Brand)
