from django.shortcuts import render,redirect
from accounts.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from chits.models import *
from django.http import HttpResponse
from accounts.models import *
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
import pandas as pd
# Create your views here.



def user_login(request) :
    if request.method == "POST" :    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password=password)
       


        if user is not None :  
            login(request,user)       
            role = user.role 
            
            if role =="DT" :
                return redirect('chits:deligate_index')
            elif role=="MD" :
                return redirect('chits:moderator_index')
            elif role =="JD" :
                return redirect('chits:judge_index') 
            else :
                messages.error(request,"Invalid credentials")
                return render(request,"accounts/login.html")        
        else :
             messages.error(request,"Invalid credentials")
             return render(request,"accounts/login.html")


    else :
        if request.user and not isinstance(request.user ,AnonymousUser):
            role = request.user.role 
            if role =="DT" :
                return redirect('chits:deligate_index')
            elif role=="MD" :
                return redirect('chits:moderator_index')
            elif role =="JD" :
                return redirect('chits:judge_index') 
            else :
                messages.error(request,"Invalid credentials")
                return render(request,"accounts/login.html")
           
        else :
          return render(request,"accounts/login.html")


class Logout(LoginRequiredMixin,View):

    def get(self,request):
        logout(request)
        return redirect('accounts:login')

logout_user = Logout.as_view()




def createUsers(request) :
    data = pd.read_csv('http://127.0.0.1:8000/static/data.csv')

    for i in range(len(data)) :
        country = data.iloc[i,0]
        username= data.iloc[i,1]
        password = data.iloc[i,2]
        c= Country.objects.create(name=country,country_id=username)
        u = User.objects.create(username=username,role="DT")
        u.set_password(password)
        p =DeligateProfile.objects.create(user=u,country=c)
        u.save()
        c.save()
        p.save()
    

    return HttpResponse("data added")



#def data_entry(request) :

#     #   for i in range(75) :
#     #       Country.objects.create(name="Country_{}".format(i+1),country_id="country_{}@iitgmun".format(i+1))
     
#     for i in range(15) :
#       team = Team.objects.create(name="Team_{}".format(i+1),info="Dummy data")
#       for j in range(5) :
#         user =  User.objects.create(username="Country{}_deligate".format(i*5+j+1),role="deligate",email="Country{}_deligate@gmail.com".format(i*5+j+1))
#         profile = DeligateProfile.objects.create(user=user,country=Country.objects.get(name="Country_{}".format(i*5+j+1)),team=team,first_name="Who tf care!",last_name="Oh lol")
#         user.save()
#         profile.save()
#         if j==0 :
#            team.leader = user
#       team.save()


   
    

       
#     return HttpResponse("data added")


