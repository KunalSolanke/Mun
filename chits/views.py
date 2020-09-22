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
from django.utils.decorators import method_decorator
import json
from chits.decorators import user_check
from django.utils import timezone
# Create your views here.

















class DeligateIndex(LoginRequiredMixin,View) :
    template_name= "chits/index.html"
    login_url = '/accounts/login/'

    
    

    @method_decorator(user_check)
    def get(self,request,*args,**kwargs) :
        
        countries = Country.objects.all().exclude(name=request.user.deligate_profile.country.name)
        context ={
            'countries':countries
        }
        return render(request,self.template_name,context=context)
         
    @method_decorator(user_check)
    def post(self,request,*args,**kwargs) :
        request_data = json.loads(request.body)
        chit_to=Country.objects.get(country_id= request_data.get('chit_to'))
        chit_from=request.user.deligate_profile.country
        chit_content =request_data['content']
        if(chit_to!=chit_from):
            chit = Chit.objects.create(chit_from = chit_from,chit_to=chit_to
            ,chit=chit_content,status =1)
            chit.save()
            return  HttpResponse(json.dumps({"message":"Chit sent to Moderator for checking","id":chit.id}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message":"Can not send chit to yourself","id":chit.id}),content_type="application/json")

deligate_index = DeligateIndex.as_view()















class DeligateReply(LoginRequiredMixin,View) :
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    @method_decorator(user_check)
    def post(self,request,*args,**kwargs) :
        request_data = json.loads(request.body)
        reply_to = request_data['reply_to']
        
        if Chit.objects.filter(reply_to_chit=int(reply_to),status = 3).exists() :
            # messages.error(request,"This chit have already been replied to.Please wait for the reply to show up or refresh the page")
            return HttpResponse(json.dumps({
            "message":"This chit have already been replied to.Please wait for the reply to show up or refresh the page"
            }),content_type="application/json")

        chit_to=Country.objects.get(country_id= request_data['chit_to'])
        reply_to_chit = Chit.objects.get(pk=int(reply_to))
        chit_content =request_data['content']
        if(chit_to!=request.user.deligate_profile.country):
            chit = Chit.objects.create(chit_from = request.user.deligate_profile.country ,chit_to=chit_to
            ,chit=chit_content,status =1,reply_to_chit=reply_to_chit)

            chit.save()
            # messages.success(request,"Reply to chit {} sent to moderator".format(replt_to))

            return HttpResponse(json.dumps({
                "message":"Reply to chit {} sent to moderator".format(reply_to),
                "id" : chit.id
            }),content_type="application/json")
        else:
            return HttpResponse(json.dumps({
                "message":"Can not reply to yourself",
                "id" : chit.id
            }),content_type="application/json")

deligate_reply = DeligateReply.as_view()       
        





        





class ModeratorIndexApprove(LoginRequiredMixin,View) :
    template_name= "chits/moderator.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    @method_decorator(user_check)
    def get(self,request,*args,**kwargs) :
        return render(request,self.template_name)

    @method_decorator(user_check)
    def post(self,request,*args,**kwargs) :
        request_data = json.loads(request.body)
        chit_id = request_data['chit_id']
        chit = Chit.objects.get(pk=chit_id)
        
        if chit.reply_to_chit and Chit.objects.filter(reply_to_chit=chit.reply_to_chit,status = 3).exists() :
            # messages.error(request,"This is a reply chit to chit_id {} ,for which already a reply has been ratified by Judge .".format(reply_to))
            return HttpResponse(json.dumps({
            "message":"This is a reply chit to chit_id {} ,for which already a reply has been ratified by Judge .".format(chit.reply_to_chit)
            }),content_type="application/json")

        chit.status =2 
        chit.save()

        return HttpResponse(json.dumps({
            "message":"Approved"
        }),content_type="application/json")

moderator_index= ModeratorIndexApprove.as_view()













class ModeratorIndexDisapprove(LoginRequiredMixin,View) :
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'

    @method_decorator(user_check)
    def post(self,request,*args,**kwargs) :
        request_data = json.loads(request.body)
        chit_id = request_data['chit_id']
        chit = Chit.objects.get(pk=chit_id) 
        chit.status = 0 
        chit.save() 
        # messages.success(request ,"Disapproved")
        return HttpResponse(json.dumps({
            "message":"Disapproved"
        }),content_type="application/json")

moderator_index_disapprove = ModeratorIndexDisapprove.as_view()













class JudgeIndexRatify(LoginRequiredMixin,View) :
    template_name= "chits/judge.html"
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'



    @method_decorator(user_check)
    def get(self,request,*args,**kwargs) :
        return render(request,self.template_name)

  
    @method_decorator(user_check)
    def post(self,request,*args,**kwargs) :
        request_data = json.loads(request.body)
        chit_id = request_data['chit_id']
        chit = get_object_or_404(Chit,pk=chit_id) 

        if chit.reply_to_chit and Chit.objects.filter(reply_to_chit=chit.reply_to_chit,status = 3).exists() :
            # messages.error(request,"This is a reply chit to chit_id {} .You have already ratifiied a reply to the same .".format(reply_to))
            return HttpResponse(json.dumps({
            "message":"This is a reply chit to chit_id {} .You have already ratifiied a reply to the same .".format(reply_to)
        }),content_type="application/json")



        chit.status = 3
        chit.save()
        # messages.success(request,'')

        return HttpResponse(json.dumps({
            "message":"Ratified"
        }),content_type="application/json")


judge_index = JudgeIndexRatify.as_view()












class JudgeIndexReject(LoginRequiredMixin,View) :
    redirect_field_name = 'redirect_to'
    login_url = '/accounts/login/'


    @method_decorator(user_check)
    def post(self,request,*args,**kwargs) :
        request_data = json.loads(request.body)
        chit_id = request_data['chit_id']
        chit = Chit.objects.get(pk=chit_id) 
        chit.status = 0 
        chit.save() 
        # messages.success(request ,"Ignored")
        return HttpResponse(json.dumps({
            "message":"Ignored"
        }),content_type="application/json")

judge_index_reject = JudgeIndexReject.as_view()














class ChitListView(ListAPIView) :
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication,BasicAuthentication]
    serializer_class = ChitSerializer 

    def get_queryset(self) :
        user = self.request.user 
        
        queryset=[]
        if(self.request.user.is_authenticated) :
            if self.kwargs['state'] !="initial" :
                if user.role == "DT" :
                    queryset = Chit.objects.filter(status=3,timestamp__gte=timezone.now()-timezone.timedelta(minutes=10))
                elif user.role == "MD" :
                        queryset = Chit.objects.filter(status=1,timestamp__gte=timezone.now()-timezone.timedelta(minutes=10)) 
                elif user.role == "JD" :
                        queryset = Chit.objects.filter(status =2,timestamp__gte=timezone.now()-timezone.timedelta(minutes=10)) 
                queryset = queryset[:300]
            else :
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
        print(self.request.session)
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


