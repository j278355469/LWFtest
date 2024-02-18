from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    user = request.user

    return render(request, "user/profile.html", {"user": user})


def user_login(request):
    message = ""
    if request.method == "POST":
        if request.POST.get("register"):
            return redirect("register")
        elif request.POST.get("login"):
            username = request.POST["username"]
            password = request.POST["password"]
            user = User.objects.filter(username=username)
            if not user:
                message = "無此帳號!"
            else:
                user = authenticate(
                    request, username=username, password=password)
                if not user:
                    message = "密碼錯誤!"
                else:
                    login(request, user)
                    message = "登入成功!"
                    return redirect("todo")

        print(user)

    return render(request, "user/login.html", {"message": message})


def register(request):
    message = ""
    if request.method == "POST":
        print(request.POST)
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        sex=request.POST["sex"]
        birthday=request.POST["birthday"]
        

        print(username, password1, password2)
        if password1 != password2:
            message = "輸入兩次密碼不相同"
        elif len(password1) < 8:
            message = "錯誤，密碼過短"
        else:
            if User.objects.filter(username=username):
                message = "帳號重複"
            else:
                user = User.objects.create_user(username=username,
                                                password=password1,
                                                email=email,
                                                sex=sex,
                                                birthday=birthday
                                                )
                user.save()
                message = "註冊成功"
                return redirect("profile")

    form = UserCreationForm()
    return render(request, "user/register.html", {"form": form, "message": message})
