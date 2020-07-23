from django.shortcuts import render,redirect
from accounts.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def login(requset) :
    if request.method == "POST" :
        username = requset.POST['username']
        password = requset.POST['password']
        user = authenticate(username = username,password=password)
        if user is not None :
            login(requset,user) 
            messages.success(requset,"Logged in successfully")
            role = user.role 
            if role =="DT" :
                return redirect('chits:deligate_index')
            elif role=="MD" :
                return redirect('chits:moderator_index')
            elif role =="JD" :
                return redirect('chits:judge_index')
        else :
             messages.error(requset,"Login Failed")
             return render(request,"accounts/login.html")
    else :
        return render(request,"accounts/login.html")


class Logout(LoginRequiredMixin,View):

    def get(self,request):
        return redirect('accounts:login')

logout_user = Logout.as_view()

def Update(request):
    username='daksh'
    password='passworddaksh'

    for i in range(10):
        user = User.objects.get(username=username+str(i+2),password=password+str(i+2))
        user.role = 'DT'
        user.save()
    return HttpResponse("Users updated successfully!")

def Entry(request):
    username='daksh'
    password='passworddaksh'
    
    for i in range(10):
        User.objects.create(username=username+str(i+2),password=password+str(i+2),role='DT')

    return HttpResponse("Users Created")



