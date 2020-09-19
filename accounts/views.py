from django.shortcuts import render,redirect
from accounts.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
# from chits.models import *
# from django.http import HttpResponse
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def login(request) :
    if request.method == "POST" :
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password=password)
        if user is not None :
            if not request.user :
                   login(request) 
            messages.success(request,"Logged in successfully")
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


