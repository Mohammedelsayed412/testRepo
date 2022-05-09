from tkinter import X
import requests
import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from products.models import Products, AuditLog
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from products.forms import ProductModelForm
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# TODO ==> Add loging for each request failure ==> Just add more conditions to check if request fails and log it 
# TODO ==> Add register form instead of using django admin to add users ==> same like login and just add table to save users in database

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='Login', 
                description='User Login sucess', actionType='login').save()
            backToHome = reverse("home")
            return HttpResponseRedirect(backToHome) 
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))
            AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='Login', 
                description=f'User with name = {username} try to Login but Failed', actionType='login').save()
            backToLogin = reverse("login")
            return HttpResponseRedirect(backToLogin) 	

    else:
        return render(request, 'products/login.html', {})

def logout_user(request):
    if loginState(request):	
        AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='Logout', 
        description='User Logout sucess', actionType='logout', 
        eventSpecificFields={"viewName": "productsView"}).save()
        logout(request)
        messages.success(request, ("You Were Logged Out!"))
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin)
    else:
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 
     

def loginState(request):
    if not request.user.is_authenticated:
        messages.success(request, ("Please Login First ..."))
        return False
    else:
        return True

def deactivateUser(request):
    if loginState(request):	
        user = get_object_or_404(User, username=request.user)
        user.delete()
        AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='Admin Activities', 
            description=f'Admin deactivate {request.user} from users', actionType='delete').save()

        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 

def home(request):
    AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='User Navigation', 
        description='Navigate to home Page', actionType='Read', 
        eventSpecificFields={"viewName": "home", "userLoginState":"True"}).save()
    if loginState(request):	
        return render(request, "products/home.html")
    else:
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 

def productsView(request):
    if loginState(request):	
        products = Products.objects.all().order_by('id')
        AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='User Navigation', 
            description='Navigate to Products page', actionType='Read', 
            eventSpecificFields={"viewName": "productsView"}).save()
        return render(request, "products/products.html",
                  context={"products": products})
    else:
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 
    
    
def productDetails(request, id):
    if loginState(request):	
        product = get_object_or_404(Products, pk=id)
        AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='User Navigation', 
            description=f'Navigate to {product.name} details', actionType='Read').save()
        return render(request, "products/productDetails.html", context={"product": product})  
    else:
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 
    
 
def updateorsave(request, optype, productId=None):
    name = request.POST["name"]
    price = request.POST["price"]
    count = request.POST["count"]
    desc = request.POST["desc"]

    if optype == "create":
        product = Products()
    else:
        product = get_object_or_404(Products, pk=productId)
    product.name = name
    product.price = price
    product.count = count
    product.desc = desc
    AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='Admin Activities', 
        description=f'Admin {optype} {product.name} in products', actionType=f'{optype}').save()
    product.save()


# TODO ==> make only admin user be able to add products
def addProduct(request):
    if loginState(request):	
        if request.POST:
            updateorsave(request, "create")
            backToProducts = reverse("products")
            return HttpResponseRedirect(backToProducts)
        form = ProductModelForm()
        return render(request, "products/addProduct.html", context={"form" :form})
    else:
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 
    

def editProduct(request, id):
    if loginState(request):	
        if request.POST:
            updateorsave(request, "update", id)
            backToProducts = reverse("products")
            return HttpResponseRedirect(backToProducts)

        product = get_object_or_404(Products, pk=id)
        form = ProductModelForm()
        return render(request, "products/editProduct.html", context={"product": product, "form" :form})
    else:
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 
    

def deleteProduct(request, id):
    if loginState(request):	
        product = get_object_or_404(Products, pk=id)
        product.delete()
        AuditLog(userName=request.user, ip = request.META.get('REMOTE_ADDR'), eventName='Admin Activities', 
            description=f'Admin delete {product.name} from products', actionType='delete').save()
        backToProducts = reverse("products")
        return HttpResponseRedirect(backToProducts)
    else:
        backToLogin = reverse("login")
        return HttpResponseRedirect(backToLogin) 
    

def logsView(request):
    try:
        token = Token.objects.get_or_create(user=request.user)
        # print(token)
        if loginState(request):	
            response_API = requests.get('http://127.0.0.1:8000/logApi/logList', headers={'Authorization': f'access_token {token[0]}'})
            logs = json.loads(response_API.text) 
            return render(request, "products/logs.html", context={'logs':logs})
        else:
            backToLogin = reverse("login")
            return HttpResponseRedirect(backToLogin)  
    except:
        messages.success(request, ("User token is incorrect "))
        backToHome = reverse("home")
        return HttpResponseRedirect(backToHome)  