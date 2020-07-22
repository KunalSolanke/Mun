from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages 
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated 
from rest_framework.generics import ListAPIView
from chits.serializers import ChitSerializer
from chits.models import Chit
from accounts.models import *
from django.db.models import Q 
from django.utils.decorators import method_decorator 
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

















class DeligateIndex(LoginRequiredMixin,View) :
    template_name= "chits/index.html"
    login_url = '/accounts/login/'


    def get(self,request) :
        countries = Country.objects.all() 
        context ={
            'countries':countries
        }
        return render(request,self.template_name,context=context)
         

    def post(self,request) :
        chit_to=Country.objects.get(_id= request.POST['chit_to'])
        chit_from=request.user.delegate_profile.country
        chit_content =request.POST['content']

        chit = Chit.objects.create(chit_from = chit_from,chit_to=chit_to
        ,chit=chit_content,status =1)

        chit.save()
        # messages.success(request ,"Chit sent to Moderator for checking")
        return  HttpResponse("Chit sent to Moderator for checking")

deligate_index = DeligateIndex.as_view()















class DeligateReply(LoginRequiredMixin,View) :
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'


    def post(self,request) :
        reply_to = self.kwargs['chit_id']
        if Chit.objects.get(reply_to_chit=reply_to,status = 3).exists() :
            # messages.error(request,"This chit have already been replied to.Please wait for the reply to show up or refresh the page")
            return HttpResponse("This chit have already been replied to.Please wait for the reply to show up or refresh the page")



        chit_to=Country.objects.get(name = request.POST['chit_to'])
        chit_content =request.POST['content']
        chit = Chit.objects.create(chit_from = request.user.delegate_profile.country ,chit_to=chit_to
        ,chit=chit_content,status =1,reply_to_chit=reply_to)

        chit.save()
        # messages.success(request,"Reply to chit {} sent to moderator".format(replt_to))

        return HttpResponse("Reply to chit {} sent to moderator".format(replt_to))

deligate_reply = DeligateReply.as_view()       
        





        





class ModeratorIndexApprove(LoginRequiredMixin,View) :
    template_name= "chits/moderator.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'


    def get(self,request) :
        return render(request,self.template_name)


    def post(self,request) :
        chit_id = request.POST['chit_id']
        chit = Chit.objects.get(pk=chit_id)
        if chit.reply_to_chit and chit.objects.get(reply_to_chit=chit.reply_to_chit,status = 3).exists() :
            # messages.error(request,"This is a reply chit to chit_id {} ,for which already a reply has been ratified by Judge .".format(reply_to))
            return HttpResponse("This is a reply chit to chit_id {} ,for which already a reply has been ratified by Judge .".format(reply_to))

        chit.status =2 
        chit.save()

        return HttpResponse("Approved")

moderator_index= ModeratorIndexApprove.as_view()













class ModeratorIndexDisapprove(LoginRequiredMixin,View) :
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'


    def post(self,request) :
        chit_id = request.POST['chit_id']
        chit = Chit.objects.get(pk=chit_id) 
        chit.status = 0 
        chit.save() 
        # messages.success(request ,"Disapproved")
        return HttpResponse("Disapproved")

moderator_index_disapprove = ModeratorIndexDisapprove.as_view()













class JudgeIndexRatify(LoginRequiredMixin,View) :
    template_name= "chits/judge.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'




    def get(self,request) :
        return render(request,self.template_name)



    def post(self,request) :
        chit_id = request.POST['chit_id']
        chit = get_object_or_404(Chit,pk=chit_id) 

        if chit.reply_to_chit and Chit.objects.get(reply_to_chit=chit.reply_to_chit,status = 3).exists() :
            # messages.error(request,"This is a reply chit to chit_id {} .You have already ratifiied a reply to the same .".format(reply_to))
            return HttpResponse("This is a reply chit to chit_id {} .You have already ratifiied a reply to the same .".format(reply_to))



        chit.status = 3
        chit.save()
        # messages.success(request,'')

        return HttpResponse("Ratified")


judge_index = JudgeIndexRatify.as_view()












class JudgeIndexReject(LoginRequiredMixin,View) :
    redirect_field_name = 'redirect_to'
    login_url = '/accounts/login/'



    def post(self,request) :
        chit_id = request.POST['chit_id']
        chit = Chit.objects.get(pk=chit_id) 
        chit.status = 0 
        chit.save() 
        # messages.success(request ,"Ignored")
        return HttpResponse("Ignored")

judge_index_reject = JudgeIndexReject.as_view()














class ChitListView(ListAPIView) :
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    serializer_class = ChitSerializer 

    def get_queyset(self) :
        user = self.request.user 
        if user.role == "DT" :
            queryset = Chit.objects.filter(status=3) 
        elif user.role == "MD" :
                queryset = Chit.objects.filter(status=1) 
        elif user.role == "JD" :
                queryset = Chit.objects.filter(status =2) 
        
        return queryset 


chitlist = ChitListView.as_view()











class TeamChitListView(ListAPIView) :
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    serializer_class = ChitSerializer 

    def get_queyset(self) :
        user = self.request.user
        profile = user.deligate_profile 
        team = user.deligate_profile.team 
        queryset =[]
        for deligate in team.users.all() :
            profile = user.deligate_profile 
            country = profile.country

            queryset.append(Chit.objects.filter(Q(chit_from__id =country.id) | 
            Q(chit_to__id= country.id)))

        return queryset

team_chit_list = TeamChitListView.as_view()


