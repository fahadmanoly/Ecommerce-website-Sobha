from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import Loginform,MyPasswordChangeForm





urlpatterns = [
    path('', views.Productview.as_view(), name="landing_page"),
    path('brandview/<str:name>', views.Brandview.as_view(), name="brandview"),
    
    path('otpverification/<int:userid>/<str:secret>',views.otpverification,name='otpverification'),
    path('product_detail/<int:pk><str:bname>/', views.get, name='product_detail'),
    # path('product_detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    path("cart/",views.show_cart,name="showcart"),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('orders/', views.orders, name='orders'),
    path('address/', views.address, name='address'),
    path('address/delete_address!<int:id>', views.delete_address, name='delete_address'), 
    path('orders/cancel_order!<id>',views.cancel_order,name='cancel_order'),

    

    path("user_register",views.user_register,name="user_register"),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=Loginform), name='login'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path("user_homepage",views.user_homepage,name="user_homepage"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
