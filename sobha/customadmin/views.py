from django.shortcuts import render, redirect,HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate
from django.views import View
from .models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pyotp
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from .forms import CustomerProfileForm
from django.http import JsonResponse
from myadmin.models import ProductMultipleImages,Brand,Coupon


# User sign up
@never_cache
def user_register(request):
    if 'username' in request.session:
        return redirect('user_homepage')

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_first_name = request.POST.get('first_name')
        new_last_name = request.POST.get('last_name')
        new_email = request.POST.get('email')
        new_password1 = request.POST.get('password1')
        new_password2 = request.POST.get('password2')
        if new_password1 == new_password2:
            if User.objects.filter(username=new_username).exists():
                print(1)
                message = 'username already exist'
                return render(request, 'user_register.html',{'message':message})

            elif User.objects.filter(email=new_email).exists():
                print(2)
                message = 'email already exist'
                return render(request, 'user_register.html',{'message':message})
            else:
                print(3)
                user = User.objects.create_user(
                    username=new_username, first_name=new_first_name, last_name=new_last_name, email=new_email, password=new_password1,is_active=False)
                user.save()
                secret=pyotp.random_base32()
                totp=pyotp.TOTP(secret,interval=300)
                otp=totp.now()
                send_mail('Sobha','Your OTP code is '+str(otp)+' .Please use this OTP to verify your account','fahadmanoly@gmail.com',[user.email],fail_silently=False)
                print(otp)
                response=redirect(f'otpverification/{user.id}/{secret}')
                response.set_cookie("can_otp_enter",True,max_age=300)
                messages.success(request,'Otp send to yout E-mail address')
                return response
                # return redirect('login')
        else:
            print("password doesn't match")
            return render(request, 'user_register.html')
    else:
        return render(request, 'user_register.html')


# OTP
def otpverification(request, userid, secret):
    if request.POST:
        totp = pyotp.TOTP(secret, interval=300)
        print(totp.now())
        try:
            user = User.objects.get(id=userid)
        except User.DoesNotExist:
            messages.error(request, 'user not found')
            return redirect('user_register')
        code = request.POST['1']+request.POST['2']+request.POST['3'] + \
            request.POST['4']+request.POST['5']+request.POST['6']
        if request.COOKIES.get('can_otp_enter') != None:
            if (totp.verify(code)):
                if (user.is_active != True):
                    user.is_active = True
                    user.save()
                    response = redirect('login')
                    response.set_cookie('verified', True)
                    messages.success(request, 'Otp verified you can login now')
                    return response
                                    
            else:
                 return render(request, 'otpverification.html',{'error': 'Invalid OTP'})
            # else:
            # 	pass
        else:
            return render(request, 'otpverification.html',{'error': 'Invalid or expired OTP'})
    else:
        return render(request, 'otpverification.html')

