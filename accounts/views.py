from django.shortcuts import render,redirect
from accounts.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
# from chits.models import *
# from django.http import HttpResponse
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



# def data_entry(request) :

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


