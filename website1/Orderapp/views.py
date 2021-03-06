from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, reverse
from Product.models import Category, Product, Images
from django.contrib import messages
from Orderapp.models import ShopCart, ShopingCartForm, OrderForm, Order, OrderProduct 
from django.forms import ModelForm
from webapp.models import Setting, ContactMessage, ContactForm
from Userapp.models import UserProfile
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django import db 
# Create your views here.



def Add_to_Shoping_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checking = ShopCart.objects.filter(
        product_id=id, user_id=current_user.id)
    if checking:
        control = 1
    else:
        control = 0        

    if request.method == "POST":
        form = ShopingCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.filter(
                    product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity'] 
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Your product has been added ')        
        return HttpResponseRedirect(url)
    else:
        if control == 1:
            data = ShopCart.objects.filter(
                product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Your product has been added ')
        return HttpResponseRedirect(url)


def cart_detials(request):
    current_user = request.user
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    cart_product= ShopCart.objects.filter(user_id=current_user.id)
    total_amount = 0
    for p in cart_product:
        total_amount += p.product.new_price*p.quantity

    context={
       'category': category, 
       'setting': setting,
       'cart_product': cart_product,
       'total_amount': total_amount,
    }
    return render(request, 'cart_detials.html', context)


def cart_delete(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cart_product= ShopCart.objects.filter(id=id, user_id=current_user.id)
    cart_product.delete()
    messages.warning(request, 'Your product has been deleted ')
    return HttpResponseRedirect(url)




@login_required(login_url='/user/login')
def OrderCart(request):
    current_user = request.user
    shoping_cart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for rs in shoping_cart:
        totalamount += rs.quantity*rs.product.new_price
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():    
            dat = Order()
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id = current_user.id
            dat.total = totalamount
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            dat.code = ordercode
            dat.save()

            for rs in shoping_cart:
                data = OrderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete()

            messages.success(request, 'Your order has been completed')
            category = Category.objects.all()
            setting = Setting.objects.get(id=1)
            context = {
                'ordercode': ordercode,
                'category': category, 
                'setting': setting,
                
            }
            return render(request, 'order_complated.html', context)
        else:
            messages.warning(request, form.errors)
            #return HttpResponseRedirect("/order/order_cart")
    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    total_amount = 0
    for p in shoping_cart:
        total_amount += p.product.new_price*p.quantity
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
  

    context = {
        #'category': category,
        'shoping_cart':shoping_cart,
        'totalamount': totalamount,
        'profile': profile,
        'form': form,
        'category': category,
        'setting': setting,
        'total_amount': total_amount,
        
    }   
    return render(request, 'order_form.html', context)     

            
def Order_showing(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    orders = Order.objects.filter(user_id=current_user.id)
    context= {
        'category': category,
        'setting': setting,
        'orders': orders
    }
    return render(request, 'user_order_showing.html', context)


@login_required(login_url='/user/login')
def user_order_details(request, id):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    order_products = OrderProduct.objects.filter(order_id=id)
    context = {
        'order': order,
        'order_products': order_products,
        'category': category,
        'setting': setting,

    }
    return render(request, 'user_order_details.html', context)




def Order_Product_showing(request):
        category = Category.objects.all()
        setting = Setting.objects.get(id=1)
        current_user = request.user
        order_product = OrderProduct.objects.filter(user_id=current_user.id)
        context = {
            'category': category,
            'setting': setting,
            'order_product': order_product
        }
        return render(request, 'orderproductlist.html', context)






@login_required(login_url='/user/login')
def userorderproduct_details(request, id, oid):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    order_products = OrderProduct.objects.get(user_id=current_user.id, id=id)
    context = {
        'order': order,
        'order_products': order_products,
        'category': category,
        'setting': setting,

    }
    return render(request, 'user_order_pro_details.html', context)


       