# customer profile view
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm()
        return render(request, 'profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

    def post(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            first_name  = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            email  = form.cleaned_data['email']
            phone_number  = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            district = form.cleaned_data['district']
            pincode = form.cleaned_data['pincode']
            state = form.cleaned_data['state']
            reg = Customer(user_name=usr, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, address=address, city=city, district=district, pincode=pincode, state=state)
            reg.save()
            messages.success(request, 'Congratulations!! Profile Updated Successfully.')
        return render(request, 'address.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})


# User Homepage
@never_cache
def user_homepage(request):
    if 'username' in request.session:
        watches_for_men = Product.objects.filter(category='Watches for Men')
        watches_for_women = Product.objects.filter(category='Watches for Women')
        watches_for_unisex = Product.objects.filter(category='Watches for Unisex')
        return render(request, 'ghome.html', {'watches_for_men':watches_for_men, 'watches_for_women':watches_for_women, 'watches_for_unisex':watches_for_unisex })
    else:
        return redirect('login')
         


# Landing page
class Productview(View):
    def get(self, request):
        watches_for_men = Product.objects.filter(category='Watches for Men')
        watches_for_women = Product.objects.filter(category='Watches for Women')
        watches_for_unisex = Product.objects.filter(category='Watches for Unisex')
        brand = Brand.objects.all()
        product = Product.objects.all()
        for p in product:
            for b in brand:
                if b.offer_active:
                    p.price = p.offer_price - b.discount
                    p.save()
        return render(request, 'ghome.html', {'watches_for_men':watches_for_men, 'watches_for_women':watches_for_women, 'watches_for_unisex':watches_for_unisex })



class Brandview(View):
    def get(self, request,name):
            prod = Product.objects.filter(brand__brand_name=name)
            bran = Brand.objects.filter(brand_name=name)
            for pr in prod:
                brand_title=pr.brand.brand_name
                for br in bran:
                    act = br.offer_active
                    if act == False:
                        pass
                    else:
                        pr.price = pr.offer_price-br.discount


            return render(request, 'brands.html', {'product':prod,'brand':bran,'act':act,'brand_title':brand_title})
            
    

# product single view on click
# class ProductDetailView(View):
def get(request, pk, bname):
    product = Product.objects.get(id=pk)
    prod=Product.objects.filter(id=pk)
    brand = Brand.objects.filter(brand_name=bname)
    for pr in prod:
        discounted_price = pr.price
        for br in brand:
            if br.offer_active == True:
                discounted_price = pr.offer_price-br.discount
            else:
                discounted_price = pr.offer_price
    product_gallery = ProductMultipleImages.objects.filter(product_id=product)
    return render(request, 'product_detail.html', {'product':product, 'product_gallery':product_gallery, 'discounted_price':discounted_price})

# product adding to cart
@login_required
def add_to_cart(request):
    user = request.user
    item_already_in_cart1 = False
    product = request.GET.get('prod_id')
    bran = request.GET.get('bran_id')
    brand=Brand.objects.filter(brand_name=bran)
    item_already_in_cart1 = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
    if item_already_in_cart1 ==False:
        product_title = Product.objects.get(id=product)
        Cart(user=user,product=product_title).save()
        messages.success(request,'Product added to cart')
        return redirect('/cart')
    else:
        return redirect('/cart')

# showing cart items in users
@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        vat = 0.0
        totalamount = 0.0
        # sub = Cart.objects.get()
        # print(sub)
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            
            for p in cart_product:
                bran=p.product.brand.brand_name
                brand=Brand.objects.filter(brand_name=bran)
                for br in brand:
                    if br.offer_active:
                        # discounted_price=p.product.price
                        tempamount = (p.quantity * p.product.price)
                        amnt=tempamount
                        amount += tempamount
                        vat = ((amount*5)/100)
                        totalamount = amount + vat
                        # return render(request, 'addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem, 'amnt':amnt,'act':act, 'discounted_price':discounted_price})
                    else:
                        # discounted_price = p.product.offer_price
                        tempamount = (p.quantity * p.product.offer_price)
                        amnt=tempamount
                        amount += tempamount
                        vat = ((amount*5)/100)
                        totalamount = amount + vat
                        # return render(request, 'addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem, 'amnt':amnt,'act':act, 'discounted_price':discounted_price})
                
                
            return render(request, 'addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem})
        else:
            return render(request, 'emptycart.html', {'totalitem':totalitem})
    else:
        return render(request, 'app/emptycart.html', {'totalitem':totalitem})



# Increasing the quantity of the item in the cart
@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        stock=c.product.stock
        if c.quantity<stock:
            if stock-c.quantity >10:
                c.quantity+=1
                message = ''
            else:
                c.quantity+=1
                message = 'Limited Stock'
            
        else:
            message = 'Item out of stock'
        c.save()
              
        amount = 0.0
        vat = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.offer_price)
            amount += tempamount
            vat = ((amount * 5)/100)
        
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+vat,
            'message':message
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")



# Decreasing the quantity of the item in the cart
@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        stock = c.product.stock
        if c.quantity>=2:
            c.quantity-=1
            if stock-c.quantity <= 10:
                message = 'Limited Stock'
            else:
                message =''
                pass
            
                 
        else:
            c.quantity = c.quantity
            message = 'Minimum quantity should be 1'
        c.save()
        
        amount = 0.0
        vat = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.offer_price)
            amount += tempamount
            vat = ((amount * 5)/100)
            # print(amount)
            # print(vat)
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+vat,
            'message':message
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")



# Removing items from cart
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        vat = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.offer_price)
            # print("Quantity", p.quantity)
            # print("Selling Price", p.product.discounted_price)
            # print("Before", amount)
            amount += tempamount
            vat = (amount * 5)/100
            
            # print("After", amount)
        # print("Total", amount)
        data = {
            'amount':amount,
            'totalamount':amount+vat,
        }
        return JsonResponse(data)
    else:
        return HttpResponse("")


# checkout
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user_name=user)
    cart_items = Cart.objects.filter(user=request.user)
    brand = Brand.objects.all()
    amount = 0.0
    vat = 0.0
    totalamount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.offer_price)
            amount += tempamount
            vat = ((amount*5)/100)
        totalamount = amount+vat
        couponbefore = totalamount
    if request.POST:
        cid = request.POST['add_coupon']
        coupon=Coupon.objects.filter(code=cid).first()
        if coupon is not None:
            discount=coupon.discount_price
            totalamount -=discount
            return render(request, 'checkout.html', {'add':add, 'cart_items':cart_items,'amount':amount, 'totalcost':totalamount})
        

    return render(request, 'checkout.html', {'add':add, 'cart_items':cart_items,'amount':amount, 'totalcost':totalamount})



