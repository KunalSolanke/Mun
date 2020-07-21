from django.shortcuts import render,redirect
from accounts.models import User 
from django.contrib.auth import authenticate,login
from django.contrib import messages
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
                return redirect('chit:deligate_index')
            elif role=="MD" :
                return redirect('chits:moderator_index')
            elif role =="JD" :
                return redirect('chits:judge_index')
        else :
             messages.error(requset,"Login Failed")
             return render(request,"accounts/login.html")
    else :
        return render(request,"accounts/login.html")



