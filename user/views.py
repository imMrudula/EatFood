from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from adminapp.models import Categorymodel
from .models import Restaurantmodel, Itemmodel, Eventmodel, Couponmodel


def restaurant_login(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')
        password = request.POST.get('password')

        user = Restaurantmodel.objects.filter(Phone_no=contact, Password=password).first()

        if user:
            if user.Host_status == 'Active':
                request.session['host_id'] = user.Restaurant_id
                request.session['host_name'] = user.Restaurant_name
                return redirect('hosthome')
            else:
                messages.error(request,'Account is deactivated')
                return render(request, 'hostlogin.html')
        else:
            messages.error(request,'Invalid phone number or password')
            return render(request, 'hostlogin.html')
    else:
        return render(request, 'hostlogin.html')


def load_contend(request, button_text):
    user_id = request.session.get('host_id')
    coupons=Couponmodel.objects.all()

    if user_id:
        try:
            host_details = Restaurantmodel.objects.get(Restaurant_id=user_id)

            context = {
                'button_text': button_text,
                'host_details': host_details,
                'coupons':coupons,

            }
            return render(request, 'hostprofile.html', context)
        except Restaurantmodel.DoesNotExist:
            messages.error(request, 'Restaurant not found.')
    else:
        messages.warning(request, 'You need to log in to access your profile.')

    return HttpResponseRedirect(reverse('hostlogin'))


def host_password(request):
    host_id = request.session.get('host_id')

    if host_id:
        if request.method == 'POST':
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')

            user = Restaurantmodel.objects.get(Restaurant_id=host_id)
            if user.Password== current_password:
                if new_password == confirm_new_password:
                    user.Password = new_password
                    user.save()
                    request.session.flush()
                    return redirect('hostlogin')
                else:
                    messages.error(request,'new passwords does not match')
                    return redirect(reverse('hostprofile', args=['Account Details']))
            else:
                messages.error(request, 'Invalid current password.')
                return redirect(reverse('hostprofile', args=['Account Details']))
        else:
            return redirect(reverse('hostprofile', args=['Account Details']))
    else:
        return redirect('hostlogin')



def add_item(request):
    if request.method == 'POST':
        host_id = request.session.get('host_id')

        if host_id:
            try:
                host = Restaurantmodel.objects.get(Restaurant_id=host_id)

                item_name = request.POST.get('item_name')
                description = request.POST.get('description')
                price = request.POST.get('price')
                image = request.FILES.get('image')
                quantity = request.POST.get('quantity')
                start_time = request.POST.get('start_time')
                end_time = request.POST.get('end_time')
                category_id = request.POST.get('category')
                category = Categorymodel.objects.get(Category_id=category_id)

                new_item = Itemmodel(
                    Item_name=item_name,
                    Description=description,
                    Price=price,
                    Image=image,
                    Quantity=quantity,
                    Start_time=start_time,
                    End_time=end_time,
                    Category=category,
                    Host=host,
                )
                new_item.save()

                messages.success(request, 'Item added successfully.')
                return redirect('hosthome')

            except Restaurantmodel.DoesNotExist:
                messages.error(request, 'Host not found.')

        else:
            messages.warning(request, 'You need to log in to add items.')

        return redirect('hostlogin')

    else:
        categories = Categorymodel.objects.all()
        return render(request, 'hostadditem.html', {'categories': categories})



def host_home(request):
    user_id = request.session.get('host_id')
    if user_id:
        items = Itemmodel.objects.filter(Host=user_id)

        context = {
            'items': items,

        }
        return render(request, 'hosthome.html', context)
    else:
        return render(request, 'hostlogin.html')




def delete_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Itemmodel, Item_id=item_id)
        item.delete()
        return redirect('hosthome')



def add_event(request):

    if request.method == 'POST':
        host_id = request.session.get('host_id')
        if host_id:
            event_name = request.POST.get('event_name')
            description = request.POST.get('description')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            coupon_id = request.POST.get('coupon')

            try:
                host_restaurant = Restaurantmodel.objects.get(Restaurant_id=host_id)

                new_event = Eventmodel(
                    event_name=event_name,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    coupon_id=coupon_id
                )

                new_event.save()

                messages.success(request,'event added successfully')
                return redirect(reverse('hostprofile', args=['Account Details']))

            except Restaurantmodel.DoesNotExist:
                messages.error(request, 'Host restaurant not found.')

    messages.error(request, 'Failed to add event. Please try again.')
    return redirect(reverse('hostprofile', args=['Account Details']))



def add_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('Coupon-code')
        discount_price = request.POST.get('discount_price')
        minimum_amnt = request.POST.get('minimum_amnt')

        new_coupon = Couponmodel(
            Coupon_code=coupon_code,
            discount_price=discount_price,
            minimum_amnt=minimum_amnt
        )

        new_coupon.save()

        messages.success(request, 'Coupon added successfully.')
        return redirect(reverse('hostprofile', args=['Account Details']))

def hostlogout(request):

    if 'host_id' in request.session:
        del request.session['host_id']
        del request.session['host_name']
        return redirect('hostlogin')
    else:
        return redirect('hostlogin')



