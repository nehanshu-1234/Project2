import random
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Cart,Order
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
import razorpay
import numpy as np
from django.core.mail import send_mail
from django.conf import settings


# from django.core.mail.backends.smtp import EmailBackend



# Create your views here.

def home(request):
    return render(request,"index.html")

def shop(request):
    context={}
    products=Product.objects.filter(is_active=True)
    context['Products']=products
    return render(request,"shop.html",context)



def registration(request):
    # return render(request,"registration.html")
    context={}
    if(request.method == 'POST'):
        uname = request.POST['uname']
        uemail=request.POST['uemail']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        if uname == '' or  uemail == '' or upass == '' or ucpass == '' :
            context['error']="Please fill all the fields"
            return render(request,"registration.html",context)
        elif upass!=ucpass:
            context['error']="Password and Confirm password must be same"
            return render(request,"registration.html",context)
        else:
            user_obj = User.objects.create(password=upass,username=uname,email=uemail)
            user_obj.set_password(upass)
            user_obj.save()
            context['success']="User registered successfully"
            subject="Welcome to YogaShala"
            messages="Registered Successfly!"

            send_mail(
            subject,
            messages,
            "settings.EMAIL_HOST_USER",
            [user_obj.email],
            fail_silently=False,
            )
            return render(request,"registration.html",context)
        
    else:
        return render(request,"registration.html")


def user_login(request):
    context={}
    if(request.method=="POST"):
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=='' or upass=='':
            context['error']="Please fill all the fields"
            return render(request,"login.html",context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect("/")
            else:context['error'] = "Invalid credentials"
            return render(request,"login.html",context)
        
    else:
        return render(request,"login.html")

def user_logout(request):
    logout(request)
    return redirect("/")

def catfilter(request,cid):
    context={}
    q1=Q(is_active=True)
    q2=Q(category=cid)
    products = Product.objects.filter(q1&q2)
    context['Products']=products
    return render(request,"shop.html",context)


def sort(request,s):
    context={}
    if s=='1':
        products = Product.objects.filter(is_active=True).order_by('price')
    elif s=='0':
        products = Product.objects.filter(is_active=True).order_by('-price')
    context['Products']=products
    return render(request,"shop.html",context)

def range(request):
    context={}
    if request.method=="POST":
        min = request.POST['min']
        max=request.POST['max']
        products=Product.objects.filter(is_active=True,price__gte=min,price__lte=max)
        context['Products']=products 
        return render(request,"shop.html",context)
    else:
        return render(request,"shop.html",context)



def productdetail(request,pid):
    context={}
    product = Product.objects.get(id=pid)
    context['product']=product
    return render(request,"viewdetails.html",context)

def addToCart(request,pid):
    #it will check if user is logged in
    if request.user.is_authenticated:
        #it will fetch user id
        uid = request.user.id
        u=User.objects.get(id=uid)
        p=Product.objects.get(id=pid)
        c=Cart.objects.create(uid=u,pid=p)
        c.save()
        return redirect("/shop/")
    else:
        return redirect("/login")
    
def viewcart(request):
    user_id = request.user.id 
    c = Cart.objects.filter(uid=user_id)
    sum = 0
    np = len(c)
    
    for i in c:
        sum=sum+i.pid.price*i.quantity
        
    context={}
    context['np']=np
    context['sum']=sum
    context['products']=c 
    return render(request,"cart.html",context)


def removefromcart(request,cid):
    if request.user.is_authenticated:
        c=Cart.objects.filter(id=cid)
        c.delete()
        return redirect("/viewcart")
    else:
        return redirect("/login")

    
def updateqty(request,qv,cid):
    if request.user.is_authenticated:
        c=Cart.objects.filter(id=cid)
        if qv=='1':
            t=c[0].quantity+1
            c.update(quantity=t)

        elif qv=='0':
            if c[0].quantity>1:
                t=c[0].quantity-1
                c.update(quantity=t)
            elif c[0].quantity == 1:
                c.delete()
        return redirect("/viewcart")   
    else:
        return redirect("/login")
    


def placeorder(request):
    if request.user.is_authenticated:
        user = request.user
        c=Cart.objects.filter(uid=user)
        order_id = random.randrange(1000,9999)
        for i in c:
            o=Order.objects.create(order_id=order_id,uid=user,pid=i.pid,quantity=i.quantity)
            o.save()
            i.delete()
        orders = Order.objects.filter(uid=user)
        np=len(orders)
        sum=0
        for i in orders:
            sum=sum+i.pid.price*i.quantity
        request.session['order_sum'] = sum    
        context={}
        context['products']=orders 
        context['sum']=sum 
        context['np']=np
            
        return render(request,"placeorder.html",context)





def makepayment(request):
  
    # Retrieve the sum value from the session
    order_sum = request.session.get('order_sum', 0)

    if order_sum == 0:
        # Handle the case where the sum is not available
        return redirect('some_error_view')

    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    payment = client.order.create({'amount': order_sum * 100, 'currency': 'INR', 'payment_capture': 1})
    user=request.user
    orders=Order.objects.filter(uid=user)
    for order in orders:
        order.delete()
        del context['sum']
        

    context = {'payment': payment}
    
    return render(request, "pay.html", context)


def sendusermail(request):
    msg="order placed successfully!"
    send_mail(
    "Place Order",
    msg,
    "nehanshusingh01@gmail.com",
    ["nehanshusingh01@gmail.com"],
    fail_silently=False,
    )
                            
    return redirect("/")


