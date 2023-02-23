from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('',views.admin_login,name='admin_login'),
    path('admin_login',views.admin_login,name='admin_login'),
    path("admin_home",views.index,name='admin_home'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('show_users',views.show_users,name='show_users'),
    path('block_user!<id>',views.block_user,name='block_user'),
    path('search_user',views.search_user,name='search_user'),
    
    path('add_brand',views.add_brand,name='add_brand'),
    path('show_brand',views.show_brand,name='show_brand'),
    path('edit_brand!<id>',views.edit_brand,name='edit_brand'),
    path('delete_brand!<id>',views.delete_brand,name='delete_brand'),
    path('search_brand',views.search_brand,name='search_brand'),

    path('add_product',views.add_product,name='add_product'),
    path('show_product',views.show_product,name='show_product'),
    path('edit_product!<id>',views.edit_product,name='edit_product'),
    path('delete_product!<id>',views.delete_product,name='delete_product'),
    path('search_product',views.search_product,name='search_product'),

    path('show_orders',views.show_orders,name='show_orders'),
    path('search_orders',views.search_orders,name='search_orders'),
    path('edit_orders!<id>',views.edit_orders,name='edit_orders'),

    path('add_coupon',views.add_coupon,name='add_coupon'),
    path('show_coupon',views.show_coupon,name='show_coupon'),
    path('edit_coupon!<id>',views.edit_coupon,name='edit_coupon'),
    path('delete_coupon!<id>',views.delete_coupon,name='delete_coupon'),

    path('sales_report',views.sales_report,name='sales_report'),
    


    # path('search_user',views.searched_user,name='product_search_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
