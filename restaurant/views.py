from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from .models import *
from user.models import Usermodel, Addressmodel, Wishlistmodel,Cartmodel,Reviewmodel,itemordermodel
from django.db.models import Q

# Create your views here.
def start(request):
    return render(request,'start.html')

def userlogin(request):
    if request.method=='POST':
        mobile_no=request.POST.get('contact')
        password=request.POST.get('password')
        user= Usermodel.objects.get(User_mob=mobile_no,User_password=password)
        if user:
            if user.User_status == 'Active':
                request.session['user']= user.User_name
                request.session['user_id']=user.User_id
                return redirect('/home')
            else:
                messages.warning(request,'Account is deactivated')
                return redirect('userlogin')
        else:
            messages.warning(request,'Credentials are incorrect')
            return redirect('userlogin')

    return render(request,'login.html')

def  userregister(request):
    if request.method=='POST':
        name=request.POST.get('username')
        contact=request.POST.get('contact')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        if Usermodel.objects.filter(User_mob=contact).exists():
            return render(request, 'register.html', {'error_message': '!Contact number already exists!','name':name,'contact':contact,'password1':password1,'password2':password2})
        user_obj=Usermodel()
        user_obj.User_name=name
        user_obj.User_mob=contact
        user_obj.User_password=password1
        user_obj.save()
        return redirect('/userlogin')
    return render(request,'register.html')

def home(request):
    if 'user' in request.session:
        category_data= Categorymodel.objects.all()
        rest_data=Restaurantmodel.objects.all()
        event_data=Eventmodel.objects.all()
        srch=''
        loc_srch=''
        if request.method=='POST':
            srch=request.POST.get('itemsrch')
            loc_srch=request.POST.get('locsrch')
            if srch or loc_srch:
                rest_data=rest_data.filter(Restaurant_name__icontains=srch)
                if loc_srch:
                    rest_data=rest_data.filter(Q(District__city_name__icontains=loc_srch)|Q(City__icontains=loc_srch))
        return render(request,'home.html',{'category': category_data,'restaurant':rest_data,'search':srch,'loc_srch':loc_srch,'event':event_data})
    else:
        return redirect('/userlogin')

def restaurant(request,id):
    if 'user' in request.session:
        user=request.session['user_id']
        rest_data=Restaurantmodel.objects.filter(Restaurant_id=id)
        item_data=Itemmodel.objects.filter(Host=id)
        menu_data=''
        for item in item_data:
            reviews = Reviewmodel.objects.filter(Item=item.Item_id)
            total_rating = sum(review.rating for review in reviews)
            review_count = reviews.count()
            if review_count > 0:
                item.avg_rating = total_rating / review_count
            else:
                item.avg_rating=0
            item.save()
        if request.method=='POST':
            menu_data=request.POST.get('menusrch')
            if menu_data:
                item_data=item_data.filter(Item_name__icontains=menu_data)

        return render(request,'restaarant.html', {'rest_data': rest_data, 'items': item_data, 'menu_srch': menu_data})
    else:
        return redirect('/userlogin')

def addcart(request):
    if 'user' in request.session:
        user=request.session['user_id']
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            item_qty = request.POST.get('qty')
            item_price=request.POST.get('itemprice')
            item = Itemmodel.objects.get(Item_id=item_id)
            restaurant_id = item.Host.Restaurant_id
            user_instance = Usermodel.objects.get(pk=user)
            item_instance = Itemmodel.objects.get(pk=item_id)
            if item_id and item_qty:
                item_exist=Cartmodel.objects.filter(User_id=user, Item_id=item_id)
                if item_exist:
                    messages.warning(request, 'ITEM ALREADY IN CART')
                else:
                    cart_obj = Cartmodel()
                    cart_obj.User_id = user_instance
                    cart_obj.Item_id = item_instance
                    cart_obj.Quantity = item_qty
                    cart_obj.Price=item_price
                    cart_obj.save()
                    messages.success(request, 'ITEM ADDED')
        return redirect(reverse('restaurant', args=[restaurant_id]))

def cartpage(request):
    if 'user' in request.session:
        userid=request.session['user_id']
        totalprice=0
        address_data=Addressmodel.objects.filter(User_id=userid)
        cart_data=Cartmodel.objects.filter(User_id=userid)
        cart_data_count=cart_data.count()
        for item in cart_data:
            totalprice+=item.Price

        if request.method=='POST':
            coupon=request.POST.get('coupon')
            coup=Couponmodel.objects.get(Coupon_code = coupon, is_expired=False)
            coupons=Couponmodel.objects.filter(Coupon_code = coupon, is_expired=False)
            if not coupons.exists():
                messages.warning(request,'Invalid Coupon')
            if totalprice >= coup.minimum_amnt:
                if Cartmodel.objects.filter(User_id=userid, coupon=coup.Coupon_id).exists():
                    messages.warning(request, 'Coupon already exists')
                else:
                    discount = coup.discount_price
                    totalprice -= discount
                    request.session['total_price'] = totalprice
                    request.session['applied_coupon']= coup.Coupon_code
                    request.session['coupontid']=coup.Coupon_id
                    cart_items = Cartmodel.objects.filter(User_id=userid)
                    for item in cart_items:
                        item.coupon =coup   # Associate coupon with the cart item
                        item.save()
                    messages.success(request, 'Coupon applied')
            else:
                messages.warning(request, f'Total price should be at least ₹{coup.minimum_amnt} to apply this coupon')
        return render(request,'cart.html',{'address':address_data,'cart':cart_data,'count':cart_data_count,'total_price_calculated':totalprice,'total_price_session':request.session.get('total_price'),'applied_coupon':request.session.get('applied_coupon')})
    else:
        return redirect('userlogin')

