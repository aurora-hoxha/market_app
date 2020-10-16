"""market_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from market.views import kategorite, dyqanet, produktet, cart_add, item_clear, item_increment, item_decrement, \
    cart_clear, cart_detail, porosit
from market.views import register, login_request, logout_request

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', dyqanet, name='dyqanet'),
    path('kategori/<int:dyqan_id>/', kategorite, name='kategori'),
    path('dyqan/<int:dyqan_id>/kategori/<int:kategori_id>/produkte/', produktet, name='produktet'),

    path("register/", register, name="register"),
    path("logout/", logout_request, name="logout"),
    path("login/", login_request, name="login"),

    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail, name='cart_detail'),

    path('bli/', porosit, name='porosit')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
