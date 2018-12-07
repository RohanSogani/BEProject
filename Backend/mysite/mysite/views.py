from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from appWindow.forms import SiteRegistrationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    return render(request,'upload.html',{})

#function for user login
def login_user(request):
    print request
    if request.user.is_authenticated():
        print 'in here'
        return render(request, 'home.html')
    if request.method == 'POST':
        print 'in POST'
        print request.POST
        username = request.POST['username']
        passw = request.POST['password']
        print username, passw
        user = authenticate(username=username,password=passw)
        if user is not None:
            print 'user is here'
            if user.is_active:
                print 'user is active'
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
        else:
            print 'invalid user'
            return HttpResponseRedirect('invalid/')
    print 'at the end'
    return render(request, 'login.html')


def loggedin(request):
    return render(request,'loggedin.html',{'full_name':request.user.username})


def invalid_login(request):
    return render(request,'invalid_login.html',{})

#function to logout user safely
def logout_user(request):
    logout(request)    #user is logged out using auth class
    return render(request,'home.html',{})

def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def isValidUsername(field_data):
    try:
        User.objects.get(username=field_data)
    except User.DoesNotExist:
        return True
    return False

def isValidEmail(field_data):
    try:
        User.objects.get(email=field_data)
    except User.DoesNotExist:
        return True
    return False
        

def register(request):
    if request.user.is_authenticated():
        print request.user.get_username()
        return HttpResponseRedirect(reverse('register_success'))
    if request.method == 'POST':
        print 'yolooooo22222'
        username = request.POST['inputUsername']
        emailID = request.POST['inputEmail']
        passw = request.POST['inputPassword']
        if validateEmail(emailID) == True and len(username) != 0 and len(passw) != 0 and isValidEmail(emailID) == True and isValidUsername(username) == True:
            print 'success'
            user = User.objects.create_user(username, emailID, passw)
            return HttpResponseRedirect(reverse('register_success'))
        else:
            print 'fail'
            return HttpResponseRedirect(reverse('register'))

    else:
        print 'yolooooo'
        return render(request, 'register.html')

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def register_success(request):
    return render(request,'register_success.html',{})

def index(request):
    return render(request,"index.html",{})
