from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
import random

# Create your views here.
def index(request):
    return render(request,'user/index.html')

def auth(request):
    return render(request,'user/auth.html')

def log_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            username = User.objects.get(email=email).username
            password = request.POST['password']
            user = authenticate(username=username, password=password)
        except:
            user = None
        if user is not None:
            login(request,user)
            return redirect('/?message=logged in sucessfully')
        else:
            return render(request,'user/auth.html',{'message': 'Invalid credentials'})
        
def sign_up(request):
    if request.method == 'POST':
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        if_exist = User.objects.filter(email=email).exists()
        if if_exist:
            return render(request, 'user/auth.html', {'message': 'User already exists'})
        try:
            password = request.POST['password']
            username = firstname[:3] + lastname[:2] + str(random.randint(100,999)) 
            user = User.objects.create_user(username, email, password)
            login(request,user)
            user.save()
            return redirect('/')
        except:
            return render(request, 'user/auth.html', {'message': 'something went wrong'})
        
def log_out(request):
    logout(request)
    return redirect('/')
