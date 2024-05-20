"""
URL configuration for eatfood project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from restaurant import views as userviews
from user import views as hostviews
from adminapp import views as adminviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',userviews.home, name='home'),
    path('', userviews.start),
    path('userlogin',userviews.userlogin, name='userlogin'),
    path('userregister', userviews.userregister, name='userregister'),
    path('restaurant/<int:id>',userviews.restaurant,name='restaurant'),
    path('category/restaurant/<int:id>',userviews.restaurant,name='restaurant'),
    path('category/restaurant/addtoWishlist/<int:id>',userviews.addwishlist),
    path('category/<int:id>',userviews.category,name='category'),
    path('addCart',userviews.addcart,name='addtocart'),
    path('cart',userviews.cartpage,name='cart'),
    path('delcoupon',userviews.delcoupon,name='deletecoupon'),
    path('delcart/<int:id>',userviews.delcartitem),
    path('restaurant/addtoWishlist/<int:id>',userviews.addwishlist),
    path('wishlist',userviews.wishlist,name='wishlist'),
    path('delwishlistitem/<int:id>',userviews.delwishlistitem),
    path('load_content/<str:button_text>/', userviews.load_content, name='load_content'),
    path('change_password/', userviews.change_password, name='change_password'),
    path('add_address/', userviews.add_address, name='add_address'),
    path('delete_address/', userviews.delete_address, name='delete_address'),
    path('add_rating',userviews.myorders, name='add_rating'),
    path('logout/', userviews.logout,name='logout'),

    path('hostlogin',hostviews.restaurant_login, name='hostlogin'),
    path('hostpage/<str:button_text>/', hostviews.load_contend, name='hostprofile'),
    path('host_password/',hostviews.host_password, name='host_password'),
    path('host_home', hostviews.host_home,name='hosthome'),
    path('delete_item/<int:item_id>/',hostviews.delete_item, name='delete_item'),
    path('add_event/', hostviews.add_event, name='add_event'),
    path('add_coupon/', hostviews.add_coupon, name='add_coupon'),
    path('add-item/', hostviews.add_item, name='add_item'),
    path('hostlogout/', hostviews.hostlogout,name='hostlogout'),

    path('adminhome', adminviews.adminhome, name='admin'),
    path('activate_user/<int:user_id>/', adminviews.activate_user, name='activate_user'),
    path('activate_host/<int:host_id>/', adminviews.activate_host, name='activate_host'),
    path('managecategory', adminviews.managecategory,name='managecategory'),
    path('managecategory/delete/<int:category_id>/', adminviews.delete_category, name='delete_category'),
    path('category/update/<int:category_id>/', adminviews.update_category, name='update_category'),
    path('addcategory', adminviews.add_category,name='addcategory'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