def delcoupon(request):
    cart_data=Cartmodel.objects.filter(coupon=request.session.get('coupontid'))
    for item in cart_data:
        item.coupon=None
        item.save()
    del request.session['total_price']
    del request.session['applied_coupon']
    del request.session['coupontid']
    messages.success(request, 'Coupon removed')
    return redirect('cart')

def delcartitem(request,id):
    cart_data= Cartmodel.objects.get(Item_id=id)
    cart_data.delete()
    return redirect('/cart')



def addwishlist(request,id):
    if 'user' in request.session:
        user=request.session['user_id']
        item=Itemmodel.objects.get(Item_id=id)
        restaurant_id = item.Host.Restaurant_id
        if not Wishlistmodel.objects.filter(Item=id, User=user).exists():
            wishlist_obj=Wishlistmodel()
            wishlist_obj.Item=Itemmodel.objects.get(Item_id=id)
            wishlist_obj.User=Usermodel.objects.get(User_id=user)
            wishlist_obj.save()
            item.is_in_wishlist=True
            item.save()

        return redirect(reverse('restaurant', args=[restaurant_id]))

def category(request,id):
    item=Itemmodel.objects.filter(Category=id)
    category=Categorymodel.objects.get(Category_id=id)
    name=category.Category
    return render(request,'category.html',{'item':item,'category_name':name})
def wishlist(request):
    if 'user' in request.session:
        user = request.session['user_id']
        wishlist_data=Wishlistmodel.objects.filter(User=user)
        wishlist_count = wishlist_data.count()
        return render(request,'wishlist.html',{'wishlist_data':wishlist_data,'wishlist_count':wishlist_count})
    else:
        return redirect('/userlogin')

def delwishlistitem(request,id):
    wishlist_data= Wishlistmodel.objects.get(Item=id)
    wishlist_data.delete()
    item_data=Itemmodel.objects.get(Item_id=id)
    item_data.is_in_wishlist=False
    item_data.save()
    return redirect('/wishlist')


def load_content(request, button_text):
    user_id = request.session.get('user_id')

    if user_id:
        user_details = Usermodel.objects.get(User_id=user_id)
        address_details = Addressmodel.objects.filter(User_id=user_id)
        orderdata = itemordermodel.objects.filter(User_id=user_id)

        context = {
            'button_text': button_text,
            'user_details': user_details,
            'address_details': address_details,
            'order_data': orderdata
        }
        return render(request, 'userprofile.html', context)
    else:
        messages.warning(request, 'You need to log in to access your profile.')
        return HttpResponseRedirect(reverse('login'))





def change_password(request):
    user_id = request.session.get('user_id')

    if user_id:
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            user = Usermodel.objects.get(User_id=user_id)
            if user.User_password == current_password:
                if new_password == confirm_new_password:
                    user.User_password = new_password
                    user.save()
                    request.session.flush()
                    return redirect('home')
                else:
                    return render(request, 'userprofile.html', {'error': "New passwords don't match."})
            else:
                return render(request, 'userprofile.html', {'error': 'Invalid current password.'})
        else:
            return render(request, 'userprofile.html')
    else:
        return redirect('userlogin')


def add_address(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if user_id:
            address = request.POST.get('Address')
            city = request.POST.get('district')
            state = request.POST.get('state')
            pincode = request.POST.get('pincode')
            new_address = Addressmodel.objects.create(User_id_id=user_id, Location=address,
                                                      District=city, State=state,  Pincode=pincode)

            if new_address:
                messages.success(request, 'Address added successfully.')
                return redirect(reverse('load_content',args=['Account Details']))
    messages.error(request, 'Failed to add address. Please try again.')
    return redirect('home')




def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address = Addressmodel.objects.get(Address_id=address_id)
        address.delete()

        return redirect(reverse('load_content', args=['Account Details']))

def myorders(request):
    userid= request.session.get('user_id')
    if request.method=='POST':
        rating=request.POST.get('rating')
        itemid=request.POST.get('itemid')
        item=Itemmodel.objects.get(Item_id=itemid)
        user=Usermodel.objects.get(User_id=userid)
        rateobj=Reviewmodel()
        rateobj.User_id=user
        rateobj.Item=item
        rateobj.rating=rating
        rateobj.save()
        messages.success(request, 'Thank you for the feedback')
        return redirect(reverse('load_content', args=['Account Details']))




def logout(request):

    if 'user_id' in request.session:
        del request.session['user_id']
        del request.session['user']
    return redirect('userlogin')


