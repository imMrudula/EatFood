from django.shortcuts import render, redirect
from user.models import Usermodel, Reviewmodel,itemordermodel
from restaurant.models import Restaurantmodel
from adminapp.models import Categorymodel
from .forms import CategoryForm
# Create your views here.

def adminhome(request):
    userdata=Usermodel.objects.all()
    hostdata = Restaurantmodel.objects.all()
    reviewdata= Reviewmodel.objects.all()
    # orderdata=itemordermodel.objects.all()
    usercount=userdata.count()
    hostcount=hostdata.count()
    reviewcount= reviewdata.count()
    # ordercount=orderdata.count()
    return render(request,'admin.html',{'user':userdata,'host':hostdata,
                                        'usercount':usercount,'hostcount':hostcount,'reviewcount':reviewcount})

def activate_user(request, user_id):
    user = Usermodel.objects.get(pk=user_id)
    if user.User_status == 'Active':
        user.User_status = 'Inactive'
    else:
        user.User_status = 'Active'
    user.save()
    return redirect('admin')

def activate_host(request, host_id):
    host = Restaurantmodel.objects.get(pk=host_id)
    if host.Host_status == 'Active':
        host.Host_status = 'Inactive'
    else:
        host.Host_status = 'Active'
    host.save()
    return redirect('admin')

def managecategory(request):
    category= Categorymodel.objects.all()
    return render(request,'admincategory.html',{'category':category})

def delete_category(request, category_id):
    category = Categorymodel.objects.get(Category_id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('managecategory')  # Redirect to category table after deletion

def update_category(request, category_id):
    category = Categorymodel.objects.get(Category_id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('managecategory')
    else:
        form = CategoryForm(instance=category)
        return render(request, 'editcategoryadmin.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('managecategory')
    form = CategoryForm()
    return render(request, 'addcategoryadmin.html', {'form': form})
