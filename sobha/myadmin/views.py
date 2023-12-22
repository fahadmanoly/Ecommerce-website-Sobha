from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .models import Product, Brand
from .forms import ProductForm,ProductImageForm,OrderForm
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.models import User
from customadmin.models import Customer,Orders
from .models import Brand,ProductMultipleImages,Coupon
from django.contrib import messages
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import TableStyle,Table
from reportlab.lib import colors
from datetime import datetime, time, timedelta

       


@never_cache
def admin_login(request):
    if 'username' in request.session:
        return redirect('admin_home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_obj = User.objects.filter(username=username)
        if not user_obj.exists():
            return render(request, 'admin_login.html')
        user_obj = authenticate(username=username, password=password)

        if user_obj and user_obj.is_superuser:
            request.session["username"] = username
            return redirect('admin_home')
        else:
            return render(request, 'admin_login.html')

    else:
        return render(request, 'admin_login.html')


@never_cache
def index(request):
    if 'username' in request.session:
        chart_data = Orders.objects.all()
        salespermonth = [0,0,0,0,0,0,0,0,0,0,0,0]
        for a in range(12):
            for b in chart_data:
                if b.order_date.month == a+1:
                    salespermonth[a]+=1
    

        category = Brand.objects.all()
        total_order = len(chart_data)
        total_purchase_amount = int()
        total_product_qty = int()
        for data in chart_data:
            # total_purchase_amount += data.order.order_total
            total_product_qty += data.quantity

        barlist =[]

        for x in category:
            n=0
            for y in chart_data:
                p = Product.objects.get(title = y.product.title)
                if x.brand_name == p.brand.brand_name:
                    n+=1
            barlist.append(n)

        content = {
            'total_order':total_order,
            'total_purchase_amount':total_purchase_amount,
            'total_product_qty':total_product_qty,
            'barlist':barlist,
            'category':category,
            'salespermonth':salespermonth
        } 
        return render(request,'admin_home.html',content)
   
    else:
        return redirect('admin_login')
    

@never_cache
def admin_logout(request):
    if 'username' in request.session:
        print(request.session['username'])
        del request.session['username']
    return redirect('admin_login')


@never_cache
def show_users(request):
    if 'username' in request.session:
        users = Customer.objects.all()
        return render(request, 'show_users.html', {"users": users,})
    else:
        return redirect('admin_login')
    

@never_cache
def block_user(request, id):
    if 'username' in request.session:
        user = User.objects.get(id=id)
        if user.is_active is True:
            user.is_active=False
            user.save()
        else:
            user.is_active=True
            user.save()
        return redirect('show_users')
    else:
        return redirect('admin_login')
    

def search_user(request):
    if request.method == 'POST':
            data = request.POST['searched_data']
            user_data = Customer.objects.filter(user_name__contains=data).all()
            if user_data:
                return render(request, 'search_user.html', {'user_data': user_data, 'data1': data})
            else:
                msg = "No such customer found"
                return render(request, 'search_user.html', {'m': msg})


def add_brand(request):
    if 'username' in request.session:
        if request.method=='POST':
            add_brand_title=request.POST.get("add_brand_title")
            add_discount=request.POST.get("add_discount")
            Brand.objects.create(brand_name=add_brand_title, discount=add_discount)
            return redirect('show_brand')
        else:
            return render(request,'add_brand.html')
    return redirect('admin_login')


def show_brand(request):
    if 'username' in request.session:
        brand = Brand.objects.all()
        return render(request, 'show_brand.html', { 'brand': brand})
    else:
        return redirect('admin_login')


@never_cache
def edit_brand(request, id):
    if 'username' in request.session:
        brand = Brand.objects.get(id=id)
        if request.method == "POST":
            brand_data = Brand.objects.filter(id=id).all()
            brand_name = request.POST['add_brand_title']
            offer_active = request.POST['offer_active']
            discount = request.POST['add_discount']
            for b in brand_data:
                b.brand_name= brand_name
                b.offer_active = offer_active
                b.discount = discount
                b.save()
            return redirect('show_brand')
        else:
            return render(request, 'edit_brand.html', {'brand': brand})
    else:
        return redirect('admin_login')


@never_cache
def delete_brand(request, id):
    if 'username' in request.session:
        brand = Brand.objects.filter(id=id).all()
        brand.delete()
        return redirect('show_brand')
    else:
        return redirect('admin_login')
    

def search_brand(request):
    if request.method == 'POST':
            data = request.POST['searched_data']
            brand_data = Brand.objects.filter(brand_name__contains=data).all()
            if brand_data:
                return render(request, 'search_brand.html', {'brand_data': brand_data, 'data1': data})
            else:
                msg = "No such brand found"
                return render(request, 'search_brand.html', {'m': msg})
    

def add_product(request):
    if 'username' in request.session:
        data=Brand.objects.all()
        product=ProductForm()
        multiple_image_form=ProductImageForm()
        if request.method=='POST':
            multiple_image_form= ProductImageForm(request.POST or None, request.FILES or None)
            images = request.FILES.getlist('image')
            add_product_title=request.POST.get("add_product_title")
            add_price=request.POST.get("add_price")
            add_offer_price=request.POST.get("add_offer_price")
            add_description=request.POST.get("add_description")
            add_stock=request.POST.get("add_stock")
            add_brand=request.POST.get('add_brand')
            add_category=request.POST.get("category")
            main_image=request.FILES.get("main_image")
            data = Brand.objects.get(id=add_brand)
            #add_image=request.FILES.get("add_image")
            
            productdata= Product.objects.create(title=add_product_title, price=add_price, offer_price=add_offer_price, description=add_description, stock=add_stock, brand=data, category=add_category, product_image=main_image)
            for image in images:
                ProductMultipleImages.objects.create(product=productdata, image=image)

            return redirect('show_product')
        else:
            return render(request,'add_product.html',{'data':data,'product':product, 'multiple_image':multiple_image_form})
    else:
        return render(request,'admin_login.html')


def show_product(request):
    if 'username' in request.session:
        products = Product.objects.all()
        return render(request, 'show_product.html', {'products':products})
    else:
        return redirect('admin_login')
    




def edit_product(request, id):
    if 'username' in request.session:
        data=Brand.objects.all()
        id =int(id)
        product = Product.objects.get(id=id)
        if request.method == "POST":
            prod=ProductForm(request.POST)
            print(request.POST)
            product.title = request.POST.get('title')
            product.price = request.POST.get('price')
            product.offer_price = request.POST.get('offer_price')
            product.description = request.POST.get('description')
            product.stock = request.POST.get('stock')
            brand = request.POST['data']
            product.category = request.POST['category']
            product.product_image = request.FILES['main_image']
            data = Brand.objects.get(id=brand)
            product.brand=data
            product.save()
            print("worked")
            if prod.is_valid():
                print("enter")
                prod.save()

                # prod_obj=prod.save() 
                # prod_obj.title=title
                # prod_obj.price=price
                # prod_obj.offer_price=offer_price
                # prod_obj.description=description
                # prod_obj.stock=stock
                # prod_obj.brand=data
                # prod_obj.category=category
                # prod_obj.product_image=main_image
            try:
                pass
                # prod_obj .save()
                # return redirect('show_product')
            #    Product.objects.filter(pk=id).update(title=title, price=price, offer_price=offer_price, description=description, stock=stock, brand=data,category=category, product_image=main_image)
            except:
                # Product.objects.filter(pk=id).update(title=title, price=price, offer_price=offer_price, description=description, stock=stock, brand=data,category=category, product_image=main_image)
                print("error")
                # prod_obj .save()
            return redirect('show_product')
        else:
            prod=ProductForm()
            return render(request, 'edit_product.html', {'data':data, 'prod':prod, 'product': product})
    else:
        return redirect('admin_login')
    

@never_cache
def delete_product(request, id):
    if 'username' in request.session:
        product = Product.objects.filter(id=id).all()
        product.delete()
        return redirect('show_product')
    else:
        return redirect('admin_login')
    


def search_product(request):
    if request.method == 'POST':
            data = request.POST['searched_data']
            product_data = Product.objects.filter(title__contains=data).all()
            if product_data:
                return render(request, 'search_product.html', {'product_data': product_data, 'data1': data})
            else:
                msg = "No such product found"
                return render(request, 'search_product.html', {'m': msg})
            


def show_orders(request):
    if 'username' in request.session:
        order = Orders.objects.all()
        return render(request, 'show_orders.html', { 'order': order})
    else:
        return redirect('admin_login')  


def search_orders(request):
    if request.method == 'POST':
            data = request.POST['searched_data']
            order_data = Orders.objects.filter(customer__contains=data).all()
            if order_data:
                return render(request, 'search_orders.html', {'order_data': order_data, 'data1': data})
            else:
                msg = "No such order found"
                return render(request, 'search_orders.html', {'m': msg})


@never_cache
def edit_orders(request, id):
    if 'username' in request.session:
        order = Orders.objects.get(id=id)
        ord=OrderForm()

        if request.method == "POST":
            order_data = Orders.objects.filter(id=id).all()
            order_status= request.POST.get('order_status')
            payment_status= request.POST.get('payment_status')
            payment_method= request.POST.get('payment_method')
            try:
               Orders.objects.filter(pk=id).update(order_status=order_status, payment_status=payment_status,payment_method=payment_method,)
            except:
                print("error")
                Orders.objects.filter(pk=id).update(order_status=order_status, payment_status=payment_status,payment_method=payment_method,)

            
            return redirect('show_orders')
        else:
            return render(request, 'edit_orders.html', {'order': order, 'ord':ord})
    else:
        return redirect('admin_login')   



def dashboard(request):
    
    chart_data = Orders.objects.all()
    salespermonth = [0,0,0,0,0,0,0,0,0,0,0,0]
    for a in range(12):
        for b in chart_data:
            if b.order_date.month == a+1:
                salespermonth[a]+=1
  

    category = Brand.objects.all()
    total_order = len(chart_data)
    total_product_qty = int()
    for data in chart_data:
        total_product_qty += data.quantity

    barlist =[]

    for x in category:
        n=0
        for y in chart_data:
            p = Product.objects.get(title = y.product.title)
            if x.brand_name == p.category.brand_name:
                n+=1
        barlist.append(n)


    content = {
        'total_order':total_order,
        'total_product_qty':total_product_qty,
        'barlist':barlist,
        'category':category,
        'salespermonth':salespermonth
    }

    return render(request,'admin_home.html',content)


def add_coupon(request):
    if 'username' in request.session:
        data=Coupon.objects.all()
        if request.method=='POST':
            add_code=request.POST.get("add_code")
            # add_is_active = request.POST.get("add_is_active")
            add_discount_price = request.POST.get("add_discount_price")
            Coupon.objects.create(code=add_code, discount_price=add_discount_price)
            return redirect('show_coupon')
        else:
            return render(request,'add_coupon.html',{'data':data})
    return redirect('admin_login')

def show_coupon(request):
    if 'username' in request.session:
        coupon = Coupon.objects.all()
        return render(request, 'show_coupon.html', { 'coupon': coupon})
    else:
        return redirect('admin_login')


    

@never_cache
def edit_coupon(request, id):
    if 'username' in request.session:
        coupon = Coupon.objects.get(id=id)
        if coupon.is_active is True:
            coupon.is_active=False
            coupon.save()
        else:
            coupon.is_active=True
            coupon.save()
        return redirect('show_coupon')
    else:
        return redirect('admin_login')


@never_cache
def delete_coupon(request, id):
    if 'username' in request.session:
        coupon = Coupon.objects.filter(id=id).all()
        coupon.delete()
        return redirect('show_coupon')
    else:
        return redirect('admin_login')
    


def sales_report(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 16)

    if request.method == 'POST':    
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        orders = Orders.objects.all()

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            orders = orders.order_by('-order_date').filter(order_date__range=[start_date, end_date])
        else:
            orders = Orders.objects.all().order_by('-order_date')

            
        #create table header
        table_header = ["Customer Name", "Product Title", "Quantity", "Order Date", "Order Status", "Payment Status"]
        
        #create table data
        table_data = []
        for ord in orders:
            row_data = [ord.customer.user_name.username, ord.product.title, str(ord.quantity), str(ord.order_date), str(ord.order_status), str(ord.payment_status)]
            table_data += [row_data]

        # Create the PDFTable object
        pdfTable = Table([table_header] +table_data)
        
        # Set style for the table header
        pdfTableStyle = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)]) 

        # Add style to the PDFTable object
        pdfTable.setStyle(pdfTableStyle)


        # Draw the PDFTable object on the canvas
        pdfTable.wrapOn(c, 100, 100)

        # Set position of the PDFTable object on the canvas
        pdfTable.drawOn(c, 10, 10 + 5)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename="Sales report.pdf")
    else:
        return render(request,'sales_report.html')

    # lines = []
    # for ord in orders:
    #     lines.append(ord.customer.user_name.username)
    #     lines.append(ord.product.title)
    #     lines.append(str(ord.quantity))
    #     lines.append(str(ord.order_date))
    #     lines.append(str(ord.order_status))
    #     lines.append(str(ord.payment_status))
    #     lines.append(str(ord.payment_method))
    # for line in lines:
    #     textob.textLine(line)
    # c.drawText(textob)
    # c.showPage()
    # c.save()
    # buf.seek(0)
    # return FileResponse(buf, as_attachment=True, filename="Sales report.pdf")












    














