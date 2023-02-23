"""sobha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# from user import views




urlpatterns = [
    path('defaultadmin/', admin.site.urls),
    path('', include('customadmin.urls')),
    path('admin/', include('myadmin.urls')),
    # path('user_signup/',views.user_signup,name='user_signup'),
    # path('user_login/', views.user_login, name='user_login'),
    # path('user_home/', views.user_homepage,name='user_home'),
    # path('user_logout/',views.user_logout, name = 'user_logout'),   

]