# from cart to order
@login_required
def payment_done(request):
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		Orders(user=user, customer=customer, product=cid.product, quantity=cid.quantity).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
	return redirect("orders")



# Order page
@login_required
def orders(request):
	op = Orders.objects.filter(user=request.user)
	return render(request, 'orders.html', {'order_placed':op})

@login_required
def cancel_order(request, id):
    if request.user.is_authenticated:
        order = Orders.objects.get(id=id)
        print('order is is ',order)
        # for ord in order:
        if order.order_status =='Accepted':
            order.order_status = 'Cancelled by Customer'
            order.save()

        elif order.order_status =='Delivered':
            order.order_status = 'Product Return'
            order.save()
                   
        else:
            # message = "You can not cancel the order which is shipped or Delivered"
            pass

        return redirect('orders')
    return redirect('login')
        




# user delivery address
@login_required
def address(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	add = Customer.objects.filter(user_name=request.user)
	return render(request, 'address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

# deleting address
@login_required
def delete_address(request,id):
        add = Customer.objects.filter(id=id).all()
        add.delete()
        return redirect('address')







# Brands
# class Brandview(View):
#     def get(self, request):
#         omega = Product.objects.filter(brand='Omega')
#         rolex = Product.objects.filter(brand='Rolex')
#         rado = Product.objects.filter(brand='Rado')
#         tissot = Product.objects.filter(brand='Tissot')
#         arnold_son = Product.objects.filter(brand='Arnold Son')
#         girard_perre = Product.objects.filter(brand='Girard Perre')
#         bvlgari = Product.objects.filter(brand='Bvlgari')
#         calvin_klein = Product.objects.filter(brand='Calvin Klein')
#         corum = Product.objects.filter(brand='Corum')
#         return render(request, 'brand.html', {'omega':omega, 'rolex':rolex, 'rado':rado, 'tissot':tissot, 'arnold_son':arnold_son, 'girard_perre':girard_perre, 'bvlgari':bvlgari, 'calvin_klein':calvin_klein, 'corum':corum})




 























    





    



    

    
