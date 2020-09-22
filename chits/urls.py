from django.urls import path,re_path
from chits.views import *


app_name = 'chits'



urlpatterns = [
    re_path(r'^api/messages/(?P<state>.+)$',view=chitlist,name="chitlist") ,
    re_path(r'^api/messages/team$',view=team_chit_list,name="teamchitlist") ,
    path('deligate', deligate_index,{'role':"DT"} ,name = "deligate_index"),
    path('deligate/reply', deligate_reply,{'role':"DT"} ,name = "deligate_reply"),
    path('moderator/', moderator_index,{'role':"MD"},name = "moderator_index"),
    path('moderator/disapprove/', moderator_index_disapprove ,{'role':"MD"},name = "moderator_index_disapprove"),#only post request
    path('judge/', judge_index,{'role':"JD"} ,name = "judge_index"),
    path('judge/reject/', judge_index_reject,{'role':"JD"} ,name = "judge_index_reject"), #only post request  ,
]