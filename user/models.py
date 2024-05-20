from django.db import models
from restaurant.models import Itemmodel, Couponmodel
from django.db.models import Avg
from restaurant.models import *
# Create your models here.
class Usermodel(models.Model):
    User_id=models.AutoField(primary_key=True)
    User_name=models.CharField(max_length=200)
    User_password=models.CharField(max_length=200)
    User_mob=models.CharField(max_length=100)
    User_email=models.EmailField(null=True)
    User_create_at=models.DateTimeField(auto_now_add=True)
    User_status=models.CharField(max_length=200,default='Active')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.User_name


class Userimagemodel(models.Model):
    Image_id=models.IntegerField(primary_key=True)
    Image=models.ImageField(upload_to='images/userimg')
    User_id=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True)

    class Meta:
        db_table = 'user_image'

    def __str__(self):
        return self.User_id.User_name


class Addressmodel(models.Model):
    Address_id=models.AutoField(primary_key=True)
    User_id=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True)
    Location=models.CharField(max_length=200)
    District=models.CharField(max_length=200, null=True)
    State = models.CharField(max_length=200, null=True)
    Pincode=models.CharField(max_length=100)

    class Meta:
        db_table = 'user_address'

    def __str__(self):
        return self.User_id.User_name


class Cartmodel(models.Model):
    Cart_id = models.AutoField(primary_key=True)
    User_id = models.ForeignKey(Usermodel, on_delete=models.CASCADE, null=True)
    Item_id = models.ForeignKey(Itemmodel,on_delete=models.CASCADE,null=True)
    Quantity= models.IntegerField(null=True)
    Price= models.IntegerField(null=True)
    coupon = models.ForeignKey(Couponmodel, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'cart'

    def __str__(self):
        return self.Item_id.Item_name


class Wishlistmodel(models.Model):
    Wishlist_id = models.AutoField(primary_key=True)
    User = models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True)
    Item =models.ForeignKey(Itemmodel,on_delete=models.CASCADE,null=True)


    class Meta:
        db_table = 'Wishlist'

    def __str__(self):
        return self.Item.Item_name


class itemordermodel(models.Model):
    id=models.AutoField(primary_key=True)
    Orderid = models.CharField(max_length=200)
    User_id = models.ForeignKey(Usermodel, on_delete=models.CASCADE, null=True)
    Item = models.ForeignKey(Itemmodel, on_delete=models.CASCADE, null=True)
    Quantity = models.IntegerField()
    Address = models.ForeignKey(Addressmodel, on_delete=models.CASCADE)
    Status = models.CharField(max_length=200, default='Active')
    Order_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'itemorder'

    def __str__(self):
        return self.User_id.User_name


class Deliveryusermodel(models.Model):
    Delivery_id = models.IntegerField(primary_key=True)
    Order_id = models.ForeignKey(itemordermodel, on_delete=models.CASCADE, null=True)
    Address = models.ForeignKey(Addressmodel,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=200,default='Active')
    Deliver_time = models.DateTimeField()

    class Meta:
        db_table = 'delivery_detail'

    def __str__(self):
        return self.Item_id.Item_name


class Paymentmodel(models.Model):
    payment_id=models.IntegerField(primary_key=True)
    User_id=models.ForeignKey(Usermodel,on_delete=models.CASCADE,null=True)
    Order_id=models.ForeignKey(itemordermodel,on_delete=models.CASCADE,null=True)
    Amount=models.FloatField()
    Paymentmethod=models.CharField(max_length=200)
    Time=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return self.User_id.User_name


class Reviewmodel(models.Model):
    Review_id = models.AutoField(primary_key=True)
    User_id = models.ForeignKey(Usermodel, on_delete=models.CASCADE, null=True)
    Item = models.ForeignKey(Itemmodel, on_delete=models.CASCADE, null=True, related_name='reviews')
    rating=models.IntegerField(default=0)
    Date=models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        db_table = 'review'

    def __str__(self):
        return self.Review_id

