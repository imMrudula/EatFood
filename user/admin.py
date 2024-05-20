from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Usermodel)
admin.site.register(Userimagemodel)
admin.site.register(Addressmodel)
admin.site.register(Cartmodel)
admin.site.register(itemordermodel)
admin.site.register(Deliveryusermodel)
admin.site.register(Paymentmodel)
admin.site.register(Reviewmodel)
admin.site.register(Wishlistmodel)