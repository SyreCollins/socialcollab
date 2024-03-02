from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
#from .models import UserProfile

# Create your views here.
def Home(request):
    if request.method == 'POST':
        return redirect('register')

    return render(request, "home.html", {})

def Register(request):
    if request.method == 'POST':
        ig_username = request.POST['ig_username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        #content = request.POST['content-type']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists Boyy.')
                return redirect('register')
            elif User.objects.filter(username=ig_username).exists():
                messages.info(request, 'Instagram Username don de Database oo.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=ig_username, email=email, password=password)
                #user.content_type = content
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'The 2 passwords de different oo.')
            return redirect('register')

    return render(request, "register.html", {})

def Login(request):
    if request.method == "POST":
        username = request.POST['ig_username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Authentication failed.')
            return redirect('login')
    return render(request, "login.html", {})

def scrape_instagram_profile(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        profile_picture = soup.select_one('meta[property="og:image"]')
        bio = soup.find('meta', property='og:description')
        if profile_picture and bio:
            return profile_picture['content'], bio['content'].split('-')[0].strip()
    return None, None

def Dashboard(request):
    users = User.objects.exclude(pk=request.user.pk)
    user_profiles = []
    for user in users:
        profile_picture, bio = scrape_instagram_profile(user.username)
        user_profiles.append({'user': user, 'profile_picture': profile_picture, 'bio': bio})
    return render(request, "dashboard.html", {'user_profiles': user_profiles})