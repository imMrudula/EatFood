from django.db import models
from user.models import *
from adminapp.models import *

# Create your models here.

class statemodel(models.Model):
    state_id=models.IntegerField(primary_key=True)
    state_name=models.CharField(max_length=50)

    class Meta:
        db_table = 'states'

    def __str__(self):
        return self.state_name

class Districtmodel(models.Model):
    city_id=models.IntegerField(primary_key=True)
    city_name=models.CharField(max_length=50)
    state_id=models.ForeignKey(statemodel,on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'city'

    def __str__(self):
        return self.city_name

class Restaurantmodel(models.Model):
    Restaurant_id=models.IntegerField(primary_key=True)
    Restaurant_name=models.CharField(max_length=200)
    Password=models.CharField(max_length=200)
    License=models.CharField(max_length=200)
    City=models.CharField(max_length=200, null=True)
    District=models.ForeignKey(Districtmodel, on_delete=models.CASCADE,null=True)
    Address=models.CharField(max_length=200)
    pincode = models.CharField(max_length=100)
    Discription=models.TextField()
    Phone_no=models.CharField(max_length=100)
    Email=models.CharField(max_length=200)
    Image=models.ImageField(upload_to='images/host/')
    Host_status=models.CharField(max_length=200,default='Active')

    class Meta:
        db_table='Restaurant'
    def __str__(self):
        return self.Restaurant_name

class Itemmodel(models.Model):
    Item_id=models.AutoField(primary_key=True)
    Item_name=models.CharField(max_length=200)
    Description=models.TextField()
    Price=models.FloatField()
    Quantity=models.CharField(max_length=200)
    Start_time=models.DateTimeField()
    End_time=models.DateTimeField()
    Image = models.ImageField(upload_to='images/item/')
    Category=models.ForeignKey(Categorymodel,on_delete=models.CASCADE,null=True)
    avg_rating = models.FloatField(default=0,null=True)
    Host=models.ForeignKey(Restaurantmodel,on_delete=models.CASCADE,null=True)
    is_in_wishlist=models.BooleanField(default=False,null=True)
    Status=models.CharField(max_length=200,default='Active')

    class Meta:
        db_table='Items'

    def __str__(self):
        return self.Item_name



class Couponmodel(models.Model):
    Coupon_id=models.AutoField(primary_key=True)
    Coupon_code=models.CharField(max_length=10)
    is_expired=models.BooleanField(default=False)
    discount_price=models.IntegerField()
    minimum_amnt=models.IntegerField()

    class Meta:
        db_table = 'Coupon'

    def __str__(self):
        return self.Coupon_code

class Eventmodel(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=250)
    description = models.TextField()
    start_date=models.DateTimeField(null=True)
    end_date=models.DateTimeField(null=True)
    image=models.ImageField(null=True)
    coupon= models.ForeignKey(Couponmodel,on_delete=models.CASCADE,null=True)
    status = models.CharField(max_length=50,default='Active')

    class Meta:
        db_table = 'Event'

    def __str__(self):
        return self.event_name






